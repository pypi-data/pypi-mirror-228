# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_endpoints.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17gcp/gcp_endpoints.proto\x12\x19oak9.tython.gcp.endpoints\x1a\x13shared/shared.proto\"K\n\x19\x45ndpointsServiceXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\xac\x04\n\x10\x45ndpointsService\x12\x43\n\x04\x61pis\x18\x01 \x03(\x0b\x32\x35.oak9.tython.gcp.endpoints.EndpointsService.ApisEntry\x12\x11\n\tconfig_id\x18\x02 \x01(\t\x12\x13\n\x0b\x64ns_address\x18\x03 \x01(\t\x12M\n\tendpoints\x18\x04 \x03(\x0b\x32:.oak9.tython.gcp.endpoints.EndpointsService.EndpointsEntry\x12\x13\n\x0bgrpc_config\x18\x05 \x01(\t\x12\n\n\x02id\x18\x06 \x01(\t\x12\x16\n\x0eopenapi_config\x18\x07 \x01(\t\x12\x0f\n\x07project\x18\x08 \x01(\t\x12\x1c\n\x14protoc_output_base64\x18\t \x01(\t\x12\x14\n\x0cservice_name\x18\n \x01(\t\x12\x46\n\x08timeouts\x18\x0b \x01(\x0b\x32\x34.oak9.tython.gcp.endpoints.EndpointsServiceXTimeouts\x12\x37\n\rresource_info\x18\x0c \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a+\n\tApisEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x30\n\x0e\x45ndpointsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"g\n-EndpointsServiceConsumersIamBindingXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\xa4\x02\n#EndpointsServiceConsumersIamBinding\x12\x18\n\x10\x63onsumer_project\x18\x01 \x01(\t\x12\x0c\n\x04\x65tag\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0f\n\x07members\x18\x04 \x03(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\x12\x14\n\x0cservice_name\x18\x06 \x01(\t\x12[\n\tcondition\x18\x07 \x01(\x0b\x32H.oak9.tython.gcp.endpoints.EndpointsServiceConsumersIamBindingXCondition\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"f\n,EndpointsServiceConsumersIamMemberXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\xa1\x02\n\"EndpointsServiceConsumersIamMember\x12\x18\n\x10\x63onsumer_project\x18\x01 \x01(\t\x12\x0c\n\x04\x65tag\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0e\n\x06member\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\x12\x14\n\x0cservice_name\x18\x06 \x01(\t\x12Z\n\tcondition\x18\x07 \x01(\x0b\x32G.oak9.tython.gcp.endpoints.EndpointsServiceConsumersIamMemberXCondition\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xbc\x01\n\"EndpointsServiceConsumersIamPolicy\x12\x18\n\x10\x63onsumer_project\x18\x01 \x01(\t\x12\x0c\n\x04\x65tag\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x13\n\x0bpolicy_data\x18\x04 \x01(\t\x12\x14\n\x0cservice_name\x18\x05 \x01(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"^\n$EndpointsServiceIamBindingXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\xf8\x01\n\x1a\x45ndpointsServiceIamBinding\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07members\x18\x03 \x03(\t\x12\x0c\n\x04role\x18\x04 \x01(\t\x12\x14\n\x0cservice_name\x18\x05 \x01(\t\x12R\n\tcondition\x18\x06 \x01(\x0b\x32?.oak9.tython.gcp.endpoints.EndpointsServiceIamBindingXCondition\x12\x37\n\rresource_info\x18\x07 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"]\n#EndpointsServiceIamMemberXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\xf5\x01\n\x19\x45ndpointsServiceIamMember\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06member\x18\x03 \x01(\t\x12\x0c\n\x04role\x18\x04 \x01(\t\x12\x14\n\x0cservice_name\x18\x05 \x01(\t\x12Q\n\tcondition\x18\x06 \x01(\x0b\x32>.oak9.tython.gcp.endpoints.EndpointsServiceIamMemberXCondition\x12\x37\n\rresource_info\x18\x07 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x99\x01\n\x19\x45ndpointsServiceIamPolicy\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x13\n\x0bpolicy_data\x18\x03 \x01(\t\x12\x14\n\x0cservice_name\x18\x04 \x01(\t\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_endpoints_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ENDPOINTSSERVICE_APISENTRY._options = None
  _ENDPOINTSSERVICE_APISENTRY._serialized_options = b'8\001'
  _ENDPOINTSSERVICE_ENDPOINTSENTRY._options = None
  _ENDPOINTSSERVICE_ENDPOINTSENTRY._serialized_options = b'8\001'
  _ENDPOINTSSERVICEXTIMEOUTS._serialized_start=75
  _ENDPOINTSSERVICEXTIMEOUTS._serialized_end=150
  _ENDPOINTSSERVICE._serialized_start=153
  _ENDPOINTSSERVICE._serialized_end=709
  _ENDPOINTSSERVICE_APISENTRY._serialized_start=616
  _ENDPOINTSSERVICE_APISENTRY._serialized_end=659
  _ENDPOINTSSERVICE_ENDPOINTSENTRY._serialized_start=661
  _ENDPOINTSSERVICE_ENDPOINTSENTRY._serialized_end=709
  _ENDPOINTSSERVICECONSUMERSIAMBINDINGXCONDITION._serialized_start=711
  _ENDPOINTSSERVICECONSUMERSIAMBINDINGXCONDITION._serialized_end=814
  _ENDPOINTSSERVICECONSUMERSIAMBINDING._serialized_start=817
  _ENDPOINTSSERVICECONSUMERSIAMBINDING._serialized_end=1109
  _ENDPOINTSSERVICECONSUMERSIAMMEMBERXCONDITION._serialized_start=1111
  _ENDPOINTSSERVICECONSUMERSIAMMEMBERXCONDITION._serialized_end=1213
  _ENDPOINTSSERVICECONSUMERSIAMMEMBER._serialized_start=1216
  _ENDPOINTSSERVICECONSUMERSIAMMEMBER._serialized_end=1505
  _ENDPOINTSSERVICECONSUMERSIAMPOLICY._serialized_start=1508
  _ENDPOINTSSERVICECONSUMERSIAMPOLICY._serialized_end=1696
  _ENDPOINTSSERVICEIAMBINDINGXCONDITION._serialized_start=1698
  _ENDPOINTSSERVICEIAMBINDINGXCONDITION._serialized_end=1792
  _ENDPOINTSSERVICEIAMBINDING._serialized_start=1795
  _ENDPOINTSSERVICEIAMBINDING._serialized_end=2043
  _ENDPOINTSSERVICEIAMMEMBERXCONDITION._serialized_start=2045
  _ENDPOINTSSERVICEIAMMEMBERXCONDITION._serialized_end=2138
  _ENDPOINTSSERVICEIAMMEMBER._serialized_start=2141
  _ENDPOINTSSERVICEIAMMEMBER._serialized_end=2386
  _ENDPOINTSSERVICEIAMPOLICY._serialized_start=2389
  _ENDPOINTSSERVICEIAMPOLICY._serialized_end=2542
# @@protoc_insertion_point(module_scope)
