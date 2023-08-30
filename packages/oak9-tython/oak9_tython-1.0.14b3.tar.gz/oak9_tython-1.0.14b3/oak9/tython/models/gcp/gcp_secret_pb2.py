# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_secret.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14gcp/gcp_secret.proto\x12\x16oak9.tython.gcp.secret\x1a\x13shared/shared.proto\"f\nNSecretManagerSecretXReplicationXUserManagedXReplicasXCustomerManagedEncryption\x12\x14\n\x0ckms_key_name\x18\x01 \x01(\t\"\xd6\x01\n4SecretManagerSecretXReplicationXUserManagedXReplicas\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x8b\x01\n\x1b\x63ustomer_managed_encryption\x18\x02 \x01(\x0b\x32\x66.oak9.tython.gcp.secret.SecretManagerSecretXReplicationXUserManagedXReplicasXCustomerManagedEncryption\"\x8d\x01\n+SecretManagerSecretXReplicationXUserManaged\x12^\n\x08replicas\x18\x01 \x03(\x0b\x32L.oak9.tython.gcp.secret.SecretManagerSecretXReplicationXUserManagedXReplicas\"\x8f\x01\n\x1fSecretManagerSecretXReplication\x12\x11\n\tautomatic\x18\x01 \x01(\x08\x12Y\n\x0cuser_managed\x18\x02 \x01(\x0b\x32\x43.oak9.tython.gcp.secret.SecretManagerSecretXReplicationXUserManaged\"S\n\x1cSecretManagerSecretXRotation\x12\x1a\n\x12next_rotation_time\x18\x01 \x01(\t\x12\x17\n\x0frotation_period\x18\x02 \x01(\t\"N\n\x1cSecretManagerSecretXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"*\n\x1aSecretManagerSecretXTopics\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xdd\x04\n\x13SecretManagerSecret\x12\x13\n\x0b\x63reate_time\x18\x01 \x01(\t\x12\x13\n\x0b\x65xpire_time\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12G\n\x06labels\x18\x04 \x03(\x0b\x32\x37.oak9.tython.gcp.secret.SecretManagerSecret.LabelsEntry\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x0f\n\x07project\x18\x06 \x01(\t\x12\x11\n\tsecret_id\x18\x07 \x01(\t\x12\x0b\n\x03ttl\x18\x08 \x01(\t\x12L\n\x0breplication\x18\t \x01(\x0b\x32\x37.oak9.tython.gcp.secret.SecretManagerSecretXReplication\x12\x46\n\x08rotation\x18\n \x01(\x0b\x32\x34.oak9.tython.gcp.secret.SecretManagerSecretXRotation\x12\x46\n\x08timeouts\x18\x0b \x01(\x0b\x32\x34.oak9.tython.gcp.secret.SecretManagerSecretXTimeouts\x12\x42\n\x06topics\x18\x0c \x03(\x0b\x32\x32.oak9.tython.gcp.secret.SecretManagerSecretXTopics\x12\x37\n\rresource_info\x18\r \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"a\n\'SecretManagerSecretIamBindingXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\x89\x02\n\x1dSecretManagerSecretIamBinding\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07members\x18\x03 \x03(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\x12\x11\n\tsecret_id\x18\x06 \x01(\t\x12R\n\tcondition\x18\x07 \x01(\x0b\x32?.oak9.tython.gcp.secret.SecretManagerSecretIamBindingXCondition\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"`\n&SecretManagerSecretIamMemberXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\x86\x02\n\x1cSecretManagerSecretIamMember\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06member\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\x12\x11\n\tsecret_id\x18\x06 \x01(\t\x12Q\n\tcondition\x18\x07 \x01(\x0b\x32>.oak9.tython.gcp.secret.SecretManagerSecretIamMemberXCondition\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xaa\x01\n\x1cSecretManagerSecretIamPolicy\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x13\n\x0bpolicy_data\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x11\n\tsecret_id\x18\x05 \x01(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"E\n#SecretManagerSecretVersionXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\"\x9f\x02\n\x1aSecretManagerSecretVersion\x12\x13\n\x0b\x63reate_time\x18\x01 \x01(\t\x12\x14\n\x0c\x64\x65stroy_time\x18\x02 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x03 \x01(\x08\x12\n\n\x02id\x18\x04 \x01(\t\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x0e\n\x06secret\x18\x06 \x01(\t\x12\x13\n\x0bsecret_data\x18\x07 \x01(\t\x12M\n\x08timeouts\x18\x08 \x01(\x0b\x32;.oak9.tython.gcp.secret.SecretManagerSecretVersionXTimeouts\x12\x37\n\rresource_info\x18\t \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_secret_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SECRETMANAGERSECRET_LABELSENTRY._options = None
  _SECRETMANAGERSECRET_LABELSENTRY._serialized_options = b'8\001'
  _SECRETMANAGERSECRETXREPLICATIONXUSERMANAGEDXREPLICASXCUSTOMERMANAGEDENCRYPTION._serialized_start=69
  _SECRETMANAGERSECRETXREPLICATIONXUSERMANAGEDXREPLICASXCUSTOMERMANAGEDENCRYPTION._serialized_end=171
  _SECRETMANAGERSECRETXREPLICATIONXUSERMANAGEDXREPLICAS._serialized_start=174
  _SECRETMANAGERSECRETXREPLICATIONXUSERMANAGEDXREPLICAS._serialized_end=388
  _SECRETMANAGERSECRETXREPLICATIONXUSERMANAGED._serialized_start=391
  _SECRETMANAGERSECRETXREPLICATIONXUSERMANAGED._serialized_end=532
  _SECRETMANAGERSECRETXREPLICATION._serialized_start=535
  _SECRETMANAGERSECRETXREPLICATION._serialized_end=678
  _SECRETMANAGERSECRETXROTATION._serialized_start=680
  _SECRETMANAGERSECRETXROTATION._serialized_end=763
  _SECRETMANAGERSECRETXTIMEOUTS._serialized_start=765
  _SECRETMANAGERSECRETXTIMEOUTS._serialized_end=843
  _SECRETMANAGERSECRETXTOPICS._serialized_start=845
  _SECRETMANAGERSECRETXTOPICS._serialized_end=887
  _SECRETMANAGERSECRET._serialized_start=890
  _SECRETMANAGERSECRET._serialized_end=1495
  _SECRETMANAGERSECRET_LABELSENTRY._serialized_start=1450
  _SECRETMANAGERSECRET_LABELSENTRY._serialized_end=1495
  _SECRETMANAGERSECRETIAMBINDINGXCONDITION._serialized_start=1497
  _SECRETMANAGERSECRETIAMBINDINGXCONDITION._serialized_end=1594
  _SECRETMANAGERSECRETIAMBINDING._serialized_start=1597
  _SECRETMANAGERSECRETIAMBINDING._serialized_end=1862
  _SECRETMANAGERSECRETIAMMEMBERXCONDITION._serialized_start=1864
  _SECRETMANAGERSECRETIAMMEMBERXCONDITION._serialized_end=1960
  _SECRETMANAGERSECRETIAMMEMBER._serialized_start=1963
  _SECRETMANAGERSECRETIAMMEMBER._serialized_end=2225
  _SECRETMANAGERSECRETIAMPOLICY._serialized_start=2228
  _SECRETMANAGERSECRETIAMPOLICY._serialized_end=2398
  _SECRETMANAGERSECRETVERSIONXTIMEOUTS._serialized_start=2400
  _SECRETMANAGERSECRETVERSIONXTIMEOUTS._serialized_end=2469
  _SECRETMANAGERSECRETVERSION._serialized_start=2472
  _SECRETMANAGERSECRETVERSION._serialized_end=2759
# @@protoc_insertion_point(module_scope)
