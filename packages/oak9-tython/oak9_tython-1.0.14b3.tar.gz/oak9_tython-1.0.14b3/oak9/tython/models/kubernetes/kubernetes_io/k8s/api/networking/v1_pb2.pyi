"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import kubernetes.kubernetes_io.k8s.api.core.v1_pb2
import kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2
import kubernetes.kubernetes_io.k8s.apimachinery.pkg.util.intstr_pb2
import shared.shared_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class HTTPIngressPath(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BACKEND_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    PATH_TYPE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def backend(self) -> global___IngressBackend: ...
    path: builtins.str
    path_type: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        backend: global___IngressBackend | None = ...,
        path: builtins.str = ...,
        path_type: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["backend", b"backend", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["backend", b"backend", "path", b"path", "path_type", b"path_type", "resource_info", b"resource_info"]) -> None: ...

global___HTTPIngressPath = HTTPIngressPath

@typing_extensions.final
class HTTPIngressRuleValue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PATHS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def paths(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HTTPIngressPath]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        paths: collections.abc.Iterable[global___HTTPIngressPath] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["paths", b"paths", "resource_info", b"resource_info"]) -> None: ...

global___HTTPIngressRuleValue = HTTPIngressRuleValue

@typing_extensions.final
class IPBlock(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CIDR_FIELD_NUMBER: builtins.int
    EXCEPT_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    cidr: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        cidr: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cidr", b"cidr", "except", b"except", "resource_info", b"resource_info"]) -> None: ...

global___IPBlock = IPBlock

@typing_extensions.final
class Ingress(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SPEC_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta: ...
    @property
    def spec(self) -> global___IngressSpec: ...
    @property
    def status(self) -> global___IngressStatus: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta | None = ...,
        spec: global___IngressSpec | None = ...,
        status: global___IngressStatus | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec", "status", b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec", "status", b"status"]) -> None: ...

global___Ingress = Ingress

@typing_extensions.final
class IngressBackend(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_FIELD_NUMBER: builtins.int
    SERVICE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> kubernetes.kubernetes_io.k8s.api.core.v1_pb2.TypedLocalObjectReference: ...
    @property
    def service(self) -> global___IngressServiceBackend: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        resource: kubernetes.kubernetes_io.k8s.api.core.v1_pb2.TypedLocalObjectReference | None = ...,
        service: global___IngressServiceBackend | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource", b"resource", "resource_info", b"resource_info", "service", b"service"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource", b"resource", "resource_info", b"resource_info", "service", b"service"]) -> None: ...

global___IngressBackend = IngressBackend

@typing_extensions.final
class IngressClass(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SPEC_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta: ...
    @property
    def spec(self) -> global___IngressClassSpec: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta | None = ...,
        spec: global___IngressClassSpec | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec"]) -> None: ...

global___IngressClass = IngressClass

@typing_extensions.final
class IngressClassList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    ITEMS_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    @property
    def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___IngressClass]: ...
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        items: collections.abc.Iterable[global___IngressClass] | None = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "items", b"items", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info"]) -> None: ...

global___IngressClassList = IngressClassList

@typing_extensions.final
class IngressClassParametersReference(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_GROUP_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    SCOPE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_group: builtins.str
    kind: builtins.str
    name: builtins.str
    namespace: builtins.str
    scope: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_group: builtins.str = ...,
        kind: builtins.str = ...,
        name: builtins.str = ...,
        namespace: builtins.str = ...,
        scope: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_group", b"api_group", "kind", b"kind", "name", b"name", "namespace", b"namespace", "resource_info", b"resource_info", "scope", b"scope"]) -> None: ...

global___IngressClassParametersReference = IngressClassParametersReference

@typing_extensions.final
class IngressClassSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTROLLER_FIELD_NUMBER: builtins.int
    PARAMETERS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    controller: builtins.str
    @property
    def parameters(self) -> global___IngressClassParametersReference: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        controller: builtins.str = ...,
        parameters: global___IngressClassParametersReference | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["parameters", b"parameters", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["controller", b"controller", "parameters", b"parameters", "resource_info", b"resource_info"]) -> None: ...

global___IngressClassSpec = IngressClassSpec

@typing_extensions.final
class IngressList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    ITEMS_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    @property
    def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Ingress]: ...
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        items: collections.abc.Iterable[global___Ingress] | None = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "items", b"items", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info"]) -> None: ...

global___IngressList = IngressList

@typing_extensions.final
class IngressLoadBalancerIngress(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HOSTNAME_FIELD_NUMBER: builtins.int
    IP_FIELD_NUMBER: builtins.int
    PORTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    hostname: builtins.str
    ip: builtins.str
    @property
    def ports(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___IngressPortStatus]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        hostname: builtins.str = ...,
        ip: builtins.str = ...,
        ports: collections.abc.Iterable[global___IngressPortStatus] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["hostname", b"hostname", "ip", b"ip", "ports", b"ports", "resource_info", b"resource_info"]) -> None: ...

global___IngressLoadBalancerIngress = IngressLoadBalancerIngress

@typing_extensions.final
class IngressLoadBalancerStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INGRESS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def ingress(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___IngressLoadBalancerIngress]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        ingress: collections.abc.Iterable[global___IngressLoadBalancerIngress] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ingress", b"ingress", "resource_info", b"resource_info"]) -> None: ...

global___IngressLoadBalancerStatus = IngressLoadBalancerStatus

@typing_extensions.final
class IngressPortStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ERROR_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    PROTOCOL_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    error: builtins.str
    port: builtins.int
    protocol: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        error: builtins.str = ...,
        port: builtins.int = ...,
        protocol: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["error", b"error", "port", b"port", "protocol", b"protocol", "resource_info", b"resource_info"]) -> None: ...

global___IngressPortStatus = IngressPortStatus

@typing_extensions.final
class IngressRule(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HOST_FIELD_NUMBER: builtins.int
    HTTP_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    host: builtins.str
    @property
    def http(self) -> global___HTTPIngressRuleValue: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        host: builtins.str = ...,
        http: global___HTTPIngressRuleValue | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["http", b"http", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["host", b"host", "http", b"http", "resource_info", b"resource_info"]) -> None: ...

global___IngressRule = IngressRule

@typing_extensions.final
class IngressServiceBackend(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def port(self) -> global___ServiceBackendPort: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        port: global___ServiceBackendPort | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["port", b"port", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "port", b"port", "resource_info", b"resource_info"]) -> None: ...

global___IngressServiceBackend = IngressServiceBackend

@typing_extensions.final
class IngressSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEFAULT_BACKEND_FIELD_NUMBER: builtins.int
    INGRESS_CLASS_NAME_FIELD_NUMBER: builtins.int
    RULES_FIELD_NUMBER: builtins.int
    TLS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def default_backend(self) -> global___IngressBackend: ...
    ingress_class_name: builtins.str
    @property
    def rules(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___IngressRule]: ...
    @property
    def tls(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___IngressTLS]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        default_backend: global___IngressBackend | None = ...,
        ingress_class_name: builtins.str = ...,
        rules: collections.abc.Iterable[global___IngressRule] | None = ...,
        tls: collections.abc.Iterable[global___IngressTLS] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["default_backend", b"default_backend", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["default_backend", b"default_backend", "ingress_class_name", b"ingress_class_name", "resource_info", b"resource_info", "rules", b"rules", "tls", b"tls"]) -> None: ...

global___IngressSpec = IngressSpec

@typing_extensions.final
class IngressStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOAD_BALANCER_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def load_balancer(self) -> global___IngressLoadBalancerStatus: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        load_balancer: global___IngressLoadBalancerStatus | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["load_balancer", b"load_balancer", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["load_balancer", b"load_balancer", "resource_info", b"resource_info"]) -> None: ...

global___IngressStatus = IngressStatus

@typing_extensions.final
class IngressTLS(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HOSTS_FIELD_NUMBER: builtins.int
    SECRET_NAME_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def hosts(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    secret_name: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        hosts: collections.abc.Iterable[builtins.str] | None = ...,
        secret_name: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["hosts", b"hosts", "resource_info", b"resource_info", "secret_name", b"secret_name"]) -> None: ...

global___IngressTLS = IngressTLS

@typing_extensions.final
class NetworkPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SPEC_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta: ...
    @property
    def spec(self) -> global___NetworkPolicySpec: ...
    @property
    def status(self) -> global___NetworkPolicyStatus: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta | None = ...,
        spec: global___NetworkPolicySpec | None = ...,
        status: global___NetworkPolicyStatus | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec", "status", b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec", "status", b"status"]) -> None: ...

global___NetworkPolicy = NetworkPolicy

@typing_extensions.final
class NetworkPolicyEgressRule(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PORTS_FIELD_NUMBER: builtins.int
    TO_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def ports(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___NetworkPolicyPort]: ...
    @property
    def to(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___NetworkPolicyPeer]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        ports: collections.abc.Iterable[global___NetworkPolicyPort] | None = ...,
        to: collections.abc.Iterable[global___NetworkPolicyPeer] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ports", b"ports", "resource_info", b"resource_info", "to", b"to"]) -> None: ...

global___NetworkPolicyEgressRule = NetworkPolicyEgressRule

@typing_extensions.final
class NetworkPolicyIngressRule(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FROM_FIELD_NUMBER: builtins.int
    PORTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def ports(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___NetworkPolicyPort]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        ports: collections.abc.Iterable[global___NetworkPolicyPort] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["from", b"from", "ports", b"ports", "resource_info", b"resource_info"]) -> None: ...

global___NetworkPolicyIngressRule = NetworkPolicyIngressRule

@typing_extensions.final
class NetworkPolicyList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    ITEMS_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    @property
    def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___NetworkPolicy]: ...
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        items: collections.abc.Iterable[global___NetworkPolicy] | None = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "items", b"items", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info"]) -> None: ...

global___NetworkPolicyList = NetworkPolicyList

@typing_extensions.final
class NetworkPolicyPeer(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IP_BLOCK_FIELD_NUMBER: builtins.int
    NAMESPACE_SELECTOR_FIELD_NUMBER: builtins.int
    POD_SELECTOR_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def ip_block(self) -> global___IPBlock: ...
    @property
    def namespace_selector(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector: ...
    @property
    def pod_selector(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        ip_block: global___IPBlock | None = ...,
        namespace_selector: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector | None = ...,
        pod_selector: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ip_block", b"ip_block", "namespace_selector", b"namespace_selector", "pod_selector", b"pod_selector", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ip_block", b"ip_block", "namespace_selector", b"namespace_selector", "pod_selector", b"pod_selector", "resource_info", b"resource_info"]) -> None: ...

global___NetworkPolicyPeer = NetworkPolicyPeer

@typing_extensions.final
class NetworkPolicyPort(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    END_PORT_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    PROTOCOL_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    end_port: builtins.int
    @property
    def port(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.util.intstr_pb2.IntOrString: ...
    protocol: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        end_port: builtins.int = ...,
        port: kubernetes.kubernetes_io.k8s.apimachinery.pkg.util.intstr_pb2.IntOrString | None = ...,
        protocol: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["port", b"port", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["end_port", b"end_port", "port", b"port", "protocol", b"protocol", "resource_info", b"resource_info"]) -> None: ...

global___NetworkPolicyPort = NetworkPolicyPort

@typing_extensions.final
class NetworkPolicySpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EGRESS_FIELD_NUMBER: builtins.int
    INGRESS_FIELD_NUMBER: builtins.int
    POD_SELECTOR_FIELD_NUMBER: builtins.int
    POLICY_TYPES_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def egress(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___NetworkPolicyEgressRule]: ...
    @property
    def ingress(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___NetworkPolicyIngressRule]: ...
    @property
    def pod_selector(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector: ...
    @property
    def policy_types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        egress: collections.abc.Iterable[global___NetworkPolicyEgressRule] | None = ...,
        ingress: collections.abc.Iterable[global___NetworkPolicyIngressRule] | None = ...,
        pod_selector: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector | None = ...,
        policy_types: collections.abc.Iterable[builtins.str] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pod_selector", b"pod_selector", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["egress", b"egress", "ingress", b"ingress", "pod_selector", b"pod_selector", "policy_types", b"policy_types", "resource_info", b"resource_info"]) -> None: ...

global___NetworkPolicySpec = NetworkPolicySpec

@typing_extensions.final
class NetworkPolicyStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONDITIONS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def conditions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.Condition]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        conditions: collections.abc.Iterable[kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.Condition] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["conditions", b"conditions", "resource_info", b"resource_info"]) -> None: ...

global___NetworkPolicyStatus = NetworkPolicyStatus

@typing_extensions.final
class ServiceBackendPort(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    NUMBER_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    name: builtins.str
    number: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        number: builtins.int = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "number", b"number", "resource_info", b"resource_info"]) -> None: ...

global___ServiceBackendPort = ServiceBackendPort
