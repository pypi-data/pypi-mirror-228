"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import gcp.gcp_cloudfunctions_pb2
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
class GoogleCloudfunctions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLOUDFUNCTIONS_FUNCTION_FIELD_NUMBER: builtins.int
    CLOUDFUNCTIONS_FUNCTION_IAM_BINDING_FIELD_NUMBER: builtins.int
    CLOUDFUNCTIONS_FUNCTION_IAM_MEMBER_FIELD_NUMBER: builtins.int
    CLOUDFUNCTIONS_FUNCTION_IAM_POLICY_FIELD_NUMBER: builtins.int
    @property
    def cloudfunctions_function(self) -> gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunction: ...
    @property
    def cloudfunctions_function_iam_binding(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunctionIamBinding]: ...
    @property
    def cloudfunctions_function_iam_member(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunctionIamMember]: ...
    @property
    def cloudfunctions_function_iam_policy(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunctionIamPolicy]: ...
    def __init__(
        self,
        *,
        cloudfunctions_function: gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunction | None = ...,
        cloudfunctions_function_iam_binding: collections.abc.Iterable[gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunctionIamBinding] | None = ...,
        cloudfunctions_function_iam_member: collections.abc.Iterable[gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunctionIamMember] | None = ...,
        cloudfunctions_function_iam_policy: collections.abc.Iterable[gcp.gcp_cloudfunctions_pb2.CloudfunctionsFunctionIamPolicy] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["cloudfunctions_function", b"cloudfunctions_function"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cloudfunctions_function", b"cloudfunctions_function", "cloudfunctions_function_iam_binding", b"cloudfunctions_function_iam_binding", "cloudfunctions_function_iam_member", b"cloudfunctions_function_iam_member", "cloudfunctions_function_iam_policy", b"cloudfunctions_function_iam_policy"]) -> None: ...

global___GoogleCloudfunctions = GoogleCloudfunctions
