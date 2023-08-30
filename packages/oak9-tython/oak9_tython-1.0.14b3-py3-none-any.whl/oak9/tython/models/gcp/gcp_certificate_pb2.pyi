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
class CertificateManagerCertificateXManaged(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DNS_AUTHORIZATIONS_FIELD_NUMBER: builtins.int
    DOMAINS_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    @property
    def dns_authorizations(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def domains(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    state: builtins.str
    def __init__(
        self,
        *,
        dns_authorizations: collections.abc.Iterable[builtins.str] | None = ...,
        domains: collections.abc.Iterable[builtins.str] | None = ...,
        state: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["dns_authorizations", b"dns_authorizations", "domains", b"domains", "state", b"state"]) -> None: ...

global___CertificateManagerCertificateXManaged = CertificateManagerCertificateXManaged

@typing_extensions.final
class CertificateManagerCertificateXSelfManaged(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CERTIFICATE_PEM_FIELD_NUMBER: builtins.int
    PRIVATE_KEY_PEM_FIELD_NUMBER: builtins.int
    certificate_pem: builtins.str
    private_key_pem: builtins.str
    def __init__(
        self,
        *,
        certificate_pem: builtins.str = ...,
        private_key_pem: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["certificate_pem", b"certificate_pem", "private_key_pem", b"private_key_pem"]) -> None: ...

global___CertificateManagerCertificateXSelfManaged = CertificateManagerCertificateXSelfManaged

@typing_extensions.final
class CertificateManagerCertificateXTimeouts(google.protobuf.message.Message):
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

global___CertificateManagerCertificateXTimeouts = CertificateManagerCertificateXTimeouts

@typing_extensions.final
class CertificateManagerCertificate(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class LabelsEntry(google.protobuf.message.Message):
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

    DESCRIPTION_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    SCOPE_FIELD_NUMBER: builtins.int
    MANAGED_FIELD_NUMBER: builtins.int
    SELF_MANAGED_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    description: builtins.str
    id: builtins.str
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    name: builtins.str
    project: builtins.str
    scope: builtins.str
    @property
    def managed(self) -> global___CertificateManagerCertificateXManaged: ...
    @property
    def self_managed(self) -> global___CertificateManagerCertificateXSelfManaged: ...
    @property
    def timeouts(self) -> global___CertificateManagerCertificateXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        description: builtins.str = ...,
        id: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        name: builtins.str = ...,
        project: builtins.str = ...,
        scope: builtins.str = ...,
        managed: global___CertificateManagerCertificateXManaged | None = ...,
        self_managed: global___CertificateManagerCertificateXSelfManaged | None = ...,
        timeouts: global___CertificateManagerCertificateXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["managed", b"managed", "resource_info", b"resource_info", "self_managed", b"self_managed", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "id", b"id", "labels", b"labels", "managed", b"managed", "name", b"name", "project", b"project", "resource_info", b"resource_info", "scope", b"scope", "self_managed", b"self_managed", "timeouts", b"timeouts"]) -> None: ...

global___CertificateManagerCertificate = CertificateManagerCertificate

@typing_extensions.final
class CertificateManagerCertificateMapXTimeouts(google.protobuf.message.Message):
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

global___CertificateManagerCertificateMapXTimeouts = CertificateManagerCertificateMapXTimeouts

@typing_extensions.final
class CertificateManagerCertificateMap(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class GclbTargetsEntry(google.protobuf.message.Message):
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

    @typing_extensions.final
    class LabelsEntry(google.protobuf.message.Message):
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

    CREATE_TIME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    GCLB_TARGETS_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    UPDATE_TIME_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    create_time: builtins.str
    description: builtins.str
    @property
    def gclb_targets(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    id: builtins.str
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    name: builtins.str
    project: builtins.str
    update_time: builtins.str
    @property
    def timeouts(self) -> global___CertificateManagerCertificateMapXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        create_time: builtins.str = ...,
        description: builtins.str = ...,
        gclb_targets: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        id: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        name: builtins.str = ...,
        project: builtins.str = ...,
        update_time: builtins.str = ...,
        timeouts: global___CertificateManagerCertificateMapXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["create_time", b"create_time", "description", b"description", "gclb_targets", b"gclb_targets", "id", b"id", "labels", b"labels", "name", b"name", "project", b"project", "resource_info", b"resource_info", "timeouts", b"timeouts", "update_time", b"update_time"]) -> None: ...

global___CertificateManagerCertificateMap = CertificateManagerCertificateMap

@typing_extensions.final
class CertificateManagerCertificateMapEntryXTimeouts(google.protobuf.message.Message):
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

global___CertificateManagerCertificateMapEntryXTimeouts = CertificateManagerCertificateMapEntryXTimeouts

@typing_extensions.final
class CertificateManagerCertificateMapEntry(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class LabelsEntry(google.protobuf.message.Message):
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

    CERTIFICATES_FIELD_NUMBER: builtins.int
    CREATE_TIME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    HOSTNAME_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    MAP_FIELD_NUMBER: builtins.int
    MATCHER_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    UPDATE_TIME_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def certificates(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    create_time: builtins.str
    description: builtins.str
    hostname: builtins.str
    id: builtins.str
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    map: builtins.str
    matcher: builtins.str
    name: builtins.str
    project: builtins.str
    state: builtins.str
    update_time: builtins.str
    @property
    def timeouts(self) -> global___CertificateManagerCertificateMapEntryXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        certificates: collections.abc.Iterable[builtins.str] | None = ...,
        create_time: builtins.str = ...,
        description: builtins.str = ...,
        hostname: builtins.str = ...,
        id: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        map: builtins.str = ...,
        matcher: builtins.str = ...,
        name: builtins.str = ...,
        project: builtins.str = ...,
        state: builtins.str = ...,
        update_time: builtins.str = ...,
        timeouts: global___CertificateManagerCertificateMapEntryXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["certificates", b"certificates", "create_time", b"create_time", "description", b"description", "hostname", b"hostname", "id", b"id", "labels", b"labels", "map", b"map", "matcher", b"matcher", "name", b"name", "project", b"project", "resource_info", b"resource_info", "state", b"state", "timeouts", b"timeouts", "update_time", b"update_time"]) -> None: ...

global___CertificateManagerCertificateMapEntry = CertificateManagerCertificateMapEntry

@typing_extensions.final
class CertificateManagerDnsAuthorizationXTimeouts(google.protobuf.message.Message):
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

global___CertificateManagerDnsAuthorizationXTimeouts = CertificateManagerDnsAuthorizationXTimeouts

@typing_extensions.final
class CertificateManagerDnsAuthorization(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class DnsResourceRecordEntry(google.protobuf.message.Message):
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

    @typing_extensions.final
    class LabelsEntry(google.protobuf.message.Message):
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

    DESCRIPTION_FIELD_NUMBER: builtins.int
    DNS_RESOURCE_RECORD_FIELD_NUMBER: builtins.int
    DOMAIN_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    description: builtins.str
    @property
    def dns_resource_record(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    domain: builtins.str
    id: builtins.str
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    name: builtins.str
    project: builtins.str
    @property
    def timeouts(self) -> global___CertificateManagerDnsAuthorizationXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        description: builtins.str = ...,
        dns_resource_record: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        domain: builtins.str = ...,
        id: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        name: builtins.str = ...,
        project: builtins.str = ...,
        timeouts: global___CertificateManagerDnsAuthorizationXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "dns_resource_record", b"dns_resource_record", "domain", b"domain", "id", b"id", "labels", b"labels", "name", b"name", "project", b"project", "resource_info", b"resource_info", "timeouts", b"timeouts"]) -> None: ...

global___CertificateManagerDnsAuthorization = CertificateManagerDnsAuthorization
