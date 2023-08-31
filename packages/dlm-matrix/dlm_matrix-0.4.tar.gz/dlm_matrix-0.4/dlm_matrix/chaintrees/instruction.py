class ChainInstruction:
    def __init__(
        self,
        instruction_type,
        content=None,
        coordinate=None,
        priority=0,
        func=None,
        metadata=None,
    ):
        self.instruction_type = instruction_type
        self.content = content
        self.coordinate = coordinate
        self.priority = priority
        self.func = func
        self.metadata = metadata or {}

    def validate(self):
        """
        Validate the chain instruction to ensure all required fields are present and valid.
        """
        if not self.instruction_type:
            raise ValueError("The instruction_type field is required.")

        if not isinstance(self.instruction_type, str):
            raise TypeError("The instruction_type field must be a string.")

        if self.instruction_type == "custom":
            if not callable(self.func):
                raise ValueError(
                    "The 'func' field must be a callable function for custom instructions."
                )

        if self.content is not None and not isinstance(self.content, str):
            raise TypeError("The content field must be a string or None.")

        if self.coordinate is not None and not isinstance(self.coordinate):
            raise TypeError(
                "The coordinate field must be an instance of the Coordinate class or None."
            )

        if not isinstance(self.priority, int):
            raise TypeError("The priority field must be an integer.")

        if self.priority < 0:
            raise ValueError("The priority field must be a non-negative integer.")

        if not isinstance(self.metadata, dict):
            raise TypeError("The metadata field must be a dictionary.")

    def to_dict(self):
        """
        Convert the chain instruction to a dictionary representation.
        """
        instruction_dict = {
            "instruction_type": self.instruction_type,
            "content": self.content,
            "coordinate": self.coordinate.to_dict() if self.coordinate else None,
            "priority": self.priority,
            "func": self.func,
            "metadata": self.metadata,
        }
        return instruction_dict

    @classmethod
    def from_dict(cls, instruction_dict):
        """
        Create a ChainInstruction instance from a dictionary representation.
        """
        if not isinstance(instruction_dict, dict):
            raise TypeError("The instruction_dict must be a dictionary.")

        instruction_type = instruction_dict.get("instruction_type")
        content = instruction_dict.get("content")
        coordinate = instruction_dict.get("coordinate")
        priority = instruction_dict.get("priority", 0)
        func = instruction_dict.get("func")
        metadata = instruction_dict.get("metadata")

        return cls(instruction_type, content, coordinate, priority, func, metadata)

    def __repr__(self):
        """
        Return a string representation of the ChainInstruction object.
        """
        return (
            f"ChainInstruction(instruction_type={self.instruction_type}, content={self.content}, "
            f"coordinate={self.coordinate}, priority={self.priority}, func={self.func}, metadata={self.metadata})"
        )

    def __eq__(self, other):
        """
        Check if two ChainInstruction objects are equal.
        """
        if isinstance(other, ChainInstruction):
            return (
                self.instruction_type == other.instruction_type
                and self.content == other.content
                and self.coordinate == other.coordinate
                and self.priority == other.priority
                and self.func == other.func
                and self.metadata == other.metadata
            )
        return False

    def add_metadata(self, key, value):
        """
        Add a metadata entry to the ChainInstruction.
        """
        self.metadata[key] = value

    def remove_metadata(self, key):
        """
        Remove a metadata entry from the ChainInstruction based on the given key.
        """
        if key in self.metadata:
            del self.metadata[key]

    def get_metadata(self, key, default=None):
        """
        Get the value of a metadata entry from the ChainInstruction based on the given key.
        If the key is not found, return the default value.
        """
        return self.metadata.get(key, default)

    def has_metadata(self, key):
        """
        Check if the ChainInstruction has a metadata entry with the given key.
        """
        return key in self.metadata

    def clear_metadata(self):
        """
        Clear all metadata entries from the ChainInstruction.
        """
        self.metadata = {}


class DynamicInstruction(ChainInstruction):
    def __init__(
        self,
        instruction_type,
        content=None,
        coordinate=None,
        priority=0,
        func=None,
        metadata=None,
    ):
        super().__init__(
            instruction_type, content, coordinate, priority, func, metadata
        )
        self.dynamic_data = None
        self.conditions = []
        self.loop_iterations = None
        self.loop_condition = None

    def set_dynamic_data(self, dynamic_data):
        """
        Set the dynamic data for the instruction.
        """
        self.dynamic_data = dynamic_data

    def get_dynamic_data(self):
        """
        Get the dynamic data of the instruction.
        """
        return self.dynamic_data

    def add_condition(self, condition):
        """
        Add a condition for the instruction to be executed.
        """
        self.conditions.append(condition)

    def set_loop_iterations(self, iterations):
        """
        Set the number of loop iterations for the instruction.
        """
        self.loop_iterations = iterations

    def set_loop_condition(self, condition):
        """
        Set the loop condition for the instruction.
        """
        self.loop_condition = condition

    def validate(self):
        """
        Validate the dynamic instruction, including the base class validation.
        """
        super().validate()

        if self.instruction_type == "dynamic" and self.dynamic_data is None:
            raise ValueError("Dynamic instructions require setting dynamic data.")

        if self.conditions:
            for condition in self.conditions:
                if not callable(condition):
                    raise ValueError("Conditions must be callable functions.")

        if self.loop_iterations is not None and not isinstance(
            self.loop_iterations, int
        ):
            raise TypeError("Loop iterations must be an integer.")

        if self.loop_condition is not None and not callable(self.loop_condition):
            raise ValueError("Loop condition must be a callable function.")

    def to_dict(self):
        """
        Convert the dynamic instruction to a dictionary representation.
        """
        instruction_dict = super().to_dict()
        instruction_dict["dynamic_data"] = self.dynamic_data
        instruction_dict["conditions"] = self.conditions
        instruction_dict["loop_iterations"] = self.loop_iterations
        instruction_dict["loop_condition"] = self.loop_condition
        return instruction_dict

    @classmethod
    def from_dict(cls, instruction_dict):
        """
        Create a DynamicInstruction instance from a dictionary representation.
        """
        dynamic_data = instruction_dict.get("dynamic_data")
        conditions = instruction_dict.get("conditions")
        loop_iterations = instruction_dict.get("loop_iterations")
        loop_condition = instruction_dict.get("loop_condition")

        dynamic_instruction = super().from_dict(instruction_dict)
        dynamic_instruction.dynamic_data = dynamic_data
        dynamic_instruction.conditions = conditions
        dynamic_instruction.loop_iterations = loop_iterations
        dynamic_instruction.loop_condition = loop_condition

        return dynamic_instruction

    def __repr__(self):
        """
        Return a string representation of the DynamicInstruction object.
        """
        return (
            f"DynamicInstruction(instruction_type={self.instruction_type}, content={self.content}, "
            f"coordinate={self.coordinate}, priority={self.priority}, func={self.func}, "
            f"metadata={self.metadata}, dynamic_data={self.dynamic_data}, "
            f"conditions={self.conditions}, loop_iterations={self.loop_iterations}, "
            f"loop_condition={self.loop_condition})"
        )

    def execute(self):
        """
        Execute the dynamic instruction based on conditions and loop settings.
        """
        if self.instruction_type == "dynamic" and callable(self.func):
            if self._check_conditions():
                if self.loop_iterations is not None and callable(self.loop_condition):
                    for _ in range(self.loop_iterations):
                        if self.loop_condition():
                            self.func(self.dynamic_data)
                        else:
                            break

                else:
                    self.func(self.dynamic_data)

    def _check_conditions(self):
        """
        Check if the conditions for the dynamic instruction are met.
        """
        if self.conditions:
            for condition in self.conditions:
                if not condition():
                    return False
        return True


# from .chain import Coordinate
# from .chain_instruction import ChainInstruction
# from .reply_chain_director import ReplyChainDirector

# # Create a ReplyChainDirector instance
# director = ReplyChainDirector()

# # Create a list of ChainInstructions
# chain_instructions = [
#     ChainInstruction(
#         instruction_type="system",
#         content="Perform system-level action",
#         coordinate=Coordinate(x=0, y=0, z=0, t=1),
#         priority=2,
#     ),
#     ChainInstruction(
#         instruction_type="condition",
#         conditions=[
#             {
#                 "func": lambda data: data.get("user_input") == "yes",
#                 "instructions": [
#                     ChainInstruction(
#                         instruction_type="custom",
#                         func=lambda external_data: print("Custom instruction executed."),
#                     ),
#                     ChainInstruction(
#                         instruction_type="prompt",
#                         content="Please provide additional information:",
#                     ),
#                 ],
#             },
#             {
#                 "func": lambda data: data.get("user_input") == "no",
#                 "instructions": [
#                     ChainInstruction(
#                         instruction_type="branch",
#                         condition_func=lambda external_data: external_data.get("branch_condition"),
#                         instructions=[
#                             ChainInstruction(
#                                 instruction_type="prompt",
#                                 content="Please provide an alternative option:",
#                             ),
#                         ],
#                     ),
#                 ],
#             },
#         ],
#         default_instructions=[
#             ChainInstruction(
#                 instruction_type="prompt",
#                 content="Please enter your response:",
#             ),
#         ],
#     ),
# ]

# # Create external data
# external_data = {
#     "user_input": input("Enter your input (yes/no): "),
#     "branch_condition": True,
# }

# # Construct the dynamic chain
# director.construct(answer="Answer", question="Question", chain_instructions=chain_instructions, external_data=external_data)
