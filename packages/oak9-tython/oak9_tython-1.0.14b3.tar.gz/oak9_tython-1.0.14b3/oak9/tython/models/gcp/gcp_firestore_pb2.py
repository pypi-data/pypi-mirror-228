# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_firestore.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17gcp/gcp_firestore.proto\x12\x19oak9.tython.gcp.firestore\x1a\x13shared/shared.proto\"L\n\x1a\x46irestoreDocumentXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\xc3\x02\n\x11\x46irestoreDocument\x12\x12\n\ncollection\x18\x01 \x01(\t\x12\x13\n\x0b\x63reate_time\x18\x02 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x03 \x01(\t\x12\x13\n\x0b\x64ocument_id\x18\x04 \x01(\t\x12\x0e\n\x06\x66ields\x18\x05 \x01(\t\x12\n\n\x02id\x18\x06 \x01(\t\x12\x0c\n\x04name\x18\x07 \x01(\t\x12\x0c\n\x04path\x18\x08 \x01(\t\x12\x0f\n\x07project\x18\t \x01(\t\x12\x13\n\x0bupdate_time\x18\n \x01(\t\x12G\n\x08timeouts\x18\x0b \x01(\x0b\x32\x35.oak9.tython.gcp.firestore.FirestoreDocumentXTimeouts\x12\x37\n\rresource_info\x18\x0c \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"P\n\x15\x46irestoreIndexXFields\x12\x14\n\x0c\x61rray_config\x18\x01 \x01(\t\x12\x12\n\nfield_path\x18\x02 \x01(\t\x12\r\n\x05order\x18\x03 \x01(\t\"9\n\x17\x46irestoreIndexXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\"\xb7\x02\n\x0e\x46irestoreIndex\x12\x12\n\ncollection\x18\x01 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07project\x18\x05 \x01(\t\x12\x13\n\x0bquery_scope\x18\x06 \x01(\t\x12@\n\x06\x66ields\x18\x07 \x03(\x0b\x32\x30.oak9.tython.gcp.firestore.FirestoreIndexXFields\x12\x44\n\x08timeouts\x18\x08 \x01(\x0b\x32\x32.oak9.tython.gcp.firestore.FirestoreIndexXTimeouts\x12\x37\n\rresource_info\x18\t \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_firestore_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FIRESTOREDOCUMENTXTIMEOUTS._serialized_start=75
  _FIRESTOREDOCUMENTXTIMEOUTS._serialized_end=151
  _FIRESTOREDOCUMENT._serialized_start=154
  _FIRESTOREDOCUMENT._serialized_end=477
  _FIRESTOREINDEXXFIELDS._serialized_start=479
  _FIRESTOREINDEXXFIELDS._serialized_end=559
  _FIRESTOREINDEXXTIMEOUTS._serialized_start=561
  _FIRESTOREINDEXXTIMEOUTS._serialized_end=618
  _FIRESTOREINDEX._serialized_start=621
  _FIRESTOREINDEX._serialized_end=932
# @@protoc_insertion_point(module_scope)
