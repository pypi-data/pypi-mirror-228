from typing import Dict, List, Optional, Tuple, Any
from dlm_matrix.representation.chain import ChainRepresentation
from dlm_matrix.representation.filters import ChainFilter
from dlm_matrix.representation.handler import ChainHandler
from dlm_matrix.embedding.spatial import SpatialSimilarity
from dlm_matrix.builder import ChainTreeBuilder
from dlm_matrix.context import get_file_paths, DEFAULT_PERSIST_DIR
import pandas as pd


def compute_and_combine(main_dfs: List[pd.DataFrame]) -> Tuple[float, pd.DataFrame]:
    """
    Efficiently compute the mean n_neighbors from the list of main_dfs and combine them into a single DataFrame.

    Args:
        main_dfs (List[pd.DataFrame]): List of DataFrames containing n_neighbors column.

    Returns:
        Tuple[float, pd.DataFrame]: Tuple containing the mean value of n_neighbors and the combined DataFrame.
    """
    combined_df = pd.concat(
        main_dfs, ignore_index=True
    )  # Using ignore_index=True to reindex combined DataFrame

    total_sum = 0
    total_count = 0

    for df in main_dfs:
        total_sum += df["n_neighbors"].sum()
        total_count += len(df)

    mean_neighbors = total_sum / total_count if total_count != 0 else 0.0

    return mean_neighbors, combined_df


class ChainCombiner(ChainTreeBuilder):
    def __init__(
        self,
        target_number: int = 10,
        path: Optional[str] = None,
        api_key: Optional[str] = None,
        output_name: Optional[str] = None,
        chain_filter: Optional[ChainFilter] = None,
        chain_handler: Optional[ChainHandler] = None,
        base_persist_dir: Optional[str] = DEFAULT_PERSIST_DIR,
    ):
        super().__init__(path=path, base_persist_dir=base_persist_dir)
        self.chain_filter = chain_filter if chain_filter else ChainFilter()
        self.chain_handler = chain_handler if chain_handler else ChainHandler()
        self.conversation_trees = self.create_conversation_trees(target_number)
        self.semantic_similarity = SpatialSimilarity()
        self.base_persist_dir = base_persist_dir
        self.output_name = output_name
        self.api_key = api_key

    def _validate_use_graph_index(self, use_graph_index):
        if use_graph_index is not None and not isinstance(use_graph_index, int):
            raise ValueError("use_graph_index should be an integer or None.")

    def _process_tree_range(self, tree_range):
        start, end = tree_range
        if end is None:
            end = len(self.conversation_trees)
        return start, end

    def _filter_conversation_trees(self, start, end, skip_indexes):
        if skip_indexes is not None:
            filtered_trees = [
                ct
                for i, ct in enumerate(self.conversation_trees[start:end])
                if i not in skip_indexes
            ]
        else:
            filtered_trees = self.conversation_trees[start:end]
        return filtered_trees

    def process_and_filter_trees(self, tree_range, use_graph_index, skip_indexes):
        self._validate_use_graph_index(use_graph_index)
        start, end = self._process_tree_range(tree_range)
        filtered_trees = self._filter_conversation_trees(start, end, skip_indexes)

        return filtered_trees, start

    def process_trees(
        self,
        use_graph: bool = False,
        use_graph_index: Optional[int] = None,
        tree_range: Optional[Tuple[int, int]] = (0, None),
        skip_indexes: Optional[List[int]] = None,
        animate: bool = False,
        use_openai: bool = False,
    ) -> pd.DataFrame:
        """
        Main method to process trees and return a DataFrame.

        Args:
            use_graph: Whether to use a graph representation.
            use_graph_index: Index of the graph to use, if any.
            tree_range: Tuple specifying the range of trees to process.
            skip_indexes: List of tree indexes to skip.
            animate: Whether to animate the process.

        Returns:
            A DataFrame containing the processed information.
        """

        # Automatically set pre_computed_embeddings based on use_openai
        pre_computed_embeddings = not use_openai

        filtered_trees, start = self.process_and_filter_trees(
            tree_range, use_graph_index, skip_indexes
        )
        main_dfs = []

        for start_count, conversation_tree in enumerate(filtered_trees, start=start):
            tetra = self.initialize_conversation_tree(conversation_tree, self.api_key)
            tree_docs, relationship_df = self.process_coordinates_and_features(
                tetra, use_graph, animate, pre_computed_embeddings, use_openai
            )

            if tree_docs is not None:
                self.update_mapping_with_features(tetra, tree_docs)

            main_df = self.create_and_save_dataframes(tetra, tree_docs, relationship_df)
            main_dfs.append(main_df)

        mean_n_neighbors, combined_df = compute_and_combine(main_dfs)

        df = self.format_as_dataframe(
            data=combined_df,
            neighbors=mean_n_neighbors,
            embedding_model=self.semantic_similarity,
            path=self.output_name,
            use_embeddings=False,
        )

        return df

    def initialize_conversation_tree(
        self, conversation_tree: Dict[str, Any], api_key: Optional[str] = None
    ) -> ChainRepresentation:
        """
        Initialize a conversation tree and print its title.

        Args:
            conversation_tree: The conversation tree to initialize.

        Returns:
            Initialized ChainRepresentation object.
        """
        tetra = ChainRepresentation(
            conversation_tree=conversation_tree, api_key=api_key
        )
        title = tetra.conversation.conversation.title
        print(f"Processing conversation {title}.")
        return tetra

    def process_coordinates_and_features(
        self,
        tetra: ChainRepresentation,
        use_graph: bool,
        animate: bool,
        pre_computed_embeddings=False,
        use_openai=False,
    ) -> Tuple[List, pd.DataFrame]:
        """
        Process the coordinates and features of the conversation tree.

        Args:
            tetra: The initialized ChainRepresentation object.
            use_graph: Whether to use a graph representation.
            animate: Whether to animate the process.

        Returns:
            A tuple containing the processed tree documents and the relationship DataFrame.
        """
        tree_docs = tetra._procces_coordnates(use_graph=use_graph, animate=animate)
        relationship_df = tetra.create_prompt_response_df(
            pre_computed_embeddings, use_openai
        )
        return tree_docs, relationship_df

    def update_mapping_with_features(
        self, tetra: ChainRepresentation, tree_docs
    ) -> None:
        """
        Update the mapping of the conversation tree with new features.

        Args:
            tetra: The initialized ChainRepresentation object.
            tree_docs: The processed tree documents containing new features.

        Returns:
            None
        """
        for doc in tree_docs:
            message = tetra.conversation.conversation.mapping[doc.doc_id].message
            attributes_to_update = ["umap_embeddings", "cluster_label", "n_neighbors"]

            for attr in attributes_to_update:
                setattr(message, attr, getattr(doc, attr))

    def create_and_save_dataframes(
        self, tetra: ChainRepresentation, tree_docs: List, relationship_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create and save DataFrames for the conversation tree.

        Args:
            tetra: The initialized ChainRepresentation object.
            tree_docs: The processed tree documents.
            relationship_df: The DataFrame containing relationships among messages.

        Returns:
            The main DataFrame.
        """
        mapping_dict = tetra.conversation.conversation.dict()
        (
            persist_dir,
            main_df_name,
            global_embedding_name,
            conversation_tree_name,
            relationship_name,
        ) = get_file_paths(self.base_persist_dir, tetra.conversation.conversation.title)

        main_df = tetra.handler.create_and_persist_dataframes(
            persist_dir,
            main_df_name,
            global_embedding_name,
            conversation_tree_name,
            relationship_name,
            mapping_dict,
            tree_docs,
            relationship_df,
        )
        return main_df
