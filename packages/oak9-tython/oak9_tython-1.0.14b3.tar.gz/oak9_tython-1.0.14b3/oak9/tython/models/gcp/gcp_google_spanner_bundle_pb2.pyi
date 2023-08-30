"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import gcp.gcp_spanner_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class GoogleSpanner(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SPANNER_DATABASE_FIELD_NUMBER: builtins.int
    SPANNER_DATABASE_IAM_BINDING_FIELD_NUMBER: builtins.int
    SPANNER_DATABASE_IAM_MEMBER_FIELD_NUMBER: builtins.int
    SPANNER_DATABASE_IAM_POLICY_FIELD_NUMBER: builtins.int
    SPANNER_INSTANCE_FIELD_NUMBER: builtins.int
    SPANNER_INSTANCE_IAM_BINDING_FIELD_NUMBER: builtins.int
    SPANNER_INSTANCE_IAM_MEMBER_FIELD_NUMBER: builtins.int
    SPANNER_INSTANCE_IAM_POLICY_FIELD_NUMBER: builtins.int
    @property
    def spanner_database(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerDatabase]: ...
    @property
    def spanner_database_iam_binding(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerDatabaseIamBinding]: ...
    @property
    def spanner_database_iam_member(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerDatabaseIamMember]: ...
    @property
    def spanner_database_iam_policy(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerDatabaseIamPolicy]: ...
    @property
    def spanner_instance(self) -> gcp.gcp_spanner_pb2.SpannerInstance: ...
    @property
    def spanner_instance_iam_binding(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerInstanceIamBinding]: ...
    @property
    def spanner_instance_iam_member(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerInstanceIamMember]: ...
    @property
    def spanner_instance_iam_policy(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_spanner_pb2.SpannerInstanceIamPolicy]: ...
    def __init__(
        self,
        *,
        spanner_database: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerDatabase] | None = ...,
        spanner_database_iam_binding: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerDatabaseIamBinding] | None = ...,
        spanner_database_iam_member: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerDatabaseIamMember] | None = ...,
        spanner_database_iam_policy: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerDatabaseIamPolicy] | None = ...,
        spanner_instance: gcp.gcp_spanner_pb2.SpannerInstance | None = ...,
        spanner_instance_iam_binding: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerInstanceIamBinding] | None = ...,
        spanner_instance_iam_member: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerInstanceIamMember] | None = ...,
        spanner_instance_iam_policy: collections.abc.Iterable[gcp.gcp_spanner_pb2.SpannerInstanceIamPolicy] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["spanner_instance", b"spanner_instance"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["spanner_database", b"spanner_database", "spanner_database_iam_binding", b"spanner_database_iam_binding", "spanner_database_iam_member", b"spanner_database_iam_member", "spanner_database_iam_policy", b"spanner_database_iam_policy", "spanner_instance", b"spanner_instance", "spanner_instance_iam_binding", b"spanner_instance_iam_binding", "spanner_instance_iam_member", b"spanner_instance_iam_member", "spanner_instance_iam_policy", b"spanner_instance_iam_policy"]) -> None: ...

global___GoogleSpanner = GoogleSpanner
