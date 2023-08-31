import ast
from pydantic import create_model, Field, BaseModel, PrivateAttr
from typing import Any, List, Dict, Optional, Type, Tuple, Literal
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

type_mapping = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "List[int]": List[int],
    "List[float]": List[float],
    "List[str]": List[str],
    "Dict[str, int]": Dict[str, int],
    "Dict[str, float]": Dict[str, float],
    "Dict[str, str]": Dict[str, str],
}


class BaseEntity(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def __call__(self, **data: Any) -> BaseModel:
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


class FieldConfig(BaseModel):
    type: str
    default: Optional[Any] = None


class MethodConfig(BaseModel):
    code: str = Field(..., description="The Python code of the method.")
    args: Dict[str, str] = Field(..., description="The types of the method arguments.")
    return_type: str = Field(..., description="The return type of the method.")


class RelationshipConfig(BaseModel):
    target: str = Field(..., description="The name of the target entity.")

    type: Literal["one-to-one", "one-to-many", "many-to-many", "many-to-one"] = Field(
        ..., description="The type of the relationship."
    )
    back_populates: Optional[str] = Field(
        None, description="The name of the back reference in the target entity."
    )
    uselist: Optional[bool] = Field(
        None,
        description="Specifies if a list or a scalar should be used for the relationship.",
    )
    join_condition: Optional[str] = Field(
        None,
        description="The condition that determines how the entities are related in the relationship.",
    )
    cascade: Optional[str] = Field(
        None, description="The cascading behavior of the relationship."
    )
    single_parent: Optional[bool] = Field(
        None,
        description="If set to True, it ensures that only one parent object is associated with this child object.",
    )


class EntityCreation(BaseModel):
    name: str = Field(..., description="The unique name of the entity to be created.")
    fields: Dict[str, FieldConfig] = Field(..., description="The fields of the entity.")
    methods: Dict[str, MethodConfig] = Field(
        default_factory=dict, description="The methods of the entity."
    )
    base: Optional[Type[BaseModel]] = Field(
        None, description="The base class of the entity."
    )
    relationships: Dict[str, RelationshipConfig] = Field(
        default_factory=dict, description="The relationships of the entity."
    )

    def create(self) -> BaseEntity:
        return Entity(
            name=self.name,
            fields={
                name: (field.type, field.default) for name, field in self.fields.items()
            },
            methods=self.methods,
            base=self.base,
            relationships=self.relationships,
        )


class Entity(BaseEntity):
    def __init__(
        self,
        name: str,
        fields: Dict[str, Tuple[str, Optional[Any]]],
        methods: Dict[str, MethodConfig],
        base: Optional[BaseEntity] = None,
        relationships: Dict[str, RelationshipConfig] = None,
    ) -> None:
        self.name = name  # initialize self.name first
        self.fields = fields
        self.methods = methods
        self.base = base
        self.relationships = relationships
        self._model = self.__create_model__()  # then initialize self._model

    def __create_model__(self) -> Type[BaseModel]:
        annotations = {
            name: (type_mapping[type_name], default)
            for name, (type_name, default) in self.fields.items()
        }
        base_model = self.base._model if self.base else BaseModel
        model = create_model(self.name, **annotations, __base__=base_model)

        for name, method in self.methods.items():
            code_tree = ast.parse(method.code, mode="exec")
            assert len(code_tree.body) == 1
            assert isinstance(code_tree.body[0], ast.FunctionDef)
            code_obj = compile(code_tree, filename="<ast>", mode="exec")
            local_scope = {}
            exec(code_obj, None, local_scope)
            func = local_scope[name]
            setattr(model, name, func)

        return model

    def __call__(self, **data: Any) -> BaseModel:
        return self._model(**data)


class EntityConfig(BaseModel):
    creations: List[EntityCreation] = Field(
        ..., description="The entities to be created."
    )

    def create_entities(self) -> Dict[str, Entity]:
        return {creation.name: creation.create() for creation in self.creations}


# person_creation = EntityCreation(
#     name="Person",
#     fields={
#         "name": FieldConfig(type="str"),
#         "age": FieldConfig(type="int", default=0),
#         "pets": FieldConfig(type="List[str]", default_factory=list),
#     },
#     relationships={
#         "pets": RelationshipConfig(
#             target="Pet",
#             type="one-to-many",
#             back_populates="owner",
#         )
#     },
#     methods={
#         "get_older": MethodConfig(
#             code="""
# def get_older(self, years: int) -> None:
#     self.age += years
# """,
#             args={"years": "int"},
#             return_type="None",
#         )
#     },
# )

# pet_creation = EntityCreation(
#     name="Pet",
#     fields={
#         "name": FieldConfig(type="str"),
#         "species": FieldConfig(type="str"),
#         "owner": FieldConfig(type="str", default=None),
#     },
#     relationships={
#         "owner": RelationshipConfig(
#             target="Person",
#             type="many-to-one",
#             back_populates="pets",
#         )
#     },
# )

# config = EntityConfig(creations=[person_creation, pet_creation])

# entities = config.create_entities()

# person = entities["Person"](name="John Doe")
# rex = entities["Pet"](name="Rex", species="Dog")
# donald = entities["Pet"](name="Donald", species="Cat")

# rex.owner = person.name
# donald.owner = person.name

# person.pets = [rex]
# person.pets.append(donald)

# person.get_older(5)
# print(
#     person.dict()
# )  # Output: {"name": "John Doe", "age": 0, "pets": [{"name": "Rex", "species": "Dog", "owner": "John Doe"}]}
# print(rex.dict())  # Output: {"name": "Rex", "species": "Dog", "owner": "John Doe"}
# print(
#     donald.dict()
# )  # Output: {"name": "Donald", "species": "Cat", "owner": "John Doe"}
