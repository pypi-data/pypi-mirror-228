from typing import List, Tuple, Union
from sklearn.metrics.pairwise import cosine_similarity
import openai
from tqdm import tqdm
import logging
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from functools import wraps


class BaseSimilarity:
    def __init__(self, api_key: str = None):
        """Initialize a SemanticSimilarity."""
        self._semantic_vectors = []
        self.keywords = []
        self._openai_api_key = api_key
        self.embedding_ctx_length = 8191
        self.show_progress_bar = True
        self.MAX_RETRIES = 3

    def _create_retry_decorator(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            retry_decorator = retry(
                stop=stop_after_attempt(self.MAX_RETRIES),
                wait=wait_exponential(multiplier=1, min=2, max=6),
                retry=(
                    retry_if_exception_type(openai.error.Timeout)
                    | retry_if_exception_type(openai.error.APIError)
                    | retry_if_exception_type(openai.error.APIConnectionError)
                    | retry_if_exception_type(openai.error.RateLimitError)
                    | retry_if_exception_type(openai.error.ServiceUnavailableError)
                ),
                before_sleep=before_sleep_log(logging.getLogger(), logging.WARNING),
            )
            return retry_decorator(func)(*args, **kwargs)

        return wrapped_func

    def compute_similarity_scores(
        self,
        query: Union[str, List[str]],
        keywords: List[str],
        batches: bool = False,
        top_k: int = None,
    ) -> Union[List[Tuple[str, float]], List[List[Tuple[str, float]]]]:
        """
        Compute similarity scores between a query and a list of keywords.

        Parameters:
            query (Union[str, List[str]]): The query or list of queries for which similarity scores need to be computed.
            keywords (List[str]): A list of keywords to compare similarity with the query.
            batches (bool, optional): A flag to specify if the function is being used in a batch processing context.
                Defaults to False.
            top_k (int, optional): The number of top similar keywords to return. If None, all will be returned.

        Returns:
            Union[List[Tuple[str, float]], List[List[Tuple[str, float]]]]: A list of tuples if single query, or a list of list of tuples if batch queries.
        """

        if batches:
            query_vectors = self._embed_text_batch(query)
            similarities = cosine_similarity(
                query_vectors, self._embed_keywords(keywords)
            )

            similarity_scores = []
            for sim_array in similarities:
                scores = [
                    (keyword, float(similarity))
                    for keyword, similarity in zip(keywords, sim_array)
                ]
                scores.sort(key=lambda x: x[1], reverse=True)
                if top_k is not None:
                    scores = scores[:top_k]

                similarity_scores.append(scores)

            return similarity_scores

        else:
            query_vector = self._embed_text(query)
            similarities = cosine_similarity(
                [query_vector], self._embed_keywords(keywords)
            )[0]

            similarity_scores = [
                (keyword, float(similarity))
                for keyword, similarity in zip(keywords, similarities)
            ]

            similarity_scores.sort(key=lambda x: x[1], reverse=True)

            if top_k is not None:
                similarity_scores = similarity_scores[:top_k]

            return similarity_scores

    def _create_embedding(self, text: Union[str, List[str]]) -> List[float]:
        @self._create_retry_decorator
        def inner_function(*args, **kwargs):
            try:
                self._check_and_set_openai_api()
                if not text:
                    logging.error("No text provided to embed")
                    return []

                response = openai.Embedding.create(
                    input=text[: self.embedding_ctx_length],
                    engine="text-embedding-ada-002",
                )
                return [item["embedding"] for item in response["data"]]
            except openai.error.OpenAIError as e:
                logging.error(f"An OpenAI error occurred: {e}")
                raise e
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                raise e

        return inner_function(self, text)

    def _embed_text_batch(self, keywords: List[str]) -> List[List[float]]:
        """Embed a list of keywords as a list of lists of floats using the OpenAI API."""
        all_embeddings = []

        # Display progress bar if the flag is True
        iterable = tqdm(keywords) if self.show_progress_bar else keywords

        for i in range(0, len(iterable), self.embedding_ctx_length):
            embeddings = self._create_embedding(
                keywords[i : i + self.embedding_ctx_length]
            )
            all_embeddings.extend(embeddings)

        print(f"Embedding {all_embeddings} keywords")
        return all_embeddings

    def _check_and_set_openai_api(self):
        """Check and set OpenAI API."""
        if not self._openai_api_key:
            raise ValueError("OpenAI API key not set")
        openai.api_key = self._openai_api_key

    def _embed_text(self, text: str) -> List[float]:
        """Embed a piece of text as a list of floats using the OpenAI API."""
        self._check_and_set_openai_api()
        embeddings = self._create_embedding(text)
        return embeddings[0] if embeddings else []

    def _embed_keywords(self, keywords: List[str]) -> List[List[float]]:
        """Embed a list of keywords as a list of lists of floats using a specified language model."""
        return [self._embed_text(keyword) for keyword in keywords]

    def _compute_semantic_vectors(
        self, keywords: List[str]
    ) -> List[Tuple[str, List[float]]]:
        """Compute semantic vectors for a list of keywords."""
        return [(keyword, self._embed_text(keyword)) for keyword in keywords]
