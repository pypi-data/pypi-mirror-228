import logging
import re
from typing import List, Tuple, Union, Dict, Optional, Callable
import pandas as pd
from dlm_matrix.utility.helper import DataHelper
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from collections import Counter
from dlm_matrix.embedding import SpatialSimilarity
from dlm_matrix.embedding.utils import (
    compute_similar_keywords_query,
    compute_similar_keywords_per_keyword,
    compute_similar_keywords_global,
)


class DataRetriever:
    def __init__(self, data_helper: DataHelper):
        """Initializes the DataRetriever with a given DataHelper."""
        self.data = data_helper.finalize()
        self.prompt_col = data_helper.prompt_col
        self.response_col = data_helper.response_col
        self.model = SpatialSimilarity()
        self._validate_columns()

    def _validate_columns(self) -> None:
        """Validates if the specified columns exist in the dataset."""
        for col in [self.prompt_col, self.response_col]:
            if col not in self.data.columns:
                logging.error(f"Column '{col}' not found in data.")
                raise ValueError(f"Column '{col}' not found in data.")

    def _validate_pair_type(self, pair_type: str) -> None:
        """Validates if the provided pair_type is valid."""
        valid_pair_types = ["both", self.prompt_col, self.response_col]
        if pair_type not in valid_pair_types:
            logging.error(
                f"Invalid pair_type. Choose from {', '.join(valid_pair_types)}"
            )
            raise ValueError(
                f"Invalid pair_type. Choose from {', '.join(valid_pair_types)}"
            )

    def _get_data_by_pair_type(
        self, data_subset: pd.DataFrame, pair_type: str
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Returns data based on the pair_type from a given data subset."""
        self._validate_pair_type(pair_type)

        if pair_type == "both":
            return list(
                zip(
                    data_subset[self.prompt_col].tolist(),
                    data_subset[self.response_col].tolist(),
                )
            )
        return data_subset[pair_type].tolist()

    def get_examples(
        self, pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Gets examples of the specified type from the data."""
        return self._get_data_by_pair_type(self.data, pair_type)

    def get_random_examples(
        self, n: int, pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Gets n random examples of the specified type from the data."""
        return self._get_data_by_pair_type(self.data.sample(n), pair_type)

    def get_first_n_examples(
        self, n: int, pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Gets the first n examples of the specified type from the data."""
        return self._get_data_by_pair_type(self.data.head(n), pair_type)

    def search_examples(
        self, keywords: Union[str, List[str]], pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Searches examples containing the keyword(s) of the specified type from the data."""
        if isinstance(keywords, str):
            keywords = [keywords]

        mask = self.data[self.prompt_col].str.contains(
            "|".join(map(re.escape, keywords))
        ) | self.data[self.response_col].str.contains(
            "|".join(map(re.escape, keywords))
        )

        filtered_data = self.data[mask]
        return self._get_data_by_pair_type(filtered_data, pair_type)

    def count_keyword(
        self, keyword: str, pair_type: str = "both"
    ) -> Union[int, Dict[str, int]]:
        data = self.data  # We get the data directly from the DataHelper instance

        if pair_type == "both":
            return {
                "prompt": data[self.prompt_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum(),
                "response": data[self.response_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum(),
            }
        elif pair_type == self.prompt_col:
            return (
                data[self.prompt_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum()
            )
        elif pair_type == self.response_col:
            return (
                data[self.response_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum()
            )
        else:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}', 'both'"
            )

    def create_prompt_matrix(self) -> csr_matrix:
        """Creates a sparse matrix of prompts"""
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(self.data[self.prompt_col].tolist())

    def filter_data(self, word: str, pair_type: str = None) -> List[str]:
        """Returns the data that contain a specific word"""
        if pair_type not in [self.prompt_col, self.response_col]:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}'"
            )
        data_column = (
            self.prompt_col if pair_type == self.prompt_col else self.response_col
        )
        data = self.data[data_column].tolist()
        return [text for text in data if word in text]

    def count_occurrences(self, word: str, pair_type: str = "prompt") -> int:
        """Counts the number of occurrences of a word in the data"""
        if pair_type not in [self.prompt_col, self.response_col, "both"]:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}', 'both'"
            )

        text = ""
        if pair_type in [self.prompt_col, "both"]:
            text += " ".join(self.data[self.prompt_col].tolist())

        if pair_type in [self.response_col, "both"]:
            text += " ".join(self.data[self.response_col].tolist())

        return Counter(text.split())[word]

    def compute_similar_keywords(
        self,
        keywords: List[str],
        num_keywords: int = 10,
        use_argmax: bool = True,
        per_keyword: bool = False,
        query: Optional[str] = None,
    ) -> List[str]:
        """
        Compute similar keywords based on embeddings.

        Args:
            keywords (List[str]): List of keywords for which to find similar keywords.
            num_keywords (int, optional): Number of similar keywords to return. Defaults to 10.
            use_argmax (bool, optional): Whether to use argmax for similarity scores. Defaults to True.
            per_keyword (bool, optional): Whether to compute similar keywords per keyword. Defaults to False.
            query (Optional[str], optional): Query keyword for which to find similar keywords. Defaults to None.

        Returns:
            List[str]: List of similar keywords.
        """
        embeddings = self.model.fit(keywords)

        if query is not None:
            query_vector = self.model.fit([query])[0]
            similarity_scores = compute_similar_keywords_query(
                keywords, query_vector, use_argmax, query
            )
        else:
            if per_keyword:
                similarity_scores = compute_similar_keywords_per_keyword(
                    keywords, embeddings, num_keywords
                )
            else:
                similarity_scores = compute_similar_keywords_global(
                    keywords, embeddings, use_argmax, num_keywords
                )

        return similarity_scores
