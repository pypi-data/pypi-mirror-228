from typing import List, Dict
from dlm_matrix.transformation import Coordinate
from dlm_matrix.context import MultiLevelContext, DataFrameStore, JsonStore
from dlm_matrix.embedding.spatial import SpatialSimilarity
from dlm_matrix.models import ChainDocument, ChainDocumentStore
from pydantic import BaseModel
import pandas as pd
import logging


class ChainHandler(BaseModel):
    chain_documents: List[ChainDocument] = []
    flattened_dict_id_coord: Dict[str, Coordinate] = {}
    spatial_similarity_model = SpatialSimilarity()
    docstore = ChainDocumentStore()

    class Config:
        arbitrary_types_allowed = True

    def add_local_embeddings(self, docs: List[ChainDocument]) -> None:
        for doc in docs:
            if doc is None:
                continue
            self.chain_documents.append(doc)
            self.docstore.add_documents([doc])  # Add single document
            self.flattened_dict_id_coord[doc.doc_id] = doc.coordinate

    def create_dataframe(self) -> pd.DataFrame:
        """
        Create a DataFrame from the chain documents.
        """
        data = [doc.dict() for doc in self.chain_documents]

        # Handle the special case for 'doc_id' where it can default to an empty string
        for entry in data:
            entry["doc_id"] = entry["doc_id"] if entry["doc_id"] else ""

        main_df = pd.DataFrame(data)
        return main_df

    def add_documents_and_create_dataframe(
        self, docs: List[ChainDocument], n_jobs=4
    ) -> pd.DataFrame:
        """
        Adds local embeddings to the documents and creates a DataFrame.

        Args:
            docs (List[ChainDocument]): A list of ChainDocument objects.
            n_jobs (int): The number of threads for parallel processing.

        Returns:
            pd.DataFrame: A DataFrame containing the document data.
        """
        try:
            self.add_local_embeddings(docs)
            return self.create_dataframe()
        except Exception as e:
            logging.error(f"Error while adding documents and creating DataFrame: {e}")
            return pd.DataFrame()  # return an empty DataFrame in case of error

    def add_coordinates_to_dataframe(
        self, storage_context: MultiLevelContext, keep_old_columns=False
    ):
        """
        Adds coordinates to the DataFrame and performs related operations.

        Args:
            storage_context (MultiLevelContext): The storage context containing the DataFrame.
            keep_old_columns (bool): Whether to keep the old columns ("coordinate" and "umap_embeddings") in the DataFrame.
        """
        self._add_coordinate_column(storage_context)
        self._split_coordinate_column(storage_context)
        self._split_umap_embeddings(storage_context)

        if not keep_old_columns:
            storage_context.main_df_store.df.drop(
                ["coordinate", "umap_embeddings"], axis=1, inplace=True
            )

    def _add_coordinate_column(self, storage_context: MultiLevelContext):
        """Adds a 'coordinate' column to the DataFrame.

        Args:
            storage_context (MultiLevelContext): The storage context containing the DataFrame.
        """
        # assuming that all keys are present in the dictionary
        storage_context.main_df_store.df[
            "coordinate"
        ] = storage_context.main_df_store.df["doc_id"].map(self.flattened_dict_id_coord)

    def _split_coordinate_column(self, storage_context: MultiLevelContext):
        """Splits the 'coordinate' column into multiple columns.

        Args:
            storage_context (MultiLevelContext): The storage context containing the DataFrame.
        """
        coord_names = Coordinate.get_coordinate_names()
        storage_context.main_df_store.df[
            coord_names
        ] = storage_context.main_df_store.df["coordinate"].apply(pd.Series)

    def _split_umap_embeddings(self, storage_context: MultiLevelContext):
        """Splits the 'umap_embeddings' column into x, y, z columns.

        Args:
            storage_context (MultiLevelContext): The storage context containing the DataFrame.
        """
        storage_context.main_df_store.df[["x", "y", "z"]] = pd.DataFrame(
            storage_context.main_df_store.df["umap_embeddings"].tolist(),
            index=storage_context.main_df_store.df.index,
        )

    def initialize_storage_context(
        self,
        main_df: pd.DataFrame,
        conversation_tree: dict,
        relationship_df=pd.DataFrame,
    ):
        return MultiLevelContext.from_defaults(
            main_df_store=DataFrameStore(main_df),
            relationship_store=DataFrameStore(relationship_df),
            conversation_tree_store=JsonStore(conversation_tree),
        )

    def create_and_persist_dataframes(
        self,
        persist_dir,
        main_df_name,
        global_embedding_name,
        conversation_tree_name,
        relationship_name,
        conversation_tree,
        tree_docs,
        relationship_df,
    ):
        try:
            # Create the main_df DataFrame
            main_df = self.add_documents_and_create_dataframe(tree_docs)

            # Initialize storage context with main_df
            storage_context = self.initialize_storage_context(
                main_df, conversation_tree, relationship_df
            )

            # Add coordinates to the DataFrame
            self.add_coordinates_to_dataframe(storage_context)

            # Persist the storage context
            storage_context.persist(
                persist_dir=persist_dir,
                main_df_fname=main_df_name,
                global_embedding_fname=global_embedding_name,
                conversation_tree_fname=conversation_tree_name,
                relationship_fname=relationship_name,
            )
            return main_df

        except Exception as e:
            # Handle any exceptions that might occur and return None
            print("An error occurred while creating and persisting dataframes:", str(e))
            return None

    def persist_dataframes(
        self,
        main_df: pd.DataFrame,
        persist_dir: str,
        main_df_name: str,
        global_embedding_name: str,
        conversation_tree_name: str,
        relationship_name: str,
        conversation_tree: dict,
        relationship_df=pd.DataFrame,
    ):
        try:
            # Initialize storage context with main_df
            storage_context = self.initialize_storage_context(
                main_df, conversation_tree, relationship_df
            )

            # Persist the storage context
            storage_context.persist(
                persist_dir=persist_dir,
                main_df_fname=main_df_name,
                global_embedding_fname=global_embedding_name,
                conversation_tree_fname=conversation_tree_name,
                relationship_fname=relationship_name,
            )

        except Exception as e:
            # Handle any exceptions that might occur
            print("An error occurred while persisting dataframes:", str(e))
