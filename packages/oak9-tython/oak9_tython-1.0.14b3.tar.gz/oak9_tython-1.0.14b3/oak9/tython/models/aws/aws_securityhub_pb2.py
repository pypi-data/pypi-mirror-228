# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_securityhub.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x61ws/aws_securityhub.proto\x12\x1boak9.tython.aws.securityhub\x1a\x13shared/shared.proto\"\xa5\x01\n\x03Hub\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x38\n\x04tags\x18\x02 \x03(\x0b\x32*.oak9.tython.aws.securityhub.Hub.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"<\n\x0bSecurityHub\x12-\n\x03hub\x18\x01 \x03(\x0b\x32 .oak9.tython.aws.securityhub.Hubb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_securityhub_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _HUB_TAGSENTRY._options = None
  _HUB_TAGSENTRY._serialized_options = b'8\001'
  _HUB._serialized_start=80
  _HUB._serialized_end=245
  _HUB_TAGSENTRY._serialized_start=202
  _HUB_TAGSENTRY._serialized_end=245
  _SECURITYHUB._serialized_start=247
  _SECURITYHUB._serialized_end=307
# @@protoc_insertion_point(module_scope)
