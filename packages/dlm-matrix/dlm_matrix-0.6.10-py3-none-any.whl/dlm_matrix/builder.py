from typing import Optional, Dict, Any, List, Tuple, Union
from dlm_matrix.models import ChainTreeIndex, ChainTree, ChainMap, Message
from dlm_matrix.parsers import ChainTreeParser
from dlm_matrix.embedding import SpatialSimilarity
from dlm_matrix.utils import load_json
import pandas as pd
from tqdm import tqdm
import os
import json


class ChainTreeBuilder:
    def __init__(
        self,
        base_persist_dir: str,
        path: Optional[str] = None,
        key: Optional[str] = "title",
        data: Union[Dict, List[Dict], None] = None,
    ):
        self.base_persist_dir = base_persist_dir
        self.path = (
            None
            if data
            else (
                path
                if os.path.isabs(path)
                else os.path.join(self.base_persist_dir, path)
            )
        )
        self.key = key

        if data:
            self.data = data
        elif self.path:
            self.data = load_json(self.path)
        else:
            raise ValueError("Either 'path' or 'data' must be provided.")

        self.conversations = ChainTreeParser.parse_chain_tree(self.data)
        self.message_coord_map = {}
        self.less_than_target = []

    def as_list(self) -> List[ChainTreeIndex]:
        return self.create_conversation_trees()

    def as_dict(self) -> Dict[str, ChainTreeIndex]:
        if not self.key:
            raise ValueError("Key must be provided when building a dictionary.")
        conversation_trees = self.create_conversation_trees()
        return {
            getattr(conversation, self.key): tree
            for conversation, tree in zip(self.conversations, conversation_trees)
        }

    def get_index_by_title(self, title: str) -> int:
        for i, conversation in enumerate(self.conversations):
            if conversation.title == title:
                return i
        return -1

    def get(self, index: int) -> ChainTreeIndex:
        return self.create_conversation_trees()[index]

    def __iter__(self):
        return iter(self.create_conversation_trees())

    def __getitem__(self, index: int) -> ChainTreeIndex:
        return self.get(index)

    def __len__(self) -> int:
        return len(self.create_conversation_trees())

    def get_tree_by_title(self, title: str) -> ChainTreeIndex:
        index = self.get_index_by_title(title)
        if index == -1:
            raise ValueError(f"Conversation with title {title} not found.")
        return self.get(index)

    def create_conversation_trees(
        self, target_num: Optional[int] = 6
    ) -> Tuple[List[ChainTreeIndex], List[ChainTreeIndex]]:
        greater_than_target = []
        for i, conversation in enumerate(self.conversations):
            if conversation is not None:
                if len(conversation.mapping) >= target_num:
                    greater_than_target.append(
                        ChainTreeIndex(conversation=conversation)
                    )
                else:
                    # Only update title for conversations that are less than target_num
                    conversation.title = str(i)
                    self.less_than_target.append(
                        ChainTreeIndex(conversation=conversation)
                    )

        return greater_than_target

    def create_message_map(
        self,
        neighbors: Optional[int] = 20,
        min_messages: Optional[int] = 10,
        trees: Optional[List[ChainTreeIndex]] = None,
        format: Optional[str] = "df",
        exclude_key: Optional[List[str]] = None,
        path: Optional[str] = None,
        embedding_model: Optional[object] = None,
    ) -> Union[Dict, pd.DataFrame, None]:
        if embedding_model:
            format = "df"

        if trees is None:
            trees = self.create_conversation_trees(min_messages)

        message_coord_map = self.extract_messages_from_trees(trees, exclude_key)

        return self.format_and_save_data(
            message_coord_map, format, path, neighbors, embedding_model
        )

    def extract_messages_from_trees(
        self, trees: List[ChainTreeIndex], exclude_key: List[str]
    ):
        message_coord_map = {}
        for tree in trees:
            for message_id, mapping in tree.conversation.mapping.items():
                if self.should_include_message(tree, mapping):
                    message_data = self.extract_message_data(mapping, tree)
                    self.exclude_specified_keys(message_data, exclude_key)
                    message_coord_map[message_id] = message_data
        return message_coord_map

    def should_include_message(self, tree: ChainTreeIndex, mapping: ChainMap):
        title_is_int = self.is_title_an_integer(tree)
        return (
            mapping.message is not None
            and mapping.message.author.role != "system"
            and not title_is_int
        )

    def is_title_an_integer(self, tree: ChainTreeIndex):
        try:
            int(tree.conversation.title)
            return True
        except ValueError:
            return False

    def extract_message_data(self, mapping: ChainMap, tree: ChainTreeIndex):
        return {
            "message_id": mapping.message.id,
            "text": mapping.message.content.text if mapping.message.content else "",
            "author": mapping.message.author.role,
            "create_time": mapping.message.create_time,
            "title": tree.conversation.title,
            "embeddings": mapping.message.embedding,
        }

    def exclude_specified_keys(self, message_data: Dict, exclude_key: List[str]):
        if exclude_key:
            for key in exclude_key:
                message_data.pop(key, None)

    def format_and_save_data(
        self, message_coord_map, format, path, neighbors, embedding_model
    ):
        if format == "json":
            return self.format_as_json(message_coord_map, path)
        elif format == "df":
            return self.format_as_dataframe(
                message_coord_map, path, neighbors, embedding_model
            )
        elif format is None:
            return message_coord_map
        else:
            raise ValueError(
                "Invalid format. Accepted formats are 'json', 'df', or None."
            )

    def format_as_json(self, data, path):
        json_result = json.dumps(data)
        if path:
            with open(path, "w") as json_file:
                json_file.write(json_result)
            return None
        return json_result

    def format_as_dataframe(
        self,
        data: Union[Dict, pd.DataFrame],
        path: Optional[str] = None,
        neighbors: int = 5,
        embedding_model: Optional[SpatialSimilarity] = None,
        use_embeddings: bool = True,
    ):
        if isinstance(data, pd.DataFrame):
            df_result = data
        else:
            df_result = pd.DataFrame(data.values())

        if embedding_model:
            df_result = embedding_model.compute_message_embeddings(
                neighbors=neighbors,
                main_df=df_result,
                use_embeddings=use_embeddings,
            )

        if path:
            df_result.to_csv(self.base_persist_dir + path + ".csv", index=False)
            self.create_prompt_response_df(df_result).to_csv(
                self.base_persist_dir + path + "_prompt_response.csv", index=False
            )
            return df_result

        return df_result

    def format_dataframe(self, df: pd.DataFrame, exclude_columns: List[str] = None):
        if exclude_columns is not None:
            df = df.drop(columns=exclude_columns)

        df = df.reset_index(drop=True)

        return df

    def create_prompt_response_df(
        self, df_result: pd.DataFrame, embedding_model: SpatialSimilarity = None
    ) -> Optional[pd.DataFrame]:
        """
        Creates a new DataFrame where the 'text' column is split into 'prompt' and 'response'
        based on the 'author' column.

        Parameters:
        - df_result (pd.DataFrame): The original DataFrame.
        - embedding_model (SpatialSimilarity): The embedding model for encoding texts.

        Returns:
        - pd.DataFrame: A new DataFrame with 'prompt' and 'response' columns, or None if DataFrame is empty after filtering.
        """

        # Filter out rows where the author is 'system'
        df_result = df_result[df_result["author"] != "system"]

        # Check if DataFrame is empty after filtering
        if df_result.empty:
            return None

        # Initialize lists to hold prompts and responses
        prompts = []
        responses = []

        # Initialize a variable to hold the last prompt
        last_prompt = None

        for index, row in df_result.iterrows():
            if row["author"] == "user":
                last_prompt = row["text"]
                prompts.append(last_prompt)
                responses.append(None)
            else:
                prompts.append(last_prompt)
                responses.append(row["text"])

        # Create a new DataFrame
        new_df = df_result.copy()

        # Drop the 'text' and 'author' columns
        new_df.drop(columns=["text", "author"], inplace=True)

        # Add 'prompt' and 'response' columns
        new_df["prompt"] = prompts
        new_df["response"] = responses

        # drop embeddings column if it exists
        if "embeddings" in new_df.columns:
            new_df.drop(columns=["embeddings"], inplace=True)

        # Embedding creation (if embedding_model is provided)
        if embedding_model:
            prompt_encodings = []
            response_encodings = []

            for prompt in prompts:
                prompt_encoding = embedding_model.encode_texts(prompt)
                prompt_encodings.append(prompt_encoding)

            for response in responses:
                if response is not None:
                    response_encoding = embedding_model.encode_texts(response)
                    response_encodings.append(response_encoding)
                else:
                    response_encodings.append(None)

            # Add 'prompt_embedding' and 'response_embedding' columns
            new_df["prompt_embedding"] = prompt_encodings
            new_df["response_embedding"] = response_encodings

        return new_df

    def combine_conversations_in_batches(
        self, conversation_trees: List[ChainTreeIndex], batch_size: int = 1000
    ) -> List[ChainTreeIndex]:
        batched_trees = []
        for i in tqdm(
            range(0, len(conversation_trees), batch_size), desc="Processing batches"
        ):
            batch = conversation_trees[i : i + batch_size]
            combined_tree = self.combine_conversations(batch)
            batched_trees.append(combined_tree)
        return batched_trees

    def retrieve_mappings(
        self, conversation_trees: List[ChainTreeIndex]
    ) -> List[ChainMap]:
        print("Retrieving mappings from conversations...")
        mappings = []
        for tree in tqdm(conversation_trees):
            mappings.extend(list(tree.conversation.mapping.values()))
        return mappings

    def update_parent_child(self, mappings: List[ChainMap]) -> Dict[str, str]:
        print("Creating new IDs for mappings...")

        # If mappings is None or empty, return an empty dictionary
        if not mappings:
            return {}

        new_mapping_ids = {}
        parent_child_map = {}

        for mapping in tqdm(mappings):
            if mapping.message is not None:
                # Still retain the message ID mapping, as you did before
                new_mapping_ids[mapping.message.id] = mapping.message.id

                # Check for parent and establish a parent-child relationship
                parent_id = mapping.parent
                if parent_id:
                    # Store children IDs in a list against their parent
                    if parent_id not in parent_child_map:
                        parent_child_map[parent_id] = []
                    parent_child_map[parent_id].append(mapping.message.id)

        # Now, update the children information for each mapping based on the parent_child_map
        for mapping in mappings:
            if mapping.message and mapping.message.id in parent_child_map:
                mapping.children = parent_child_map[mapping.message.id]

        return new_mapping_ids

    def extract_and_sort_messages(
        self, mappings: List[ChainMap], new_mapping_ids: Dict[str, str]
    ) -> List[Message]:
        print("Extracting and sorting messages...")
        sorted_messages = []

        for mapping in tqdm(mappings):
            if mapping.message is not None:
                mapping.message.id = new_mapping_ids[mapping.message.id]
                sorted_messages.append(mapping.message)

        # Sort the messages based on their creation time
        sorted_messages.sort(key=lambda m: (m.create_time is None, m.create_time))

        return sorted_messages

    def create_linked_list(
        self, sorted_messages: List[Message]
    ) -> Tuple[Dict[str, str], List[Message]]:
        print("Creating linked list...")
        id_mapping = {}
        for i, message in tqdm(enumerate(sorted_messages)):
            # For each message, determine its previous and next based on its position in the sorted list
            message.prev = sorted_messages[i - 1].id if i > 0 else None
            message.next = (
                sorted_messages[i + 1].id if i < len(sorted_messages) - 1 else None
            )
            id_mapping[message.id] = message.id
        return sorted_messages

    def update_mappings(
        self, sorted_messages: List[Message], conversation_trees: List[ChainTreeIndex]
    ) -> List[ChainMap]:
        print("Updating mappings...")
        combined_mappings = []

        # Create a message_id to ChainMap dictionary for quick look-up
        existing_mappings = {
            mapping.message.id: mapping
            for tree in conversation_trees
            for mapping in tree.conversation.mapping.values()
            if mapping.message is not None
        }

        # Initialize previous message variable
        prev_message = None

        for message in tqdm(sorted_messages):
            if message.id in existing_mappings:
                mapping = existing_mappings[message.id]
                mapping.message = message
            else:
                mapping = ChainMap(id=message.id, message=message)

            # Check if message is by system
            if message.author.role == "system":
                # If message is by system, check if it is a prompt
                related_conversation = None
                for index, conv in enumerate(conversation_trees):
                    if conv.conversation.mapping.get(message.id):
                        related_conversation = conv
                        break

                if related_conversation:
                    # If message is a prompt, update the message content
                    message.content.text = f"Conversation {index + 1}: {related_conversation.conversation.title}"
                    message.content.parts = [message.content.text]
                    message.create_time = related_conversation.conversation.create_time

                if prev_message:
                    mapping.parent = prev_message.id
                    prev_mapping = existing_mappings.get(
                        prev_message.id,
                        ChainMap(id=prev_message.id, message=prev_message),
                    )
                    if prev_mapping.children:
                        prev_mapping.children.append(message.id)
                    else:
                        prev_mapping.children = [message.id]

            combined_mappings.append(mapping)
            prev_message = message

        return combined_mappings

    def combine_conversations(
        self, filtered_trees: List[ChainTreeIndex], title: str = "Combined Conversation"
    ) -> ChainTreeIndex:
        try:
            mappings = self.retrieve_mappings(filtered_trees)
            new_mapping_ids = self.update_parent_child(mappings)
            sorted_messages = self.extract_and_sort_messages(mappings, new_mapping_ids)
            sorted_messages = self.create_linked_list(sorted_messages)
            combined_mappings = self.update_mappings(sorted_messages, filtered_trees)
            print("Creating combined conversation...")
            # convert the combined mappings to a dictionary
            combined_mappings = {mapping.id: mapping for mapping in combined_mappings}
            # sort the combined mappings by create_time
            combined_mappings = dict(
                sorted(
                    combined_mappings.items(),
                    key=lambda item: item[1].message.create_time,
                )
            )

            combined_conversation = ChainTree(
                title=title,
                create_time=sorted_messages[0].create_time,
                update_time=sorted_messages[-1].create_time,
                mapping=combined_mappings,
                moderation_results=[],
                current_node="",
            )
            # convert the combined tree to a dictionary
            combined_tree = [combined_conversation.dict()]

            return combined_tree

        except Exception as e:
            print(e)
            return None


def get_message_map(path: str) -> Dict[str, Any]:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.create_message_map()


def get_chain_trees_list(path: str) -> List[ChainTreeIndex]:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.as_list()


def get_chain_trees_dict(path: str, key: str) -> Dict[str, ChainTreeIndex]:
    conversation_trees = ChainTreeBuilder(path, key)
    return conversation_trees.as_dict()


def get_chain_tree(path: str, index: int, key: str = "title") -> ChainTreeIndex:
    conversation_trees = ChainTreeBuilder(path, key)
    return conversation_trees.get(index)


def get_combined_conversations(path: str, batch_size: int) -> List[ChainTreeIndex]:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.combine_conversations_in_batches(
        conversation_trees.as_list(), batch_size
    )
