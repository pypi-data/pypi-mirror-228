# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kubernetes/kubernetes_io.k8s.kubeaggregator.pkg.apis.apiregistration.v1.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_apimachinery_dot_pkg_dot_apis_dot_meta_dot_v1__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nMkubernetes/kubernetes_io.k8s.kubeaggregator.pkg.apis.apiregistration.v1.proto\x12:oak9.tython.k8s.kubeaggregator.pkg.apis.apiregistration.v1\x1a\x13shared/shared.proto\x1a@kubernetes/kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1.proto\"\xed\x02\n\nAPIService\x12\x13\n\x0b\x61pi_version\x18\x01 \x01(\t\x12\x0c\n\x04kind\x18\x02 \x01(\t\x12K\n\x08metadata\x18\x03 \x01(\x0b\x32\x39.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta\x12X\n\x04spec\x18\x04 \x01(\x0b\x32J.oak9.tython.k8s.kubeaggregator.pkg.apis.apiregistration.v1.APIServiceSpec\x12\\\n\x06status\x18\x05 \x01(\x0b\x32L.oak9.tython.k8s.kubeaggregator.pkg.apis.apiregistration.v1.APIServiceStatus\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xe0\x01\n\x13\x41PIServiceCondition\x12Q\n\x14last_transition_time\x18\x01 \x01(\x0b\x32\x33.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.Time\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06reason\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x8e\x02\n\x0e\x41PIServiceList\x12\x13\n\x0b\x61pi_version\x18\x01 \x01(\t\x12U\n\x05items\x18\x02 \x03(\x0b\x32\x46.oak9.tython.k8s.kubeaggregator.pkg.apis.apiregistration.v1.APIService\x12\x0c\n\x04kind\x18\x03 \x01(\t\x12I\n\x08metadata\x18\x04 \x01(\x0b\x32\x37.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.ListMeta\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xb7\x02\n\x0e\x41PIServiceSpec\x12\x11\n\tca_bundle\x18\x01 \x01(\t\x12\r\n\x05group\x18\x02 \x01(\t\x12\x1e\n\x16group_priority_minimum\x18\x03 \x01(\x05\x12 \n\x18insecure_skip_tls_verify\x18\x04 \x01(\x08\x12]\n\x07service\x18\x05 \x01(\x0b\x32L.oak9.tython.k8s.kubeaggregator.pkg.apis.apiregistration.v1.ServiceReference\x12\x0f\n\x07version\x18\x06 \x01(\t\x12\x18\n\x10version_priority\x18\x07 \x01(\x05\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xb0\x01\n\x10\x41PIServiceStatus\x12\x63\n\nconditions\x18\x01 \x03(\x0b\x32O.oak9.tython.k8s.kubeaggregator.pkg.apis.apiregistration.v1.APIServiceCondition\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"z\n\x10ServiceReference\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tnamespace\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\x12\x37\n\rresource_info\x18\x04 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kubernetes.kubernetes_io.k8s.kubeaggregator.pkg.apis.apiregistration.v1_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _APISERVICE._serialized_start=229
  _APISERVICE._serialized_end=594
  _APISERVICECONDITION._serialized_start=597
  _APISERVICECONDITION._serialized_end=821
  _APISERVICELIST._serialized_start=824
  _APISERVICELIST._serialized_end=1094
  _APISERVICESPEC._serialized_start=1097
  _APISERVICESPEC._serialized_end=1408
  _APISERVICESTATUS._serialized_start=1411
  _APISERVICESTATUS._serialized_end=1587
  _SERVICEREFERENCE._serialized_start=1589
  _SERVICEREFERENCE._serialized_end=1711
# @@protoc_insertion_point(module_scope)
