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
class Microsoft_Kubernetes(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTED_CLUSTERS_FIELD_NUMBER: builtins.int
    @property
    def connected_clusters(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ConnectedClusters]: ...
    def __init__(
        self,
        *,
        connected_clusters: collections.abc.Iterable[global___ConnectedClusters] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["connected_clusters", b"connected_clusters"]) -> None: ...

global___Microsoft_Kubernetes = Microsoft_Kubernetes

@typing_extensions.final
class ConnectedClusters(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class TagsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    IDENTITY_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    AGENT_PUBLIC_KEY_CERTIFICATE_FIELD_NUMBER: builtins.int
    DISTRIBUTION_FIELD_NUMBER: builtins.int
    INFRASTRUCTURE_FIELD_NUMBER: builtins.int
    PROVISIONING_STATE_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def identity(self) -> global___ConnectedClusterIdentity: ...
    location: builtins.str
    name: builtins.str
    agent_public_key_certificate: builtins.str
    distribution: builtins.str
    infrastructure: builtins.str
    provisioning_state: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        identity: global___ConnectedClusterIdentity | None = ...,
        location: builtins.str = ...,
        name: builtins.str = ...,
        agent_public_key_certificate: builtins.str = ...,
        distribution: builtins.str = ...,
        infrastructure: builtins.str = ...,
        provisioning_state: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["identity", b"identity", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["agent_public_key_certificate", b"agent_public_key_certificate", "distribution", b"distribution", "identity", b"identity", "infrastructure", b"infrastructure", "location", b"location", "name", b"name", "provisioning_state", b"provisioning_state", "resource_info", b"resource_info", "tags", b"tags"]) -> None: ...

global___ConnectedClusters = ConnectedClusters

@typing_extensions.final
class ConnectedClusterIdentity(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TYPE_FIELD_NUMBER: builtins.int
    type: builtins.str
    def __init__(
        self,
        *,
        type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["type", b"type"]) -> None: ...

global___ConnectedClusterIdentity = ConnectedClusterIdentity
