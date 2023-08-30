"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import shared.shared_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class FirestoreDocumentXTimeouts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATE_FIELD_NUMBER: builtins.int
    DELETE_FIELD_NUMBER: builtins.int
    UPDATE_FIELD_NUMBER: builtins.int
    create: builtins.str
    delete: builtins.str
    update: builtins.str
    def __init__(
        self,
        *,
        create: builtins.str = ...,
        delete: builtins.str = ...,
        update: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["create", b"create", "delete", b"delete", "update", b"update"]) -> None: ...

global___FirestoreDocumentXTimeouts = FirestoreDocumentXTimeouts

@typing_extensions.final
class FirestoreDocument(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COLLECTION_FIELD_NUMBER: builtins.int
    CREATE_TIME_FIELD_NUMBER: builtins.int
    DATABASE_FIELD_NUMBER: builtins.int
    DOCUMENT_ID_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    UPDATE_TIME_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    collection: builtins.str
    create_time: builtins.str
    database: builtins.str
    document_id: builtins.str
    fields: builtins.str
    id: builtins.str
    name: builtins.str
    path: builtins.str
    project: builtins.str
    update_time: builtins.str
    @property
    def timeouts(self) -> global___FirestoreDocumentXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        collection: builtins.str = ...,
        create_time: builtins.str = ...,
        database: builtins.str = ...,
        document_id: builtins.str = ...,
        fields: builtins.str = ...,
        id: builtins.str = ...,
        name: builtins.str = ...,
        path: builtins.str = ...,
        project: builtins.str = ...,
        update_time: builtins.str = ...,
        timeouts: global___FirestoreDocumentXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["collection", b"collection", "create_time", b"create_time", "database", b"database", "document_id", b"document_id", "fields", b"fields", "id", b"id", "name", b"name", "path", b"path", "project", b"project", "resource_info", b"resource_info", "timeouts", b"timeouts", "update_time", b"update_time"]) -> None: ...

global___FirestoreDocument = FirestoreDocument

@typing_extensions.final
class FirestoreIndexXFields(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ARRAY_CONFIG_FIELD_NUMBER: builtins.int
    FIELD_PATH_FIELD_NUMBER: builtins.int
    ORDER_FIELD_NUMBER: builtins.int
    array_config: builtins.str
    field_path: builtins.str
    order: builtins.str
    def __init__(
        self,
        *,
        array_config: builtins.str = ...,
        field_path: builtins.str = ...,
        order: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["array_config", b"array_config", "field_path", b"field_path", "order", b"order"]) -> None: ...

global___FirestoreIndexXFields = FirestoreIndexXFields

@typing_extensions.final
class FirestoreIndexXTimeouts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATE_FIELD_NUMBER: builtins.int
    DELETE_FIELD_NUMBER: builtins.int
    create: builtins.str
    delete: builtins.str
    def __init__(
        self,
        *,
        create: builtins.str = ...,
        delete: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["create", b"create", "delete", b"delete"]) -> None: ...

global___FirestoreIndexXTimeouts = FirestoreIndexXTimeouts

@typing_extensions.final
class FirestoreIndex(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COLLECTION_FIELD_NUMBER: builtins.int
    DATABASE_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    QUERY_SCOPE_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    collection: builtins.str
    database: builtins.str
    id: builtins.str
    name: builtins.str
    project: builtins.str
    query_scope: builtins.str
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___FirestoreIndexXFields]: ...
    @property
    def timeouts(self) -> global___FirestoreIndexXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        collection: builtins.str = ...,
        database: builtins.str = ...,
        id: builtins.str = ...,
        name: builtins.str = ...,
        project: builtins.str = ...,
        query_scope: builtins.str = ...,
        fields: collections.abc.Iterable[global___FirestoreIndexXFields] | None = ...,
        timeouts: global___FirestoreIndexXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["collection", b"collection", "database", b"database", "fields", b"fields", "id", b"id", "name", b"name", "project", b"project", "query_scope", b"query_scope", "resource_info", b"resource_info", "timeouts", b"timeouts"]) -> None: ...

global___FirestoreIndex = FirestoreIndex
