"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2
import kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2
import shared.shared_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ContainerResourceMetricSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTAINER_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    TARGET_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    container: builtins.str
    name: builtins.str
    @property
    def target(self) -> global___MetricTarget: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        container: builtins.str = ...,
        name: builtins.str = ...,
        target: global___MetricTarget | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "target", b"target"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["container", b"container", "name", b"name", "resource_info", b"resource_info", "target", b"target"]) -> None: ...

global___ContainerResourceMetricSource = ContainerResourceMetricSource

@typing_extensions.final
class ContainerResourceMetricStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTAINER_FIELD_NUMBER: builtins.int
    CURRENT_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    container: builtins.str
    @property
    def current(self) -> global___MetricValueStatus: ...
    name: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        container: builtins.str = ...,
        current: global___MetricValueStatus | None = ...,
        name: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current", b"current", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["container", b"container", "current", b"current", "name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___ContainerResourceMetricStatus = ContainerResourceMetricStatus

@typing_extensions.final
class CrossVersionObjectReference(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    kind: builtins.str
    name: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        kind: builtins.str = ...,
        name: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "kind", b"kind", "name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___CrossVersionObjectReference = CrossVersionObjectReference

@typing_extensions.final
class ExternalMetricSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    METRIC_FIELD_NUMBER: builtins.int
    TARGET_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def metric(self) -> global___MetricIdentifier: ...
    @property
    def target(self) -> global___MetricTarget: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        metric: global___MetricIdentifier | None = ...,
        target: global___MetricTarget | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metric", b"metric", "resource_info", b"resource_info", "target", b"target"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["metric", b"metric", "resource_info", b"resource_info", "target", b"target"]) -> None: ...

global___ExternalMetricSource = ExternalMetricSource

@typing_extensions.final
class ExternalMetricStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CURRENT_FIELD_NUMBER: builtins.int
    METRIC_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def current(self) -> global___MetricValueStatus: ...
    @property
    def metric(self) -> global___MetricIdentifier: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        current: global___MetricValueStatus | None = ...,
        metric: global___MetricIdentifier | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current", b"current", "metric", b"metric", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["current", b"current", "metric", b"metric", "resource_info", b"resource_info"]) -> None: ...

global___ExternalMetricStatus = ExternalMetricStatus

@typing_extensions.final
class HPAScalingPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PERIOD_SECONDS_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    period_seconds: builtins.int
    type: builtins.str
    value: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        period_seconds: builtins.int = ...,
        type: builtins.str = ...,
        value: builtins.int = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["period_seconds", b"period_seconds", "resource_info", b"resource_info", "type", b"type", "value", b"value"]) -> None: ...

global___HPAScalingPolicy = HPAScalingPolicy

@typing_extensions.final
class HPAScalingRules(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POLICIES_FIELD_NUMBER: builtins.int
    SELECT_POLICY_FIELD_NUMBER: builtins.int
    STABILIZATION_WINDOW_SECONDS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def policies(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HPAScalingPolicy]: ...
    select_policy: builtins.str
    stabilization_window_seconds: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        policies: collections.abc.Iterable[global___HPAScalingPolicy] | None = ...,
        select_policy: builtins.str = ...,
        stabilization_window_seconds: builtins.int = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["policies", b"policies", "resource_info", b"resource_info", "select_policy", b"select_policy", "stabilization_window_seconds", b"stabilization_window_seconds"]) -> None: ...

global___HPAScalingRules = HPAScalingRules

@typing_extensions.final
class HorizontalPodAutoscaler(google.protobuf.message.Message):
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
    def spec(self) -> global___HorizontalPodAutoscalerSpec: ...
    @property
    def status(self) -> global___HorizontalPodAutoscalerStatus: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ObjectMeta | None = ...,
        spec: global___HorizontalPodAutoscalerSpec | None = ...,
        status: global___HorizontalPodAutoscalerStatus | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec", "status", b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info", "spec", b"spec", "status", b"status"]) -> None: ...

global___HorizontalPodAutoscaler = HorizontalPodAutoscaler

@typing_extensions.final
class HorizontalPodAutoscalerBehavior(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SCALE_DOWN_FIELD_NUMBER: builtins.int
    SCALE_UP_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def scale_down(self) -> global___HPAScalingRules: ...
    @property
    def scale_up(self) -> global___HPAScalingRules: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        scale_down: global___HPAScalingRules | None = ...,
        scale_up: global___HPAScalingRules | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "scale_down", b"scale_down", "scale_up", b"scale_up"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "scale_down", b"scale_down", "scale_up", b"scale_up"]) -> None: ...

global___HorizontalPodAutoscalerBehavior = HorizontalPodAutoscalerBehavior

@typing_extensions.final
class HorizontalPodAutoscalerCondition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LAST_TRANSITION_TIME_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    REASON_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def last_transition_time(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.Time: ...
    message: builtins.str
    reason: builtins.str
    status: builtins.str
    type: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        last_transition_time: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.Time | None = ...,
        message: builtins.str = ...,
        reason: builtins.str = ...,
        status: builtins.str = ...,
        type: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["last_transition_time", b"last_transition_time", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["last_transition_time", b"last_transition_time", "message", b"message", "reason", b"reason", "resource_info", b"resource_info", "status", b"status", "type", b"type"]) -> None: ...

global___HorizontalPodAutoscalerCondition = HorizontalPodAutoscalerCondition

@typing_extensions.final
class HorizontalPodAutoscalerList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    API_VERSION_FIELD_NUMBER: builtins.int
    ITEMS_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    api_version: builtins.str
    @property
    def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HorizontalPodAutoscaler]: ...
    kind: builtins.str
    @property
    def metadata(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        api_version: builtins.str = ...,
        items: collections.abc.Iterable[global___HorizontalPodAutoscaler] | None = ...,
        kind: builtins.str = ...,
        metadata: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.ListMeta | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_version", b"api_version", "items", b"items", "kind", b"kind", "metadata", b"metadata", "resource_info", b"resource_info"]) -> None: ...

global___HorizontalPodAutoscalerList = HorizontalPodAutoscalerList

@typing_extensions.final
class HorizontalPodAutoscalerSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BEHAVIOR_FIELD_NUMBER: builtins.int
    MAX_REPLICAS_FIELD_NUMBER: builtins.int
    METRICS_FIELD_NUMBER: builtins.int
    MIN_REPLICAS_FIELD_NUMBER: builtins.int
    SCALE_TARGET_REF_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def behavior(self) -> global___HorizontalPodAutoscalerBehavior: ...
    max_replicas: builtins.int
    @property
    def metrics(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MetricSpec]: ...
    min_replicas: builtins.int
    @property
    def scale_target_ref(self) -> global___CrossVersionObjectReference: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        behavior: global___HorizontalPodAutoscalerBehavior | None = ...,
        max_replicas: builtins.int = ...,
        metrics: collections.abc.Iterable[global___MetricSpec] | None = ...,
        min_replicas: builtins.int = ...,
        scale_target_ref: global___CrossVersionObjectReference | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["behavior", b"behavior", "resource_info", b"resource_info", "scale_target_ref", b"scale_target_ref"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["behavior", b"behavior", "max_replicas", b"max_replicas", "metrics", b"metrics", "min_replicas", b"min_replicas", "resource_info", b"resource_info", "scale_target_ref", b"scale_target_ref"]) -> None: ...

global___HorizontalPodAutoscalerSpec = HorizontalPodAutoscalerSpec

@typing_extensions.final
class HorizontalPodAutoscalerStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONDITIONS_FIELD_NUMBER: builtins.int
    CURRENT_METRICS_FIELD_NUMBER: builtins.int
    CURRENT_REPLICAS_FIELD_NUMBER: builtins.int
    DESIRED_REPLICAS_FIELD_NUMBER: builtins.int
    LAST_SCALE_TIME_FIELD_NUMBER: builtins.int
    OBSERVED_GENERATION_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def conditions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HorizontalPodAutoscalerCondition]: ...
    @property
    def current_metrics(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MetricStatus]: ...
    current_replicas: builtins.int
    desired_replicas: builtins.int
    @property
    def last_scale_time(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.Time: ...
    observed_generation: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        conditions: collections.abc.Iterable[global___HorizontalPodAutoscalerCondition] | None = ...,
        current_metrics: collections.abc.Iterable[global___MetricStatus] | None = ...,
        current_replicas: builtins.int = ...,
        desired_replicas: builtins.int = ...,
        last_scale_time: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.Time | None = ...,
        observed_generation: builtins.int = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["last_scale_time", b"last_scale_time", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["conditions", b"conditions", "current_metrics", b"current_metrics", "current_replicas", b"current_replicas", "desired_replicas", b"desired_replicas", "last_scale_time", b"last_scale_time", "observed_generation", b"observed_generation", "resource_info", b"resource_info"]) -> None: ...

global___HorizontalPodAutoscalerStatus = HorizontalPodAutoscalerStatus

@typing_extensions.final
class MetricIdentifier(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    SELECTOR_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def selector(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        selector: kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1_pb2.LabelSelector | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "selector", b"selector"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info", "selector", b"selector"]) -> None: ...

global___MetricIdentifier = MetricIdentifier

@typing_extensions.final
class MetricSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTAINER_RESOURCE_FIELD_NUMBER: builtins.int
    EXTERNAL_FIELD_NUMBER: builtins.int
    OBJECT_FIELD_NUMBER: builtins.int
    PODS_FIELD_NUMBER: builtins.int
    RESOURCE_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def container_resource(self) -> global___ContainerResourceMetricSource: ...
    @property
    def external(self) -> global___ExternalMetricSource: ...
    @property
    def object(self) -> global___ObjectMetricSource: ...
    @property
    def pods(self) -> global___PodsMetricSource: ...
    @property
    def resource(self) -> global___ResourceMetricSource: ...
    type: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        container_resource: global___ContainerResourceMetricSource | None = ...,
        external: global___ExternalMetricSource | None = ...,
        object: global___ObjectMetricSource | None = ...,
        pods: global___PodsMetricSource | None = ...,
        resource: global___ResourceMetricSource | None = ...,
        type: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["container_resource", b"container_resource", "external", b"external", "object", b"object", "pods", b"pods", "resource", b"resource", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["container_resource", b"container_resource", "external", b"external", "object", b"object", "pods", b"pods", "resource", b"resource", "resource_info", b"resource_info", "type", b"type"]) -> None: ...

global___MetricSpec = MetricSpec

@typing_extensions.final
class MetricStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTAINER_RESOURCE_FIELD_NUMBER: builtins.int
    EXTERNAL_FIELD_NUMBER: builtins.int
    OBJECT_FIELD_NUMBER: builtins.int
    PODS_FIELD_NUMBER: builtins.int
    RESOURCE_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def container_resource(self) -> global___ContainerResourceMetricStatus: ...
    @property
    def external(self) -> global___ExternalMetricStatus: ...
    @property
    def object(self) -> global___ObjectMetricStatus: ...
    @property
    def pods(self) -> global___PodsMetricStatus: ...
    @property
    def resource(self) -> global___ResourceMetricStatus: ...
    type: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        container_resource: global___ContainerResourceMetricStatus | None = ...,
        external: global___ExternalMetricStatus | None = ...,
        object: global___ObjectMetricStatus | None = ...,
        pods: global___PodsMetricStatus | None = ...,
        resource: global___ResourceMetricStatus | None = ...,
        type: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["container_resource", b"container_resource", "external", b"external", "object", b"object", "pods", b"pods", "resource", b"resource", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["container_resource", b"container_resource", "external", b"external", "object", b"object", "pods", b"pods", "resource", b"resource", "resource_info", b"resource_info", "type", b"type"]) -> None: ...

global___MetricStatus = MetricStatus

@typing_extensions.final
class MetricTarget(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AVERAGE_UTILIZATION_FIELD_NUMBER: builtins.int
    AVERAGE_VALUE_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    average_utilization: builtins.int
    @property
    def average_value(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity: ...
    type: builtins.str
    @property
    def value(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        average_utilization: builtins.int = ...,
        average_value: kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity | None = ...,
        type: builtins.str = ...,
        value: kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["average_value", b"average_value", "resource_info", b"resource_info", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["average_utilization", b"average_utilization", "average_value", b"average_value", "resource_info", b"resource_info", "type", b"type", "value", b"value"]) -> None: ...

global___MetricTarget = MetricTarget

@typing_extensions.final
class MetricValueStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AVERAGE_UTILIZATION_FIELD_NUMBER: builtins.int
    AVERAGE_VALUE_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    average_utilization: builtins.int
    @property
    def average_value(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity: ...
    @property
    def value(self) -> kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        average_utilization: builtins.int = ...,
        average_value: kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity | None = ...,
        value: kubernetes.kubernetes_io.k8s.apimachinery.pkg.api.resource_pb2.Quantity | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["average_value", b"average_value", "resource_info", b"resource_info", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["average_utilization", b"average_utilization", "average_value", b"average_value", "resource_info", b"resource_info", "value", b"value"]) -> None: ...

global___MetricValueStatus = MetricValueStatus

@typing_extensions.final
class ObjectMetricSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DESCRIBED_OBJECT_FIELD_NUMBER: builtins.int
    METRIC_FIELD_NUMBER: builtins.int
    TARGET_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def described_object(self) -> global___CrossVersionObjectReference: ...
    @property
    def metric(self) -> global___MetricIdentifier: ...
    @property
    def target(self) -> global___MetricTarget: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        described_object: global___CrossVersionObjectReference | None = ...,
        metric: global___MetricIdentifier | None = ...,
        target: global___MetricTarget | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["described_object", b"described_object", "metric", b"metric", "resource_info", b"resource_info", "target", b"target"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["described_object", b"described_object", "metric", b"metric", "resource_info", b"resource_info", "target", b"target"]) -> None: ...

global___ObjectMetricSource = ObjectMetricSource

@typing_extensions.final
class ObjectMetricStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CURRENT_FIELD_NUMBER: builtins.int
    DESCRIBED_OBJECT_FIELD_NUMBER: builtins.int
    METRIC_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def current(self) -> global___MetricValueStatus: ...
    @property
    def described_object(self) -> global___CrossVersionObjectReference: ...
    @property
    def metric(self) -> global___MetricIdentifier: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        current: global___MetricValueStatus | None = ...,
        described_object: global___CrossVersionObjectReference | None = ...,
        metric: global___MetricIdentifier | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current", b"current", "described_object", b"described_object", "metric", b"metric", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["current", b"current", "described_object", b"described_object", "metric", b"metric", "resource_info", b"resource_info"]) -> None: ...

global___ObjectMetricStatus = ObjectMetricStatus

@typing_extensions.final
class PodsMetricSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    METRIC_FIELD_NUMBER: builtins.int
    TARGET_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def metric(self) -> global___MetricIdentifier: ...
    @property
    def target(self) -> global___MetricTarget: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        metric: global___MetricIdentifier | None = ...,
        target: global___MetricTarget | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metric", b"metric", "resource_info", b"resource_info", "target", b"target"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["metric", b"metric", "resource_info", b"resource_info", "target", b"target"]) -> None: ...

global___PodsMetricSource = PodsMetricSource

@typing_extensions.final
class PodsMetricStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CURRENT_FIELD_NUMBER: builtins.int
    METRIC_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def current(self) -> global___MetricValueStatus: ...
    @property
    def metric(self) -> global___MetricIdentifier: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        current: global___MetricValueStatus | None = ...,
        metric: global___MetricIdentifier | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current", b"current", "metric", b"metric", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["current", b"current", "metric", b"metric", "resource_info", b"resource_info"]) -> None: ...

global___PodsMetricStatus = PodsMetricStatus

@typing_extensions.final
class ResourceMetricSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    TARGET_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def target(self) -> global___MetricTarget: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        target: global___MetricTarget | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "target", b"target"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info", "target", b"target"]) -> None: ...

global___ResourceMetricSource = ResourceMetricSource

@typing_extensions.final
class ResourceMetricStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CURRENT_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def current(self) -> global___MetricValueStatus: ...
    name: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        current: global___MetricValueStatus | None = ...,
        name: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current", b"current", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["current", b"current", "name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___ResourceMetricStatus = ResourceMetricStatus
