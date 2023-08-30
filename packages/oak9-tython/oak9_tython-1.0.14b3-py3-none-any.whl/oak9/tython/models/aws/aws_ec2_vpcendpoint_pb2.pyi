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
class VPCEndpoint(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class PolicyDocumentEntry(google.protobuf.message.Message):
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
    POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    PRIVATE_DNS_ENABLED_FIELD_NUMBER: builtins.int
    ROUTE_TABLE_IDS_FIELD_NUMBER: builtins.int
    SECURITY_GROUP_IDS_FIELD_NUMBER: builtins.int
    SERVICE_NAME_FIELD_NUMBER: builtins.int
    SUBNET_IDS_FIELD_NUMBER: builtins.int
    VPC_ENDPOINT_TYPE_FIELD_NUMBER: builtins.int
    VPC_ID_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def policy_document(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    private_dns_enabled: builtins.bool
    @property
    def route_table_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def security_group_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    service_name: builtins.str
    @property
    def subnet_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    vpc_endpoint_type: builtins.str
    vpc_id: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        policy_document: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        private_dns_enabled: builtins.bool = ...,
        route_table_ids: collections.abc.Iterable[builtins.str] | None = ...,
        security_group_ids: collections.abc.Iterable[builtins.str] | None = ...,
        service_name: builtins.str = ...,
        subnet_ids: collections.abc.Iterable[builtins.str] | None = ...,
        vpc_endpoint_type: builtins.str = ...,
        vpc_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["policy_document", b"policy_document", "private_dns_enabled", b"private_dns_enabled", "resource_info", b"resource_info", "route_table_ids", b"route_table_ids", "security_group_ids", b"security_group_ids", "service_name", b"service_name", "subnet_ids", b"subnet_ids", "vpc_endpoint_type", b"vpc_endpoint_type", "vpc_id", b"vpc_id"]) -> None: ...

global___VPCEndpoint = VPCEndpoint

@typing_extensions.final
class EC2_VPCEndpoint(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VPC_ENDPOINT_FIELD_NUMBER: builtins.int
    VPC_ENDPOINT_SERVICE_FIELD_NUMBER: builtins.int
    VPC_ENDPOINT_SERVICE_PERMISSIONS_FIELD_NUMBER: builtins.int
    @property
    def vpc_endpoint(self) -> global___VPCEndpoint: ...
    @property
    def vpc_endpoint_service(self) -> global___VPCEndpointService: ...
    @property
    def vpc_endpoint_service_permissions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___VPCEndpointServicePermissions]: ...
    def __init__(
        self,
        *,
        vpc_endpoint: global___VPCEndpoint | None = ...,
        vpc_endpoint_service: global___VPCEndpointService | None = ...,
        vpc_endpoint_service_permissions: collections.abc.Iterable[global___VPCEndpointServicePermissions] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["vpc_endpoint", b"vpc_endpoint", "vpc_endpoint_service", b"vpc_endpoint_service"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["vpc_endpoint", b"vpc_endpoint", "vpc_endpoint_service", b"vpc_endpoint_service", "vpc_endpoint_service_permissions", b"vpc_endpoint_service_permissions"]) -> None: ...

global___EC2_VPCEndpoint = EC2_VPCEndpoint

@typing_extensions.final
class VPCEndpointService(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NETWORK_LOAD_BALANCER_ARNS_FIELD_NUMBER: builtins.int
    ACCEPTANCE_REQUIRED_FIELD_NUMBER: builtins.int
    APPLIANCE_LOAD_BALANCER_ARNS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def network_load_balancer_arns(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    acceptance_required: builtins.bool
    @property
    def appliance_load_balancer_arns(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        network_load_balancer_arns: collections.abc.Iterable[builtins.str] | None = ...,
        acceptance_required: builtins.bool = ...,
        appliance_load_balancer_arns: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["acceptance_required", b"acceptance_required", "appliance_load_balancer_arns", b"appliance_load_balancer_arns", "network_load_balancer_arns", b"network_load_balancer_arns", "resource_info", b"resource_info"]) -> None: ...

global___VPCEndpointService = VPCEndpointService

@typing_extensions.final
class VPCEndpointServicePermissions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ALLOWED_PRINCIPALS_FIELD_NUMBER: builtins.int
    SERVICE_ID_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def allowed_principals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    service_id: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        allowed_principals: collections.abc.Iterable[builtins.str] | None = ...,
        service_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["allowed_principals", b"allowed_principals", "resource_info", b"resource_info", "service_id", b"service_id"]) -> None: ...

global___VPCEndpointServicePermissions = VPCEndpointServicePermissions
