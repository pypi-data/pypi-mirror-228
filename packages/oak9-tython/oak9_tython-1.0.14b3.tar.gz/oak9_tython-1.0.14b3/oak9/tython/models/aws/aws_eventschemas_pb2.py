# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_eventschemas.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x61ws/aws_eventschemas.proto\x12\x1coak9.tython.aws.eventschemas\x1a\x13shared/shared.proto\"j\n\x13\x44iscovererTagsEntry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\"\xaf\x01\n\nDiscoverer\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\nsource_arn\x18\x03 \x01(\t\x12?\n\x04tags\x18\x04 \x03(\x0b\x32\x31.oak9.tython.aws.eventschemas.DiscovererTagsEntry\"\x83\x02\n\x0c\x45ventSchemas\x12<\n\ndiscoverer\x18\x01 \x03(\x0b\x32(.oak9.tython.aws.eventschemas.Discoverer\x12\x38\n\x08registry\x18\x02 \x03(\x0b\x32&.oak9.tython.aws.eventschemas.Registry\x12\x45\n\x0fregistry_policy\x18\x03 \x03(\x0b\x32,.oak9.tython.aws.eventschemas.RegistryPolicy\x12\x34\n\x06schema\x18\x04 \x03(\x0b\x32$.oak9.tython.aws.eventschemas.Schema\"h\n\x11RegistryTagsEntry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\"\xae\x01\n\x08Registry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x15\n\rregistry_name\x18\x03 \x01(\t\x12=\n\x04tags\x18\x04 \x03(\x0b\x32/.oak9.tython.aws.eventschemas.RegistryTagsEntry\"\xee\x01\n\x0eRegistryPolicy\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12H\n\x06policy\x18\x02 \x03(\x0b\x32\x38.oak9.tython.aws.eventschemas.RegistryPolicy.PolicyEntry\x12\x15\n\rregistry_name\x18\x03 \x01(\t\x12\x13\n\x0brevision_id\x18\x04 \x01(\t\x1a-\n\x0bPolicyEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"f\n\x0fSchemaTagsEntry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\"\xde\x01\n\x06Schema\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x15\n\rregistry_name\x18\x05 \x01(\t\x12\x13\n\x0bschema_name\x18\x06 \x01(\t\x12;\n\x04tags\x18\x07 \x03(\x0b\x32-.oak9.tython.aws.eventschemas.SchemaTagsEntryb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_eventschemas_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTRYPOLICY_POLICYENTRY._options = None
  _REGISTRYPOLICY_POLICYENTRY._serialized_options = b'8\001'
  _DISCOVERERTAGSENTRY._serialized_start=81
  _DISCOVERERTAGSENTRY._serialized_end=187
  _DISCOVERER._serialized_start=190
  _DISCOVERER._serialized_end=365
  _EVENTSCHEMAS._serialized_start=368
  _EVENTSCHEMAS._serialized_end=627
  _REGISTRYTAGSENTRY._serialized_start=629
  _REGISTRYTAGSENTRY._serialized_end=733
  _REGISTRY._serialized_start=736
  _REGISTRY._serialized_end=910
  _REGISTRYPOLICY._serialized_start=913
  _REGISTRYPOLICY._serialized_end=1151
  _REGISTRYPOLICY_POLICYENTRY._serialized_start=1106
  _REGISTRYPOLICY_POLICYENTRY._serialized_end=1151
  _SCHEMATAGSENTRY._serialized_start=1153
  _SCHEMATAGSENTRY._serialized_end=1255
  _SCHEMA._serialized_start=1258
  _SCHEMA._serialized_end=1480
# @@protoc_insertion_point(module_scope)
