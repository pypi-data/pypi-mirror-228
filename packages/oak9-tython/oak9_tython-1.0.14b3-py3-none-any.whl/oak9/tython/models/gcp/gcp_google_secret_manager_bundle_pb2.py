# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_google_secret_manager_bundle.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2
from oak9.tython.models.gcp import gcp_secret_pb2 as gcp_dot_gcp__secret__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*gcp/gcp_google_secret_manager_bundle.proto\x12,oak9.tython.gcp.google_secret_manager_bundle\x1a\x13shared/shared.proto\x1a\x14gcp/gcp_secret.proto\"\xde\x03\n\x13GoogleSecretManager\x12J\n\x15secret_manager_secret\x18\x01 \x01(\x0b\x32+.oak9.tython.gcp.secret.SecretManagerSecret\x12`\n!secret_manager_secret_iam_binding\x18\x02 \x03(\x0b\x32\x35.oak9.tython.gcp.secret.SecretManagerSecretIamBinding\x12^\n secret_manager_secret_iam_member\x18\x03 \x03(\x0b\x32\x34.oak9.tython.gcp.secret.SecretManagerSecretIamMember\x12^\n secret_manager_secret_iam_policy\x18\x04 \x03(\x0b\x32\x34.oak9.tython.gcp.secret.SecretManagerSecretIamPolicy\x12Y\n\x1dsecret_manager_secret_version\x18\x05 \x01(\x0b\x32\x32.oak9.tython.gcp.secret.SecretManagerSecretVersionb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_google_secret_manager_bundle_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GOOGLESECRETMANAGER._serialized_start=136
  _GOOGLESECRETMANAGER._serialized_end=614
# @@protoc_insertion_point(module_scope)
