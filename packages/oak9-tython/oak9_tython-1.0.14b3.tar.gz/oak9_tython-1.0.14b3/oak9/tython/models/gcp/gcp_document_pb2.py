# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_document.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16gcp/gcp_document.proto\x12\x18oak9.tython.gcp.document\x1a\x13shared/shared.proto\">\n\x1c\x44ocumentAiProcessorXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\"\x8f\x02\n\x13\x44ocumentAiProcessor\x12\x14\n\x0c\x64isplay_name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x14\n\x0ckms_key_name\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x0f\n\x07project\x18\x06 \x01(\t\x12\x0c\n\x04type\x18\x07 \x01(\t\x12H\n\x08timeouts\x18\x08 \x01(\x0b\x32\x36.oak9.tython.gcp.document.DocumentAiProcessorXTimeouts\x12\x37\n\rresource_info\x18\t \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"L\n*DocumentAiProcessorDefaultVersionXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\"\xe4\x01\n!DocumentAiProcessorDefaultVersion\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tprocessor\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12V\n\x08timeouts\x18\x04 \x01(\x0b\x32\x44.oak9.tython.gcp.document.DocumentAiProcessorDefaultVersionXTimeouts\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_document_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DOCUMENTAIPROCESSORXTIMEOUTS._serialized_start=73
  _DOCUMENTAIPROCESSORXTIMEOUTS._serialized_end=135
  _DOCUMENTAIPROCESSOR._serialized_start=138
  _DOCUMENTAIPROCESSOR._serialized_end=409
  _DOCUMENTAIPROCESSORDEFAULTVERSIONXTIMEOUTS._serialized_start=411
  _DOCUMENTAIPROCESSORDEFAULTVERSIONXTIMEOUTS._serialized_end=487
  _DOCUMENTAIPROCESSORDEFAULTVERSION._serialized_start=490
  _DOCUMENTAIPROCESSORDEFAULTVERSION._serialized_end=718
# @@protoc_insertion_point(module_scope)
