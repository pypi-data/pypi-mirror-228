from typing import List, Tuple, Dict, Union, Any, Callable, Optional
from sklearn.metrics.pairwise import cosine_similarity
import torch
from torch import nn
from sentence_transformers import SentenceTransformer
import torch.nn.functional as F
from scipy.spatial.distance import cosine

model = SentenceTransformer("all-mpnet-base-v2")


def semantic_similarity_cross_entropy(
    sentence1: str,
    sentence2: str,
    model: Optional[nn.Module] = None,
    tokenizer: Optional[Any] = None,
    return_adjusted_cosine_sim: bool = False,
) -> Union[float, Tuple[float, float]]:
    if not torch:
        raise ImportError("PyTorch is not available. Please install it to proceed.")

    if model is None:
        model = SentenceTransformer("all-mpnet-base-v2")

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
        raise RuntimeError(f"Error during encoding: {e}")

    prob_dist1 = F.softmax(embedding1, dim=0)
    prob_dist2 = F.softmax(embedding2, dim=0)

    cross_entropy_loss = F.kl_div(
        F.log_softmax(prob_dist1, dim=0), prob_dist2, reduction="sum"
    ).item()

    cosine_sim = 1 - cosine(
        embedding1.detach().cpu().numpy(), embedding2.detach().cpu().numpy()
    )
    cosine_sim = max(0, min(cosine_sim, 1))

    if return_adjusted_cosine_sim:
        adjusted_cosine_sim = cosine_sim / (1 + abs(cross_entropy_loss))
        return adjusted_cosine_sim

    return cross_entropy_loss, cosine_sim


def calculate_weight_sum_squares(node1: Tuple[Any, ...], node2: Tuple[Any, ...]) -> int:
    """Calculate the weight of an edge as the sum of the squares of the node values."""
    return sum(value**2 for value in node1[1:] + node2[1:])


def custom_weight(start, end):
    return hash(start) % 10 + hash(end) % 10


def custom_node_attributes(node):
    return {"type": type(node).__name__, "hash": hash(node)}


def custom_edge_attributes(start, end):
    return {"hash_sum": hash(start) + hash(end)}


def should_connect_semantic(node1: Tuple[Any, ...], node2: Tuple[Any, ...]) -> bool:
    sentence1 = node1[0]
    sentence2 = node2[0]
    cross_entropy_threshold = 0.5
    cosine_similarity_threshold = 0.8

    cross_entropy_loss, cosine_sim = semantic_similarity_cross_entropy(
        sentence1, sentence2
    )

    if (
        cross_entropy_loss < cross_entropy_threshold
        and cosine_sim > cosine_similarity_threshold
    ):
        return True
    else:
        return False


def create_tetrahedron_sequence(
    nodes: List[Any],
    calculate_weight: Optional[Callable] = None,
    node_attributes_func: Optional[Callable] = None,
    edge_attributes_func: Optional[Callable] = None,
    multi_layered_data_func: Optional[Callable] = None,
    weighted: bool = True,
) -> List[Dict[str, Union[int, float, None, Dict]]]:
    """
    Takes a list of nodes and returns a sequence that represents a tetrahedron with multi-layered capabilities.
    """

    if len(nodes) != 4:
        raise ValueError("A tetrahedron must have exactly four nodes.")

    sequence = [
        {
            "start_node": start,
            "end_node": end,
            "weight": calculate_weight(start, end)
            if (calculate_weight and weighted)
            else None,
            "node_attr_1": node_attributes_func(start) if node_attributes_func else {},
            "node_attr_2": node_attributes_func(end) if node_attributes_func else {},
            "edge_attr": edge_attributes_func(start, end)
            if edge_attributes_func
            else {},
            "multi_layered_data": multi_layered_data_func(start, end)
            if multi_layered_data_func
            else {},
        }
        for start in nodes
        for end in nodes
        if start != end
    ]

    return sequence


def validate_parameters(
    nodes: List[Tuple[Any, ...]],
    calculate_weight: Optional[Callable],
    should_connect: Optional[Callable],
    directed: bool,
    # Add other parameters if needed
):
    if not all(isinstance(node, tuple) and len(node) >= 2 for node in nodes):
        raise ValueError(
            "Each node should be a tuple with at least two elements: an identifier and one or more values."
        )
    if calculate_weight is not None and not callable(calculate_weight):
        raise ValueError(
            "If provided, calculate_weight must be a callable function that takes two nodes and returns an integer."
        )
    if should_connect is not None and not callable(should_connect):
        raise ValueError(
            "If provided, should_connect must be a callable function that takes two nodes and returns a boolean."
        )
    if not isinstance(directed, bool):
        raise ValueError("The directed argument must be a boolean value.")


def create_fully_connected_sequence(
    nodes: List[Tuple[Any, ...]],
    calculate_weight: Optional[Callable] = calculate_weight_sum_squares,
    should_connect: Optional[Callable] = should_connect_semantic,
    directed: bool = True,
    multigraph: bool = True,
    self_loops: bool = False,
    node_attributes: Optional[Dict[Any, Dict[str, Any]]] = None,
    edge_attributes: Optional[Dict[Tuple[Any, Any], Dict[str, Any]]] = None,
) -> List[Dict[str, Union[int, float, None]]]:
    """
    Takes a list of nodes and returns a sequence that represents a fully connected graph.
    """
    validate_parameters(nodes, calculate_weight, should_connect, directed)

    seen_edges = set()  # to keep track of edges already added

    sequence = [
        {
            "start_node": nodes[i][0],
            "end_node": nodes[j][0],
            "weight": calculate_weight(nodes[i], nodes[j])
            if calculate_weight
            else None,
            "node_attr_1": node_attributes.get(nodes[i][0], {})
            if node_attributes
            else {},
            "node_attr_2": node_attributes.get(nodes[j][0], {})
            if node_attributes
            else {},
            "edge_attr": edge_attributes.get((nodes[i][0], nodes[j][0]), {})
            if edge_attributes
            else {},
        }
        for i in range(len(nodes))
        for j in range(i + 1 if not self_loops else i, len(nodes))
        if should_connect and should_connect(nodes[i], nodes[j])
        if not (not directed and (nodes[j][0], nodes[i][0]) in seen_edges)
        if not seen_edges.add(
            (nodes[i][0], nodes[j][0])
        )  # This will always evaluate to False, effectively adding the edge to seen_edges
    ]

    # If it's not a multigraph, remove duplicate entries
    if not multigraph:
        sequence = [dict(t) for t in {tuple(d.items()) for d in sequence}]

    return sequence


def create_tetrahedron_data(
    sequence: List[Dict[str, Union[Any, int, Dict[str, Any]]]]
) -> Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]:
    """Generates a tetrahedron data structure based on input sequence."""

    # Validate input sequence
    if not sequence or not isinstance(sequence, list):
        raise ValueError("Input sequence must be a non-empty list.")

    # Extract edges from the sequence
    edge_list = [
        (edge["start_node"], edge["end_node"]) for edge in sequence if edge["weight"]
    ]
    edge_set = set(edge_list)

    # Generate tetrahedron complexes
    edge_complex, triangle_complex, tetrahedron_complex = set(), set(), set()
    for a, b in edge_set:
        for c, d in edge_set:
            nodes = {a, b, c, d}
            if len(nodes) == 4:
                edge_complex.update({(a, b), (a, c), (a, d), (b, c), (b, d), (c, d)})
                triangle_complex.update({(a, b, c), (a, b, d), (a, c, d), (b, c, d)})
                tetrahedron_complex.add(tuple(nodes))

    # Construct the nested tetrahedron data
    tetrahedron_data = {}
    for tetrahedron in tetrahedron_complex:
        node_data = {}
        for node in tetrahedron:
            edge_data = {}
            relevant_edges = {edge for edge in edge_complex if node in edge}
            for edge in relevant_edges:
                triangle_data = {}
                relevant_triangles = {
                    tri for tri in triangle_complex if set(edge).issubset(set(tri))
                }
                for triangle in relevant_triangles:
                    triangle_data[triangle] = {}
                edge_data[edge] = triangle_data
            node_data[node] = edge_data
        tetrahedron_data[tetrahedron] = node_data

    return tetrahedron_data
