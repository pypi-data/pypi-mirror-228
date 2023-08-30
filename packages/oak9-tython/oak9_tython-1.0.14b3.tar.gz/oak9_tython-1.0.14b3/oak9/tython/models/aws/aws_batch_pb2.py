# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_batch.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x61ws/aws_batch.proto\x12\x15oak9.tython.aws.batch\x1a\x13shared/shared.proto\"\xb3\x01\n-ComputeEnvironmentLaunchTemplateSpecification\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1c\n\x14launch_template_name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x1a\n\x12launch_template_id\x18\x04 \x01(\t\"\xe8\x04\n\"ComputeEnvironmentComputeResources\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1b\n\x13spot_iam_fleet_role\x18\x02 \x01(\t\x12\x11\n\tmaxv_cpus\x18\x03 \x01(\x05\x12\x16\n\x0e\x62id_percentage\x18\x04 \x01(\x05\x12\x1a\n\x12security_group_ids\x18\x05 \x03(\t\x12\x0f\n\x07subnets\x18\x06 \x03(\t\x12\x1b\n\x13\x61llocation_strategy\x18\x07 \x01(\t\x12\x11\n\tminv_cpus\x18\x08 \x01(\x05\x12]\n\x0flaunch_template\x18\t \x01(\x0b\x32\x44.oak9.tython.aws.batch.ComputeEnvironmentLaunchTemplateSpecification\x12\x10\n\x08image_id\x18\n \x01(\t\x12\x15\n\rinstance_role\x18\x0b \x01(\t\x12\x16\n\x0einstance_types\x18\x0c \x03(\t\x12\x14\n\x0c\x65\x63\x32_key_pair\x18\r \x01(\t\x12\x17\n\x0fplacement_group\x18\x0e \x01(\t\x12Q\n\x04tags\x18\x0f \x03(\x0b\x32\x43.oak9.tython.aws.batch.ComputeEnvironmentComputeResources.TagsEntry\x12\x15\n\rdesiredv_cpus\x18\x10 \x01(\x05\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xf8\x01\n\x12\x43omputeEnvironment\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x14\n\x0cservice_role\x18\x03 \x01(\t\x12 \n\x18\x63ompute_environment_name\x18\x04 \x01(\t\x12T\n\x11\x63ompute_resources\x18\x05 \x01(\x0b\x32\x39.oak9.tython.aws.batch.ComputeEnvironmentComputeResources\x12\r\n\x05state\x18\x06 \x01(\t\"\xc1\x01\n\x05\x42\x61tch\x12\x46\n\x13\x63ompute_environment\x18\x01 \x03(\x0b\x32).oak9.tython.aws.batch.ComputeEnvironment\x12<\n\x0ejob_definition\x18\x02 \x03(\x0b\x32$.oak9.tython.aws.batch.JobDefinition\x12\x32\n\tjob_queue\x18\x03 \x03(\x0b\x32\x1f.oak9.tython.aws.batch.JobQueue\"p\n\x13JobDefinitionSecret\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nvalue_from\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x8a\x01\n\x12JobDefinitionTmpfs\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04size\x18\x02 \x01(\x05\x12\x16\n\x0e\x63ontainer_path\x18\x03 \x01(\t\x12\x15\n\rmount_options\x18\x04 \x03(\t\"\x8e\x01\n\x13JobDefinitionDevice\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x11\n\thost_path\x18\x02 \x01(\t\x12\x13\n\x0bpermissions\x18\x03 \x03(\t\x12\x16\n\x0e\x63ontainer_path\x18\x04 \x01(\t\"\xae\x02\n\x1cJobDefinitionLinuxParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nswappiness\x18\x02 \x01(\x05\x12\x38\n\x05tmpfs\x18\x03 \x03(\x0b\x32).oak9.tython.aws.batch.JobDefinitionTmpfs\x12\x1a\n\x12shared_memory_size\x18\x04 \x01(\x05\x12;\n\x07\x64\x65vices\x18\x05 \x03(\x0b\x32*.oak9.tython.aws.batch.JobDefinitionDevice\x12\x1c\n\x14init_process_enabled\x18\x06 \x01(\x08\x12\x10\n\x08max_swap\x18\x07 \x01(\x05\"j\n JobDefinitionResourceRequirement\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\"\xb4\x02\n\x1dJobDefinitionLogConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x42\n\x0esecret_options\x18\x02 \x03(\x0b\x32*.oak9.tython.aws.batch.JobDefinitionSecret\x12R\n\x07options\x18\x03 \x03(\x0b\x32\x41.oak9.tython.aws.batch.JobDefinitionLogConfiguration.OptionsEntry\x12\x12\n\nlog_driver\x18\x04 \x01(\t\x1a.\n\x0cOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x95\x01\n\x18JobDefinitionMountPoints\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x11\n\tread_only\x18\x02 \x01(\x08\x12\x15\n\rsource_volume\x18\x03 \x01(\t\x12\x16\n\x0e\x63ontainer_path\x18\x04 \x01(\t\"h\n\x18JobDefinitionVolumesHost\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0bsource_path\x18\x02 \x01(\t\"\x9c\x01\n\x14JobDefinitionVolumes\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12=\n\x04host\x18\x02 \x01(\x0b\x32/.oak9.tython.aws.batch.JobDefinitionVolumesHost\x12\x0c\n\x04name\x18\x03 \x01(\t\"p\n\x18JobDefinitionEnvironment\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x84\x01\n\x13JobDefinitionUlimit\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nsoft_limit\x18\x02 \x01(\x05\x12\x12\n\nhard_limit\x18\x03 \x01(\x05\x12\x0c\n\x04name\x18\x04 \x01(\t\"\xe4\x06\n JobDefinitionContainerProperties\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04user\x18\x02 \x01(\t\x12;\n\x07secrets\x18\x03 \x03(\x0b\x32*.oak9.tython.aws.batch.JobDefinitionSecret\x12\x0e\n\x06memory\x18\x04 \x01(\x05\x12\x12\n\nprivileged\x18\x05 \x01(\x08\x12M\n\x10linux_parameters\x18\x06 \x01(\x0b\x32\x33.oak9.tython.aws.batch.JobDefinitionLinuxParameters\x12\x14\n\x0cjob_role_arn\x18\x07 \x01(\t\x12 \n\x18readonly_root_filesystem\x18\x08 \x01(\x08\x12\r\n\x05vcpus\x18\t \x01(\x05\x12\r\n\x05image\x18\n \x01(\t\x12V\n\x15resource_requirements\x18\x0b \x03(\x0b\x32\x37.oak9.tython.aws.batch.JobDefinitionResourceRequirement\x12O\n\x11log_configuration\x18\x0c \x01(\x0b\x32\x34.oak9.tython.aws.batch.JobDefinitionLogConfiguration\x12\x45\n\x0cmount_points\x18\r \x03(\x0b\x32/.oak9.tython.aws.batch.JobDefinitionMountPoints\x12\x1a\n\x12\x65xecution_role_arn\x18\x0e \x01(\t\x12<\n\x07volumes\x18\x0f \x03(\x0b\x32+.oak9.tython.aws.batch.JobDefinitionVolumes\x12\x0f\n\x07\x63ommand\x18\x10 \x03(\t\x12\x44\n\x0b\x65nvironment\x18\x11 \x03(\x0b\x32/.oak9.tython.aws.batch.JobDefinitionEnvironment\x12;\n\x07ulimits\x18\x12 \x03(\x0b\x32*.oak9.tython.aws.batch.JobDefinitionUlimit\x12\x15\n\rinstance_type\x18\x13 \x01(\t\"\xbb\x01\n\x1eJobDefinitionNodeRangeProperty\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12J\n\tcontainer\x18\x02 \x01(\x0b\x32\x37.oak9.tython.aws.batch.JobDefinitionContainerProperties\x12\x14\n\x0ctarget_nodes\x18\x03 \x01(\t\"\xd2\x01\n\x1bJobDefinitionNodeProperties\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x11\n\tmain_node\x18\x02 \x01(\x05\x12T\n\x15node_range_properties\x18\x03 \x03(\x0b\x32\x35.oak9.tython.aws.batch.JobDefinitionNodeRangeProperty\x12\x11\n\tnum_nodes\x18\x04 \x01(\x05\"q\n\x14JobDefinitionTimeout\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12 \n\x18\x61ttempt_duration_seconds\x18\x02 \x01(\x05\"g\n\x1aJobDefinitionRetryStrategy\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x10\n\x08\x61ttempts\x18\x02 \x01(\x05\"\x9d\x04\n\rJobDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04type\x18\x02 \x01(\t\x12H\n\nparameters\x18\x03 \x03(\x0b\x32\x34.oak9.tython.aws.batch.JobDefinition.ParametersEntry\x12K\n\x0fnode_properties\x18\x04 \x01(\x0b\x32\x32.oak9.tython.aws.batch.JobDefinitionNodeProperties\x12<\n\x07timeout\x18\x05 \x01(\x0b\x32+.oak9.tython.aws.batch.JobDefinitionTimeout\x12U\n\x14\x63ontainer_properties\x18\x06 \x01(\x0b\x32\x37.oak9.tython.aws.batch.JobDefinitionContainerProperties\x12\x1b\n\x13job_definition_name\x18\x07 \x01(\t\x12I\n\x0eretry_strategy\x18\x08 \x01(\x0b\x32\x31.oak9.tython.aws.batch.JobDefinitionRetryStrategy\x1a\x31\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x86\x01\n\x1fJobQueueComputeEnvironmentOrder\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1b\n\x13\x63ompute_environment\x18\x02 \x01(\t\x12\r\n\x05order\x18\x03 \x01(\x05\"\xd7\x01\n\x08JobQueue\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12Y\n\x19\x63ompute_environment_order\x18\x02 \x03(\x0b\x32\x36.oak9.tython.aws.batch.JobQueueComputeEnvironmentOrder\x12\x10\n\x08priority\x18\x03 \x01(\x05\x12\r\n\x05state\x18\x04 \x01(\t\x12\x16\n\x0ejob_queue_name\x18\x05 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_batch_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMPUTEENVIRONMENTCOMPUTERESOURCES_TAGSENTRY._options = None
  _COMPUTEENVIRONMENTCOMPUTERESOURCES_TAGSENTRY._serialized_options = b'8\001'
  _JOBDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._options = None
  _JOBDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._serialized_options = b'8\001'
  _JOBDEFINITION_PARAMETERSENTRY._options = None
  _JOBDEFINITION_PARAMETERSENTRY._serialized_options = b'8\001'
  _COMPUTEENVIRONMENTLAUNCHTEMPLATESPECIFICATION._serialized_start=68
  _COMPUTEENVIRONMENTLAUNCHTEMPLATESPECIFICATION._serialized_end=247
  _COMPUTEENVIRONMENTCOMPUTERESOURCES._serialized_start=250
  _COMPUTEENVIRONMENTCOMPUTERESOURCES._serialized_end=866
  _COMPUTEENVIRONMENTCOMPUTERESOURCES_TAGSENTRY._serialized_start=823
  _COMPUTEENVIRONMENTCOMPUTERESOURCES_TAGSENTRY._serialized_end=866
  _COMPUTEENVIRONMENT._serialized_start=869
  _COMPUTEENVIRONMENT._serialized_end=1117
  _BATCH._serialized_start=1120
  _BATCH._serialized_end=1313
  _JOBDEFINITIONSECRET._serialized_start=1315
  _JOBDEFINITIONSECRET._serialized_end=1427
  _JOBDEFINITIONTMPFS._serialized_start=1430
  _JOBDEFINITIONTMPFS._serialized_end=1568
  _JOBDEFINITIONDEVICE._serialized_start=1571
  _JOBDEFINITIONDEVICE._serialized_end=1713
  _JOBDEFINITIONLINUXPARAMETERS._serialized_start=1716
  _JOBDEFINITIONLINUXPARAMETERS._serialized_end=2018
  _JOBDEFINITIONRESOURCEREQUIREMENT._serialized_start=2020
  _JOBDEFINITIONRESOURCEREQUIREMENT._serialized_end=2126
  _JOBDEFINITIONLOGCONFIGURATION._serialized_start=2129
  _JOBDEFINITIONLOGCONFIGURATION._serialized_end=2437
  _JOBDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._serialized_start=2391
  _JOBDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._serialized_end=2437
  _JOBDEFINITIONMOUNTPOINTS._serialized_start=2440
  _JOBDEFINITIONMOUNTPOINTS._serialized_end=2589
  _JOBDEFINITIONVOLUMESHOST._serialized_start=2591
  _JOBDEFINITIONVOLUMESHOST._serialized_end=2695
  _JOBDEFINITIONVOLUMES._serialized_start=2698
  _JOBDEFINITIONVOLUMES._serialized_end=2854
  _JOBDEFINITIONENVIRONMENT._serialized_start=2856
  _JOBDEFINITIONENVIRONMENT._serialized_end=2968
  _JOBDEFINITIONULIMIT._serialized_start=2971
  _JOBDEFINITIONULIMIT._serialized_end=3103
  _JOBDEFINITIONCONTAINERPROPERTIES._serialized_start=3106
  _JOBDEFINITIONCONTAINERPROPERTIES._serialized_end=3974
  _JOBDEFINITIONNODERANGEPROPERTY._serialized_start=3977
  _JOBDEFINITIONNODERANGEPROPERTY._serialized_end=4164
  _JOBDEFINITIONNODEPROPERTIES._serialized_start=4167
  _JOBDEFINITIONNODEPROPERTIES._serialized_end=4377
  _JOBDEFINITIONTIMEOUT._serialized_start=4379
  _JOBDEFINITIONTIMEOUT._serialized_end=4492
  _JOBDEFINITIONRETRYSTRATEGY._serialized_start=4494
  _JOBDEFINITIONRETRYSTRATEGY._serialized_end=4597
  _JOBDEFINITION._serialized_start=4600
  _JOBDEFINITION._serialized_end=5141
  _JOBDEFINITION_PARAMETERSENTRY._serialized_start=5092
  _JOBDEFINITION_PARAMETERSENTRY._serialized_end=5141
  _JOBQUEUECOMPUTEENVIRONMENTORDER._serialized_start=5144
  _JOBQUEUECOMPUTEENVIRONMENTORDER._serialized_end=5278
  _JOBQUEUE._serialized_start=5281
  _JOBQUEUE._serialized_end=5496
# @@protoc_insertion_point(module_scope)
