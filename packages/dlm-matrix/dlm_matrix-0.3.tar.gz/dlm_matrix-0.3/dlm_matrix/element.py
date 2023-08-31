from typing import Optional, Callable, Union, Tuple, List
import os
import re
import json
import glob
import uuid
import logging
import pandas as pd
import networkx as nx
from dlm_matrix.type import ElementType
from dlm_matrix.embedding import SpatialSimilarity


class ElementLoader:
    def __init__(self, prompt_dir: str, key: str, verbose: bool = False):
        self.prompt_dir = prompt_dir
        self.key = key
        self.logger = logging.getLogger("DataPromptLoader")
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.semantic_model = SpatialSimilarity()

    def reverse_conversion(
        self, subgraph: nx.Graph, original_graph: nx.Graph, message_id: int
    ) -> pd.DataFrame:
        original_subgraph = nx.ego_graph(
            original_graph, message_id, radius=1, center=True
        )
        mapping = {i: node for i, node in enumerate(original_subgraph.nodes())}
        relabeled_subgraph = nx.relabel_nodes(subgraph, mapping)
        df = nx.to_pandas_adjacency(relabeled_subgraph)
        return df

    def load_all(self, file_pattern="*.csv") -> pd.DataFrame:
        """
        Load all prompt objects from the prompt directory based on the file_pattern and return as a single DataFrame.
        """
        dataframes = []

        prompt_files = glob.glob(os.path.join(self.prompt_dir, f"**/{file_pattern}"))

        if not prompt_files:
            print("No prompt files found.")
            return pd.DataFrame()  # return an empty DataFrame

        def get_sort_key(f):
            match = re.search(r"\d+", os.path.basename(f))
            return int(match.group()) if match else float("inf")

        prompt_files.sort(key=get_sort_key)

        for prompt_file in prompt_files:
            if file_pattern.endswith(".csv"):
                df = pd.read_csv(prompt_file)
            elif file_pattern.endswith(".json"):
                with open(prompt_file, "r") as f:
                    data = json.load(f)

                # Extracting data from the "mapping" key
                mapping_data = data.get("mapping", {})
                if isinstance(mapping_data, dict):
                    df = pd.DataFrame([mapping_data])
                else:
                    raise ValueError(
                        f"Unexpected structure under 'mapping' in file: {prompt_file}"
                    )
            else:
                raise ValueError(f"Unsupported file pattern: {file_pattern}")
            dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df

    def traverse_keys(
        self,
        data: dict,
        keys: List[str],
        return_all_values: bool = False,
        include_key_with_value: bool = False,
        callback: Optional[Callable] = None,
    ) -> Union[dict, List[dict], List[Tuple[str, dict]], None]:
        """
        Traverse through the keys in the given data.

        Args:
            data (dict): Data to traverse.
            keys (List[str]): List of keys to follow.
            return_all_values (bool, optional): If True, returns all values from the keys. Defaults to False.
            include_key_with_value (bool, optional): If True, returns a tuple of key and value. Defaults to False.
            callback (Optional[Callable], optional): A function to apply to each value as it is retrieved. Defaults to None.

        Returns:
            Union[dict, List[dict], List[Tuple[str, dict]], None]: Resulting value(s) or None if keys are not found.
        """

        # Initialize a list to store all values if return_all_values is True
        all_values = []

        try:
            # Iterate through the provided keys to traverse the data
            for key in keys:
                # Check if the key exists in the current level of the data
                if isinstance(data, dict) and key in data:
                    value = data[key]

                    # Apply the callback function to the value if provided
                    if callback:
                        value = callback(value)

                    # If return_all_values is True, store the value (and key if include_key_with_value is True)
                    if return_all_values:
                        result = (key, value) if include_key_with_value else value
                        all_values.append(result)

                    # Move to the next level of the data using the current key
                    data = value
                else:
                    # If the key is not found, return None
                    return None

            # Return either all the values or the final value, depending on return_all_values
            return all_values if return_all_values else data

        except Exception as e:
            # Log an error if an exception occurs during traversal
            self.logger.error(f"Error traversing keys {keys}: {str(e)}")
            return None

    def get_prompt_files(
        self,
        directory: Optional[str] = None,
        file_pattern: str = "**/*.json",
        sort_function: Optional[Callable] = None,
    ) -> List[str]:
        """
        Retrieve the list of prompt files from a specified directory.

        Args:
            directory (str): The directory to search for prompt files.
            file_pattern (str, optional): The pattern to match files. Defaults to "**/*.json" (matches all JSON files in the directory).
            sort_function (Callable, optional): A custom sorting function. Defaults to None.

        Returns:
            List[str]: A list of paths to prompt files.
        """

        dir_to_use = directory if directory else self.prompt_dir

        # Use glob to match all files in the directory with the specified pattern (e.g., all JSON files).
        prompt_files = glob.glob(os.path.join(dir_to_use, file_pattern))

        # Sort the files using the custom sort function if provided.
        if sort_function:
            prompt_files.sort(key=sort_function)
        else:
            # If no custom sort function is provided, sort the files based on the numeric part in their filenames.
            prompt_files.sort(
                key=lambda f: int(re.search(r"\d+", os.path.basename(f)).group())
                if re.search(r"\d+", os.path.basename(f))
                else 0
            )

        # Return the list of prompt files.
        return prompt_files

    def filter_by_prefix(
        self,
        data: Union[List[str], List[dict]],
        prefix: str,
        include_more: bool = False,
        case_sensitive: bool = False,
        match_strategy: str = "start",
    ) -> List[Union[str, dict]]:
        """
        Filter the given data based on the provided prefix.

        Args:
            data (Union[List[str], List[dict]]): Data to filter. Accepts both string lists and dictionaries.
            prefix (str): Prefix to match against each data item.
            include_more (bool, optional): Include data with content beyond the prefix. Defaults to False.
            case_sensitive (bool, optional): Consider case in matching. Defaults to False.
            match_strategy (str, optional): Matching strategy ("start", "exact", "contains"). Defaults to "start".

        Returns:
            List[Union[str, dict]]: Filtered data.
        """

        # Convert the prefix to lowercase if case sensitivity is not required.
        if not case_sensitive:
            prefix = prefix.lower()

        # Inner function to determine if an item matches the prefix based on the specified match strategy.
        def match(item):
            # Convert the item to string for uniformity, and make it lowercase if case sensitivity is off.
            content = item if isinstance(item, str) else str(item)
            if not case_sensitive:
                content = content.lower()

            # Determine if the content matches the prefix based on the match strategy.
            if match_strategy == "start":
                return content.startswith(prefix)
            elif match_strategy == "exact":
                return content == prefix
            elif match_strategy == "contains":
                return prefix in content
            else:
                # Log an error if an unknown match strategy is used.
                self.logger.error(f"Unknown match strategy: {match_strategy}")
                return False

        # Apply the match function to filter the data based on the prefix.
        filtered_data = [item for item in data if match(item)]

        # If the include_more option is enabled, filter the data to include items with more content than the prefix.
        if include_more:
            filtered_data = [
                item
                for item in filtered_data
                if len(str(item).strip()) > len(prefix) and str(item).strip() != prefix
            ]

        # Return the filtered data.
        return filtered_data

    def prepare_initial_data(
        self,
        processed_elements: List[List[str]],
        element_type: ElementType = ElementType.STEP,
    ) -> pd.DataFrame:
        """
        Create a DataFrame from the processed elements.
        Compute embeddings for each element and group similar terms.
        Perform element-wise similarity propagation and add columns for propagated similarity information.
        Retrieve pattern frequency information and add columns 'exact_frequency' and 'similar_frequency'.
        Return the resulting DataFrame.

        Args:
            processed_elements (List[List[str]]): The list of processed elements.
            element_type (ElementType, optional): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
                Defaults to ElementType.STEP.

        Returns:
            pd.DataFrame: The DataFrame containing the elements and their embeddings.
        """
        try:
            # Check if elements are already present in the data
            if all(len(row) >= 2 for row in processed_elements):
                # Elements are already present, use the default elements
                elements = [
                    f"{element_type.value} {i}"
                    for i in range(len(processed_elements[0]) - 1)
                ]  # Subtract 1 for the prefix column
            else:
                # Elements are not present, add elements accordingly
                num_elements = (
                    len(processed_elements[0]) - 1
                )  # Subtract 1 for the prefix column
                elements = [f"{element_type.value} {i}" for i in range(num_elements)]

            # Prepare the initial data using the computed elements
            data = {"Prefix": [row[0] for row in processed_elements]}
            for i, element in enumerate(elements):
                data[element] = [
                    row[i + 1] if len(row) > (i + 1) else ""
                    for row in processed_elements
                ]

            df = pd.DataFrame(data)

            # Filter rows that do not start with the element name
            for element in elements:
                df = df[df[element].str.startswith(element + ":")]

        except Exception as e:
            print(f"Error processing elements: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of errors

        return df

    def load_data_prompts(
        self,
        min_length: Optional[int] = None,
        prefix: Optional[str] = None,
        include_more: bool = False,
    ) -> List[dict]:
        """
        Load all prompt objects from the stored JSON files.

        Args:
            min_length (int, optional): Minimum length of the prompt objects to filter. Defaults to None.
            prefix (str, optional): Prefix to check for in the first index of each prompt object. Defaults to None.
            include_more (bool, optional): Whether to include prompt objects with content beyond the specified prefix. Defaults to False.

        Returns:
            List[dict]: A list of prompt objects.
        """
        prompt_objects = []
        prompt_files = glob.glob(os.path.join(self.prompt_dir, "**/*.json"))
        if prompt_files:
            prompt_files.sort(
                key=lambda f: int(re.search(r"\d+", os.path.basename(f)).group())
            )
            for prompt_file in prompt_files:
                with open(prompt_file, "r") as f:
                    prompt_object = json.load(f)
                prompt_objects.append(prompt_object[self.key])

            # Filter the prompt objects based on the minimum length if specified
            if min_length is not None:
                prompt_objects = [
                    prompt for prompt in prompt_objects if len(prompt) >= min_length
                ]

            def clean_prompt_object(prompt_object: List[str]) -> List[str]:
                return [item.strip() for item in prompt_object]

            # Clean the prompt objects by removing leading and trailing whitespaces
            prompt_objects = [clean_prompt_object(prompt) for prompt in prompt_objects]

            # Check if the first index of each prompt object starts with the provided prefix
            if prefix is not None:
                # Clean the prefix by removing leading and trailing whitespaces
                prefix = prefix.strip()
                prompt_objects = [
                    prompt for prompt in prompt_objects if prompt[0] == prefix
                ]

                # Optionally include prompt objects with content beyond the specified prefix
                if include_more:
                    prompt_objects = [
                        prompt
                        for prompt in prompt_objects
                        if len(prompt[0]) > len(prefix) and prompt[0].strip() != prefix
                    ]

            return prompt_objects

        else:
            print("No prompt files found.")
            return None

    def compute_embeddings(
        self, df: pd.DataFrame, element_type: ElementType, separate_columns: bool = True
    ) -> pd.DataFrame:
        """
        Compute embeddings for each step.

        Args:
            df (pd.DataFrame): The DataFrame containing the steps.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            separate_columns (bool, optional): Whether to separate the columns (Prefix and Steps)
                during the embedding process. Defaults to True.

        Returns:
            pd.DataFrame: The DataFrame with added columns for embeddings.
        """
        try:
            # Prepare the data for embedding
            if separate_columns:
                # Separate the columns (Prefix and Elements) and drop NaN values
                element_columns = [
                    col for col in df.columns if col.startswith(element_type.value)
                ]
                all_elements = pd.concat(
                    [df[col] for col in element_columns], ignore_index=True
                )
                prefix = pd.Series(
                    dtype=str
                )  # Explicitly specify the dtype of the empty Series
            else:
                # Combine all columns (Prefix and Elements) into a single column and drop NaN values
                all_elements = df.stack().dropna()
                prefix = pd.Series(
                    dtype=str
                )  # Explicitly specify the dtype of the empty Series

            # Compute embeddings for all elements
            embeddings = self.semantic_model.fit(
                all_elements.tolist() + prefix.tolist()
            )
            embedding_dict = {i: embeddings[i] for i in range(len(embeddings))}

            # Add embeddings to the DataFrame for each element
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            for col in df_copy.columns:
                if col.startswith(element_type.value):
                    element_len = len(df_copy[col])
                    embedding_col = f"{col} embedding"
                    if separate_columns:
                        # Separate columns: Add embeddings for each element separately
                        df_copy[embedding_col] = (
                            pd.Series(embedding_dict).loc[: element_len - 1].tolist()
                        )
                    else:
                        # Combined columns: Add embeddings for all elements in a single column
                        df_copy[embedding_col] = pd.Series(
                            list(embedding_dict.values())
                        )

                    embedding_dict = {
                        k - element_len: v
                        for k, v in embedding_dict.items()
                        if k >= element_len
                    }

            return df_copy

        except Exception as e:
            print(f"Error computing embeddings: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of errors

    def create_prompt_response_dataframe(
        self, df: pd.DataFrame, element_type: ElementType
    ) -> pd.DataFrame:
        """
        Create a new dataframe with prompt and response columns where the prefix is removed and step 1 is the prompt and the remaining steps are cobined the response

        Args:
            df (pd.DataFrame): The DataFrame containing the steps.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).

        Returns:
            pd.DataFrame: The DataFrame with added columns for prompt and response.
        """
        try:
            # Create a new dataframe with prompt and response columns where the prefix is removed and step 1 is the prompt and the remaining steps are cobined the response
            prompt_response_df = pd.DataFrame()
            prompt_response_df["prompt"] = df[element_type.value + " 0"]
            prompt_response_df["response"] = df.iloc[:, 2:].apply(
                lambda x: " ".join(x.dropna().astype(str)), axis=1
            )

            # reset index
            prompt_response_df.reset_index(drop=True, inplace=True)

            return prompt_response_df

        except Exception as e:
            print(f"Error creating prompt and response dataframe: {e}")
            return pd.DataFrame()

    def build_incremental_row(self, row, element_col, element_embed_col, element_id, i):
        return {
            "id": str(uuid.uuid4()),
            "element_id": element_id,
            "Element Type": element_col.split(" ")[0],
            "Element Index": i,
            "Element Text": row[element_col],
            "Embedding": row[element_embed_col],
        }

    def build_linear_row(self, row, element_col, element_embed_col, i):
        return {
            "id": str(uuid.uuid4()),
            "Prefix": row[f"{element_col.split(' ')[0]} 0"],
            "Element": i,
            "Element Text": row[element_col],
            "Embedding": row[element_embed_col],
        }

    def convert_to_long_format(
        self, df: pd.DataFrame, element_type: ElementType, format_type: str = "linear"
    ) -> pd.DataFrame:
        long_format_data = []
        num_elements = df.columns.str.startswith(element_type.value).sum()
        element_id_dict = {}

        for idx, row in df.iterrows():
            prefix_text = row["Prefix"]
            element_id = element_id_dict.get(prefix_text)
            if element_id is None:
                element_id = str(uuid.uuid4())
                element_id_dict[prefix_text] = element_id

            for i in range(num_elements):
                element_col = f"{element_type.value} {i}"
                element_embed_col = f"{element_type.value} {i} embedding"
                if element_col in df.columns and element_embed_col in df.columns:
                    if format_type == "incremental":
                        long_format_data.append(
                            self.build_incremental_row(
                                row, element_col, element_embed_col, element_id, i
                            )
                        )
                    elif format_type == "linear":
                        long_format_data.append(
                            self.build_linear_row(
                                row, element_col, element_embed_col, i
                            )
                        )

        long_df = pd.DataFrame(long_format_data)
        return long_df
