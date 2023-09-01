import numpy as np
from dlm_matrix.relationship import Relationship
from datetime import datetime
from typing import List, Tuple, Union, Dict
from dlm_matrix.models import ChainMap
from dlm_matrix.type import ScalingType, MethodType
import logging
from sklearn.metrics.pairwise import cosine_similarity


class MessageLayout(Relationship):
    def __init__(self) -> None:
        """Initializer for the MessageLayout class."""
        self.temporal_scale = 1.0  # Adjust this scale factor as needed

    def calculate_xy_coordinates(
        self,
        i: int,
        depth: int,
        z_coord: float,
        scaling: ScalingType,
        alpha_scale: float,
    ) -> Tuple[float, float]:
        """
        Calculate the x and y coordinates based on the given scaling method and parameters.

        Args:
            i: Index of the message.
            depth: Depth level of the message in the tree.
            z_coord: Calculated z-coordinate for the message.
            scaling: The type of scaling to use, as defined in ScalingType.
            alpha_scale: A float value for scaling in the 'linear_combination' type. Must be between 0 and 1.

        Returns:
            Tuple containing the x and y coordinates.
        """

        if not (0 <= alpha_scale <= 1):
            logging.error("alpha_scale must be between 0 and 1.")
            return 0.0, 0.0

        if depth < 0:
            logging.error("Depth cannot be negative.")
            return 0.0, 0.0

        try:
            # Pre-computed values for efficiency
            scaled_depth = alpha_scale * depth
            scaled_index = alpha_scale * (i + 1)
            scaled_z_coord = (1 - alpha_scale) * z_coord

            # Using a dictionary to map scaling types to calculations
            methods = {
                ScalingType.LINEAR_COMBINATION: (
                    scaled_depth + scaled_z_coord,
                    scaled_index + scaled_z_coord,
                ),
                ScalingType.DIRECT: (depth + z_coord, i + 1 + z_coord),
            }

            return methods.get(scaling, (0.0, 0.0))

        except Exception as e:
            logging.error(
                f"Error occurred while calculating x and y coordinates: {str(e)}"
            )
            return 0.0, 0.0

    def calculate_sibling_spacing(
        self,
        children_ids: List[str],
        temporal_weights: np.array,
        method: str = MethodType.BOTH,
        alpha_final_z: float = 0.5,
        alpha_similarity: float = 0.2,
    ) -> float:
        """
        Calculate the spacing between siblings based on similarity scores, temporal weights, and spacing.

        Args:
            children_ids: List of children IDs.
            temporal_weights: Numpy array of temporal weights.
            method: String indicating which method to use for calculation. Can be "weighted", "spacing", or "both". Defaults to "both".
            alpha_final_z: Weighting factor for combining weighted_z_coord and sibling_spacing. Defaults to 0.5.
            alpha_similarity: Weighting factor for adding the influence of similarity scores. Defaults to 0.2.

        Returns:
            The final z-coordinate as a float.
        """

        if len(children_ids) == 1:
            return 0

        similarity_scores = self._gather_similarity_scores(children_ids)
        normalized_scores = self.normalize_scores(similarity_scores)

        weighted_z_coord = self.calculate_final_z_coord(
            normalized_scores, temporal_weights, children_ids, alpha_final_z, method
        )

        # Now you can include the similarity score's influence on spacing
        mean_similarity = np.mean(similarity_scores) if similarity_scores else 0
        weighted_z_coord += alpha_similarity * mean_similarity

        return weighted_z_coord

    def _calculate_coordinates(
        self,
        i: int,
        children_ids: List[str],
        depth: int,
        mapping: object,
        scaling: str = ScalingType.DIRECT,
        alpha_scale: float = 1,
        method: str = MethodType.BOTH,
        alpha_final_z: float = 0.7,
    ) -> Tuple[float, float, float, float, int]:
        """
        Calculate the 3D coordinates for a message based on its relationships.

        Args:
            i: Index of the message.
            children_ids: List of children IDs.
            depth: Depth level of the message in the tree.
            mapping: A mapping object representing the relationship of messages.
            scaling: A string indicating the type of scaling to use ("linear_combination", "normalized", "direct").
            alpha_scale: A float value for scaling in the 'linear_combination' type.
            method: Method for calculating z-coordinate ("weighted", "spacing", or "both").
            alpha_final_z: Weighting factor for calculating final z-coordinate.

        Returns:
            Tuple containing the x, y, and z coordinates, t_coord, and n_parts.
        """

        # Validate parameters
        if depth < 0 or not (0 <= alpha_scale <= 1) or not (0 <= alpha_final_z <= 1):
            logging.error("Invalid parameters.")
            return 0.0, 0.0, 0.0, 0.0, 0

        try:
            # Pre-calculate common variables
            temporal_weights = self.calculate_temporal_weights(self.message_dict)

            # Z-coordinate
            z_coord = self.calculate_sibling_spacing(
                children_ids, temporal_weights, method, alpha_final_z
            )

            # Time coordinate and number of parts
            t_coord = self.calculate_time_coordinate(mapping, children_ids)
            n_parts = len(mapping.message.content.text.split("\n\n"))

            # Coordinate calculation methods
            methods = {
                MethodType.SPACING: (depth, i + 1),
                MethodType.WEIGHTED: self.calculate_xy_coordinates(
                    i, depth, z_coord, scaling, alpha_scale
                ),
                MethodType.BOTH: self.calculate_xy_coordinates(
                    i, depth, z_coord, scaling, alpha_scale
                ),
            }

            x_coord, y_coord = methods.get(method, (0.0, 0.0))

            return x_coord, y_coord, z_coord, t_coord, n_parts

        except Exception as e:
            logging.error(f"Error occurred while calculating coordinates: {str(e)}")
            return 0.0, 0.0, 0.0, 0.0, 0

    def calculate_final_z_coord(
        self,
        normalized_scores: List[float],
        temporal_weights: np.array,
        children_ids: List[str],
        alpha_final_z: float = 0.7,
        method: str = MethodType.BOTH,
    ) -> float:
        """
        Calculate the final z-coordinate incorporating both weights and sibling spacing.

        Args:
            normalized_scores: List of normalized similarity scores.
            temporal_weights: Numpy array of temporal weights.
            children_ids: List of children IDs.
            alpha_final_z: Weighting factor for combining weighted_z_coord and sibling_spacing. Defaults to 0.7.
            method: String indicating which method to use for calculation. Can be "weighted", "spacing", or "both". Defaults to "both".

        Returns:
            The final z-coordinate as a float.
        """

        # Early exit for invalid method
        if method not in MethodType:
            raise ValueError(f"Invalid method type. Choose from {list(MethodType)}.")

        # Validate alpha_final_z
        if not (0 <= alpha_final_z <= 1):
            raise ValueError("alpha_final_z must be between 0 and 1.")

        weighted_z_coord = sibling_spacing = 0.0

        # Calculate based on method types
        if method in [MethodType.WEIGHTED, MethodType.BOTH]:
            weighted_z_coord = self.calculate_weighted_z_coord(
                normalized_scores, temporal_weights
            )

        if method in [MethodType.SPACING, MethodType.BOTH]:
            sibling_spacing = self.calculate_spacing(
                children_ids, normalized_scores, method
            )

        # Final calculation
        final_z_coord = (
            (alpha_final_z * weighted_z_coord + (1 - alpha_final_z) * sibling_spacing)
            if method == MethodType.BOTH
            else weighted_z_coord
            if method == MethodType.WEIGHTED
            else sibling_spacing
        )

        return final_z_coord

    def calculate_spacing(
        self, children_ids: List[str], normalized_scores, method: str
    ) -> float:
        """
        Calculate the spacing between siblings based on similarity.

        Args:
            children_ids: The IDs of the message's children.
            normalized_scores: Normalized similarity scores.
            method: The method used for calculating spacing ("both" or "spacing").

        Returns:
            The calculated spacing as a float.
        """

        if len(children_ids) <= 1:
            return 0

        if method == MethodType.BOTH:
            # Calculate the average normalized similarity score among siblings
            avg_similarity = np.mean(normalized_scores) if normalized_scores else 0

            # Calculate the spacing factor based on similarity
            spacing_factor = -0.5 + avg_similarity * 0.5
            spacing = spacing_factor * (len(children_ids) - 1)
        else:
            # Use the original formula without considering similarity
            spacing = 0 if len(children_ids) == 1 else -0.5 * (len(children_ids) - 1)

        return spacing

    def _gather_similarity_scores(self, children_ids: List[str]) -> List[float]:
        """
        Gather similarity scores for a list of children messages.

        Args:
            children_ids (List[str]): A list of IDs for children messages.

        Returns:
            List[float]: A list of similarity scores.
        """

        # Pre-calculate previous and next sibling IDs for all children
        prev_sibling_ids = [
            self._get_previous_sibling_id(child_id) for child_id in children_ids
        ]
        next_sibling_ids = [
            self._get_next_sibling_id(child_id) for child_id in children_ids
        ]

        # Gather similarity scores where both prev and next siblings exist
        similarity_scores = [
            self.calculate_similarity_score(prev_id, next_id)
            for prev_id, next_id in zip(prev_sibling_ids[:-1], next_sibling_ids[1:])
            if prev_id and next_id
        ]

        return similarity_scores

    def calculate_similarity_score(self, child_id: str, next_child_id: str) -> float:
        """
        Calculate the cosine similarity score between two child messages.

        Args:
            child_id (str): The ID of the first child message.
            next_child_id (str): The ID of the second child message.

        Returns:
            float: The cosine similarity score between the two messages.
        """
        try:
            child_embedding = np.array(
                self.message_dict[child_id].message.embedding
            ).reshape(1, -1)
            next_child_embedding = np.array(
                self.message_dict[next_child_id].message.embedding
            ).reshape(1, -1)

            similarity_score = cosine_similarity(child_embedding, next_child_embedding)

            return similarity_score[0][0]  # Unpack the result from the 2D array
        except Exception as e:
            print(f"An error occurred while calculating the similarity score: {e}")
            return 0.0  # Return a default similarity score

    def normalize_scores(self, scores: List[float]) -> List[float]:
        """
        Normalize a list of scores to the range [0, 1].

        Args:
            scores (List[float]): A list of scores to normalize.

        Returns:
            List[float]: A list of normalized scores.
        """
        scores = np.array(scores)

        # Handle empty scores
        if scores.size == 0:
            return []

        # Calculate min and max scores
        min_score, max_score = np.min(scores), np.max(scores)

        # Check for division by zero
        if max_score == min_score:
            return [1.0] * len(scores)  # All scores are the same, normalize to 1

        # Perform normalization
        normalized_scores = (scores - min_score) / (max_score - min_score)

        return list(normalized_scores)

    def calculate_weighted_z_coord(
        self, normalized_scores: List[float], temporal_weights: np.array
    ) -> float:
        """Calculate a weighted z-coordinate based on normalized scores and temporal weights."""
        weighted_z_coord = 0
        for i, score in enumerate(normalized_scores):
            weighted_z_coord += score * temporal_weights[i]
        return weighted_z_coord

    def calculate_temporal_weights(self, message_dict: Dict[str, object]) -> np.ndarray:
        """
        Calculate the temporal weights for a given message dictionary.

        Args:
            message_dict (Dict[str, object]): The message dictionary.

        Returns:
            np.ndarray: A NumPy array of temporal weights.
        """
        valid_messages = [
            message.message.create_time
            for message in message_dict.values()
            if message.message and message.message.create_time is not None
        ]

        # Create NumPy arrays from valid create_times
        create_times = np.array(valid_messages)

        # Calculate the pairwise time differences using broadcasting
        delta_times = np.abs(create_times[:, np.newaxis] - create_times)

        # Apply the decay function element-wise
        temporal_weights = np.vectorize(self.time_diff_decay_function)(
            delta_times, "exponential"
        )

        # Remove diagonal elements (i.e., where i = j) to replicate the original function behavior
        temporal_weights = temporal_weights[
            np.where(~np.eye(temporal_weights.shape[0], dtype=bool))
        ]

        return temporal_weights

    def calculate_temporal_weight(self, mapping: ChainMap) -> float:
        """Calculate the temporal weight for a given mapping."""
        # Choose a t_metric that suits your needs
        children_ids = self.get_children_ids(
            mapping.parent
        )  # Assuming you have a method to get children IDs
        time_decay_factor = self.calculate_time_coordinate(mapping, children_ids)
        return time_decay_factor

    def calculate_time_coordinate(
        self, message: ChainMap, children_ids: List[str]
    ) -> float:
        """Calculate the time coordinate based on message and its children."""
        sibling_time_differences = [
            self.message_dict[child_id].message.create_time
            - message.message.create_time
            for child_id in children_ids
        ]

        # Calculate the time decay factor
        time_decay_factor = self.time_decay_factor(message, sibling_time_differences)
        return time_decay_factor

    def time_decay_factor(
        self, message: Union[ChainMap, None], sibling_time_differences: List[float]
    ) -> float:
        """Calculate the time decay factor for a given message based on its relationship with its siblings."""
        try:
            # Check if message or message.message is None
            if (
                message is None
                or not hasattr(message, "message")
                or message.message is None
            ):
                logging.error("Message or message.message is None.")
                return 1.0

            # Check if message.message.create_time is None
            if message.message.create_time is None:
                logging.error("Message.create_time is None.")
                return 1.0

            # Find a root message with a valid create_time
            root_message = None
            for potential_root in self.message_dict.values():
                if (
                    potential_root
                    and hasattr(potential_root, "message")
                    and potential_root.message
                    and potential_root.message.create_time is not None
                ):
                    root_message = potential_root
                    break

            if root_message is None:
                logging.error("Could not find a root message with a valid create_time.")
                return 1.0

            time_diff = (
                datetime.fromtimestamp(message.message.create_time)
                - datetime.fromtimestamp(root_message.message.create_time)
            ).total_seconds() / 60

            # Calculate the time decay factor
            decay_factor = self.time_diff_decay_function(time_diff)

            # Adjust the time decay factor based on time differences between the message and its siblings
            if isinstance(sibling_time_differences, list) and sibling_time_differences:
                decay_factor *= np.mean(sibling_time_differences)

            return decay_factor

        except Exception as e:
            logging.error(
                f"Error occurred while calculating time decay factor: {str(e)}"
            )
            return 1.0

    def time_diff_decay_function(
        self, time_diff: float, decay_type: str = "exponential", half_life: float = 60
    ) -> float:
        """Calculate the decay function based on the type of decay selected."""
        try:
            # Exponential decay
            if decay_type == "exponential":
                decay_factor = 0.5 ** (time_diff / half_life)
            # Logarithmic decay
            elif decay_type == "logarithmic":
                decay_factor = 1 / (1 + np.log(time_diff + 1))
            # Linear decay
            elif decay_type == "linear":
                decay_factor = max(1 - time_diff / (time_diff + half_life), 0)
            else:
                raise ValueError(f"Unsupported decay type: {decay_type}")

            return decay_factor

        except Exception as e:
            logging.error(
                f"Error occurred while calculating time decay factor: {str(e)}"
            )
            return 1.0  # Default value
