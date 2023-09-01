from typing import List, Tuple, Dict, Any, Union, Optional, Callable
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import logging
from dlm_matrix.embedding.utils import (
    apply_umap,
    apply_hdbscan,
)


class SpatialSimilarity:
    def __init__(
        self,
        reduce_dimensions=True,
        batch_size=128,
        n_components=3,
        weights=None,
        model_name="all-mpnet-base-v2",
    ):
        """Initialize a SemanticSimilarity."""
        self._model_name = model_name
        self._semantic_vectors = []
        self.keywords = []
        self._model = SentenceTransformer(self._model_name)  # Initialize model here
        self.weights = weights if weights is not None else {}
        self.default_options = {
            "n_components": n_components,
            "reduce_dimensions": reduce_dimensions,
            "n_neighbors": None,
        }
        self.batch_size = batch_size
        self._semantic_vectors = []
        self.keywords = []

    @property
    def model_name(self) -> str:
        return self._model_name

    @model_name.setter
    def model_name(self, model_name: str):
        self._model_name = model_name
        self._model = SentenceTransformer(self._model_name)

    def fit(self, keywords: List[str]) -> None:
        """Fit the model to a list of keywords."""

        # Compute semantic vectors
        self.keywords = keywords
        self._semantic_vectors = self.encode_texts(keywords)
        return self._semantic_vectors

    def encode_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts as a list of lists of floats using the SentenceTransformer.
        """
        # Preprocess the texts
        self._model.max_seq_length = 512

        # Get embeddings for preprocessed texts
        embeddings = self._model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return embeddings

    def encode_texts_in_batches(
        self, texts: List[str], batch_size: int = 100
    ) -> List[Optional[float]]:
        """Encode texts in batches to avoid memory issues."""
        encodings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            try:
                batch_encodings = self.encode_texts(batch_texts)
                encodings.extend(batch_encodings)
            except Exception as e:
                logging.warning(f"Failed to encode texts: {e}")
                encodings.extend([None] * len(batch_texts))
        return encodings

    def process_message_dict(
        self, message_dict: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        """
        Extract the message text and ID from the message dictionary.
        """
        message_texts = []
        message_ids = []
        for message_id, message in message_dict.items():
            if isinstance(message, str):
                message_texts.append(message)
                message_ids.append(message_id)
            elif message.message and message.message.author.role != "system":
                message_texts.append(message.message.content.parts[0])
                message_ids.append(message.id)
        return message_texts, message_ids

    def generate_message_to_embedding_dict(
        self, message_ids: List[str], embeddings: List[np.array]
    ) -> Dict[str, np.array]:
        """
        Generate a dictionary mapping message IDs to embeddings.
        """
        return {message_ids[i]: embeddings[i] for i in range(len(message_ids))}

    def compute_neighbors(self, grid, message_dict: Dict[str, Any]) -> Dict[str, int]:
        """
        For each message, determine the number of neighbors.
        """
        n_neighbors_dict = {}
        for message_id in message_dict:
            n_neighbors_dict[message_id] = grid.determine_n_neighbors(message_id)
        return n_neighbors_dict

    def update_message_dict_with_embeddings(
        self,
        message_dict: Dict[str, Any],
        embeddings: Any,
    ) -> None:
        """
        Update the 'embedding' or 'umap_embedding' fields of each Message object
        in the provided message_dict based on the embedding_type.

        Parameters:
            message_dict: A dictionary containing Message objects.
            embeddings: A dictionary mapping message IDs to their embeddings.
            embedding_type: A string indicating the type of embeddings ('basic' or 'umap').

        Returns:
            None
        """

        for message_id, embedding in embeddings.items():
            if message_id in message_dict:
                message_dict[message_id].message.embedding = embedding.tolist()

    def generate_embeddings(
        self,
        message_dict: Dict[str, Any],
    ) -> Dict[str, np.array]:
        """
        Generate basic semantic embeddings for the messages.
        """
        # Extract the message text and ID from the message dictionary
        message_texts, message_ids = self.process_message_dict(message_dict)

        # Encode the message texts to obtain their embeddings
        embeddings = self.encode_texts(message_texts)

        # Create a dictionary mapping message IDs to embeddings
        message_embeddings = self.generate_message_to_embedding_dict(
            message_ids, embeddings
        )

        # Update the message dictionary with the embeddings
        self.update_message_dict_with_embeddings(message_dict, message_embeddings)
        return embeddings, message_ids

    def generate_message_embeddings(
        self,
        grid,
        message_dict: Dict[str, Any],
        embeddings: Dict[str, np.array],
        message_ids: List[str],
        options: dict = None,
    ) -> Dict[str, Union[np.array, Tuple[str, str]]]:
        """
        Generate semantic embeddings for the messages in the conversation tree using a sentence transformer.
        """

        # Update default options with user-specified options
        if options is not None:
            self.default_options.update(options)

        if len(message_dict) > 1:
            n_neighbors_dict = self.compute_neighbors(grid, message_dict)
            self.default_options["n_neighbors"] = np.mean(
                list(n_neighbors_dict.values())
            )
            reduced_embeddings = self.generate_reduced_embeddings(
                embeddings, self.default_options
            )

            message_embeddings = self.generate_message_to_embedding_dict(
                message_ids, reduced_embeddings
            )
            clusters = self.cluster_terms(list(message_embeddings.items()))

            # Assign each message id to a cluster label
            clustered_messages = {}
            for cluster_label, terms in clusters.items():
                for term in terms:
                    # Assuming term is a tuple with more than 2 elements, we only take the first one
                    term_id = term[0]
                    clustered_messages[term_id] = (
                        message_embeddings[term_id],
                        cluster_label,
                        embeddings,
                        n_neighbors_dict[
                            term_id
                        ],  # Add the count of neighbors to the dictionary
                    )

            return clustered_messages

    def generate_reduced_embeddings(
        self, embeddings: np.ndarray, options: dict = None
    ) -> np.ndarray:
        """
        Reduce the dimensionality of the embeddings if necessary.
        """
        # convert embeddings dictionary to numpy array
        if isinstance(embeddings, dict):
            embeddings = np.array(list(embeddings.values()))

        # Update default options with user-specified options
        if options is not None:
            self.default_options.update(options)

        if self.default_options["reduce_dimensions"]:
            embeddings = apply_umap(
                embeddings,
                self.default_options["n_neighbors"],
                self.default_options["n_components"],
            )

        return embeddings

    def cluster_terms(
        self, terms: List[Tuple[str, List[float]]]
    ) -> Dict[int, List[Tuple[str, List[float]]]]:
        try:
            if not terms:
                print("No terms provided for grouping")
                return {}

            # Extract the embeddings from the terms
            embeddings = np.array([embedding for _, embedding in terms])

            # Apply weights if available
            for i, (term, _) in enumerate(terms):
                if term in self.weights:
                    embeddings[i] *= self.weights[term]

            clustering = apply_hdbscan(embeddings)
            # Assign each term to a cluster
            clusters = {i: [] for i in set(clustering.labels_)}
            for i, label in enumerate(clustering.labels_):
                clusters[label].append(terms[i])

            return clusters

        except Exception as e:
            print(f"Error in cluster_terms: {e}")
            return {}

    def get_global_embedding(
        self, main_df: pd.DataFrame, use_embeddings: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, pd.DataFrame]]:
        if use_embeddings:
            # Explicitly convert to a numpy array with a predefined shape, e.g., (-1, <embedding_dim>)
            embeddings = np.array(main_df["embedding"].tolist())
            return embeddings
        else:
            embeddings = self.encode_texts(main_df["text"].tolist())

            # Explicitly convert to a numpy array with a predefined shape, e.g., (-1, <embedding_dim>)
            embeddings = np.array(embeddings)
            return embeddings

    def create_umap_embeddings(
        self, global_embedding: List, mean_n_neighbors: int
    ) -> List:
        return apply_umap(global_embedding, mean_n_neighbors, 3).tolist()

    def _apply_clustering_common(self, main_df, umap_embeddings):
        umap_array = np.array(umap_embeddings)

        # Store UMAP embeddings and cluster labels in main_df
        main_df["umap_embeddings"] = umap_embeddings
        main_df["x"] = umap_array[:, 0]
        main_df["y"] = umap_array[:, 1]
        main_df["z"] = umap_array[:, 2]

        labels = apply_hdbscan(umap_array)
        labels = labels.labels_

        # Add cluster labels to main_df
        main_df["cluster_label"] = labels

        # Determine the correct id column: either "doc_id" or "message_id"
        id_column = "doc_id" if "doc_id" in main_df.columns else "message_id"

        # Update the DataFrame directly with the id_column
        main_df[id_column] = main_df[id_column]

        return main_df

    def compute_message_embeddings(
        self,
        neighbors,
        main_df: pd.DataFrame,
        use_embeddings: bool = True,
    ) -> None:
        global_embedding = self.get_global_embedding(main_df, use_embeddings)

        umap_embeddings = self.create_umap_embeddings(global_embedding, neighbors)
        result3d = self._apply_clustering_common(main_df, umap_embeddings)

        return result3d
