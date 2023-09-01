from typing import List, Tuple, Optional, Any, Dict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from hdbscan import HDBSCAN
import warnings
import torch.nn.functional as F
from scipy.spatial.distance import cosine
import torch
from torch import nn
from dlm_matrix.utils import log_handler
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

with warnings.catch_warnings():
    from numba.core.errors import NumbaWarning

    warnings.simplefilter("ignore", category=NumbaWarning)
    from umap import UMAP

model = SentenceTransformer("all-mpnet-base-v2")


def apply_umap(
    combined_features: np.ndarray,
    n_neighbors: int,
    n_components: int,
):
    # Check if n_neighbors is larger than the dataset size
    if n_neighbors > len(combined_features):
        # You can either set n_neighbors to the dataset size or another sensible value
        n_neighbors = len(combined_features)
        # You might want to log or print a warning here
        print(
            f"Warning: n_neighbors was larger than the dataset size; truncating to {n_neighbors}"
        )

    umap_embedding = UMAP(
        n_neighbors=int(n_neighbors),
        n_components=n_components,
        n_epochs=6000,
        min_dist=1,
        low_memory=False,
        learning_rate=0.5,
        verbose=False,
        metric="cosine",
    ).fit_transform(combined_features)

    return umap_embedding


def apply_hdbscan(
    embeddings: np.ndarray,
    min_samples: int = 5,
    cluster_selection_epsilon: float = 0.1,
    min_cluster_size: int = 70,
):
    cluster = HDBSCAN(
        metric="euclidean",
        min_samples=min_samples,
        min_cluster_size=min_cluster_size,
        core_dist_n_jobs=1,
        cluster_selection_epsilon=cluster_selection_epsilon,
        cluster_selection_method="leaf",
        leaf_size=40,
        algorithm="best",
    ).fit(embeddings)

    return cluster


def semantic_similarity_cross_entropy_adjusted(
    sentence1: str,
    sentence2: str,
    model: Optional[
        nn.Module
    ] = None,  # We allow a model to be passed, but assume a default model if not
    tokenizer: Optional[
        Any
    ] = None,  # This can be useful if the model requires a specific tokenizer
) -> float:
    """Calculates the semantic similarity between two sentences, adjusted by cross-entropy."""

    if not torch:
        raise ImportError("PyTorch is not available. Please install it to proceed.")

    # Use default model if none is provided
    if model is None:
        log_handler("Using default model", level="info")
        model = SentenceTransformer("all-mpnet-base-v2")

    # Perform encoding
    try:
        if tokenizer:
            input1 = tokenizer(
                sentence1, return_tensors="pt", truncation=True, max_length=512
            )
            input2 = tokenizer(
                sentence2, return_tensors="pt", truncation=True, max_length=512
            )
            embedding1 = model(**input1).last_hidden_state.mean(dim=1)
            embedding2 = model(**input2).last_hidden_state.mean(dim=1)
        else:
            embedding1 = model.encode(sentence1, convert_to_tensor=True)
            embedding2 = model.encode(sentence2, convert_to_tensor=True)
    except Exception as e:
        log_handler(f"Encoding failed: {e}", level="error")
        raise RuntimeError(f"Error during encoding: {e}")

    # Convert to probability distributions
    prob_dist1 = F.softmax(embedding1, dim=0)
    prob_dist2 = F.softmax(embedding2, dim=0)

    # Compute cross-entropy
    try:
        cross_entropy_loss = F.kl_div(
            F.log_softmax(prob_dist1, dim=0), prob_dist2, reduction="sum"
        )
    except Exception as e:
        log_handler(f"Cross-entropy calculation failed: {e}", level="error")
        raise RuntimeError(f"Error computing cross-entropy: {e}")

    # Compute cosine similarity
    try:
        cosine_sim = 1 - cosine(
            embedding1.detach().cpu().numpy(), embedding2.detach().cpu().numpy()
        )
    except Exception as e:
        log_handler(f"Cosine similarity calculation failed: {e}", level="error")
        raise RuntimeError(f"Error computing cosine similarity: {e}")

    # Clip the cosine similarity to [0, 1] range
    cosine_sim = max(0, min(cosine_sim, 1))

    # Compute the adjusted cosine similarity
    adjusted_cosine_sim = cosine_sim / (1 + abs(cross_entropy_loss.item()))

    return adjusted_cosine_sim


def calculate_similarity(embeddings1: List[float], embeddings2: List[float]) -> float:
    """
    Calculate semantic similarity between two sets of embeddings using cosine similarity.

    Args:
        embeddings1 (List[float]): Embeddings of the first message.
        embeddings2 (List[float]): Embeddings of the second message.

    Returns:
        float: Semantic similarity score between the two sets of embeddings.
    """
    # Convert the embeddings lists to numpy arrays
    embeddings1_array = np.array(embeddings1).reshape(1, -1)
    embeddings2_array = np.array(embeddings2).reshape(1, -1)

    # Calculate cosine similarity between the embeddings
    similarity_matrix = cosine_similarity(embeddings1_array, embeddings2_array)

    # The similarity score is the value in the similarity matrix
    similarity_score = similarity_matrix[0][0]

    return similarity_score


def compute_similar_keywords_global(
    keywords: List[str],
    embeddings: List[List[float]],
    use_argmax: bool,
    num_keywords: int,
) -> List[Tuple[str, float]]:
    """
    Compute similarity scores for keywords against a global embedding.

    Args:
        keywords (List[str]): List of keywords to compute similarity for.
        embeddings (List[List[float]]): List of embeddings for the keywords.
        use_argmax (bool): Whether to use argmax for similarity scores.
        num_keywords (int): Number of similar keywords to return.

    Returns:
        List[Tuple[str, float]]: List of tuples containing keyword and similarity score.
    """
    similarity_scores = cosine_similarity(embeddings, embeddings)
    similarity_scores = np.triu(similarity_scores, k=1)
    similarity_scores = similarity_scores.flatten()
    similarity_scores = similarity_scores[similarity_scores != 0]
    similarity_scores = np.sort(similarity_scores)[::-1]

    if use_argmax:
        similarity_scores = similarity_scores[:num_keywords]
    else:
        similarity_scores = similarity_scores[: num_keywords * len(keywords)]

    similarity_scores = similarity_scores.reshape(len(keywords), num_keywords)

    similar_keywords = []

    for i, keyword in enumerate(keywords):
        keyword_scores = similarity_scores[i]
        similar_keywords.append(
            [keywords[j] for j in np.argsort(keyword_scores)[::-1][:num_keywords]]
        )

    return similar_keywords


def compute_similar_keywords_query(
    keywords: List[str],
    query_vector: List[float],
    use_argmax: bool,
    query: str,
) -> List[Tuple[str, float]]:
    """
    Compute similarity scores for keywords against a query vector.

    Args:
        keywords (List[str]): List of keywords to compute similarity for.
        query_vector (List[float]): Vector representing the query.
        use_argmax (bool): Whether to use argmax for similarity scores.

    Returns:
        List[Tuple[str, float]]: List of tuples containing keyword and similarity score.
    """
    # Remove the query keyword from the list of keywords
    keywords = [
        keyword.strip()
        for keyword in keywords
        if keyword.strip().lower() != query.strip().lower()
    ]

    similarity_scores = []

    for keyword in keywords:
        keyword_vector = model.encode(keyword)
        similarity = cosine_similarity([query_vector], [keyword_vector])[0][0]
        similarity_scores.append((keyword, similarity))

    if use_argmax:
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[:1]
    else:
        similarity_scores = sorted(similarity_scores, key=lambda x: x[0])

    return similarity_scores


def compute_similar_keywords_per_keyword(
    keywords: List[str], embeddings: List[List[float]], num_keywords: int
) -> List[List[str]]:
    similarity_scores_list = [
        cosine_similarity([vector], embeddings)[0] for vector in embeddings
    ]
    similar_keywords_list = [
        [keywords[i] for i in np.argsort(similarity_scores)[::-1][:num_keywords]]
        for similarity_scores in similarity_scores_list
    ]

    return similar_keywords_list


def group_terms(
    terms: List[Tuple[str, List[float]]], use_argmax: bool = True
) -> Dict[Tuple[int], List[Tuple[str, List[float]]]]:
    """
    Group a list of terms by their semantic similarity using a specified language model.
    If 'use_argmax' is True, return the most similar term for each term in 'terms'.
    If 'use_argmax' is False, return the most similar terms for each term in 'terms'.
    """
    try:
        # Compute similarity scores
        similarities = cosine_similarity(
            [vector for _, vector in terms], [vector for _, vector in terms]
        )
        similarity_scores = np.argsort(similarities, axis=1)

        # Group terms
        clusters = {}
        for i, term in enumerate(terms):
            if use_argmax:
                cluster_id = tuple([similarity_scores[i][-2]])
            else:
                cluster_id = tuple(similarity_scores[i][-2:-11:-1])
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(term)

        return clusters

    except ValueError as e:
        log_handler(message=f"Error in group_terms: {e}", level="error")
        return {}
