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
class AccessKey(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    SERIAL_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    USER_NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    serial: builtins.int
    status: builtins.str
    user_name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        serial: builtins.int = ...,
        status: builtins.str = ...,
        user_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "serial", b"serial", "status", b"status", "user_name", b"user_name"]) -> None: ...

global___AccessKey = AccessKey

@typing_extensions.final
class IAM(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GROUP_FIELD_NUMBER: builtins.int
    MANAGED_POLICY_FIELD_NUMBER: builtins.int
    POLICY_FIELD_NUMBER: builtins.int
    ROLE_FIELD_NUMBER: builtins.int
    USER_FIELD_NUMBER: builtins.int
    @property
    def group(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Group]: ...
    @property
    def managed_policy(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ManagedPolicy]: ...
    @property
    def policy(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Policy]: ...
    @property
    def role(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Role]: ...
    @property
    def user(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___User]: ...
    def __init__(
        self,
        *,
        group: collections.abc.Iterable[global___Group] | None = ...,
        managed_policy: collections.abc.Iterable[global___ManagedPolicy] | None = ...,
        policy: collections.abc.Iterable[global___Policy] | None = ...,
        role: collections.abc.Iterable[global___Role] | None = ...,
        user: collections.abc.Iterable[global___User] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["group", b"group", "managed_policy", b"managed_policy", "policy", b"policy", "role", b"role", "user", b"user"]) -> None: ...

global___IAM = IAM

@typing_extensions.final
class GroupPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    POLICY_NAME_FIELD_NUMBER: builtins.int
    POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    policy_name: builtins.str
    policy_document: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        policy_name: builtins.str = ...,
        policy_document: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["policy_document", b"policy_document", "policy_name", b"policy_name", "resource_info", b"resource_info"]) -> None: ...

global___GroupPolicy = GroupPolicy

@typing_extensions.final
class Group(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    GROUP_NAME_FIELD_NUMBER: builtins.int
    MANAGED_POLICY_ARNS_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    POLICIES_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    group_name: builtins.str
    @property
    def managed_policy_arns(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    path: builtins.str
    @property
    def policies(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GroupPolicy]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        group_name: builtins.str = ...,
        managed_policy_arns: collections.abc.Iterable[builtins.str] | None = ...,
        path: builtins.str = ...,
        policies: collections.abc.Iterable[global___GroupPolicy] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["group_name", b"group_name", "managed_policy_arns", b"managed_policy_arns", "path", b"path", "policies", b"policies", "resource_info", b"resource_info"]) -> None: ...

global___Group = Group

@typing_extensions.final
class InstanceProfile(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    INSTANCE_PROFILE_NAME_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    ROLES_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    instance_profile_name: builtins.str
    path: builtins.str
    @property
    def roles(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        instance_profile_name: builtins.str = ...,
        path: builtins.str = ...,
        roles: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["instance_profile_name", b"instance_profile_name", "path", b"path", "resource_info", b"resource_info", "roles", b"roles"]) -> None: ...

global___InstanceProfile = InstanceProfile

@typing_extensions.final
class ManagedPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    GROUPS_FIELD_NUMBER: builtins.int
    MANAGED_POLICY_NAME_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    ROLES_FIELD_NUMBER: builtins.int
    USERS_FIELD_NUMBER: builtins.int
    POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    @property
    def groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    managed_policy_name: builtins.str
    path: builtins.str
    @property
    def roles(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def users(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    policy_document: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        groups: collections.abc.Iterable[builtins.str] | None = ...,
        managed_policy_name: builtins.str = ...,
        path: builtins.str = ...,
        roles: collections.abc.Iterable[builtins.str] | None = ...,
        users: collections.abc.Iterable[builtins.str] | None = ...,
        policy_document: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "groups", b"groups", "managed_policy_name", b"managed_policy_name", "path", b"path", "policy_document", b"policy_document", "resource_info", b"resource_info", "roles", b"roles", "users", b"users"]) -> None: ...

global___ManagedPolicy = ManagedPolicy

@typing_extensions.final
class Policy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    GROUPS_FIELD_NUMBER: builtins.int
    POLICY_NAME_FIELD_NUMBER: builtins.int
    ROLES_FIELD_NUMBER: builtins.int
    USERS_FIELD_NUMBER: builtins.int
    POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    policy_name: builtins.str
    @property
    def roles(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def users(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    policy_document: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        groups: collections.abc.Iterable[builtins.str] | None = ...,
        policy_name: builtins.str = ...,
        roles: collections.abc.Iterable[builtins.str] | None = ...,
        users: collections.abc.Iterable[builtins.str] | None = ...,
        policy_document: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["groups", b"groups", "policy_document", b"policy_document", "policy_name", b"policy_name", "resource_info", b"resource_info", "roles", b"roles", "users", b"users"]) -> None: ...

global___Policy = Policy

@typing_extensions.final
class RolePolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    POLICY_NAME_FIELD_NUMBER: builtins.int
    POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    policy_name: builtins.str
    policy_document: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        policy_name: builtins.str = ...,
        policy_document: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["policy_document", b"policy_document", "policy_name", b"policy_name", "resource_info", b"resource_info"]) -> None: ...

global___RolePolicy = RolePolicy

@typing_extensions.final
class Role(google.protobuf.message.Message):
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
    MANAGED_POLICY_ARNS_FIELD_NUMBER: builtins.int
    MAX_SESSION_DURATION_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    PERMISSIONS_BOUNDARY_FIELD_NUMBER: builtins.int
    POLICIES_FIELD_NUMBER: builtins.int
    ROLE_NAME_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    ASSUME_ROLE_POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    @property
    def managed_policy_arns(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    max_session_duration: builtins.int
    path: builtins.str
    permissions_boundary: builtins.str
    @property
    def policies(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RolePolicy]: ...
    role_name: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    assume_role_policy_document: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        managed_policy_arns: collections.abc.Iterable[builtins.str] | None = ...,
        max_session_duration: builtins.int = ...,
        path: builtins.str = ...,
        permissions_boundary: builtins.str = ...,
        policies: collections.abc.Iterable[global___RolePolicy] | None = ...,
        role_name: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        assume_role_policy_document: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["assume_role_policy_document", b"assume_role_policy_document", "description", b"description", "managed_policy_arns", b"managed_policy_arns", "max_session_duration", b"max_session_duration", "path", b"path", "permissions_boundary", b"permissions_boundary", "policies", b"policies", "resource_info", b"resource_info", "role_name", b"role_name", "tags", b"tags"]) -> None: ...

global___Role = Role

@typing_extensions.final
class ServiceLinkedRole(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CUSTOM_SUFFIX_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    AWS_SERVICE_NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    custom_suffix: builtins.str
    description: builtins.str
    aws_service_name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        custom_suffix: builtins.str = ...,
        description: builtins.str = ...,
        aws_service_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["aws_service_name", b"aws_service_name", "custom_suffix", b"custom_suffix", "description", b"description", "resource_info", b"resource_info"]) -> None: ...

global___ServiceLinkedRole = ServiceLinkedRole

@typing_extensions.final
class UserLoginProfile(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    PASSWORD_RESET_REQUIRED_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    password: builtins.str
    password_reset_required: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        password: builtins.str = ...,
        password_reset_required: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["password", b"password", "password_reset_required", b"password_reset_required", "resource_info", b"resource_info"]) -> None: ...

global___UserLoginProfile = UserLoginProfile

@typing_extensions.final
class UserPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    POLICY_NAME_FIELD_NUMBER: builtins.int
    POLICY_DOCUMENT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    policy_name: builtins.str
    policy_document: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        policy_name: builtins.str = ...,
        policy_document: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["policy_document", b"policy_document", "policy_name", b"policy_name", "resource_info", b"resource_info"]) -> None: ...

global___UserPolicy = UserPolicy

@typing_extensions.final
class User(google.protobuf.message.Message):
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
    GROUPS_FIELD_NUMBER: builtins.int
    LOGIN_PROFILE_FIELD_NUMBER: builtins.int
    MANAGED_POLICY_ARNS_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    PERMISSIONS_BOUNDARY_FIELD_NUMBER: builtins.int
    POLICIES_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    USER_NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def login_profile(self) -> global___UserLoginProfile: ...
    @property
    def managed_policy_arns(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    path: builtins.str
    permissions_boundary: builtins.str
    @property
    def policies(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___UserPolicy]: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    user_name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        groups: collections.abc.Iterable[builtins.str] | None = ...,
        login_profile: global___UserLoginProfile | None = ...,
        managed_policy_arns: collections.abc.Iterable[builtins.str] | None = ...,
        path: builtins.str = ...,
        permissions_boundary: builtins.str = ...,
        policies: collections.abc.Iterable[global___UserPolicy] | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        user_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["login_profile", b"login_profile", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["groups", b"groups", "login_profile", b"login_profile", "managed_policy_arns", b"managed_policy_arns", "path", b"path", "permissions_boundary", b"permissions_boundary", "policies", b"policies", "resource_info", b"resource_info", "tags", b"tags", "user_name", b"user_name"]) -> None: ...

global___User = User

@typing_extensions.final
class UserToGroupAddition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    GROUP_NAME_FIELD_NUMBER: builtins.int
    USERS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    group_name: builtins.str
    @property
    def users(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        group_name: builtins.str = ...,
        users: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["group_name", b"group_name", "resource_info", b"resource_info", "users", b"users"]) -> None: ...

global___UserToGroupAddition = UserToGroupAddition
