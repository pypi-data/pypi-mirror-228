from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import networkx as nx
from dlm_matrix.models import ChainTreeIndex, Message, Content, Coordinate
from dlm_matrix.type import NodeRelationship
import numpy as np
import logging
from dlm_matrix.representation.layout import MessageLayout


class Representation(MessageLayout):
    RELATIONSHIP_WEIGHTS = {
        "siblings": 1,
        "cousins": 2,
        "uncles_aunts": 3,
        "nephews_nieces": 3,
        "grandparents": 4,
        "ancestors": 5,
        "descendants": 5,
        NodeRelationship.PARENT: 1,
        NodeRelationship.CHILD: 1,
        NodeRelationship.PREVIOUS: 1,
        NodeRelationship.NEXT: 1,
        NodeRelationship.SOURCE: 1,
    }

    def __init__(
        self,
        conversation_tree: ChainTreeIndex,
        message_dict: Dict[str, Message] = None,
        tetra_dict: Dict[str, Tuple[float, float, float, float]] = None,
        root_component_values: Dict[str, Any] = None,
    ):
        self.conversation = conversation_tree
        self.mapping = conversation_tree.conversation.mapping
        self.message_dict = message_dict
        self.tetra_dict = tetra_dict
        self.conversation_dict = self._conversation_representation()
        self.relationships = {}
        self.default_root_component_values = {
            "depth_args": [0],
            "sibling_args": [0],
            "sibling_count_args": [0],
            "time_args": [0],
        }

        # If root component values are provided, update the default ones
        if root_component_values:
            self.default_root_component_values.update(root_component_values)

        # Construct root coordinate with updated component values
        self.root_coordinate = Coordinate.create(**self.default_root_component_values)

    def _create_graph(self) -> nx.Graph:
        """
        Creates a networkx Graph representation of the conversation tree.
        """
        G = nx.Graph()
        for node in self.mapping.values():
            G.add_node(node.id, message=node.message)
            if node.parent:
                G.add_edge(node.parent, node.id)

        return G

    def _create_representation(self, include_system: bool = False) -> nx.DiGraph:
        """
        Creates a NetworkX directed graph representation of the conversation tree.
        Each node in the graph is a message, and each edge indicates a response
        relationship between messages. Nodes are annotated with message content
        and authors, and edges are annotated with the response time between
        messages.

        Args:
            include_system (bool): Whether to include system messages in the graph.

        Returns:
            A NetworkX directed graph representation of the conversation tree.
        """
        graph = nx.DiGraph()
        prev_node = None

        for mapping_id, mapping in self.mapping.items():
            if mapping.message is None:
                if self.root_message_id == mapping_id:
                    print(f"Root message {mapping_id}. Skipping...")
                continue  # Skip this iteration if the message is None

            # Skip system messages if include_system is False
            if not include_system and mapping.message.author.role == "system":
                continue

            # Add the node to the graph
            graph.add_node(mapping_id, **mapping.message.dict())

            # If this isn't the first node, create an edge from the previous node
            if prev_node is not None:
                graph.add_edge(prev_node, mapping_id)

            # If the mapping has a parent, create an edge from the parent
            if mapping.parent is not None:
                graph.add_edge(mapping.parent, mapping_id)

            # Add edges to all references
            for ref_id in mapping.references:
                if ref_id in self.mapping:
                    graph.add_edge(mapping_id, ref_id)

            # Update the previous node
            prev_node = mapping_id

        return graph

    def create_representation(
        self,
        node_ids: Optional[List[str]] = None,
        attribute_filter: Optional[Dict[str, Any]] = None,
        include_system: bool = True,  # New parameter
        time_range: Optional[Dict[str, Union[str, int]]] = None,  # New parameter
    ) -> nx.DiGraph:
        """
        Creates a NetworkX directed graph representation of the conversation tree.
        Each node in the graph is a message, and each edge indicates a response
        relationship between messages. Nodes are annotated with message content
        and authors, and edges are annotated with the response time between
        messages.

        Args:
            node_ids: A list of node IDs to include in the graph.
            attribute_filter: A dictionary of attributes to filter nodes by.
            include_system: Whether to include system messages.
            time_range: A dictionary containing the start and end time for filtering nodes.

        Returns:
            A NetworkX directed graph representation of the conversation tree.
        """

        # Get the full graph representation, consider the include_system flag
        graph = self._create_representation(include_system)

        # If node_ids are provided, use them to create the subgraph
        if node_ids is not None:
            subgraph = graph.subgraph(node_ids)

        # If attribute_filter is provided, select nodes based on attributes
        elif attribute_filter is not None:
            selected_nodes = [
                node
                for node, data in graph.nodes(data=True)
                if all(item in data.items() for item in attribute_filter.items())
            ]
            subgraph = graph.subgraph(selected_nodes)

        # Additional filtering based on time_range
        elif time_range is not None:
            start_time, end_time = time_range.get("start", None), time_range.get(
                "end", None
            )
            selected_nodes = [
                node
                for node, data in graph.nodes(data=True)
                if (
                    start_time is None
                    or data["message"].get("create_time") >= start_time
                )
                and (end_time is None or data["message"].get("create_time") <= end_time)
            ]
            subgraph = graph.subgraph(selected_nodes)

        # If no filters are provided, return the full graph
        else:
            subgraph = graph

        return subgraph

    def initialize_representation(
        self,
        use_graph: bool = False,
        node_ids: Optional[List[str]] = None,
        attribute_filter: Optional[Dict[str, Any]] = None,
        include_system: bool = False,  # New parameter
        time_range: Optional[Dict[str, Union[str, int]]] = None,  # New parameter
        RELATIONSHIP_TYPE=NodeRelationship,
    ) -> Tuple[Dict, Callable, Dict, str, Any]:
        """
        This method initializes the graph for the conversation. It either creates the conversation graph or uses the provided graph.

        :param use_graph: A boolean indicating whether to create a new conversation graph or use the existing one.
        :param node_ids: A list of node IDs to include in the graph.
        :param attribute_filter: A dictionary of attributes to filter nodes by.
        :param include_system: Whether to include system messages in the graph.
        :param time_range: A dictionary containing the start and end time for filtering nodes.
        :return: The root ID of the graph as a string, and a function to get the children IDs for a given node.
        """
        relationships = {}

        if use_graph:
            # Create the conversation graph
            G = self.create_representation(
                node_ids=node_ids,
                attribute_filter=attribute_filter,
                include_system=include_system,  # Added parameter
                time_range=time_range,  # Added parameter
            )

            if G.number_of_nodes() == 0:
                return {}, None, {}, "", None  # Updated to match the tuple length

            # Get the root node
            root_id = list(nx.topological_sort(G))[0]

            # Get the children IDs for a given node
            get_children_ids = lambda node_id: list(G.successors(node_id))

            # Get the tetra dict
            relationships[root_id] = {RELATIONSHIP_TYPE.SOURCE: root_id}

        else:
            if len(self.conversation_dict) == 0:
                return {}, None, {}, "", None  # Updated to match the tuple length

            root_id = list(self.conversation_dict)[0]
            get_children_ids = self.get_children_ids
            relationships[root_id] = {RELATIONSHIP_TYPE.SOURCE: root_id}

        tetra_dict = {}
        tetra_dict[root_id] = self.root_coordinate.flatten(self.root_coordinate)

        return (
            relationships,
            get_children_ids,
            tetra_dict,
            root_id,
            self.root_coordinate,
        )

    def get_message_attribute(self, message_id: str, *attributes: str):
        """
        Get a specific attribute of a message given its id.

        Args:
            message_id: The id of the message.
            attributes: The sequence of attributes to fetch (e.g., "content", "text").

        Returns:
            The desired attribute of the message.
        """
        try:
            value = self.message_dict[message_id].message
            for attribute in attributes:
                if hasattr(value, attribute):
                    value = getattr(value, attribute)
                else:
                    raise AttributeError(f"Attribute {attribute} not found in message.")
            return value
        except KeyError:
            raise ValueError(f"Message with id {message_id} not found.")

    def _assign_relationships(
        self,
        message_id: str,
        child_id: str,
        children_ids: List[str],
        i: int,
        relationships: Dict[str, Dict[str, str]],
        RELATIONSHIP_TYPE=NodeRelationship,
    ) -> Dict[str, Dict[str, str]]:
        """
        Assign relationships for a given child message ID.

        Args:
            message_id: The ID of the parent message.
            child_id: The ID of the child message.
            children_ids: A list of IDs for all children of the parent message.
            i: The index of the child in the children_ids list.
            relationships: A dictionary holding the relationships of all messages.
            RELATIONSHIP_TYPE: An enumeration defining the types of node relationships.

        Returns:
            The updated relationships dictionary.
        """

        # Define relationships for the child message
        child_relationships = {
            RELATIONSHIP_TYPE.PARENT: message_id,
            RELATIONSHIP_TYPE.CHILD: [],
            RELATIONSHIP_TYPE.PREVIOUS: children_ids[i - 1] if i > 0 else None,
            RELATIONSHIP_TYPE.NEXT: children_ids[i + 1]
            if (i >= 0 and i < len(children_ids) - 1)
            else None,
        }

        # Get extended relationships, if any
        extended_relationships = self.get_relationship_ids(child_id)

        # Merge the two dictionaries
        relationships[child_id] = {**child_relationships, **extended_relationships}

        return relationships

    def _get_message_attributes(self, child_id: str) -> Tuple[Any, Any, Any]:
        """
        Retrieve attributes of a message by its ID.

        Args:
            child_id: The ID of the child message.

        Returns:
            A tuple containing the create_time, author, and text of the message.
        """
        create_time = self.get_message_attribute(child_id, "create_time")
        author = self.get_message_attribute(child_id, "author")
        text = self.get_message_attribute(child_id, "content", "text")
        return create_time, author, text

    def _calculate_part_weight(self, n_parts: int) -> float:
        """
        Calculate the weight of each part in a multi-part message.

        Args:
            n_parts: The number of parts in the message.

        Returns:
            The weight of each part as a float.
        """
        return round(1.0 / n_parts, 2) if n_parts > 0 else 0

    def _get_mapping(self, child_id: str) -> Any:
        """
        Retrieve the mapping object for a message by its ID.

        Args:
            child_id: The ID of the child message.

        Returns:
            The mapping object associated with the child message.

        Raises:
            ValueError: If the message is not found in the message dictionary.
        """
        mapping = self.message_dict.get(child_id)
        if not mapping:
            raise ValueError(f"Message {child_id} not found in message_dict")
        return mapping

    def split_content_into_parts(self, content, n_parts):
        """
        Split the content of a message into parts.

        Args:
            content: The content of the message.
            n_parts: The number of parts to split the content into.

        Returns:
            A list of content parts.
        """
        # Split the content of the message into parts
        content_parts = content.split("\n\n")
        if len(content_parts) < n_parts:
            content_parts = content.split("\n")
        return content_parts

    def _assign_coordinates(
        self,
        child_id: str,
        i: int,
        children_ids: List[str],
        depth: int,
        **kwargs: Dict[str, Union[str, float]],
    ) -> None:
        """
        Assigns coordinates to a given child node in the mapping tree.

        Args:
            child_id: The ID of the child node.
            i: Index of the message.
            children_ids: List of children IDs.
            depth: Depth level of the message in the tree.
            kwargs: Additional keyword arguments as a dictionary, including:
                - scaling: A string indicating the type of scaling to use.
                - alpha_scale: A float value for scaling in the 'linear_combination' type.
                - method: Method for calculating z-coordinate.
                - alpha_final_z: Weighting factor for calculating final z-coordinate.

        Returns:
            None. The function assigns coordinates internally within the object.
        """

        mapping = self._get_mapping(child_id)

        x_coord, y_coord, z_coord, t_coord, n_parts = self._calculate_coordinates(
            i, children_ids, depth, mapping, **kwargs
        )

        part_weight = self._calculate_part_weight(n_parts)
        create_time, author, text = self._get_message_attributes(child_id)
        content_parts = self.split_content_into_parts(text, n_parts)

        # Create child messages for each part
        child_messages = []
        prev_child_id = None
        for index, part in enumerate(content_parts):
            new_child_id = (
                f"{child_id}_{index}"  # Create a unique ID for the child message
            )
            children_coordinate = Coordinate(
                id=new_child_id,
                x=x_coord,
                y=y_coord,
                z=z_coord,
                t=t_coord,
                n_parts=index,
            )
            child_message = self.create_child_message(
                new_child_id,
                part,
                create_time,
                author,
                part_weight,
                children_coordinate,
            )

            # Add relationship to the previous child message
            if prev_child_id:
                self.add_relationship(
                    prev_child_id, new_child_id, NodeRelationship.NEXT
                )
                self.add_relationship(
                    new_child_id, prev_child_id, NodeRelationship.PREVIOUS
                )

            # Add relationship to the parent message
            self.add_relationship(child_id, new_child_id, NodeRelationship.PARENT)
            self.add_relationship(new_child_id, child_id, NodeRelationship.CHILD)

            child_messages.append(child_message)
            prev_child_id = new_child_id

        # Update the original message, if necessary
        mapping.message.children = child_messages

        child_coordinate = Coordinate(
            id=child_id,
            x=x_coord,
            y=y_coord,
            z=z_coord,
            t=t_coord,
            n_parts=n_parts,
        )

        mapping.message.coordinate = child_coordinate

        flattened_coordinate = child_coordinate.flatten(child_coordinate)

        return flattened_coordinate

    def create_child_message(
        self,
        message_id: str,
        content_part: str,
        create_time: float,
        author: str,
        weight,
        coordinate: Coordinate,
    ):
        # Create a new message object for the content part
        child_message = Message(
            id=message_id,
            author=author,
            create_time=create_time,
            content=Content(parts=[content_part]),
            weight=weight,
            coordinate=coordinate,
        )
        return child_message

    def add_relationship(
        self, from_id: str, to_id: str, relationship: NodeRelationship
    ):
        """
        Add a relationship between two message IDs.
        """
        if from_id not in self.relationships:
            self.relationships[from_id] = {}

        self.relationships[from_id][to_id] = relationship

    def calculate_t_coordinate(self, message, children_ids) -> float:
        """
        Calculate the t-coordinate of a message based on the chosen metric.

        Args:
            message: The message for which to calculate the t-coordinate.
            children_ids: The IDs of the message's children.

        Returns:
            The calculated t-coordinate as a float.
        """
        # Calculate sibling time differences
        sibling_time_differences = [
            self.message_dict[child_id].message.create_time
            - message.message.create_time
            for child_id in children_ids
        ]

        return np.mean(sibling_time_differences)
