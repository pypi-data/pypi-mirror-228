from typing import Dict, Tuple, Any, List, Union, Optional
import collections
from dlm_matrix.representation.compute import CoordinateRepresentation
import itertools
import networkx as nx
import pandas as pd
from dlm_matrix.models import ChainTreeIndex
from dlm_matrix.transformation import Coordinate


class ChainRepresentation(CoordinateRepresentation):
    def __init__(
        self,
        conversation_tree: ChainTreeIndex,
        message_dict: Optional[Dict[str, Coordinate if Coordinate else Any]] = None,
        conversation_dict: Optional[
            Dict[str, Coordinate if Coordinate else Any]
        ] = None,
    ):
        super().__init__(conversation_tree)
        self.message_dict = (
            self._message_representation() if message_dict is None else message_dict
        )
        self.conversation_dict = (
            self._conversation_representation()
            if conversation_dict is None
            else conversation_dict
        )


    def create_prompt_response_df(self) -> pd.DataFrame:
        """Create a DataFrame capturing the relationship between prompts and responses."""

        def extract_coordinates(coordinate) -> list:
            """Extract x, y, z, t, and n_parts from the coordinate object and return them as a list."""
            return [
                coordinate.x,
                coordinate.y,
                coordinate.z,
                coordinate.t,
                coordinate.n_parts,
            ]

        message_dict = self._message_representation()
        conversation_dict = self._conversation_representation()

        prompts, responses, prompt_ids, response_ids = [], [], [], []
        created_times, prompt_coordinates, response_coordinates = [], [], []
        prompt_encodings, response_encodings = [], []

        for message_id, _ in message_dict.items():
            message_content = self.get_message_content(message_id)
            if message_content is None:
                continue

            created_time = self.get_message_create_time(message_id)
            if created_time is None:
                continue

            coordinate = self.get_message_coordinate(message_id)
            if coordinate is None:
                continue

            author = self.get_message_author_role(message_id)
            if author is None:
                continue

            children = conversation_dict.get(message_id, [None, []])[1]

            for child_id in children:
                child_message = message_dict.get(child_id)
                if child_message is None:
                    continue

                child_author = self.get_message_author_role(child_id)
                if child_author is None:
                    continue

                if author == "user" and child_author == "assistant":
                    prompts.append(message_content)
                    responses.append(self.get_message_content(child_id))
                    prompt_ids.append(message_id)
                    response_ids.append(child_id)
                    created_times.append(created_time)
                    prompt_coordinates.append(
                        extract_coordinates(self.get_message_coordinate(message_id))
                    )
                    response_coordinates.append(
                        extract_coordinates(self.get_message_coordinate(child_id))
                    )
                    prompt_encodings.append(
                        list(map(float, self.message_dict[message_id].message.embedding))
                    )
                    response_encodings.append(
                        list(map(float, self.message_dict[child_id].message.embedding))
                    )

        relationship_df = pd.DataFrame(
            {
                "prompt_id": prompt_ids,
                "response_id": response_ids,
                "prompt": prompts,
                "response": responses,
                "prompt_embedding": prompt_encodings,
                "response_embedding": response_encodings,
                "created_time": created_times,
                "prompt_coordinate": prompt_coordinates,
            }
        )

        return relationship_df

    def create_chain_representation(
        self,
        message_id_1: str,
        operation: str = None,
        message_id_2: str = None,
        n: int = None,
        return_message_info: bool = False,
        return_df: bool = False,
        return_dict: bool = False,
    ) -> Any:
        # Define the operation dictionary mapping operation strings to functions
        operation_dict = {
            "bifurcation_points": self.get_bifurcation_points,
            "merge_points": self.get_merge_points,
            "cross_references": self.get_commonly_co_referenced_messages,
            "commonly_co_referenced": self.get_co_reference_chain_between_messages,
            "relationships_between": self.get_all_relationships_between_messages,
        }

        # Validate the operation
        if operation not in operation_dict:
            raise ValueError(
                f"Invalid operation. Valid operations are: {list(operation_dict.keys())}"
            )

        # Validate the message IDs
        if message_id_1 not in self.message_dict:
            raise ValueError("Invalid message_id_1")

        if message_id_2 is not None and message_id_2 not in self.message_dict:
            raise ValueError("Invalid message_id_2")

        # Validate the number of hops
        if n is not None and not isinstance(n, int):
            raise ValueError("n must be an int")

        # Validate the return type
        if not isinstance(return_message_info, bool):
            raise ValueError("return_message_info must be a boolean")

        if not isinstance(return_df, bool):
            raise ValueError("return_df must be a boolean")

        if not isinstance(return_dict, bool):
            raise ValueError("return_dict must be a boolean")

        # Perform the operation
        if operation == "relationships_between":
            result = operation_dict[operation](
                message_id_1, message_id_2, return_message_info=return_message_info
            )

        elif operation == "commonly_co_referenced":
            result = operation_dict[operation](
                message_id_1, message_id_2, n, return_message_info=return_message_info
            )

        else:
            result = operation_dict[operation](
                message_id_1, n, return_message_info=return_message_info
            )

        # Format the result
        if return_message_info:
            result = [self.message_dict[message_id] for message_id in result]

        if return_df:
            result = pd.DataFrame(result)

        if return_dict:
            result = {
                message_id: self.message_dict[message_id] for message_id in result
            }

        return result

    def _fallback_method(self, message_id: str) -> List[str]:
        """A simple fallback method that returns all neighboring messages in case the main operation fails"""
        return self.conversation_dict[message_id][1]

    def _find_path_or_chain(
        self, message_id_1: str, message_id_2: str
    ) -> Optional[List[str]]:
        """Finds a path within a certain hop range or a connecting chain between two messages."""
        paths_within_hop_range = self._get_paths_within_hop_range(
            message_id_1, message_id_2, 2
        )
        if paths_within_hop_range:
            return paths_within_hop_range[0]  # Use the first path within the hop range
        else:
            return self._find_connecting_chain(message_id_1, message_id_2)

    def _find_connecting_chain(self, message_id_1: str, message_id_2: str) -> List[str]:
        """
        Returns a chain of messages that connect the two given messages.

        Args:
            message_id_1: The ID of the first message.
            message_id_2: The ID of the second message.

        Returns:
            A list of message IDs forming the connecting chain.
        """
        if (
            message_id_1 not in self.message_dict
            or message_id_2 not in self.message_dict
        ):
            raise ValueError("Both message IDs must exist in the conversation")

        # Get the set of messages reachable from message_id_1 and the set of messages that can reach message_id_2
        reachable_from_1 = set(nx.descendants(self._get_message_tree(), message_id_1))
        can_reach_2 = set(nx.ancestors(self._get_message_tree(), message_id_2))

        # Find the intersection of the two sets
        common_messages = reachable_from_1 & can_reach_2

        # If no common message is found, there is no connecting chain
        if not common_messages:
            return []

        # Select a message from the common messages that minimizes the total distance of the chain
        connecting_message = min(
            common_messages,
            key=lambda node: nx.shortest_path_length(
                self._get_message_tree(), message_id_1, node
            )
            + nx.shortest_path_length(self._get_message_tree(), node, message_id_2),
        )

        # Get the paths from message_id_1 to the connecting message and from the connecting message to message_id_2
        path_to_connecting = nx.shortest_path(
            self._get_message_tree(), message_id_1, connecting_message
        )
        path_from_connecting = nx.shortest_path(
            self._get_message_tree(), connecting_message, message_id_2
        )

        # Return the concatenation of the two paths, excluding the connecting message in one of them to avoid duplication
        return path_to_connecting + path_from_connecting[1:]

    def _get_paths_within_hop_range(
        self,
        message_id_1: str,
        message_id_2: str,
        hop_range: Union[int, Tuple[int, int]],
        return_message_info: bool = False,
    ) -> Union[List[List[Union[str, Dict[str, Any]]]], None]:
        """
        Returns a list of all paths between two messages within a range of
        number of steps, or None if no path exists within the given range.

        If return_message_info is True, returns information about the messages
        in the path instead of just the IDs.
        """

        # Validation
        if not isinstance(hop_range, (int, tuple)) or (
            isinstance(hop_range, tuple)
            and not len(hop_range) == 2
            and isinstance(hop_range[0], int)
            and isinstance(hop_range[1], int)
        ):
            raise ValueError("hop_range must be an int or a tuple of two ints.")

        if (
            message_id_1 not in self.message_dict
            or message_id_2 not in self.message_dict
        ):
            raise ValueError(
                "Both message_id_1 and message_id_2 must be valid message IDs."
            )

        if isinstance(hop_range, int):
            hop_range = (hop_range, hop_range)

        # Optimization: use a dictionary to store n-hop neighbors
        neighbor_cache_1 = {}
        neighbor_cache_2 = {}

        paths = []
        for hops in range(hop_range[0], hop_range[1] + 1):
            # Compute and cache n-hop neighbors if they haven't been computed yet
            if hops not in neighbor_cache_1:
                neighbor_cache_1[hops] = self._get_n_hop_neighbors(message_id_1, hops)
            if hops not in neighbor_cache_2:
                neighbor_cache_2[hops] = self._get_n_hop_neighbors(message_id_2, hops)

            # Find the intersection of the two sets of neighbors
            common_neighbors = list(
                set(neighbor_cache_1[hops]) & set(neighbor_cache_2[hops])
            )

            # For each common neighbor, get all paths from message_id_1 to the neighbor
            # and all paths from the neighbor to message_id_2, then combine them to
            # create a path from message_id_1 to message_id_2
            for neighbor in common_neighbors:
                paths_1 = nx.all_simple_paths(
                    self._get_message_tree(), message_id_1, neighbor, cutoff=hops
                )
                paths_2 = nx.all_simple_paths(
                    self._get_message_tree(), neighbor, message_id_2, cutoff=hops
                )
                for path_1 in paths_1:
                    for path_2 in paths_2:
                        path = path_1 + path_2[1:]  # Combine the two paths
                        if return_message_info:
                            path = [self.message_dict[msg_id] for msg_id in path]
                        paths.append(path)

        return paths if paths else None

    def _get_n_hop_neighbors(
        self, message_id: str, n: int
    ) -> Union[List[Dict[str, Any]], None]:
        """Returns a list of all n-hop neighbors of the message with the given ID, or None if the message doesn't exist"""
        if message_id not in self.message_dict:
            return None
        return nx.single_source_shortest_path_length(
            self._get_message_tree(), message_id, cutoff=n
        )

    def _get_n_hop_neighbors_ids(
        self, message_id: str, n: int
    ) -> Union[List[str], None]:
        """Returns a list of all n-hop neighbors of the message with the given ID, or None if the message doesn't exist"""
        neighbors = self._get_n_hop_neighbors(message_id, n)
        if neighbors is None:
            return None
        return [neighbor for neighbor in neighbors]

    def _get_paths_between_messages(
        self, message_id_1: str, message_id_2: str, all_paths: bool = False
    ) -> Union[List[str], List[List[str]], None]:
        """
        Returns the shortest path or all shortest paths between the two given messages.

        Args:
            message_id_1: The ID of the first message.
            message_id_2: The ID of the second message.
            all_paths: If True, returns all shortest paths. Otherwise, returns a single shortest path.

        Returns:
            A path or list of paths between the two messages.
        """
        try:
            if all_paths:
                return list(
                    nx.all_shortest_paths(
                        self._get_message_tree(),
                        message_id_1,
                        message_id_2,
                        weight="weight",
                    )
                )
            else:
                return nx.shortest_path(
                    self._get_message_tree(),
                    message_id_1,
                    message_id_2,
                    weight="weight",
                )
        except nx.NetworkXNoPath:
            return []

    def get_bifurcation_points(
        self, message_id_1: str, message_id_2: str
    ) -> Optional[List[str]]:
        """Return a path or chain of bifurcation points between two messages, or None if no such chain exists."""
        path_or_chain = self._find_path_or_chain(message_id_1, message_id_2)
        if path_or_chain is None:
            return None
        return [
            node for node in path_or_chain if len(self.conversation_dict[node][1]) > 1
        ]

    def get_co_reference_chain_between_messages(
        self, message_id_1: str, message_id_2: str, n: int
    ) -> Optional[List[str]]:
        """Return a path or chain of commonly co-referenced messages between two messages, or None if no such chain exists."""
        path_or_chain = self._find_path_or_chain(message_id_1, message_id_2)
        if path_or_chain is None:
            return None
        commonly_co_referenced = self.get_commonly_co_referenced_messages(
            message_id_1, n
        )
        return [node for node in path_or_chain if node in commonly_co_referenced]

    def get_cross_references(
        self, message_id_1: str, message_id_2: str
    ) -> Optional[List[str]]:
        """Return a path or chain, including cross-references, between two messages, or None if no such path or chain exists."""
        return self._find_path_or_chain(message_id_1, message_id_2)

    def get_merge_points(self, message_id: str, n: int) -> List[str]:
        """Return list of message ids within n hops of message_id that have more than one parent."""
        neighbors = self._get_n_hop_neighbors(message_id, n)
        child_parent_dict = {}
        for parent, (_, children) in self.conversation_dict.items():
            for child in children:
                if child in child_parent_dict:
                    child_parent_dict[child].append(parent)
                else:
                    child_parent_dict[child] = [parent]
        return [node for node in neighbors if len(child_parent_dict.get(node, [])) > 1]

    def get_all_relationships_between_messages(
        self, message_id_1: str, message_id_2: str, return_message_info: bool = True
    ) -> List[List[Union[str, Dict[str, Any]]]]:
        """Return all paths, including cross-references, between two messages."""

        # Check if the message_id's are valid
        if (
            message_id_1 not in self.message_dict
            or message_id_2 not in self.message_dict
        ):
            raise ValueError("Invalid message_id(s)")

        paths = self._get_paths_between_messages(
            message_id_1, message_id_2, all_paths=True
        )
        if paths is None:
            return None

        if return_message_info:
            return [[self.message_dict[msg_id] for msg_id in path] for path in paths]
        else:
            return paths

    def get_commonly_co_referenced_messages(
        self, message_id: str, n: int
    ) -> Dict[Tuple[str, str], int]:
        """Return pairs of messages within n hops of message_id that are commonly referenced together and how often they co-occur."""

        # Check if the message_id is valid
        if message_id not in self.message_dict:
            raise ValueError("Invalid message_id")

        neighbors = self._get_n_hop_neighbors_ids(message_id, n)
        if neighbors is None:
            return None

        # Get all pairs of messages within n hops of message_id
        pairs = list(itertools.combinations(neighbors, 2))

        # Get all pairs of messages that are commonly referenced together
        commonly_co_referenced = collections.Counter(
            [
                tuple(sorted(pair))
                for pair in pairs
                if self._are_commonly_co_referenced(pair[0], pair[1])
            ]
        )

        return commonly_co_referenced

    def _are_commonly_co_referenced(self, message_id_1: str, message_id_2: str) -> bool:
        # Check if the message_id's are valid
        if (
            message_id_1 not in self.message_dict
            or message_id_2 not in self.message_dict
        ):
            raise ValueError("Invalid message_id(s)")

        # Get the set of messages that reference message_id_1 and the set of messages that reference message_id_2
        references_1 = set(self._get_referencing_messages(message_id_1))
        references_2 = set(self._get_referencing_messages(message_id_2))

        # Find the intersection of the two sets
        common_references = references_1 & references_2

        # If no common message is found, the messages are not commonly co-referenced
        if not common_references:
            return False

        # Select a message from the common messages that minimizes the total distance of the chain
        common_reference = min(
            common_references,
            key=lambda node: nx.shortest_path_length(
                self._get_message_tree(), node, message_id_1
            )
            + nx.shortest_path_length(self._get_message_tree(), node, message_id_2),
        )

        # Get the paths from message_id_1 to the common reference and from the common reference to message_id_2
        path_to_common_reference = nx.shortest_path(
            self._get_message_tree(), message_id_1, common_reference
        )
        path_from_common_reference = nx.shortest_path(
            self._get_message_tree(), common_reference, message_id_2
        )

        # Return True if the paths are disjoint, False otherwise
        return not set(path_to_common_reference) & set(path_from_common_reference)

    def _get_referencing_messages(self, message_id: str) -> List[str]:
        """Returns a list of all messages that reference the message with the given ID, or None if the message doesn't exist"""
        if message_id not in self.message_dict:
            return None
        return [node for node in self._get_message_tree().predecessors(message_id)]
