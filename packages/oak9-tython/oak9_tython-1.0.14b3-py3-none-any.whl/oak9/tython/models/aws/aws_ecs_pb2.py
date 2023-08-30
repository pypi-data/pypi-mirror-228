# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_ecs.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x61ws/aws_ecs.proto\x12\x13oak9.tython.aws.ecs\x1a\x13shared/shared.proto\"\xc8\x01\n\x1e\x43\x61pacityProviderManagedScaling\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12!\n\x19minimum_scaling_step_size\x18\x02 \x01(\x05\x12!\n\x19maximum_scaling_step_size\x18\x03 \x01(\x05\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x17\n\x0ftarget_capacity\x18\x05 \x01(\x05\"\xf9\x01\n(CapacityProviderAutoScalingGroupProvider\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1e\n\x16\x61uto_scaling_group_arn\x18\x02 \x01(\t\x12L\n\x0fmanaged_scaling\x18\x03 \x01(\x0b\x32\x33.oak9.tython.aws.ecs.CapacityProviderManagedScaling\x12&\n\x1emanaged_termination_protection\x18\x04 \x01(\t\"\xa9\x02\n\x10\x43\x61pacityProvider\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x62\n\x1b\x61uto_scaling_group_provider\x18\x02 \x01(\x0b\x32=.oak9.tython.aws.ecs.CapacityProviderAutoScalingGroupProvider\x12\x0c\n\x04name\x18\x03 \x01(\t\x12=\n\x04tags\x18\x04 \x03(\x0b\x32/.oak9.tython.aws.ecs.CapacityProvider.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xd2\x02\n\x03\x45\x43S\x12@\n\x11\x63\x61pacity_provider\x18\x01 \x03(\x0b\x32%.oak9.tython.aws.ecs.CapacityProvider\x12-\n\x07\x63luster\x18\x02 \x01(\x0b\x32\x1c.oak9.tython.aws.ecs.Cluster\x12=\n\x10primary_task_set\x18\x03 \x01(\x0b\x32#.oak9.tython.aws.ecs.PrimaryTaskSet\x12-\n\x07service\x18\x04 \x03(\x0b\x32\x1c.oak9.tython.aws.ecs.Service\x12<\n\x0ftask_definition\x18\x05 \x03(\x0b\x32#.oak9.tython.aws.ecs.TaskDefinition\x12.\n\x08task_set\x18\x06 \x03(\x0b\x32\x1c.oak9.tython.aws.ecs.TaskSet\"n\n\x16\x43lusterClusterSettings\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x97\x01\n#ClusterCapacityProviderStrategyItem\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x19\n\x11\x63\x61pacity_provider\x18\x02 \x01(\t\x12\x0e\n\x06weight\x18\x03 \x01(\x05\x12\x0c\n\x04\x62\x61se\x18\x04 \x01(\x05\"\x84\x03\n\x07\x43luster\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x34\n\x04tags\x18\x02 \x03(\x0b\x32&.oak9.tython.aws.ecs.Cluster.TagsEntry\x12\x14\n\x0c\x63luster_name\x18\x03 \x01(\t\x12\x45\n\x10\x63luster_settings\x18\x04 \x03(\x0b\x32+.oak9.tython.aws.ecs.ClusterClusterSettings\x12\x1a\n\x12\x63\x61pacity_providers\x18\x05 \x03(\t\x12\x64\n\"default_capacity_provider_strategy\x18\x06 \x03(\x0b\x32\x38.oak9.tython.aws.ecs.ClusterCapacityProviderStrategyItem\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x80\x01\n\x0ePrimaryTaskSet\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0f\n\x07\x63luster\x18\x02 \x01(\t\x12\x13\n\x0btask_set_id\x18\x03 \x01(\t\x12\x0f\n\x07service\x18\x04 \x01(\t\"\x97\x01\n#ServiceCapacityProviderStrategyItem\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04\x62\x61se\x18\x02 \x01(\x05\x12\x19\n\x11\x63\x61pacity_provider\x18\x03 \x01(\t\x12\x0e\n\x06weight\x18\x04 \x01(\x05\"\x93\x01\n\x1eServiceDeploymentConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x17\n\x0fmaximum_percent\x18\x02 \x01(\x05\x12\x1f\n\x17minimum_healthy_percent\x18\x03 \x01(\x05\"V\n\x1bServiceDeploymentController\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xb4\x01\n\x13ServiceLoadBalancer\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_name\x18\x02 \x01(\t\x12\x16\n\x0e\x63ontainer_port\x18\x03 \x01(\x05\x12\x1a\n\x12load_balancer_name\x18\x04 \x01(\t\x12\x18\n\x10target_group_arn\x18\x05 \x01(\t\"\x99\x01\n\x1aServiceAwsVpcConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x18\n\x10\x61ssign_public_ip\x18\x02 \x01(\t\x12\x17\n\x0fsecurity_groups\x18\x03 \x03(\t\x12\x0f\n\x07subnets\x18\x04 \x03(\t\"\xa6\x01\n\x1bServiceNetworkConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12N\n\x15\x61ws_vpc_configuration\x18\x02 \x01(\x0b\x32/.oak9.tython.aws.ecs.ServiceAwsVpcConfiguration\"i\n\x1aServicePlacementConstraint\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nexpression\x18\x02 \x01(\t\"b\n\x18ServicePlacementStrategy\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05\x66ield\x18\x02 \x01(\t\"\xa5\x01\n\x16ServiceServiceRegistry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_name\x18\x02 \x01(\t\x12\x16\n\x0e\x63ontainer_port\x18\x03 \x01(\x05\x12\x0c\n\x04port\x18\x04 \x01(\x05\x12\x14\n\x0cregistry_arn\x18\x05 \x01(\t\"\xce\x08\n\x07Service\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0bservice_arn\x18\x02 \x01(\t\x12\\\n\x1a\x63\x61pacity_provider_strategy\x18\x03 \x03(\x0b\x32\x38.oak9.tython.aws.ecs.ServiceCapacityProviderStrategyItem\x12\x0f\n\x07\x63luster\x18\x04 \x01(\t\x12U\n\x18\x64\x65ployment_configuration\x18\x05 \x01(\x0b\x32\x33.oak9.tython.aws.ecs.ServiceDeploymentConfiguration\x12O\n\x15\x64\x65ployment_controller\x18\x06 \x01(\x0b\x32\x30.oak9.tython.aws.ecs.ServiceDeploymentController\x12\x15\n\rdesired_count\x18\x07 \x01(\x05\x12\x1f\n\x17\x65nable_ecs_managed_tags\x18\x08 \x01(\x08\x12)\n!health_check_grace_period_seconds\x18\t \x01(\x05\x12\x13\n\x0blaunch_type\x18\n \x01(\t\x12@\n\x0eload_balancers\x18\x0b \x03(\x0b\x32(.oak9.tython.aws.ecs.ServiceLoadBalancer\x12O\n\x15network_configuration\x18\x0c \x01(\x0b\x32\x30.oak9.tython.aws.ecs.ServiceNetworkConfiguration\x12N\n\x15placement_constraints\x18\r \x03(\x0b\x32/.oak9.tython.aws.ecs.ServicePlacementConstraint\x12K\n\x14placement_strategies\x18\x0e \x03(\x0b\x32-.oak9.tython.aws.ecs.ServicePlacementStrategy\x12\x18\n\x10platform_version\x18\x0f \x01(\t\x12\x16\n\x0epropagate_tags\x18\x10 \x01(\t\x12\x0c\n\x04role\x18\x11 \x01(\t\x12\x1b\n\x13scheduling_strategy\x18\x12 \x01(\t\x12\x14\n\x0cservice_name\x18\x13 \x01(\t\x12G\n\x12service_registries\x18\x14 \x03(\x0b\x32+.oak9.tython.aws.ecs.ServiceServiceRegistry\x12\x34\n\x04tags\x18\x15 \x03(\x0b\x32&.oak9.tython.aws.ecs.Service.TagsEntry\x12\x17\n\x0ftask_definition\x18\x16 \x01(\t\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"r\n\x1aTaskDefinitionKeyValuePair\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"g\n\x1dTaskDefinitionEnvironmentFile\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\"x\n\x17TaskDefinitionHostEntry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x10\n\x08hostname\x18\x02 \x01(\t\x12\x12\n\nip_address\x18\x03 \x01(\t\"\xe6\x01\n#TaskDefinitionFirelensConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12V\n\x07options\x18\x02 \x03(\x0b\x32\x45.oak9.tython.aws.ecs.TaskDefinitionFirelensConfiguration.OptionsEntry\x1a.\n\x0cOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xaf\x01\n\x19TaskDefinitionHealthCheck\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0f\n\x07\x63ommand\x18\x02 \x03(\t\x12\x10\n\x08interval\x18\x03 \x01(\x05\x12\x0f\n\x07timeout\x18\x04 \x01(\x05\x12\x0f\n\x07retries\x18\x05 \x01(\x05\x12\x14\n\x0cstart_period\x18\x06 \x01(\x05\"v\n TaskDefinitionKernelCapabilities\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0b\n\x03\x61\x64\x64\x18\x02 \x03(\t\x12\x0c\n\x04\x64rop\x18\x03 \x03(\t\"\x8f\x01\n\x14TaskDefinitionDevice\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_path\x18\x02 \x01(\t\x12\x11\n\thost_path\x18\x03 \x01(\t\x12\x13\n\x0bpermissions\x18\x04 \x03(\t\"\x8b\x01\n\x13TaskDefinitionTmpfs\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_path\x18\x02 \x01(\t\x12\x15\n\rmount_options\x18\x03 \x03(\t\x12\x0c\n\x04size\x18\x04 \x01(\x05\"\xfa\x02\n\x1dTaskDefinitionLinuxParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12K\n\x0c\x63\x61pabilities\x18\x02 \x01(\x0b\x32\x35.oak9.tython.aws.ecs.TaskDefinitionKernelCapabilities\x12:\n\x07\x64\x65vices\x18\x03 \x03(\x0b\x32).oak9.tython.aws.ecs.TaskDefinitionDevice\x12\x1c\n\x14init_process_enabled\x18\x04 \x01(\x08\x12\x10\n\x08max_swap\x18\x05 \x01(\x05\x12\x1a\n\x12shared_memory_size\x18\x06 \x01(\x05\x12\x12\n\nswappiness\x18\x07 \x01(\x05\x12\x37\n\x05tmpfs\x18\x08 \x03(\x0b\x32(.oak9.tython.aws.ecs.TaskDefinitionTmpfs\"q\n\x14TaskDefinitionSecret\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\nvalue_from\x18\x03 \x01(\t\"\xb3\x02\n\x1eTaskDefinitionLogConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nlog_driver\x18\x02 \x01(\t\x12Q\n\x07options\x18\x03 \x03(\x0b\x32@.oak9.tython.aws.ecs.TaskDefinitionLogConfiguration.OptionsEntry\x12\x41\n\x0esecret_options\x18\x04 \x03(\x0b\x32).oak9.tython.aws.ecs.TaskDefinitionSecret\x1a.\n\x0cOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x95\x01\n\x18TaskDefinitionMountPoint\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_path\x18\x02 \x01(\t\x12\x11\n\tread_only\x18\x03 \x01(\x08\x12\x15\n\rsource_volume\x18\x04 \x01(\t\"\x91\x01\n\x19TaskDefinitionPortMapping\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_port\x18\x02 \x01(\x05\x12\x11\n\thost_port\x18\x03 \x01(\x05\x12\x10\n\x08protocol\x18\x04 \x01(\t\"}\n#TaskDefinitionRepositoryCredentials\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1d\n\x15\x63redentials_parameter\x18\x02 \x01(\t\"k\n!TaskDefinitionResourceRequirement\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\"\x85\x01\n\x14TaskDefinitionUlimit\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nhard_limit\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nsoft_limit\x18\x04 \x01(\x05\"\x80\x01\n\x18TaskDefinitionVolumeFrom\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x11\n\tread_only\x18\x02 \x01(\x08\x12\x18\n\x10source_container\x18\x03 \x01(\t\"x\n\x1bTaskDefinitionSystemControl\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x11\n\tnamespace\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\xa5\x0e\n!TaskDefinitionContainerDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0f\n\x07\x63ommand\x18\x02 \x03(\t\x12\x0b\n\x03\x63pu\x18\x03 \x01(\x05\x12\x1a\n\x12\x64isable_networking\x18\x04 \x01(\x08\x12\x1a\n\x12\x64ns_search_domains\x18\x05 \x03(\t\x12\x13\n\x0b\x64ns_servers\x18\x06 \x03(\t\x12_\n\rdocker_labels\x18\x07 \x03(\x0b\x32H.oak9.tython.aws.ecs.TaskDefinitionContainerDefinition.DockerLabelsEntry\x12\x1f\n\x17\x64ocker_security_options\x18\x08 \x03(\t\x12\x13\n\x0b\x65ntry_point\x18\t \x03(\t\x12\x44\n\x0b\x65nvironment\x18\n \x03(\x0b\x32/.oak9.tython.aws.ecs.TaskDefinitionKeyValuePair\x12M\n\x11\x65nvironment_files\x18\x0b \x03(\x0b\x32\x32.oak9.tython.aws.ecs.TaskDefinitionEnvironmentFile\x12\x11\n\tessential\x18\x0c \x01(\x08\x12\x41\n\x0b\x65xtra_hosts\x18\r \x03(\x0b\x32,.oak9.tython.aws.ecs.TaskDefinitionHostEntry\x12X\n\x16\x66irelens_configuration\x18\x0e \x01(\x0b\x32\x38.oak9.tython.aws.ecs.TaskDefinitionFirelensConfiguration\x12\x44\n\x0chealth_check\x18\x0f \x01(\x0b\x32..oak9.tython.aws.ecs.TaskDefinitionHealthCheck\x12\x10\n\x08hostname\x18\x10 \x01(\t\x12\r\n\x05image\x18\x11 \x01(\t\x12\r\n\x05links\x18\x12 \x03(\t\x12L\n\x10linux_parameters\x18\x13 \x01(\x0b\x32\x32.oak9.tython.aws.ecs.TaskDefinitionLinuxParameters\x12N\n\x11log_configuration\x18\x14 \x01(\x0b\x32\x33.oak9.tython.aws.ecs.TaskDefinitionLogConfiguration\x12\x0e\n\x06memory\x18\x15 \x01(\x05\x12\x1a\n\x12memory_reservation\x18\x16 \x01(\x05\x12\x43\n\x0cmount_points\x18\x17 \x03(\x0b\x32-.oak9.tython.aws.ecs.TaskDefinitionMountPoint\x12\x0c\n\x04name\x18\x18 \x01(\t\x12\x45\n\rport_mappings\x18\x19 \x03(\x0b\x32..oak9.tython.aws.ecs.TaskDefinitionPortMapping\x12\x12\n\nprivileged\x18\x1a \x01(\x08\x12 \n\x18readonly_root_filesystem\x18\x1b \x01(\x08\x12X\n\x16repository_credentials\x18\x1c \x01(\x0b\x32\x38.oak9.tython.aws.ecs.TaskDefinitionRepositoryCredentials\x12U\n\x15resource_requirements\x18\x1d \x03(\x0b\x32\x36.oak9.tython.aws.ecs.TaskDefinitionResourceRequirement\x12:\n\x07secrets\x18\x1e \x03(\x0b\x32).oak9.tython.aws.ecs.TaskDefinitionSecret\x12\x15\n\rstart_timeout\x18\x1f \x01(\x05\x12\x14\n\x0cstop_timeout\x18  \x01(\x05\x12:\n\x07ulimits\x18! \x03(\x0b\x32).oak9.tython.aws.ecs.TaskDefinitionUlimit\x12\x0c\n\x04user\x18\" \x01(\t\x12\x43\n\x0cvolumes_from\x18# \x03(\x0b\x32-.oak9.tython.aws.ecs.TaskDefinitionVolumeFrom\x12\x19\n\x11working_directory\x18$ \x01(\t\x12\x13\n\x0binteractive\x18% \x01(\x08\x12\x17\n\x0fpseudo_terminal\x18& \x01(\x08\x12I\n\x0fsystem_controls\x18\' \x03(\x0b\x32\x30.oak9.tython.aws.ecs.TaskDefinitionSystemControl\x1a\x33\n\x11\x44ockerLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x87\x01\n\"TaskDefinitionInferenceAccelerator\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0b\x64\x65vice_name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x03 \x01(\t\"~\n/TaskDefinitionTaskDefinitionPlacementConstraint\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nexpression\x18\x02 \x01(\t\"\xcc\x01\n TaskDefinitionProxyConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_name\x18\x02 \x01(\t\x12W\n\x1eproxy_configuration_properties\x18\x03 \x03(\x0b\x32/.oak9.tython.aws.ecs.TaskDefinitionKeyValuePair\"\xb7\x03\n\'TaskDefinitionDockerVolumeConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x15\n\rautoprovision\x18\x02 \x01(\x08\x12\x0e\n\x06\x64river\x18\x03 \x01(\t\x12\x61\n\x0b\x64river_opts\x18\x04 \x03(\x0b\x32L.oak9.tython.aws.ecs.TaskDefinitionDockerVolumeConfiguration.DriverOptsEntry\x12X\n\x06labels\x18\x05 \x03(\x0b\x32H.oak9.tython.aws.ecs.TaskDefinitionDockerVolumeConfiguration.LabelsEntry\x12\r\n\x05scope\x18\x06 \x01(\t\x1a\x31\n\x0f\x44riverOptsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa1\x02\n$TaskDefinitionEFSVolumeConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x15\n\rfilesystem_id\x18\x02 \x01(\t\x12\x16\n\x0eroot_directory\x18\x03 \x01(\t\x12\x1a\n\x12transit_encryption\x18\x04 \x01(\t\x12\x1f\n\x17transit_encryption_port\x18\x05 \x01(\x05\x12T\n\x14\x61uthorization_config\x18\x06 \x01(\x0b\x32\x36.oak9.tython.aws.ecs.TaskDefinitionAuthorizationConfig\"r\n\"TaskDefinitionHostVolumeProperties\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0bsource_path\x18\x02 \x01(\t\"\xe4\x02\n\x14TaskDefinitionVolume\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x61\n\x1b\x64ocker_volume_configuration\x18\x02 \x01(\x0b\x32<.oak9.tython.aws.ecs.TaskDefinitionDockerVolumeConfiguration\x12[\n\x18\x65\x66s_volume_configuration\x18\x03 \x01(\x0b\x32\x39.oak9.tython.aws.ecs.TaskDefinitionEFSVolumeConfiguration\x12\x45\n\x04host\x18\x04 \x01(\x0b\x32\x37.oak9.tython.aws.ecs.TaskDefinitionHostVolumeProperties\x12\x0c\n\x04name\x18\x05 \x01(\t\"\x94\x06\n\x0eTaskDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0e\n\x06\x66\x61mily\x18\x02 \x01(\t\x12U\n\x15\x63ontainer_definitions\x18\x03 \x03(\x0b\x32\x36.oak9.tython.aws.ecs.TaskDefinitionContainerDefinition\x12\x0b\n\x03\x63pu\x18\x04 \x01(\t\x12\x1a\n\x12\x65xecution_role_arn\x18\x05 \x01(\t\x12W\n\x16inference_accelerators\x18\x06 \x03(\x0b\x32\x37.oak9.tython.aws.ecs.TaskDefinitionInferenceAccelerator\x12\x0e\n\x06memory\x18\x07 \x01(\t\x12\x14\n\x0cnetwork_mode\x18\x08 \x01(\t\x12\x63\n\x15placement_constraints\x18\t \x03(\x0b\x32\x44.oak9.tython.aws.ecs.TaskDefinitionTaskDefinitionPlacementConstraint\x12R\n\x13proxy_configuration\x18\n \x01(\x0b\x32\x35.oak9.tython.aws.ecs.TaskDefinitionProxyConfiguration\x12 \n\x18requires_compatibilities\x18\x0b \x03(\t\x12\x15\n\rtask_role_arn\x18\x0c \x01(\t\x12:\n\x07volumes\x18\r \x03(\x0b\x32).oak9.tython.aws.ecs.TaskDefinitionVolume\x12\x10\n\x08pid_mode\x18\x0e \x01(\t\x12\x10\n\x08ipc_mode\x18\x0f \x01(\t\x12;\n\x04tags\x18\x10 \x03(\x0b\x32-.oak9.tython.aws.ecs.TaskDefinition.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xb4\x01\n\x13TaskSetLoadBalancer\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_name\x18\x02 \x01(\t\x12\x16\n\x0e\x63ontainer_port\x18\x03 \x01(\x05\x12\x1a\n\x12load_balancer_name\x18\x04 \x01(\t\x12\x18\n\x10target_group_arn\x18\x05 \x01(\t\"\x99\x01\n\x1aTaskSetAwsVpcConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x18\n\x10\x61ssign_public_ip\x18\x02 \x01(\t\x12\x17\n\x0fsecurity_groups\x18\x03 \x03(\t\x12\x0f\n\x07subnets\x18\x04 \x03(\t\"\xa6\x01\n\x1bTaskSetNetworkConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12N\n\x15\x61ws_vpc_configuration\x18\x02 \x01(\x0b\x32/.oak9.tython.aws.ecs.TaskSetAwsVpcConfiguration\"d\n\x0cTaskSetScale\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04unit\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x01\"\xa5\x01\n\x16TaskSetServiceRegistry\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_name\x18\x02 \x01(\t\x12\x16\n\x0e\x63ontainer_port\x18\x03 \x01(\x05\x12\x0c\n\x04port\x18\x04 \x01(\x05\x12\x14\n\x0cregistry_arn\x18\x05 \x01(\t\"\xcf\x03\n\x07TaskSet\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0f\n\x07\x63luster\x18\x02 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x03 \x01(\t\x12\x13\n\x0blaunch_type\x18\x04 \x01(\t\x12@\n\x0eload_balancers\x18\x05 \x03(\x0b\x32(.oak9.tython.aws.ecs.TaskSetLoadBalancer\x12O\n\x15network_configuration\x18\x06 \x01(\x0b\x32\x30.oak9.tython.aws.ecs.TaskSetNetworkConfiguration\x12\x18\n\x10platform_version\x18\x07 \x01(\t\x12\x30\n\x05scale\x18\x08 \x01(\x0b\x32!.oak9.tython.aws.ecs.TaskSetScale\x12\x0f\n\x07service\x18\t \x01(\t\x12G\n\x12service_registries\x18\n \x03(\x0b\x32+.oak9.tython.aws.ecs.TaskSetServiceRegistry\x12\x17\n\x0ftask_definition\x18\x0b \x01(\t\"\x82\x01\n!TaskDefinitionAuthorizationConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0b\n\x03iam\x18\x02 \x01(\t\x12\x17\n\x0f\x61\x63\x63\x65ss_point_id\x18\x03 \x01(\t\"\x87\x01\n!TaskDefinitionContainerDependency\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x63ontainer_name\x18\x02 \x01(\t\x12\x11\n\tcondition\x18\x03 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_ecs_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CAPACITYPROVIDER_TAGSENTRY._options = None
  _CAPACITYPROVIDER_TAGSENTRY._serialized_options = b'8\001'
  _CLUSTER_TAGSENTRY._options = None
  _CLUSTER_TAGSENTRY._serialized_options = b'8\001'
  _SERVICE_TAGSENTRY._options = None
  _SERVICE_TAGSENTRY._serialized_options = b'8\001'
  _TASKDEFINITIONFIRELENSCONFIGURATION_OPTIONSENTRY._options = None
  _TASKDEFINITIONFIRELENSCONFIGURATION_OPTIONSENTRY._serialized_options = b'8\001'
  _TASKDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._options = None
  _TASKDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._serialized_options = b'8\001'
  _TASKDEFINITIONCONTAINERDEFINITION_DOCKERLABELSENTRY._options = None
  _TASKDEFINITIONCONTAINERDEFINITION_DOCKERLABELSENTRY._serialized_options = b'8\001'
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_DRIVEROPTSENTRY._options = None
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_DRIVEROPTSENTRY._serialized_options = b'8\001'
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_LABELSENTRY._options = None
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_LABELSENTRY._serialized_options = b'8\001'
  _TASKDEFINITION_TAGSENTRY._options = None
  _TASKDEFINITION_TAGSENTRY._serialized_options = b'8\001'
  _CAPACITYPROVIDERMANAGEDSCALING._serialized_start=64
  _CAPACITYPROVIDERMANAGEDSCALING._serialized_end=264
  _CAPACITYPROVIDERAUTOSCALINGGROUPPROVIDER._serialized_start=267
  _CAPACITYPROVIDERAUTOSCALINGGROUPPROVIDER._serialized_end=516
  _CAPACITYPROVIDER._serialized_start=519
  _CAPACITYPROVIDER._serialized_end=816
  _CAPACITYPROVIDER_TAGSENTRY._serialized_start=773
  _CAPACITYPROVIDER_TAGSENTRY._serialized_end=816
  _ECS._serialized_start=819
  _ECS._serialized_end=1157
  _CLUSTERCLUSTERSETTINGS._serialized_start=1159
  _CLUSTERCLUSTERSETTINGS._serialized_end=1269
  _CLUSTERCAPACITYPROVIDERSTRATEGYITEM._serialized_start=1272
  _CLUSTERCAPACITYPROVIDERSTRATEGYITEM._serialized_end=1423
  _CLUSTER._serialized_start=1426
  _CLUSTER._serialized_end=1814
  _CLUSTER_TAGSENTRY._serialized_start=773
  _CLUSTER_TAGSENTRY._serialized_end=816
  _PRIMARYTASKSET._serialized_start=1817
  _PRIMARYTASKSET._serialized_end=1945
  _SERVICECAPACITYPROVIDERSTRATEGYITEM._serialized_start=1948
  _SERVICECAPACITYPROVIDERSTRATEGYITEM._serialized_end=2099
  _SERVICEDEPLOYMENTCONFIGURATION._serialized_start=2102
  _SERVICEDEPLOYMENTCONFIGURATION._serialized_end=2249
  _SERVICEDEPLOYMENTCONTROLLER._serialized_start=2251
  _SERVICEDEPLOYMENTCONTROLLER._serialized_end=2337
  _SERVICELOADBALANCER._serialized_start=2340
  _SERVICELOADBALANCER._serialized_end=2520
  _SERVICEAWSVPCCONFIGURATION._serialized_start=2523
  _SERVICEAWSVPCCONFIGURATION._serialized_end=2676
  _SERVICENETWORKCONFIGURATION._serialized_start=2679
  _SERVICENETWORKCONFIGURATION._serialized_end=2845
  _SERVICEPLACEMENTCONSTRAINT._serialized_start=2847
  _SERVICEPLACEMENTCONSTRAINT._serialized_end=2952
  _SERVICEPLACEMENTSTRATEGY._serialized_start=2954
  _SERVICEPLACEMENTSTRATEGY._serialized_end=3052
  _SERVICESERVICEREGISTRY._serialized_start=3055
  _SERVICESERVICEREGISTRY._serialized_end=3220
  _SERVICE._serialized_start=3223
  _SERVICE._serialized_end=4325
  _SERVICE_TAGSENTRY._serialized_start=773
  _SERVICE_TAGSENTRY._serialized_end=816
  _TASKDEFINITIONKEYVALUEPAIR._serialized_start=4327
  _TASKDEFINITIONKEYVALUEPAIR._serialized_end=4441
  _TASKDEFINITIONENVIRONMENTFILE._serialized_start=4443
  _TASKDEFINITIONENVIRONMENTFILE._serialized_end=4546
  _TASKDEFINITIONHOSTENTRY._serialized_start=4548
  _TASKDEFINITIONHOSTENTRY._serialized_end=4668
  _TASKDEFINITIONFIRELENSCONFIGURATION._serialized_start=4671
  _TASKDEFINITIONFIRELENSCONFIGURATION._serialized_end=4901
  _TASKDEFINITIONFIRELENSCONFIGURATION_OPTIONSENTRY._serialized_start=4855
  _TASKDEFINITIONFIRELENSCONFIGURATION_OPTIONSENTRY._serialized_end=4901
  _TASKDEFINITIONHEALTHCHECK._serialized_start=4904
  _TASKDEFINITIONHEALTHCHECK._serialized_end=5079
  _TASKDEFINITIONKERNELCAPABILITIES._serialized_start=5081
  _TASKDEFINITIONKERNELCAPABILITIES._serialized_end=5199
  _TASKDEFINITIONDEVICE._serialized_start=5202
  _TASKDEFINITIONDEVICE._serialized_end=5345
  _TASKDEFINITIONTMPFS._serialized_start=5348
  _TASKDEFINITIONTMPFS._serialized_end=5487
  _TASKDEFINITIONLINUXPARAMETERS._serialized_start=5490
  _TASKDEFINITIONLINUXPARAMETERS._serialized_end=5868
  _TASKDEFINITIONSECRET._serialized_start=5870
  _TASKDEFINITIONSECRET._serialized_end=5983
  _TASKDEFINITIONLOGCONFIGURATION._serialized_start=5986
  _TASKDEFINITIONLOGCONFIGURATION._serialized_end=6293
  _TASKDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._serialized_start=4855
  _TASKDEFINITIONLOGCONFIGURATION_OPTIONSENTRY._serialized_end=4901
  _TASKDEFINITIONMOUNTPOINT._serialized_start=6296
  _TASKDEFINITIONMOUNTPOINT._serialized_end=6445
  _TASKDEFINITIONPORTMAPPING._serialized_start=6448
  _TASKDEFINITIONPORTMAPPING._serialized_end=6593
  _TASKDEFINITIONREPOSITORYCREDENTIALS._serialized_start=6595
  _TASKDEFINITIONREPOSITORYCREDENTIALS._serialized_end=6720
  _TASKDEFINITIONRESOURCEREQUIREMENT._serialized_start=6722
  _TASKDEFINITIONRESOURCEREQUIREMENT._serialized_end=6829
  _TASKDEFINITIONULIMIT._serialized_start=6832
  _TASKDEFINITIONULIMIT._serialized_end=6965
  _TASKDEFINITIONVOLUMEFROM._serialized_start=6968
  _TASKDEFINITIONVOLUMEFROM._serialized_end=7096
  _TASKDEFINITIONSYSTEMCONTROL._serialized_start=7098
  _TASKDEFINITIONSYSTEMCONTROL._serialized_end=7218
  _TASKDEFINITIONCONTAINERDEFINITION._serialized_start=7221
  _TASKDEFINITIONCONTAINERDEFINITION._serialized_end=9050
  _TASKDEFINITIONCONTAINERDEFINITION_DOCKERLABELSENTRY._serialized_start=8999
  _TASKDEFINITIONCONTAINERDEFINITION_DOCKERLABELSENTRY._serialized_end=9050
  _TASKDEFINITIONINFERENCEACCELERATOR._serialized_start=9053
  _TASKDEFINITIONINFERENCEACCELERATOR._serialized_end=9188
  _TASKDEFINITIONTASKDEFINITIONPLACEMENTCONSTRAINT._serialized_start=9190
  _TASKDEFINITIONTASKDEFINITIONPLACEMENTCONSTRAINT._serialized_end=9316
  _TASKDEFINITIONPROXYCONFIGURATION._serialized_start=9319
  _TASKDEFINITIONPROXYCONFIGURATION._serialized_end=9523
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION._serialized_start=9526
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION._serialized_end=9965
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_DRIVEROPTSENTRY._serialized_start=9869
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_DRIVEROPTSENTRY._serialized_end=9918
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_LABELSENTRY._serialized_start=9920
  _TASKDEFINITIONDOCKERVOLUMECONFIGURATION_LABELSENTRY._serialized_end=9965
  _TASKDEFINITIONEFSVOLUMECONFIGURATION._serialized_start=9968
  _TASKDEFINITIONEFSVOLUMECONFIGURATION._serialized_end=10257
  _TASKDEFINITIONHOSTVOLUMEPROPERTIES._serialized_start=10259
  _TASKDEFINITIONHOSTVOLUMEPROPERTIES._serialized_end=10373
  _TASKDEFINITIONVOLUME._serialized_start=10376
  _TASKDEFINITIONVOLUME._serialized_end=10732
  _TASKDEFINITION._serialized_start=10735
  _TASKDEFINITION._serialized_end=11523
  _TASKDEFINITION_TAGSENTRY._serialized_start=773
  _TASKDEFINITION_TAGSENTRY._serialized_end=816
  _TASKSETLOADBALANCER._serialized_start=11526
  _TASKSETLOADBALANCER._serialized_end=11706
  _TASKSETAWSVPCCONFIGURATION._serialized_start=11709
  _TASKSETAWSVPCCONFIGURATION._serialized_end=11862
  _TASKSETNETWORKCONFIGURATION._serialized_start=11865
  _TASKSETNETWORKCONFIGURATION._serialized_end=12031
  _TASKSETSCALE._serialized_start=12033
  _TASKSETSCALE._serialized_end=12133
  _TASKSETSERVICEREGISTRY._serialized_start=12136
  _TASKSETSERVICEREGISTRY._serialized_end=12301
  _TASKSET._serialized_start=12304
  _TASKSET._serialized_end=12767
  _TASKDEFINITIONAUTHORIZATIONCONFIG._serialized_start=12770
  _TASKDEFINITIONAUTHORIZATIONCONFIG._serialized_end=12900
  _TASKDEFINITIONCONTAINERDEPENDENCY._serialized_start=12903
  _TASKDEFINITIONCONTAINERDEPENDENCY._serialized_end=13038
# @@protoc_insertion_point(module_scope)
