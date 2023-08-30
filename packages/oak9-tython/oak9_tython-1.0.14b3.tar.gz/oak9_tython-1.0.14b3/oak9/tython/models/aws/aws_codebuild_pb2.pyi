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
class ProjectVpcConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    SUBNETS_FIELD_NUMBER: builtins.int
    VPC_ID_FIELD_NUMBER: builtins.int
    SECURITY_GROUP_IDS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def subnets(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    vpc_id: builtins.str
    @property
    def security_group_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        subnets: collections.abc.Iterable[builtins.str] | None = ...,
        vpc_id: builtins.str = ...,
        security_group_ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "security_group_ids", b"security_group_ids", "subnets", b"subnets", "vpc_id", b"vpc_id"]) -> None: ...

global___ProjectVpcConfig = ProjectVpcConfig

@typing_extensions.final
class ProjectSourceAuth(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    RESOURCE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    resource: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        resource: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource", b"resource", "resource_info", b"resource_info"]) -> None: ...

global___ProjectSourceAuth = ProjectSourceAuth

@typing_extensions.final
class ProjectBuildStatusConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    TARGET_URL_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    context: builtins.str
    target_url: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        context: builtins.str = ...,
        target_url: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "resource_info", b"resource_info", "target_url", b"target_url"]) -> None: ...

global___ProjectBuildStatusConfig = ProjectBuildStatusConfig

@typing_extensions.final
class ProjectGitSubmodulesConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    FETCH_SUBMODULES_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    fetch_submodules: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        fetch_submodules: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["fetch_submodules", b"fetch_submodules", "resource_info", b"resource_info"]) -> None: ...

global___ProjectGitSubmodulesConfig = ProjectGitSubmodulesConfig

@typing_extensions.final
class ProjectSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    REPORT_BUILD_STATUS_FIELD_NUMBER: builtins.int
    AUTH_FIELD_NUMBER: builtins.int
    SOURCE_IDENTIFIER_FIELD_NUMBER: builtins.int
    BUILD_SPEC_FIELD_NUMBER: builtins.int
    GIT_CLONE_DEPTH_FIELD_NUMBER: builtins.int
    BUILD_STATUS_CONFIG_FIELD_NUMBER: builtins.int
    GIT_SUBMODULES_CONFIG_FIELD_NUMBER: builtins.int
    INSECURE_SSL_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    report_build_status: builtins.bool
    @property
    def auth(self) -> global___ProjectSourceAuth: ...
    source_identifier: builtins.str
    build_spec: builtins.str
    git_clone_depth: builtins.int
    @property
    def build_status_config(self) -> global___ProjectBuildStatusConfig: ...
    @property
    def git_submodules_config(self) -> global___ProjectGitSubmodulesConfig: ...
    insecure_ssl: builtins.bool
    location: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        report_build_status: builtins.bool = ...,
        auth: global___ProjectSourceAuth | None = ...,
        source_identifier: builtins.str = ...,
        build_spec: builtins.str = ...,
        git_clone_depth: builtins.int = ...,
        build_status_config: global___ProjectBuildStatusConfig | None = ...,
        git_submodules_config: global___ProjectGitSubmodulesConfig | None = ...,
        insecure_ssl: builtins.bool = ...,
        location: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["auth", b"auth", "build_status_config", b"build_status_config", "git_submodules_config", b"git_submodules_config", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auth", b"auth", "build_spec", b"build_spec", "build_status_config", b"build_status_config", "git_clone_depth", b"git_clone_depth", "git_submodules_config", b"git_submodules_config", "insecure_ssl", b"insecure_ssl", "location", b"location", "report_build_status", b"report_build_status", "resource_info", b"resource_info", "source_identifier", b"source_identifier"]) -> None: ...

global___ProjectSource = ProjectSource

@typing_extensions.final
class ProjectFilterGroup(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> None: ...

global___ProjectFilterGroup = ProjectFilterGroup

@typing_extensions.final
class ProjectProjectTriggers(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    FILTER_GROUPS_FIELD_NUMBER: builtins.int
    WEBHOOK_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def filter_groups(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectFilterGroup]: ...
    webhook: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        filter_groups: collections.abc.Iterable[global___ProjectFilterGroup] | None = ...,
        webhook: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["filter_groups", b"filter_groups", "resource_info", b"resource_info", "webhook", b"webhook"]) -> None: ...

global___ProjectProjectTriggers = ProjectProjectTriggers

@typing_extensions.final
class ProjectArtifacts(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    ARTIFACT_IDENTIFIER_FIELD_NUMBER: builtins.int
    OVERRIDE_ARTIFACT_NAME_FIELD_NUMBER: builtins.int
    PACKAGING_FIELD_NUMBER: builtins.int
    ENCRYPTION_DISABLED_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    NAMESPACE_TYPE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    path: builtins.str
    artifact_identifier: builtins.str
    override_artifact_name: builtins.bool
    packaging: builtins.str
    encryption_disabled: builtins.bool
    location: builtins.str
    name: builtins.str
    namespace_type: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        path: builtins.str = ...,
        artifact_identifier: builtins.str = ...,
        override_artifact_name: builtins.bool = ...,
        packaging: builtins.str = ...,
        encryption_disabled: builtins.bool = ...,
        location: builtins.str = ...,
        name: builtins.str = ...,
        namespace_type: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["artifact_identifier", b"artifact_identifier", "encryption_disabled", b"encryption_disabled", "location", b"location", "name", b"name", "namespace_type", b"namespace_type", "override_artifact_name", b"override_artifact_name", "packaging", b"packaging", "path", b"path", "resource_info", b"resource_info"]) -> None: ...

global___ProjectArtifacts = ProjectArtifacts

@typing_extensions.final
class ProjectCloudWatchLogsConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    GROUP_NAME_FIELD_NUMBER: builtins.int
    STREAM_NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    status: builtins.str
    group_name: builtins.str
    stream_name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        status: builtins.str = ...,
        group_name: builtins.str = ...,
        stream_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["group_name", b"group_name", "resource_info", b"resource_info", "status", b"status", "stream_name", b"stream_name"]) -> None: ...

global___ProjectCloudWatchLogsConfig = ProjectCloudWatchLogsConfig

@typing_extensions.final
class ProjectS3LogsConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    ENCRYPTION_DISABLED_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    status: builtins.str
    encryption_disabled: builtins.bool
    location: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        status: builtins.str = ...,
        encryption_disabled: builtins.bool = ...,
        location: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["encryption_disabled", b"encryption_disabled", "location", b"location", "resource_info", b"resource_info", "status", b"status"]) -> None: ...

global___ProjectS3LogsConfig = ProjectS3LogsConfig

@typing_extensions.final
class ProjectLogsConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CLOUD_WATCH_LOGS_FIELD_NUMBER: builtins.int
    S3_LOGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def cloud_watch_logs(self) -> global___ProjectCloudWatchLogsConfig: ...
    @property
    def s3_logs(self) -> global___ProjectS3LogsConfig: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        cloud_watch_logs: global___ProjectCloudWatchLogsConfig | None = ...,
        s3_logs: global___ProjectS3LogsConfig | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["cloud_watch_logs", b"cloud_watch_logs", "resource_info", b"resource_info", "s3_logs", b"s3_logs"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cloud_watch_logs", b"cloud_watch_logs", "resource_info", b"resource_info", "s3_logs", b"s3_logs"]) -> None: ...

global___ProjectLogsConfig = ProjectLogsConfig

@typing_extensions.final
class ProjectProjectFileSystemLocation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    MOUNT_POINT_FIELD_NUMBER: builtins.int
    IDENTIFIER_FIELD_NUMBER: builtins.int
    MOUNT_OPTIONS_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    mount_point: builtins.str
    identifier: builtins.str
    mount_options: builtins.str
    location: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        mount_point: builtins.str = ...,
        identifier: builtins.str = ...,
        mount_options: builtins.str = ...,
        location: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["identifier", b"identifier", "location", b"location", "mount_options", b"mount_options", "mount_point", b"mount_point", "resource_info", b"resource_info"]) -> None: ...

global___ProjectProjectFileSystemLocation = ProjectProjectFileSystemLocation

@typing_extensions.final
class ProjectEnvironmentVariable(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    value: builtins.str
    name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        value: builtins.str = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info", "value", b"value"]) -> None: ...

global___ProjectEnvironmentVariable = ProjectEnvironmentVariable

@typing_extensions.final
class ProjectRegistryCredential(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CREDENTIAL_FIELD_NUMBER: builtins.int
    CREDENTIAL_PROVIDER_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    credential: builtins.str
    credential_provider: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        credential: builtins.str = ...,
        credential_provider: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["credential", b"credential", "credential_provider", b"credential_provider", "resource_info", b"resource_info"]) -> None: ...

global___ProjectRegistryCredential = ProjectRegistryCredential

@typing_extensions.final
class ProjectEnvironment(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: builtins.int
    PRIVILEGED_MODE_FIELD_NUMBER: builtins.int
    IMAGE_PULL_CREDENTIALS_TYPE_FIELD_NUMBER: builtins.int
    IMAGE_FIELD_NUMBER: builtins.int
    REGISTRY_CREDENTIAL_FIELD_NUMBER: builtins.int
    COMPUTE_TYPE_FIELD_NUMBER: builtins.int
    CERTIFICATE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def environment_variables(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectEnvironmentVariable]: ...
    privileged_mode: builtins.bool
    image_pull_credentials_type: builtins.str
    image: builtins.str
    @property
    def registry_credential(self) -> global___ProjectRegistryCredential: ...
    compute_type: builtins.str
    certificate: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        environment_variables: collections.abc.Iterable[global___ProjectEnvironmentVariable] | None = ...,
        privileged_mode: builtins.bool = ...,
        image_pull_credentials_type: builtins.str = ...,
        image: builtins.str = ...,
        registry_credential: global___ProjectRegistryCredential | None = ...,
        compute_type: builtins.str = ...,
        certificate: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["registry_credential", b"registry_credential", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["certificate", b"certificate", "compute_type", b"compute_type", "environment_variables", b"environment_variables", "image", b"image", "image_pull_credentials_type", b"image_pull_credentials_type", "privileged_mode", b"privileged_mode", "registry_credential", b"registry_credential", "resource_info", b"resource_info"]) -> None: ...

global___ProjectEnvironment = ProjectEnvironment

@typing_extensions.final
class ProjectProjectSourceVersion(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    SOURCE_IDENTIFIER_FIELD_NUMBER: builtins.int
    SOURCE_VERSION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    source_identifier: builtins.str
    source_version: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        source_identifier: builtins.str = ...,
        source_version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "source_identifier", b"source_identifier", "source_version", b"source_version"]) -> None: ...

global___ProjectProjectSourceVersion = ProjectProjectSourceVersion

@typing_extensions.final
class ProjectBatchRestrictions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    COMPUTE_TYPES_ALLOWED_FIELD_NUMBER: builtins.int
    MAXIMUM_BUILDS_ALLOWED_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def compute_types_allowed(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    maximum_builds_allowed: builtins.int
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        compute_types_allowed: collections.abc.Iterable[builtins.str] | None = ...,
        maximum_builds_allowed: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["compute_types_allowed", b"compute_types_allowed", "maximum_builds_allowed", b"maximum_builds_allowed", "resource_info", b"resource_info"]) -> None: ...

global___ProjectBatchRestrictions = ProjectBatchRestrictions

@typing_extensions.final
class ProjectProjectBuildBatchConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    COMBINE_ARTIFACTS_FIELD_NUMBER: builtins.int
    SERVICE_ROLE_FIELD_NUMBER: builtins.int
    TIMEOUT_IN_MINS_FIELD_NUMBER: builtins.int
    RESTRICTIONS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    combine_artifacts: builtins.bool
    service_role: builtins.str
    timeout_in_mins: builtins.int
    @property
    def restrictions(self) -> global___ProjectBatchRestrictions: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        combine_artifacts: builtins.bool = ...,
        service_role: builtins.str = ...,
        timeout_in_mins: builtins.int = ...,
        restrictions: global___ProjectBatchRestrictions | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "restrictions", b"restrictions"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["combine_artifacts", b"combine_artifacts", "resource_info", b"resource_info", "restrictions", b"restrictions", "service_role", b"service_role", "timeout_in_mins", b"timeout_in_mins"]) -> None: ...

global___ProjectProjectBuildBatchConfig = ProjectProjectBuildBatchConfig

@typing_extensions.final
class ProjectProjectCache(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    MODES_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def modes(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    location: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        modes: collections.abc.Iterable[builtins.str] | None = ...,
        location: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["location", b"location", "modes", b"modes", "resource_info", b"resource_info"]) -> None: ...

global___ProjectProjectCache = ProjectProjectCache

@typing_extensions.final
class Project(google.protobuf.message.Message):
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
    VPC_CONFIG_FIELD_NUMBER: builtins.int
    SECONDARY_SOURCES_FIELD_NUMBER: builtins.int
    ENCRYPTION_KEY_FIELD_NUMBER: builtins.int
    SOURCE_VERSION_FIELD_NUMBER: builtins.int
    TRIGGERS_FIELD_NUMBER: builtins.int
    SECONDARY_ARTIFACTS_FIELD_NUMBER: builtins.int
    SOURCE_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    ARTIFACTS_FIELD_NUMBER: builtins.int
    BADGE_ENABLED_FIELD_NUMBER: builtins.int
    LOGS_CONFIG_FIELD_NUMBER: builtins.int
    SERVICE_ROLE_FIELD_NUMBER: builtins.int
    QUEUED_TIMEOUT_IN_MINUTES_FIELD_NUMBER: builtins.int
    FILE_SYSTEM_LOCATIONS_FIELD_NUMBER: builtins.int
    ENVIRONMENT_FIELD_NUMBER: builtins.int
    SECONDARY_SOURCE_VERSIONS_FIELD_NUMBER: builtins.int
    BUILD_BATCH_CONFIG_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    TIMEOUT_IN_MINUTES_FIELD_NUMBER: builtins.int
    CACHE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    @property
    def vpc_config(self) -> global___ProjectVpcConfig: ...
    @property
    def secondary_sources(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectSource]: ...
    encryption_key: builtins.str
    source_version: builtins.str
    @property
    def triggers(self) -> global___ProjectProjectTriggers: ...
    @property
    def secondary_artifacts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectArtifacts]: ...
    @property
    def source(self) -> global___ProjectSource: ...
    name: builtins.str
    @property
    def artifacts(self) -> global___ProjectArtifacts: ...
    badge_enabled: builtins.bool
    @property
    def logs_config(self) -> global___ProjectLogsConfig: ...
    service_role: builtins.str
    queued_timeout_in_minutes: builtins.int
    @property
    def file_system_locations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectProjectFileSystemLocation]: ...
    @property
    def environment(self) -> global___ProjectEnvironment: ...
    @property
    def secondary_source_versions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectProjectSourceVersion]: ...
    @property
    def build_batch_config(self) -> global___ProjectProjectBuildBatchConfig: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    timeout_in_minutes: builtins.int
    @property
    def cache(self) -> global___ProjectProjectCache: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        vpc_config: global___ProjectVpcConfig | None = ...,
        secondary_sources: collections.abc.Iterable[global___ProjectSource] | None = ...,
        encryption_key: builtins.str = ...,
        source_version: builtins.str = ...,
        triggers: global___ProjectProjectTriggers | None = ...,
        secondary_artifacts: collections.abc.Iterable[global___ProjectArtifacts] | None = ...,
        source: global___ProjectSource | None = ...,
        name: builtins.str = ...,
        artifacts: global___ProjectArtifacts | None = ...,
        badge_enabled: builtins.bool = ...,
        logs_config: global___ProjectLogsConfig | None = ...,
        service_role: builtins.str = ...,
        queued_timeout_in_minutes: builtins.int = ...,
        file_system_locations: collections.abc.Iterable[global___ProjectProjectFileSystemLocation] | None = ...,
        environment: global___ProjectEnvironment | None = ...,
        secondary_source_versions: collections.abc.Iterable[global___ProjectProjectSourceVersion] | None = ...,
        build_batch_config: global___ProjectProjectBuildBatchConfig | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        timeout_in_minutes: builtins.int = ...,
        cache: global___ProjectProjectCache | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["artifacts", b"artifacts", "build_batch_config", b"build_batch_config", "cache", b"cache", "environment", b"environment", "logs_config", b"logs_config", "resource_info", b"resource_info", "source", b"source", "triggers", b"triggers", "vpc_config", b"vpc_config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["artifacts", b"artifacts", "badge_enabled", b"badge_enabled", "build_batch_config", b"build_batch_config", "cache", b"cache", "description", b"description", "encryption_key", b"encryption_key", "environment", b"environment", "file_system_locations", b"file_system_locations", "logs_config", b"logs_config", "name", b"name", "queued_timeout_in_minutes", b"queued_timeout_in_minutes", "resource_info", b"resource_info", "secondary_artifacts", b"secondary_artifacts", "secondary_source_versions", b"secondary_source_versions", "secondary_sources", b"secondary_sources", "service_role", b"service_role", "source", b"source", "source_version", b"source_version", "tags", b"tags", "timeout_in_minutes", b"timeout_in_minutes", "triggers", b"triggers", "vpc_config", b"vpc_config"]) -> None: ...

global___Project = Project

@typing_extensions.final
class CodeBuild(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROJECT_FIELD_NUMBER: builtins.int
    REPORT_GROUP_FIELD_NUMBER: builtins.int
    SOURCE_CREDENTIAL_FIELD_NUMBER: builtins.int
    PROJECT_WEBHOOK_FILTER_FIELD_NUMBER: builtins.int
    @property
    def project(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Project]: ...
    @property
    def report_group(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ReportGroup]: ...
    @property
    def source_credential(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SourceCredential]: ...
    @property
    def project_webhook_filter(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProjectWebhookFilter]: ...
    def __init__(
        self,
        *,
        project: collections.abc.Iterable[global___Project] | None = ...,
        report_group: collections.abc.Iterable[global___ReportGroup] | None = ...,
        source_credential: collections.abc.Iterable[global___SourceCredential] | None = ...,
        project_webhook_filter: collections.abc.Iterable[global___ProjectWebhookFilter] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["project", b"project", "project_webhook_filter", b"project_webhook_filter", "report_group", b"report_group", "source_credential", b"source_credential"]) -> None: ...

global___CodeBuild = CodeBuild

@typing_extensions.final
class ReportGroupS3ReportExportConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    BUCKET_FIELD_NUMBER: builtins.int
    PACKAGING_FIELD_NUMBER: builtins.int
    ENCRYPTION_KEY_FIELD_NUMBER: builtins.int
    ENCRYPTION_DISABLED_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    path: builtins.str
    bucket: builtins.str
    packaging: builtins.str
    encryption_key: builtins.str
    encryption_disabled: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        path: builtins.str = ...,
        bucket: builtins.str = ...,
        packaging: builtins.str = ...,
        encryption_key: builtins.str = ...,
        encryption_disabled: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bucket", b"bucket", "encryption_disabled", b"encryption_disabled", "encryption_key", b"encryption_key", "packaging", b"packaging", "path", b"path", "resource_info", b"resource_info"]) -> None: ...

global___ReportGroupS3ReportExportConfig = ReportGroupS3ReportExportConfig

@typing_extensions.final
class ReportGroupReportExportConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    S3_DESTINATION_FIELD_NUMBER: builtins.int
    EXPORT_CONFIG_TYPE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def s3_destination(self) -> global___ReportGroupS3ReportExportConfig: ...
    export_config_type: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        s3_destination: global___ReportGroupS3ReportExportConfig | None = ...,
        export_config_type: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "s3_destination", b"s3_destination"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["export_config_type", b"export_config_type", "resource_info", b"resource_info", "s3_destination", b"s3_destination"]) -> None: ...

global___ReportGroupReportExportConfig = ReportGroupReportExportConfig

@typing_extensions.final
class ReportGroup(google.protobuf.message.Message):
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
    TYPE_FIELD_NUMBER: builtins.int
    EXPORT_CONFIG_FIELD_NUMBER: builtins.int
    DELETE_REPORTS_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    type: builtins.str
    @property
    def export_config(self) -> global___ReportGroupReportExportConfig: ...
    delete_reports: builtins.bool
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        type: builtins.str = ...,
        export_config: global___ReportGroupReportExportConfig | None = ...,
        delete_reports: builtins.bool = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["export_config", b"export_config", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["delete_reports", b"delete_reports", "export_config", b"export_config", "name", b"name", "resource_info", b"resource_info", "tags", b"tags", "type", b"type"]) -> None: ...

global___ReportGroup = ReportGroup

@typing_extensions.final
class SourceCredential(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    SERVER_TYPE_FIELD_NUMBER: builtins.int
    USERNAME_FIELD_NUMBER: builtins.int
    TOKEN_FIELD_NUMBER: builtins.int
    AUTH_TYPE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    server_type: builtins.str
    username: builtins.str
    token: builtins.str
    auth_type: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        server_type: builtins.str = ...,
        username: builtins.str = ...,
        token: builtins.str = ...,
        auth_type: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auth_type", b"auth_type", "resource_info", b"resource_info", "server_type", b"server_type", "token", b"token", "username", b"username"]) -> None: ...

global___SourceCredential = SourceCredential

@typing_extensions.final
class ProjectWebhookFilter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    PATTERN_FIELD_NUMBER: builtins.int
    EXCLUDE_MATCHED_PATTERN_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    pattern: builtins.str
    exclude_matched_pattern: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        pattern: builtins.str = ...,
        exclude_matched_pattern: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["exclude_matched_pattern", b"exclude_matched_pattern", "pattern", b"pattern", "resource_info", b"resource_info"]) -> None: ...

global___ProjectWebhookFilter = ProjectWebhookFilter
