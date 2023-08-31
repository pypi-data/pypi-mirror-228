from typing import Dict, List, Optional, Tuple, Union
from dlm_matrix.representation.chain import ChainRepresentation
from dlm_matrix.representation.filters import ChainFilter
from dlm_matrix.representation.handler import ChainHandler
from dlm_matrix.embedding.spatial import SpatialSimilarity
from dlm_matrix.builder import ChainTreeBuilder
from dlm_matrix.context import get_file_paths
import pandas as pd


def compute_mean_n_neighbors(main_dfs: List[pd.DataFrame]) -> float:
    """
    Efficiently compute the mean n_neighbors from the list of main_dfs.

    Args:
        main_dfs (List[pd.DataFrame]): List of DataFrames containing n_neighbors column.

    Returns:
        float: Mean value of n_neighbors.
    """

    total_sum = 0
    total_count = 0

    for df in main_dfs:
        total_sum += df["n_neighbors"].sum()
        total_count += len(df)

    return int(total_sum / total_count if total_count != 0 else 0)


class ChainCombiner:
    def __init__(
        self,
        target_number: int = 10,
        builder: Optional[ChainTreeBuilder] = None,
        chain_filter: Optional[ChainFilter] = None,
        chain_handler: Optional[ChainHandler] = None,
    ):
        self.builder = builder if builder else ChainTreeBuilder()
        self.chain_filter = chain_filter if chain_filter else ChainFilter()
        self.chain_handler = chain_handler if chain_handler else ChainHandler()
        self.conversations = self.builder.conversations
        self.conversation_trees = self.builder.create_conversation_trees(target_number)
        self.semantic_similarity = SpatialSimilarity()
        self.base_persist_dir = self.builder.root_dir

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
        animate: bool = True,
    ):
        filtered_trees, start = self.process_and_filter_trees(
            tree_range, use_graph_index, skip_indexes
        )

        main_dfs = []

        for start_count, conversation_tree in enumerate(filtered_trees, start=start):
            tetra = ChainRepresentation(conversation_tree)

            title = tetra.conversation.conversation.title
            print(f"Processing conversation {title}.")

            tree_docs = tetra._procces_coordnates(use_graph=use_graph, animate=animate)
            relationship_df = tetra.create_prompt_response_df()

            if tree_docs is None:
                for doc in tree_docs:
                    tetra.conversation.conversation.mapping[
                        doc.doc_id
                    ].message.umap_embeddings = doc.umap_embeddings

                    tetra.conversation.conversation.mapping[
                        doc.doc_id
                    ].message.cluster_label = doc.cluster_label

                    tetra.conversation.conversation.mapping[
                        doc.doc_id
                    ].message.n_neighbors = doc.n_neighbors

            mapping_dict = tetra.conversation.conversation.dict()

            (
                persist_dir,
                main_df_name,
                global_embedding_name,
                conversation_tree_name,
                relationship_name,
            ) = get_file_paths(self.base_persist_dir, title)

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
            main_dfs.append(main_df)

        mean_n_neighbors = compute_mean_n_neighbors(main_dfs)
        print(f"Mean n_neighbors: {mean_n_neighbors}")

        return main_dfs, mean_n_neighbors

    def get_message_coord_map(
        self,
        trees: Optional[List[object]] = None,
        format: Optional[str] = None,
        exclude_key: Optional[List[str]] = None,
        path: Optional[str] = None,
        embedding_model: Optional[object] = None,
        exclude_columns=None,
    ) -> Union[Dict, pd.DataFrame, None]:
        if embedding_model:
            format = "df"

        message_coord_map = self.builder.create_message_map(
            trees=trees,
            format=format,
            exclude_key=exclude_key,
            path=path,
            embedding_model=embedding_model,
        )

        if format == "json" and path:
            return None

        if format == "df":
            main_df = message_coord_map
        else:
            main_df = pd.DataFrame.from_dict(message_coord_map, orient="index")

        main_df = self.builder.format_dataframe(main_df, exclude_columns)
        return main_df
