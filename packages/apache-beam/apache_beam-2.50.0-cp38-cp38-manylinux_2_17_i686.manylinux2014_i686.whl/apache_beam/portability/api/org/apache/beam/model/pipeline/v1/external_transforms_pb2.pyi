"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file

Protocol Buffers describing the external transforms available.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import org.apache.beam.model.pipeline.v1.schema_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ExternalConfigurationPayload(google.protobuf.message.Message):
    """A configuration payload for an external transform.
    Used as the payload of ExternalTransform as part of an ExpansionRequest.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SCHEMA_FIELD_NUMBER: builtins.int
    PAYLOAD_FIELD_NUMBER: builtins.int
    @property
    def schema(self) -> org.apache.beam.model.pipeline.v1.schema_pb2.Schema:
        """A schema for use in beam:coder:row:v1"""
    payload: builtins.bytes
    """A payload which can be decoded using beam:coder:row:v1 and the given
    schema.
    """
    def __init__(
        self,
        *,
        schema: org.apache.beam.model.pipeline.v1.schema_pb2.Schema | None = ...,
        payload: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["schema", b"schema"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["payload", b"payload", "schema", b"schema"]) -> None: ...

global___ExternalConfigurationPayload = ExternalConfigurationPayload

@typing_extensions.final
class ExpansionMethods(google.protobuf.message.Message):
    """Defines specific expansion methods that may be used to expand cross-language
    transforms.
    Has to be set as the URN of the transform of the expansion request.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Enum:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _EnumEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ExpansionMethods._Enum.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        JAVA_CLASS_LOOKUP: ExpansionMethods._Enum.ValueType  # 0
        """Expand a Java transform using specified constructor and builder methods.
        Transform payload will be of type JavaClassLookupPayload.
        """
        SCHEMA_TRANSFORM: ExpansionMethods._Enum.ValueType  # 1
        """Expanding a SchemaTransform identified by the expansion service.
        Transform payload will be of type  SchemaTransformPayload.
        """

    class Enum(_Enum, metaclass=_EnumEnumTypeWrapper): ...
    JAVA_CLASS_LOOKUP: ExpansionMethods.Enum.ValueType  # 0
    """Expand a Java transform using specified constructor and builder methods.
    Transform payload will be of type JavaClassLookupPayload.
    """
    SCHEMA_TRANSFORM: ExpansionMethods.Enum.ValueType  # 1
    """Expanding a SchemaTransform identified by the expansion service.
    Transform payload will be of type  SchemaTransformPayload.
    """

    def __init__(
        self,
    ) -> None: ...

global___ExpansionMethods = ExpansionMethods

@typing_extensions.final
class JavaClassLookupPayload(google.protobuf.message.Message):
    """A configuration payload for an external transform.
    Used to define a Java transform that can be directly instantiated by a Java
    expansion service.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLASS_NAME_FIELD_NUMBER: builtins.int
    CONSTRUCTOR_METHOD_FIELD_NUMBER: builtins.int
    CONSTRUCTOR_SCHEMA_FIELD_NUMBER: builtins.int
    CONSTRUCTOR_PAYLOAD_FIELD_NUMBER: builtins.int
    BUILDER_METHODS_FIELD_NUMBER: builtins.int
    class_name: builtins.str
    """Name of the Java transform class."""
    constructor_method: builtins.str
    """A static method to construct the initial instance of the transform.
    If not provided, the transform should be instantiated using a class
    constructor.
    """
    @property
    def constructor_schema(self) -> org.apache.beam.model.pipeline.v1.schema_pb2.Schema:
        """The top level fields of the schema represent the method parameters in
        order.
        If able, top level field names are also verified against the method
        parameters for a match.
        Any field names in the form 'ignore[0-9]+' will not be used for validation
        hence that format can be used to represent arbitrary field names.
        """
    constructor_payload: builtins.bytes
    """A payload which can be decoded using beam:coder:row:v1 and the provided
    constructor schema.
    """
    @property
    def builder_methods(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___BuilderMethod]:
        """Set of builder methods and corresponding parameters to apply after the
        transform object is constructed.
        When constructing the transform object, given builder methods will be
        applied in order.
        """
    def __init__(
        self,
        *,
        class_name: builtins.str | None = ...,
        constructor_method: builtins.str | None = ...,
        constructor_schema: org.apache.beam.model.pipeline.v1.schema_pb2.Schema | None = ...,
        constructor_payload: builtins.bytes | None = ...,
        builder_methods: collections.abc.Iterable[global___BuilderMethod] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["constructor_schema", b"constructor_schema"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["builder_methods", b"builder_methods", "class_name", b"class_name", "constructor_method", b"constructor_method", "constructor_payload", b"constructor_payload", "constructor_schema", b"constructor_schema"]) -> None: ...

global___JavaClassLookupPayload = JavaClassLookupPayload

@typing_extensions.final
class BuilderMethod(google.protobuf.message.Message):
    """This represents a builder method of the transform class that should be
    applied in-order after instantiating the initial transform object.
    Each builder method may take one or more parameters and has to return an
    instance of the transform object.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    SCHEMA_FIELD_NUMBER: builtins.int
    PAYLOAD_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Name of the builder method"""
    @property
    def schema(self) -> org.apache.beam.model.pipeline.v1.schema_pb2.Schema:
        """The top level fields of the schema represent the method parameters in
        order.
        If able, top level field names are also verified against the method
        parameters for a match.
        Any field names in the form 'ignore[0-9]+' will not be used for validation
        hence that format can be used to represent arbitrary field names.
        """
    payload: builtins.bytes
    """A payload which can be decoded using beam:coder:row:v1 and the builder
    method schema.
    """
    def __init__(
        self,
        *,
        name: builtins.str | None = ...,
        schema: org.apache.beam.model.pipeline.v1.schema_pb2.Schema | None = ...,
        payload: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["schema", b"schema"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "payload", b"payload", "schema", b"schema"]) -> None: ...

global___BuilderMethod = BuilderMethod

@typing_extensions.final
class SchemaTransformPayload(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IDENTIFIER_FIELD_NUMBER: builtins.int
    CONFIGURATION_SCHEMA_FIELD_NUMBER: builtins.int
    CONFIGURATION_ROW_FIELD_NUMBER: builtins.int
    identifier: builtins.str
    """The identifier of the SchemaTransform (typically a URN)."""
    @property
    def configuration_schema(self) -> org.apache.beam.model.pipeline.v1.schema_pb2.Schema:
        """The configuration schema of the SchemaTransform."""
    configuration_row: builtins.bytes
    """The configuration of the SchemaTransform.
    Should be decodable via beam:coder:row:v1.
    The schema of the Row should be compatible with the schema of the
    SchemaTransform.
    """
    def __init__(
        self,
        *,
        identifier: builtins.str | None = ...,
        configuration_schema: org.apache.beam.model.pipeline.v1.schema_pb2.Schema | None = ...,
        configuration_row: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["configuration_schema", b"configuration_schema"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["configuration_row", b"configuration_row", "configuration_schema", b"configuration_schema", "identifier", b"identifier"]) -> None: ...

global___SchemaTransformPayload = SchemaTransformPayload
