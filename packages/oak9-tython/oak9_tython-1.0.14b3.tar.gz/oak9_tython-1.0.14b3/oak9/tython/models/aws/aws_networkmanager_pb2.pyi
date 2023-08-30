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
class CustomerGatewayAssociation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    GLOBAL_NETWORK_ID_FIELD_NUMBER: builtins.int
    CUSTOMER_GATEWAY_ARN_FIELD_NUMBER: builtins.int
    DEVICE_ID_FIELD_NUMBER: builtins.int
    LINK_ID_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    global_network_id: builtins.str
    customer_gateway_arn: builtins.str
    device_id: builtins.str
    link_id: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        global_network_id: builtins.str = ...,
        customer_gateway_arn: builtins.str = ...,
        device_id: builtins.str = ...,
        link_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["customer_gateway_arn", b"customer_gateway_arn", "device_id", b"device_id", "global_network_id", b"global_network_id", "link_id", b"link_id", "resource_info", b"resource_info"]) -> None: ...

global___CustomerGatewayAssociation = CustomerGatewayAssociation

@typing_extensions.final
class NetworkManager(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CUSTOMER_GATEWAY_ASSOCIATION_FIELD_NUMBER: builtins.int
    DEVICE_FIELD_NUMBER: builtins.int
    GLOBAL_NETWORK_FIELD_NUMBER: builtins.int
    LINK_FIELD_NUMBER: builtins.int
    LINK_ASSOCIATION_FIELD_NUMBER: builtins.int
    SITE_FIELD_NUMBER: builtins.int
    TRANSIT_GATEWAY_REGISTRATION_FIELD_NUMBER: builtins.int
    @property
    def customer_gateway_association(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CustomerGatewayAssociation]: ...
    @property
    def device(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Device]: ...
    @property
    def global_network(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GlobalNetwork]: ...
    @property
    def link(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Link]: ...
    @property
    def link_association(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___LinkAssociation]: ...
    @property
    def site(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Site]: ...
    @property
    def transit_gateway_registration(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___TransitGatewayRegistration]: ...
    def __init__(
        self,
        *,
        customer_gateway_association: collections.abc.Iterable[global___CustomerGatewayAssociation] | None = ...,
        device: collections.abc.Iterable[global___Device] | None = ...,
        global_network: collections.abc.Iterable[global___GlobalNetwork] | None = ...,
        link: collections.abc.Iterable[global___Link] | None = ...,
        link_association: collections.abc.Iterable[global___LinkAssociation] | None = ...,
        site: collections.abc.Iterable[global___Site] | None = ...,
        transit_gateway_registration: collections.abc.Iterable[global___TransitGatewayRegistration] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["customer_gateway_association", b"customer_gateway_association", "device", b"device", "global_network", b"global_network", "link", b"link", "link_association", b"link_association", "site", b"site", "transit_gateway_registration", b"transit_gateway_registration"]) -> None: ...

global___NetworkManager = NetworkManager

@typing_extensions.final
class DeviceLocation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ADDRESS_FIELD_NUMBER: builtins.int
    LATITUDE_FIELD_NUMBER: builtins.int
    LONGITUDE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    address: builtins.str
    latitude: builtins.str
    longitude: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        address: builtins.str = ...,
        latitude: builtins.str = ...,
        longitude: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "latitude", b"latitude", "longitude", b"longitude", "resource_info", b"resource_info"]) -> None: ...

global___DeviceLocation = DeviceLocation

@typing_extensions.final
class Device(google.protobuf.message.Message):
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
    DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    GLOBAL_NETWORK_ID_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    MODEL_FIELD_NUMBER: builtins.int
    SERIAL_NUMBER_FIELD_NUMBER: builtins.int
    SITE_ID_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    VENDOR_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    global_network_id: builtins.str
    @property
    def location(self) -> global___DeviceLocation: ...
    model: builtins.str
    serial_number: builtins.str
    site_id: builtins.str
    type: builtins.str
    vendor: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        global_network_id: builtins.str = ...,
        location: global___DeviceLocation | None = ...,
        model: builtins.str = ...,
        serial_number: builtins.str = ...,
        site_id: builtins.str = ...,
        type: builtins.str = ...,
        vendor: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["location", b"location", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "global_network_id", b"global_network_id", "location", b"location", "model", b"model", "resource_info", b"resource_info", "serial_number", b"serial_number", "site_id", b"site_id", "tags", b"tags", "type", b"type", "vendor", b"vendor"]) -> None: ...

global___Device = Device

@typing_extensions.final
class GlobalNetwork(google.protobuf.message.Message):
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
    DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "resource_info", b"resource_info", "tags", b"tags"]) -> None: ...

global___GlobalNetwork = GlobalNetwork

@typing_extensions.final
class LinkBandwidth(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    DOWNLOAD_SPEED_FIELD_NUMBER: builtins.int
    UPLOAD_SPEED_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    download_speed: builtins.int
    upload_speed: builtins.int
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        download_speed: builtins.int = ...,
        upload_speed: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["download_speed", b"download_speed", "resource_info", b"resource_info", "upload_speed", b"upload_speed"]) -> None: ...

global___LinkBandwidth = LinkBandwidth

@typing_extensions.final
class Link(google.protobuf.message.Message):
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
    GLOBAL_NETWORK_ID_FIELD_NUMBER: builtins.int
    SITE_ID_FIELD_NUMBER: builtins.int
    BANDWIDTH_FIELD_NUMBER: builtins.int
    PROVIDER_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    global_network_id: builtins.str
    site_id: builtins.str
    @property
    def bandwidth(self) -> global___LinkBandwidth: ...
    provider: builtins.str
    description: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    type: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        global_network_id: builtins.str = ...,
        site_id: builtins.str = ...,
        bandwidth: global___LinkBandwidth | None = ...,
        provider: builtins.str = ...,
        description: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        type: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bandwidth", b"bandwidth", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bandwidth", b"bandwidth", "description", b"description", "global_network_id", b"global_network_id", "provider", b"provider", "resource_info", b"resource_info", "site_id", b"site_id", "tags", b"tags", "type", b"type"]) -> None: ...

global___Link = Link

@typing_extensions.final
class LinkAssociation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    GLOBAL_NETWORK_ID_FIELD_NUMBER: builtins.int
    DEVICE_ID_FIELD_NUMBER: builtins.int
    LINK_ID_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    global_network_id: builtins.str
    device_id: builtins.str
    link_id: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        global_network_id: builtins.str = ...,
        device_id: builtins.str = ...,
        link_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["device_id", b"device_id", "global_network_id", b"global_network_id", "link_id", b"link_id", "resource_info", b"resource_info"]) -> None: ...

global___LinkAssociation = LinkAssociation

@typing_extensions.final
class SiteLocation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ADDRESS_FIELD_NUMBER: builtins.int
    LATITUDE_FIELD_NUMBER: builtins.int
    LONGITUDE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    address: builtins.str
    latitude: builtins.str
    longitude: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        address: builtins.str = ...,
        latitude: builtins.str = ...,
        longitude: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "latitude", b"latitude", "longitude", b"longitude", "resource_info", b"resource_info"]) -> None: ...

global___SiteLocation = SiteLocation

@typing_extensions.final
class Site(google.protobuf.message.Message):
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
    DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    GLOBAL_NETWORK_ID_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    global_network_id: builtins.str
    @property
    def location(self) -> global___SiteLocation: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        global_network_id: builtins.str = ...,
        location: global___SiteLocation | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["location", b"location", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "global_network_id", b"global_network_id", "location", b"location", "resource_info", b"resource_info", "tags", b"tags"]) -> None: ...

global___Site = Site

@typing_extensions.final
class TransitGatewayRegistration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    GLOBAL_NETWORK_ID_FIELD_NUMBER: builtins.int
    TRANSIT_GATEWAY_ARN_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    global_network_id: builtins.str
    transit_gateway_arn: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        global_network_id: builtins.str = ...,
        transit_gateway_arn: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["global_network_id", b"global_network_id", "resource_info", b"resource_info", "transit_gateway_arn", b"transit_gateway_arn"]) -> None: ...

global___TransitGatewayRegistration = TransitGatewayRegistration
