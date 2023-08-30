# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_project.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15gcp/gcp_project.proto\x12\x17oak9.tython.gcp.project\x1a\x13shared/shared.proto\"P\n\x10ProjectXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0c\n\x04read\x18\x03 \x01(\t\x12\x0e\n\x06update\x18\x04 \x01(\t\"\x98\x03\n\x07Project\x12\x1b\n\x13\x61uto_create_network\x18\x01 \x01(\x08\x12\x17\n\x0f\x62illing_account\x18\x02 \x01(\t\x12\x11\n\tfolder_id\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\t\x12<\n\x06labels\x18\x05 \x03(\x0b\x32,.oak9.tython.gcp.project.Project.LabelsEntry\x12\x0c\n\x04name\x18\x06 \x01(\t\x12\x0e\n\x06number\x18\x07 \x01(\t\x12\x0e\n\x06org_id\x18\x08 \x01(\t\x12\x12\n\nproject_id\x18\t \x01(\t\x12\x13\n\x0bskip_delete\x18\n \x01(\x08\x12;\n\x08timeouts\x18\x0b \x01(\x0b\x32).oak9.tython.gcp.project.ProjectXTimeouts\x12\x37\n\rresource_info\x18\x0c \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"a\n.ProjectAccessApprovalSettingsXEnrolledServices\x12\x15\n\rcloud_product\x18\x01 \x01(\t\x12\x18\n\x10\x65nrollment_level\x18\x02 \x01(\t\"X\n&ProjectAccessApprovalSettingsXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\xe8\x03\n\x1dProjectAccessApprovalSettings\x12\x1a\n\x12\x61\x63tive_key_version\x18\x01 \x01(\t\x12\'\n\x1f\x61ncestor_has_active_key_version\x18\x02 \x01(\x08\x12\x19\n\x11\x65nrolled_ancestor\x18\x03 \x01(\x08\x12\n\n\x02id\x18\x04 \x01(\t\x12\x1b\n\x13invalid_key_version\x18\x05 \x01(\x08\x12\x0c\n\x04name\x18\x06 \x01(\t\x12\x1b\n\x13notification_emails\x18\x07 \x03(\t\x12\x0f\n\x07project\x18\x08 \x01(\t\x12\x12\n\nproject_id\x18\t \x01(\t\x12\x62\n\x11\x65nrolled_services\x18\n \x03(\x0b\x32G.oak9.tython.gcp.project.ProjectAccessApprovalSettingsXEnrolledServices\x12Q\n\x08timeouts\x18\x0b \x01(\x0b\x32?.oak9.tython.gcp.project.ProjectAccessApprovalSettingsXTimeouts\x12\x37\n\rresource_info\x18\x0c \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"V\n&ProjectDefaultServiceAccountsXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0c\n\x04read\x18\x03 \x01(\t\"\x8f\x03\n\x1dProjectDefaultServiceAccounts\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07project\x18\x03 \x01(\t\x12\x16\n\x0erestore_policy\x18\x04 \x01(\t\x12\x65\n\x10service_accounts\x18\x05 \x03(\x0b\x32K.oak9.tython.gcp.project.ProjectDefaultServiceAccounts.ServiceAccountsEntry\x12Q\n\x08timeouts\x18\x06 \x01(\x0b\x32?.oak9.tython.gcp.project.ProjectDefaultServiceAccountsXTimeouts\x12\x37\n\rresource_info\x18\x07 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a\x36\n\x14ServiceAccountsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"R\n$ProjectIamAuditConfigXAuditLogConfig\x12\x18\n\x10\x65xempted_members\x18\x01 \x03(\t\x12\x10\n\x08log_type\x18\x02 \x01(\t\"\xe5\x01\n\x15ProjectIamAuditConfig\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07project\x18\x03 \x01(\t\x12\x0f\n\x07service\x18\x04 \x01(\t\x12W\n\x10\x61udit_log_config\x18\x05 \x03(\x0b\x32=.oak9.tython.gcp.project.ProjectIamAuditConfigXAuditLogConfig\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"U\n\x1bProjectIamBindingXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\xdf\x01\n\x11ProjectIamBinding\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07members\x18\x03 \x03(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\x12G\n\tcondition\x18\x06 \x01(\x0b\x32\x34.oak9.tython.gcp.project.ProjectIamBindingXCondition\x12\x37\n\rresource_info\x18\x07 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xe4\x01\n\x14ProjectIamCustomRole\x12\x0f\n\x07\x64\x65leted\x18\x01 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0bpermissions\x18\x05 \x03(\t\x12\x0f\n\x07project\x18\x06 \x01(\t\x12\x0f\n\x07role_id\x18\x07 \x01(\t\x12\r\n\x05stage\x18\x08 \x01(\t\x12\r\n\x05title\x18\t \x01(\t\x12\x37\n\rresource_info\x18\n \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"T\n\x1aProjectIamMemberXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\xdc\x01\n\x10ProjectIamMember\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06member\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\x12\x46\n\tcondition\x18\x06 \x01(\x0b\x32\x33.oak9.tython.gcp.project.ProjectIamMemberXCondition\x12\x37\n\rresource_info\x18\x07 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x8b\x01\n\x10ProjectIamPolicy\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x13\n\x0bpolicy_data\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\";\n\'ProjectOrganizationPolicyXBooleanPolicy\x12\x10\n\x08\x65nforced\x18\x01 \x01(\x08\"I\n*ProjectOrganizationPolicyXListPolicyXAllow\x12\x0b\n\x03\x61ll\x18\x01 \x01(\x08\x12\x0e\n\x06values\x18\x02 \x03(\t\"H\n)ProjectOrganizationPolicyXListPolicyXDeny\x12\x0b\n\x03\x61ll\x18\x01 \x01(\x08\x12\x0e\n\x06values\x18\x02 \x03(\t\"\x82\x02\n$ProjectOrganizationPolicyXListPolicy\x12\x1b\n\x13inherit_from_parent\x18\x01 \x01(\x08\x12\x17\n\x0fsuggested_value\x18\x02 \x01(\t\x12R\n\x05\x61llow\x18\x03 \x01(\x0b\x32\x43.oak9.tython.gcp.project.ProjectOrganizationPolicyXListPolicyXAllow\x12P\n\x04\x64\x65ny\x18\x04 \x01(\x0b\x32\x42.oak9.tython.gcp.project.ProjectOrganizationPolicyXListPolicyXDeny\":\n\'ProjectOrganizationPolicyXRestorePolicy\x12\x0f\n\x07\x64\x65\x66\x61ult\x18\x01 \x01(\x08\"b\n\"ProjectOrganizationPolicyXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0c\n\x04read\x18\x03 \x01(\t\x12\x0e\n\x06update\x18\x04 \x01(\t\"\x90\x04\n\x19ProjectOrganizationPolicy\x12\x12\n\nconstraint\x18\x01 \x01(\t\x12\x0c\n\x04\x65tag\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x13\n\x0bupdate_time\x18\x05 \x01(\t\x12\x0f\n\x07version\x18\x06 \x01(\x01\x12X\n\x0e\x62oolean_policy\x18\x07 \x01(\x0b\x32@.oak9.tython.gcp.project.ProjectOrganizationPolicyXBooleanPolicy\x12R\n\x0blist_policy\x18\x08 \x01(\x0b\x32=.oak9.tython.gcp.project.ProjectOrganizationPolicyXListPolicy\x12X\n\x0erestore_policy\x18\t \x01(\x0b\x32@.oak9.tython.gcp.project.ProjectOrganizationPolicyXRestorePolicy\x12M\n\x08timeouts\x18\n \x01(\x0b\x32;.oak9.tython.gcp.project.ProjectOrganizationPolicyXTimeouts\x12\x37\n\rresource_info\x18\x0b \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"W\n\x17ProjectServiceXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0c\n\x04read\x18\x03 \x01(\t\x12\x0e\n\x06update\x18\x04 \x01(\t\"\xfb\x01\n\x0eProjectService\x12\"\n\x1a\x64isable_dependent_services\x18\x01 \x01(\x08\x12\x1a\n\x12\x64isable_on_destroy\x18\x02 \x01(\x08\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x0f\n\x07service\x18\x05 \x01(\t\x12\x42\n\x08timeouts\x18\x06 \x01(\x0b\x32\x30.oak9.tython.gcp.project.ProjectServiceXTimeouts\x12\x37\n\rresource_info\x18\x07 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"C\n!ProjectUsageExportBucketXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\"\xe3\x01\n\x18ProjectUsageExportBucket\x12\x13\n\x0b\x62ucket_name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06prefix\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12L\n\x08timeouts\x18\x05 \x01(\x0b\x32:.oak9.tython.gcp.project.ProjectUsageExportBucketXTimeouts\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_project_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PROJECT_LABELSENTRY._options = None
  _PROJECT_LABELSENTRY._serialized_options = b'8\001'
  _PROJECTDEFAULTSERVICEACCOUNTS_SERVICEACCOUNTSENTRY._options = None
  _PROJECTDEFAULTSERVICEACCOUNTS_SERVICEACCOUNTSENTRY._serialized_options = b'8\001'
  _PROJECTXTIMEOUTS._serialized_start=71
  _PROJECTXTIMEOUTS._serialized_end=151
  _PROJECT._serialized_start=154
  _PROJECT._serialized_end=562
  _PROJECT_LABELSENTRY._serialized_start=517
  _PROJECT_LABELSENTRY._serialized_end=562
  _PROJECTACCESSAPPROVALSETTINGSXENROLLEDSERVICES._serialized_start=564
  _PROJECTACCESSAPPROVALSETTINGSXENROLLEDSERVICES._serialized_end=661
  _PROJECTACCESSAPPROVALSETTINGSXTIMEOUTS._serialized_start=663
  _PROJECTACCESSAPPROVALSETTINGSXTIMEOUTS._serialized_end=751
  _PROJECTACCESSAPPROVALSETTINGS._serialized_start=754
  _PROJECTACCESSAPPROVALSETTINGS._serialized_end=1242
  _PROJECTDEFAULTSERVICEACCOUNTSXTIMEOUTS._serialized_start=1244
  _PROJECTDEFAULTSERVICEACCOUNTSXTIMEOUTS._serialized_end=1330
  _PROJECTDEFAULTSERVICEACCOUNTS._serialized_start=1333
  _PROJECTDEFAULTSERVICEACCOUNTS._serialized_end=1732
  _PROJECTDEFAULTSERVICEACCOUNTS_SERVICEACCOUNTSENTRY._serialized_start=1678
  _PROJECTDEFAULTSERVICEACCOUNTS_SERVICEACCOUNTSENTRY._serialized_end=1732
  _PROJECTIAMAUDITCONFIGXAUDITLOGCONFIG._serialized_start=1734
  _PROJECTIAMAUDITCONFIGXAUDITLOGCONFIG._serialized_end=1816
  _PROJECTIAMAUDITCONFIG._serialized_start=1819
  _PROJECTIAMAUDITCONFIG._serialized_end=2048
  _PROJECTIAMBINDINGXCONDITION._serialized_start=2050
  _PROJECTIAMBINDINGXCONDITION._serialized_end=2135
  _PROJECTIAMBINDING._serialized_start=2138
  _PROJECTIAMBINDING._serialized_end=2361
  _PROJECTIAMCUSTOMROLE._serialized_start=2364
  _PROJECTIAMCUSTOMROLE._serialized_end=2592
  _PROJECTIAMMEMBERXCONDITION._serialized_start=2594
  _PROJECTIAMMEMBERXCONDITION._serialized_end=2678
  _PROJECTIAMMEMBER._serialized_start=2681
  _PROJECTIAMMEMBER._serialized_end=2901
  _PROJECTIAMPOLICY._serialized_start=2904
  _PROJECTIAMPOLICY._serialized_end=3043
  _PROJECTORGANIZATIONPOLICYXBOOLEANPOLICY._serialized_start=3045
  _PROJECTORGANIZATIONPOLICYXBOOLEANPOLICY._serialized_end=3104
  _PROJECTORGANIZATIONPOLICYXLISTPOLICYXALLOW._serialized_start=3106
  _PROJECTORGANIZATIONPOLICYXLISTPOLICYXALLOW._serialized_end=3179
  _PROJECTORGANIZATIONPOLICYXLISTPOLICYXDENY._serialized_start=3181
  _PROJECTORGANIZATIONPOLICYXLISTPOLICYXDENY._serialized_end=3253
  _PROJECTORGANIZATIONPOLICYXLISTPOLICY._serialized_start=3256
  _PROJECTORGANIZATIONPOLICYXLISTPOLICY._serialized_end=3514
  _PROJECTORGANIZATIONPOLICYXRESTOREPOLICY._serialized_start=3516
  _PROJECTORGANIZATIONPOLICYXRESTOREPOLICY._serialized_end=3574
  _PROJECTORGANIZATIONPOLICYXTIMEOUTS._serialized_start=3576
  _PROJECTORGANIZATIONPOLICYXTIMEOUTS._serialized_end=3674
  _PROJECTORGANIZATIONPOLICY._serialized_start=3677
  _PROJECTORGANIZATIONPOLICY._serialized_end=4205
  _PROJECTSERVICEXTIMEOUTS._serialized_start=4207
  _PROJECTSERVICEXTIMEOUTS._serialized_end=4294
  _PROJECTSERVICE._serialized_start=4297
  _PROJECTSERVICE._serialized_end=4548
  _PROJECTUSAGEEXPORTBUCKETXTIMEOUTS._serialized_start=4550
  _PROJECTUSAGEEXPORTBUCKETXTIMEOUTS._serialized_end=4617
  _PROJECTUSAGEEXPORTBUCKET._serialized_start=4620
  _PROJECTUSAGEEXPORTBUCKET._serialized_end=4847
# @@protoc_insertion_point(module_scope)
