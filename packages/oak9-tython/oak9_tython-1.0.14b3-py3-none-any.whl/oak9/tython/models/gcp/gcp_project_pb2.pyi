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
class ProjectXTimeouts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATE_FIELD_NUMBER: builtins.int
    DELETE_FIELD_NUMBER: builtins.int
    READ_FIELD_NUMBER: builtins.int
    UPDATE_FIELD_NUMBER: builtins.int
    create: builtins.str
    delete: builtins.str
    read: builtins.str
    update: builtins.str
    def __init__(
        self,
        *,
        create: builtins.str = ...,
        delete: builtins.str = ...,
        read: builtins.str = ...,
        update: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["create", b"create", "delete", b"delete", "read", b"read", "update", b"update"]) -> None: ...

global___ProjectXTimeouts = ProjectXTimeouts

@typing_extensions.final
class Project(google.protobuf.message.Message):
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

    AUTO_CREATE_NETWORK_FIELD_NUMBER: builtins.int
    BILLING_ACCOUNT_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    NUMBER_FIELD_NUMBER: builtins.int
    ORG_ID_FIELD_NUMBER: builtins.int
    PROJECT_ID_FIELD_NUMBER: builtins.int
    SKIP_DELETE_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    auto_create_network: builtins.bool
    billing_account: builtins.str
    folder_id: builtins.str
    id: builtins.str
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    name: builtins.str
    number: builtins.str
    org_id: builtins.str
    project_id: builtins.str
    skip_delete: builtins.bool
    @property
    def timeouts(self) -> global___ProjectXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        auto_create_network: builtins.bool = ...,
        billing_account: builtins.str = ...,
        folder_id: builtins.str = ...,
        id: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        name: builtins.str = ...,
        number: builtins.str = ...,
        org_id: builtins.str = ...,
        project_id: builtins.str = ...,
        skip_delete: builtins.bool = ...,
        timeouts: global___ProjectXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auto_create_network", b"auto_create_network", "billing_account", b"billing_account", "folder_id", b"folder_id", "id", b"id", "labels", b"labels", "name", b"name", "number", b"number", "org_id", b"org_id", "project_id", b"project_id", "resource_info", b"resource_info", "skip_delete", b"skip_delete", "timeouts", b"timeouts"]) -> None: ...

global___Project = Project

@typing_extensions.final
class ProjectAccessApprovalSettingsXEnrolledServices(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLOUD_PRODUCT_FIELD_NUMBER: builtins.int
    ENROLLMENT_LEVEL_FIELD_NUMBER: builtins.int
    cloud_product: builtins.str
    enrollment_level: builtins.str
    def __init__(
        self,
        *,
        cloud_product: builtins.str = ...,
        enrollment_level: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["cloud_product", b"cloud_product", "enrollment_level", b"enrollment_level"]) -> None: ...

global___ProjectAccessApprovalSettingsXEnrolledServices = ProjectAccessApprovalSettingsXEnrolledServices

@typing_extensions.final
class ProjectAccessApprovalSettingsXTimeouts(google.protobuf.message.Message):
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

global___ProjectAccessApprovalSettingsXTimeouts = ProjectAccessApprovalSettingsXTimeouts

@typing_extensions.final
class ProjectAccessApprovalSettings(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACTIVE_KEY_VERSION_FIELD_NUMBER: builtins.int
    ANCESTOR_HAS_ACTIVE_KEY_VERSION_FIELD_NUMBER: builtins.int
    ENROLLED_ANCESTOR_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    INVALID_KEY_VERSION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    NOTIFICATION_EMAILS_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    PROJECT_ID_FIELD_NUMBER: builtins.int
    ENROLLED_SERVICES_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    active_key_version: builtins.str
    ancestor_has_active_key_version: builtins.bool
    enrolled_ancestor: builtins.bool
    id: builtins.str
    invalid_key_version: builtins.bool
    name: builtins.str
    @property
    def notification_emails(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    project: builtins.str
    project_id: builtins.str
    @property
    def enrolled_services(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectAccessApprovalSettingsXEnrolledServices]: ...
    @property
    def timeouts(self) -> global___ProjectAccessApprovalSettingsXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        active_key_version: builtins.str = ...,
        ancestor_has_active_key_version: builtins.bool = ...,
        enrolled_ancestor: builtins.bool = ...,
        id: builtins.str = ...,
        invalid_key_version: builtins.bool = ...,
        name: builtins.str = ...,
        notification_emails: collections.abc.Iterable[builtins.str] | None = ...,
        project: builtins.str = ...,
        project_id: builtins.str = ...,
        enrolled_services: collections.abc.Iterable[global___ProjectAccessApprovalSettingsXEnrolledServices] | None = ...,
        timeouts: global___ProjectAccessApprovalSettingsXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["active_key_version", b"active_key_version", "ancestor_has_active_key_version", b"ancestor_has_active_key_version", "enrolled_ancestor", b"enrolled_ancestor", "enrolled_services", b"enrolled_services", "id", b"id", "invalid_key_version", b"invalid_key_version", "name", b"name", "notification_emails", b"notification_emails", "project", b"project", "project_id", b"project_id", "resource_info", b"resource_info", "timeouts", b"timeouts"]) -> None: ...

global___ProjectAccessApprovalSettings = ProjectAccessApprovalSettings

@typing_extensions.final
class ProjectDefaultServiceAccountsXTimeouts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATE_FIELD_NUMBER: builtins.int
    DELETE_FIELD_NUMBER: builtins.int
    READ_FIELD_NUMBER: builtins.int
    create: builtins.str
    delete: builtins.str
    read: builtins.str
    def __init__(
        self,
        *,
        create: builtins.str = ...,
        delete: builtins.str = ...,
        read: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["create", b"create", "delete", b"delete", "read", b"read"]) -> None: ...

global___ProjectDefaultServiceAccountsXTimeouts = ProjectDefaultServiceAccountsXTimeouts

@typing_extensions.final
class ProjectDefaultServiceAccounts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ServiceAccountsEntry(google.protobuf.message.Message):
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

    ACTION_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    RESTORE_POLICY_FIELD_NUMBER: builtins.int
    SERVICE_ACCOUNTS_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    action: builtins.str
    id: builtins.str
    project: builtins.str
    restore_policy: builtins.str
    @property
    def service_accounts(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    @property
    def timeouts(self) -> global___ProjectDefaultServiceAccountsXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        action: builtins.str = ...,
        id: builtins.str = ...,
        project: builtins.str = ...,
        restore_policy: builtins.str = ...,
        service_accounts: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        timeouts: global___ProjectDefaultServiceAccountsXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["action", b"action", "id", b"id", "project", b"project", "resource_info", b"resource_info", "restore_policy", b"restore_policy", "service_accounts", b"service_accounts", "timeouts", b"timeouts"]) -> None: ...

global___ProjectDefaultServiceAccounts = ProjectDefaultServiceAccounts

@typing_extensions.final
class ProjectIamAuditConfigXAuditLogConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXEMPTED_MEMBERS_FIELD_NUMBER: builtins.int
    LOG_TYPE_FIELD_NUMBER: builtins.int
    @property
    def exempted_members(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    log_type: builtins.str
    def __init__(
        self,
        *,
        exempted_members: collections.abc.Iterable[builtins.str] | None = ...,
        log_type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["exempted_members", b"exempted_members", "log_type", b"log_type"]) -> None: ...

global___ProjectIamAuditConfigXAuditLogConfig = ProjectIamAuditConfigXAuditLogConfig

@typing_extensions.final
class ProjectIamAuditConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ETAG_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    SERVICE_FIELD_NUMBER: builtins.int
    AUDIT_LOG_CONFIG_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    etag: builtins.str
    id: builtins.str
    project: builtins.str
    service: builtins.str
    @property
    def audit_log_config(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectIamAuditConfigXAuditLogConfig]: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        etag: builtins.str = ...,
        id: builtins.str = ...,
        project: builtins.str = ...,
        service: builtins.str = ...,
        audit_log_config: collections.abc.Iterable[global___ProjectIamAuditConfigXAuditLogConfig] | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["audit_log_config", b"audit_log_config", "etag", b"etag", "id", b"id", "project", b"project", "resource_info", b"resource_info", "service", b"service"]) -> None: ...

global___ProjectIamAuditConfig = ProjectIamAuditConfig

@typing_extensions.final
class ProjectIamBindingXCondition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DESCRIPTION_FIELD_NUMBER: builtins.int
    EXPRESSION_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    description: builtins.str
    expression: builtins.str
    title: builtins.str
    def __init__(
        self,
        *,
        description: builtins.str = ...,
        expression: builtins.str = ...,
        title: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "expression", b"expression", "title", b"title"]) -> None: ...

global___ProjectIamBindingXCondition = ProjectIamBindingXCondition

@typing_extensions.final
class ProjectIamBinding(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ETAG_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    MEMBERS_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    ROLE_FIELD_NUMBER: builtins.int
    CONDITION_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    etag: builtins.str
    id: builtins.str
    @property
    def members(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    project: builtins.str
    role: builtins.str
    @property
    def condition(self) -> global___ProjectIamBindingXCondition: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        etag: builtins.str = ...,
        id: builtins.str = ...,
        members: collections.abc.Iterable[builtins.str] | None = ...,
        project: builtins.str = ...,
        role: builtins.str = ...,
        condition: global___ProjectIamBindingXCondition | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["condition", b"condition", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["condition", b"condition", "etag", b"etag", "id", b"id", "members", b"members", "project", b"project", "resource_info", b"resource_info", "role", b"role"]) -> None: ...

global___ProjectIamBinding = ProjectIamBinding

@typing_extensions.final
class ProjectIamCustomRole(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DELETED_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PERMISSIONS_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    ROLE_ID_FIELD_NUMBER: builtins.int
    STAGE_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    deleted: builtins.bool
    description: builtins.str
    id: builtins.str
    name: builtins.str
    @property
    def permissions(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    project: builtins.str
    role_id: builtins.str
    stage: builtins.str
    title: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        deleted: builtins.bool = ...,
        description: builtins.str = ...,
        id: builtins.str = ...,
        name: builtins.str = ...,
        permissions: collections.abc.Iterable[builtins.str] | None = ...,
        project: builtins.str = ...,
        role_id: builtins.str = ...,
        stage: builtins.str = ...,
        title: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["deleted", b"deleted", "description", b"description", "id", b"id", "name", b"name", "permissions", b"permissions", "project", b"project", "resource_info", b"resource_info", "role_id", b"role_id", "stage", b"stage", "title", b"title"]) -> None: ...

global___ProjectIamCustomRole = ProjectIamCustomRole

@typing_extensions.final
class ProjectIamMemberXCondition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DESCRIPTION_FIELD_NUMBER: builtins.int
    EXPRESSION_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    description: builtins.str
    expression: builtins.str
    title: builtins.str
    def __init__(
        self,
        *,
        description: builtins.str = ...,
        expression: builtins.str = ...,
        title: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "expression", b"expression", "title", b"title"]) -> None: ...

global___ProjectIamMemberXCondition = ProjectIamMemberXCondition

@typing_extensions.final
class ProjectIamMember(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ETAG_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    MEMBER_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    ROLE_FIELD_NUMBER: builtins.int
    CONDITION_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    etag: builtins.str
    id: builtins.str
    member: builtins.str
    project: builtins.str
    role: builtins.str
    @property
    def condition(self) -> global___ProjectIamMemberXCondition: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        etag: builtins.str = ...,
        id: builtins.str = ...,
        member: builtins.str = ...,
        project: builtins.str = ...,
        role: builtins.str = ...,
        condition: global___ProjectIamMemberXCondition | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["condition", b"condition", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["condition", b"condition", "etag", b"etag", "id", b"id", "member", b"member", "project", b"project", "resource_info", b"resource_info", "role", b"role"]) -> None: ...

global___ProjectIamMember = ProjectIamMember

@typing_extensions.final
class ProjectIamPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ETAG_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    POLICY_DATA_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    etag: builtins.str
    id: builtins.str
    policy_data: builtins.str
    project: builtins.str
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        etag: builtins.str = ...,
        id: builtins.str = ...,
        policy_data: builtins.str = ...,
        project: builtins.str = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["etag", b"etag", "id", b"id", "policy_data", b"policy_data", "project", b"project", "resource_info", b"resource_info"]) -> None: ...

global___ProjectIamPolicy = ProjectIamPolicy

@typing_extensions.final
class ProjectOrganizationPolicyXBooleanPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENFORCED_FIELD_NUMBER: builtins.int
    enforced: builtins.bool
    def __init__(
        self,
        *,
        enforced: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["enforced", b"enforced"]) -> None: ...

global___ProjectOrganizationPolicyXBooleanPolicy = ProjectOrganizationPolicyXBooleanPolicy

@typing_extensions.final
class ProjectOrganizationPolicyXListPolicyXAllow(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ALL_FIELD_NUMBER: builtins.int
    VALUES_FIELD_NUMBER: builtins.int
    all: builtins.bool
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        all: builtins.bool = ...,
        values: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["all", b"all", "values", b"values"]) -> None: ...

global___ProjectOrganizationPolicyXListPolicyXAllow = ProjectOrganizationPolicyXListPolicyXAllow

@typing_extensions.final
class ProjectOrganizationPolicyXListPolicyXDeny(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ALL_FIELD_NUMBER: builtins.int
    VALUES_FIELD_NUMBER: builtins.int
    all: builtins.bool
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        all: builtins.bool = ...,
        values: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["all", b"all", "values", b"values"]) -> None: ...

global___ProjectOrganizationPolicyXListPolicyXDeny = ProjectOrganizationPolicyXListPolicyXDeny

@typing_extensions.final
class ProjectOrganizationPolicyXListPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INHERIT_FROM_PARENT_FIELD_NUMBER: builtins.int
    SUGGESTED_VALUE_FIELD_NUMBER: builtins.int
    ALLOW_FIELD_NUMBER: builtins.int
    DENY_FIELD_NUMBER: builtins.int
    inherit_from_parent: builtins.bool
    suggested_value: builtins.str
    @property
    def allow(self) -> global___ProjectOrganizationPolicyXListPolicyXAllow: ...
    @property
    def deny(self) -> global___ProjectOrganizationPolicyXListPolicyXDeny: ...
    def __init__(
        self,
        *,
        inherit_from_parent: builtins.bool = ...,
        suggested_value: builtins.str = ...,
        allow: global___ProjectOrganizationPolicyXListPolicyXAllow | None = ...,
        deny: global___ProjectOrganizationPolicyXListPolicyXDeny | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["allow", b"allow", "deny", b"deny"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["allow", b"allow", "deny", b"deny", "inherit_from_parent", b"inherit_from_parent", "suggested_value", b"suggested_value"]) -> None: ...

global___ProjectOrganizationPolicyXListPolicy = ProjectOrganizationPolicyXListPolicy

@typing_extensions.final
class ProjectOrganizationPolicyXRestorePolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEFAULT_FIELD_NUMBER: builtins.int
    default: builtins.bool
    def __init__(
        self,
        *,
        default: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["default", b"default"]) -> None: ...

global___ProjectOrganizationPolicyXRestorePolicy = ProjectOrganizationPolicyXRestorePolicy

@typing_extensions.final
class ProjectOrganizationPolicyXTimeouts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATE_FIELD_NUMBER: builtins.int
    DELETE_FIELD_NUMBER: builtins.int
    READ_FIELD_NUMBER: builtins.int
    UPDATE_FIELD_NUMBER: builtins.int
    create: builtins.str
    delete: builtins.str
    read: builtins.str
    update: builtins.str
    def __init__(
        self,
        *,
        create: builtins.str = ...,
        delete: builtins.str = ...,
        read: builtins.str = ...,
        update: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["create", b"create", "delete", b"delete", "read", b"read", "update", b"update"]) -> None: ...

global___ProjectOrganizationPolicyXTimeouts = ProjectOrganizationPolicyXTimeouts

@typing_extensions.final
class ProjectOrganizationPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONSTRAINT_FIELD_NUMBER: builtins.int
    ETAG_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    UPDATE_TIME_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    BOOLEAN_POLICY_FIELD_NUMBER: builtins.int
    LIST_POLICY_FIELD_NUMBER: builtins.int
    RESTORE_POLICY_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    constraint: builtins.str
    etag: builtins.str
    id: builtins.str
    project: builtins.str
    update_time: builtins.str
    version: builtins.float
    @property
    def boolean_policy(self) -> global___ProjectOrganizationPolicyXBooleanPolicy: ...
    @property
    def list_policy(self) -> global___ProjectOrganizationPolicyXListPolicy: ...
    @property
    def restore_policy(self) -> global___ProjectOrganizationPolicyXRestorePolicy: ...
    @property
    def timeouts(self) -> global___ProjectOrganizationPolicyXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        constraint: builtins.str = ...,
        etag: builtins.str = ...,
        id: builtins.str = ...,
        project: builtins.str = ...,
        update_time: builtins.str = ...,
        version: builtins.float = ...,
        boolean_policy: global___ProjectOrganizationPolicyXBooleanPolicy | None = ...,
        list_policy: global___ProjectOrganizationPolicyXListPolicy | None = ...,
        restore_policy: global___ProjectOrganizationPolicyXRestorePolicy | None = ...,
        timeouts: global___ProjectOrganizationPolicyXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["boolean_policy", b"boolean_policy", "list_policy", b"list_policy", "resource_info", b"resource_info", "restore_policy", b"restore_policy", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["boolean_policy", b"boolean_policy", "constraint", b"constraint", "etag", b"etag", "id", b"id", "list_policy", b"list_policy", "project", b"project", "resource_info", b"resource_info", "restore_policy", b"restore_policy", "timeouts", b"timeouts", "update_time", b"update_time", "version", b"version"]) -> None: ...

global___ProjectOrganizationPolicy = ProjectOrganizationPolicy

@typing_extensions.final
class ProjectServiceXTimeouts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATE_FIELD_NUMBER: builtins.int
    DELETE_FIELD_NUMBER: builtins.int
    READ_FIELD_NUMBER: builtins.int
    UPDATE_FIELD_NUMBER: builtins.int
    create: builtins.str
    delete: builtins.str
    read: builtins.str
    update: builtins.str
    def __init__(
        self,
        *,
        create: builtins.str = ...,
        delete: builtins.str = ...,
        read: builtins.str = ...,
        update: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["create", b"create", "delete", b"delete", "read", b"read", "update", b"update"]) -> None: ...

global___ProjectServiceXTimeouts = ProjectServiceXTimeouts

@typing_extensions.final
class ProjectService(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DISABLE_DEPENDENT_SERVICES_FIELD_NUMBER: builtins.int
    DISABLE_ON_DESTROY_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    SERVICE_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    disable_dependent_services: builtins.bool
    disable_on_destroy: builtins.bool
    id: builtins.str
    project: builtins.str
    service: builtins.str
    @property
    def timeouts(self) -> global___ProjectServiceXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        disable_dependent_services: builtins.bool = ...,
        disable_on_destroy: builtins.bool = ...,
        id: builtins.str = ...,
        project: builtins.str = ...,
        service: builtins.str = ...,
        timeouts: global___ProjectServiceXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["disable_dependent_services", b"disable_dependent_services", "disable_on_destroy", b"disable_on_destroy", "id", b"id", "project", b"project", "resource_info", b"resource_info", "service", b"service", "timeouts", b"timeouts"]) -> None: ...

global___ProjectService = ProjectService

@typing_extensions.final
class ProjectUsageExportBucketXTimeouts(google.protobuf.message.Message):
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

global___ProjectUsageExportBucketXTimeouts = ProjectUsageExportBucketXTimeouts

@typing_extensions.final
class ProjectUsageExportBucket(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BUCKET_NAME_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    PREFIX_FIELD_NUMBER: builtins.int
    PROJECT_FIELD_NUMBER: builtins.int
    TIMEOUTS_FIELD_NUMBER: builtins.int
    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    bucket_name: builtins.str
    id: builtins.str
    prefix: builtins.str
    project: builtins.str
    @property
    def timeouts(self) -> global___ProjectUsageExportBucketXTimeouts: ...
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        bucket_name: builtins.str = ...,
        id: builtins.str = ...,
        prefix: builtins.str = ...,
        project: builtins.str = ...,
        timeouts: global___ProjectUsageExportBucketXTimeouts | None = ...,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "timeouts", b"timeouts"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bucket_name", b"bucket_name", "id", b"id", "prefix", b"prefix", "project", b"project", "resource_info", b"resource_info", "timeouts", b"timeouts"]) -> None: ...

global___ProjectUsageExportBucket = ProjectUsageExportBucket
