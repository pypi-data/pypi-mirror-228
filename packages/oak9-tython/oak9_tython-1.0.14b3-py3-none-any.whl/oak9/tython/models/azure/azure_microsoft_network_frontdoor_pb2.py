# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: azure/azure_microsoft_network_frontdoor.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-azure/azure_microsoft_network_frontdoor.proto\x12-oak9.tython.azure.microsoft_network_frontdoor\x1a\x13shared/shared.proto\"\xe6\x02\n\x1bMicrosoft_Network_FrontDoor\x12\x8c\x01\n,front_door_web_application_firewall_policies\x18\x01 \x03(\x0b\x32V.oak9.tython.azure.microsoft_network_frontdoor.FrontDoorWebApplicationFirewallPolicies\x12N\n\x0b\x66ront_doors\x18\x02 \x01(\x0b\x32\x39.oak9.tython.azure.microsoft_network_frontdoor.FrontDoors\x12h\n\x19\x66ront_doors_rules_engines\x18\x03 \x03(\x0b\x32\x45.oak9.tython.azure.microsoft_network_frontdoor.FrontDoorsRulesEngines\"\xac\x01\n\x15LoadBalancingSettings\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0eresource_state\x18\x03 \x01(\t\x12\'\n\x1f\x61\x64\x64itional_latency_milliseconds\x18\x04 \x01(\x05\x12\x13\n\x0bsample_size\x18\x05 \x01(\x05\x12#\n\x1bsuccessful_samples_required\x18\x06 \x01(\x05\"\xb8\x01\n\x13HealthProbeSettings\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\renabled_state\x18\x03 \x01(\t\x12\x1b\n\x13health_probe_method\x18\x04 \x01(\t\x12\x1b\n\x13interval_in_seconds\x18\x05 \x01(\x05\x12\x0c\n\x04path\x18\x06 \x01(\t\x12\x10\n\x08protocol\x18\x07 \x01(\t\x12\x16\n\x0eresource_state\x18\x08 \x01(\t\"\xf5\x04\n\'FrontDoorWebApplicationFirewallPolicies\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04\x65tag\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12S\n\x0c\x63ustom_rules\x18\x05 \x01(\x0b\x32=.oak9.tython.azure.microsoft_network_frontdoor.CustomRuleList\x12X\n\rmanaged_rules\x18\x06 \x01(\x0b\x32\x41.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleSetList\x12V\n\x0fpolicy_settings\x18\x07 \x01(\x0b\x32=.oak9.tython.azure.microsoft_network_frontdoor.PolicySettings\x12n\n\x04tags\x18\x08 \x03(\x0b\x32`.oak9.tython.azure.microsoft_network_frontdoor.FrontDoorWebApplicationFirewallPolicies.TagsEntry\x12?\n\x03sku\x18\t \x01(\x0b\x32\x32.oak9.tython.azure.microsoft_network_frontdoor.Sku\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x13\n\x03Sku\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x9a\x01\n\x0ePolicySettings\x12\"\n\x1a\x63ustom_block_response_body\x18\x01 \x01(\t\x12)\n!custom_block_response_status_code\x18\x02 \x01(\x05\x12\x15\n\renabled_state\x18\x03 \x01(\t\x12\x0c\n\x04mode\x18\x04 \x01(\t\x12\x14\n\x0credirect_url\x18\x05 \x01(\t\"n\n\x12ManagedRuleSetList\x12X\n\x11managed_rule_sets\x18\x01 \x03(\x0b\x32=.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleSet\"\x9a\x02\n\x0eManagedRuleSet\x12W\n\nexclusions\x18\x01 \x03(\x0b\x32\x43.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleExclusion\x12\x65\n\x14rule_group_overrides\x18\x02 \x03(\x0b\x32G.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleGroupOverride\x12\x15\n\rrule_set_type\x18\x03 \x01(\t\x12\x18\n\x10rule_set_version\x18\x04 \x01(\t\x12\x17\n\x0frule_set_action\x18\x05 \x01(\t\"\xdf\x01\n\x18ManagedRuleGroupOverride\x12W\n\nexclusions\x18\x01 \x03(\x0b\x32\x43.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleExclusion\x12\x17\n\x0frule_group_name\x18\x02 \x01(\t\x12Q\n\x05rules\x18\x03 \x03(\x0b\x32\x42.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleOverride\"\xa6\x01\n\x13ManagedRuleOverride\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x15\n\renabled_state\x18\x02 \x01(\t\x12W\n\nexclusions\x18\x03 \x03(\x0b\x32\x43.oak9.tython.azure.microsoft_network_frontdoor.ManagedRuleExclusion\x12\x0f\n\x07rule_id\x18\x04 \x01(\t\"a\n\x14ManagedRuleExclusion\x12\x16\n\x0ematch_variable\x18\x01 \x01(\t\x12\x10\n\x08selector\x18\x02 \x01(\t\x12\x1f\n\x17selector_match_operator\x18\x03 \x01(\t\"Z\n\x0e\x43ustomRuleList\x12H\n\x05rules\x18\x01 \x03(\x0b\x32\x39.oak9.tython.azure.microsoft_network_frontdoor.CustomRule\"\x85\x02\n\nCustomRule\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x15\n\renabled_state\x18\x02 \x01(\t\x12W\n\x10match_conditions\x18\x03 \x03(\x0b\x32=.oak9.tython.azure.microsoft_network_frontdoor.MatchCondition\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x10\n\x08priority\x18\x05 \x01(\x05\x12&\n\x1erate_limit_duration_in_minutes\x18\x06 \x01(\x05\x12\x1c\n\x14rate_limit_threshold\x18\x07 \x01(\x05\x12\x11\n\trule_type\x18\x08 \x01(\t\"\x8f\x01\n\x0eMatchCondition\x12\x13\n\x0bmatch_value\x18\x01 \x03(\t\x12\x16\n\x0ematch_variable\x18\x02 \x01(\t\x12\x18\n\x10negate_condition\x18\x03 \x01(\x08\x12\x10\n\x08operator\x18\x04 \x01(\t\x12\x10\n\x08selector\x18\x05 \x01(\t\x12\x12\n\ntransforms\x18\x06 \x03(\t\"\xc6\x01\n\x16\x46rontDoorsRulesEngines\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0eresource_state\x18\x03 \x01(\t\x12M\n\x05rules\x18\x04 \x03(\x0b\x32>.oak9.tython.azure.microsoft_network_frontdoor.RulesEngineRule\"\x8a\x02\n\x0fRulesEngineRule\x12P\n\x06\x61\x63tion\x18\x01 \x01(\x0b\x32@.oak9.tython.azure.microsoft_network_frontdoor.RulesEngineAction\x12\x62\n\x10match_conditions\x18\x02 \x03(\x0b\x32H.oak9.tython.azure.microsoft_network_frontdoor.RulesEngineMatchCondition\x12!\n\x19match_processing_behavior\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x10\n\x08priority\x18\x05 \x01(\x05\"\xc1\x01\n\x19RulesEngineMatchCondition\x12\x18\n\x10negate_condition\x18\x01 \x01(\x08\x12 \n\x18rules_engine_match_value\x18\x02 \x03(\t\x12#\n\x1brules_engine_match_variable\x18\x03 \x01(\t\x12\x1d\n\x15rules_engine_operator\x18\x04 \x01(\t\x12\x10\n\x08selector\x18\x05 \x01(\t\x12\x12\n\ntransforms\x18\x06 \x03(\t\"\xb7\x02\n\x11RulesEngineAction\x12[\n\x16request_header_actions\x18\x01 \x03(\x0b\x32;.oak9.tython.azure.microsoft_network_frontdoor.HeaderAction\x12\\\n\x17response_header_actions\x18\x02 \x03(\x0b\x32;.oak9.tython.azure.microsoft_network_frontdoor.HeaderAction\x12g\n\x1croute_configuration_override\x18\x03 \x01(\x0b\x32\x41.oak9.tython.azure.microsoft_network_frontdoor.RouteConfiguration\"N\n\x0cHeaderAction\x12\x1a\n\x12header_action_type\x18\x01 \x01(\t\x12\x13\n\x0bheader_name\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\xdd\x06\n\nFrontDoors\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x10\n\x08location\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12Q\n\rbackend_pools\x18\x04 \x03(\x0b\x32:.oak9.tython.azure.microsoft_network_frontdoor.BackendPool\x12\x63\n\x16\x62\x61\x63kend_pools_settings\x18\x05 \x01(\x0b\x32\x43.oak9.tython.azure.microsoft_network_frontdoor.BackendPoolsSettings\x12\x15\n\renabled_state\x18\x06 \x01(\t\x12\x15\n\rfriendly_name\x18\x07 \x01(\t\x12[\n\x12\x66rontend_endpoints\x18\x08 \x03(\x0b\x32?.oak9.tython.azure.microsoft_network_frontdoor.FrontendEndpoint\x12\x61\n\x15health_probe_settings\x18\t \x03(\x0b\x32\x42.oak9.tython.azure.microsoft_network_frontdoor.HealthProbeSettings\x12\x65\n\x17load_balancing_settings\x18\n \x03(\x0b\x32\x44.oak9.tython.azure.microsoft_network_frontdoor.LoadBalancingSettings\x12\x16\n\x0eresource_state\x18\x0b \x01(\t\x12Q\n\rrouting_rules\x18\x0c \x03(\x0b\x32:.oak9.tython.azure.microsoft_network_frontdoor.RoutingRule\x12Q\n\x04tags\x18\r \x03(\x0b\x32\x43.oak9.tython.azure.microsoft_network_frontdoor.FrontDoors.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xfb\x03\n\x0bRoutingRule\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\renabled_state\x18\x03 \x01(\t\x12\x19\n\x11patterns_to_match\x18\x04 \x03(\t\x12\x16\n\x0eresource_state\x18\x05 \x01(\t\x12^\n\x13route_configuration\x18\x06 \x01(\x0b\x32\x41.oak9.tython.azure.microsoft_network_frontdoor.RouteConfiguration\x12\x14\n\x0crules_engine\x18\x07 \x01(\t\x12\x98\x01\n$web_application_firewall_policy_link\x18\x08 \x01(\x0b\x32j.oak9.tython.azure.microsoft_network_frontdoor.RoutingRuleUpdateParametersWebApplicationFirewallPolicyLink\x12[\n\x12\x66rontend_endpoints\x18\t \x03(\x0b\x32?.oak9.tython.azure.microsoft_network_frontdoor.FrontendEndpoint\x12\x1a\n\x12\x61\x63\x63\x65pted_protocols\x18\n \x01(\t\"I\n;RoutingRuleUpdateParametersWebApplicationFirewallPolicyLink\x12\n\n\x02id\x18\x01 \x01(\t\"\"\n\x12RouteConfiguration\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xc5\x02\n\x10\x46rontendEndpoint\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\thost_name\x18\x03 \x01(\t\x12\x16\n\x0eresource_state\x18\x04 \x01(\t\x12&\n\x1esession_affinity_enabled_state\x18\x05 \x01(\t\x12$\n\x1csession_affinity_ttl_seconds\x18\x06 \x01(\x05\x12\x9d\x01\n$web_application_firewall_policy_link\x18\x07 \x01(\x0b\x32o.oak9.tython.azure.microsoft_network_frontdoor.FrontendEndpointUpdateParametersWebApplicationFirewallPolicyLink\"N\n@FrontendEndpointUpdateParametersWebApplicationFirewallPolicyLink\x12\n\n\x02id\x18\x01 \x01(\t\"a\n\x14\x42\x61\x63kendPoolsSettings\x12&\n\x1e\x65nforce_certificate_name_check\x18\x01 \x01(\t\x12!\n\x19send_recv_timeout_seconds\x18\x02 \x01(\x05\"\xd3\x02\n\x0b\x42\x61\x63kendPool\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12H\n\x08\x62\x61\x63kends\x18\x03 \x03(\x0b\x32\x36.oak9.tython.azure.microsoft_network_frontdoor.Backend\x12\x61\n\x15health_probe_settings\x18\x04 \x01(\x0b\x32\x42.oak9.tython.azure.microsoft_network_frontdoor.HealthProbeSettings\x12\x65\n\x17load_balancing_settings\x18\x05 \x01(\x0b\x32\x44.oak9.tython.azure.microsoft_network_frontdoor.LoadBalancingSettings\x12\x16\n\x0eresource_state\x18\x06 \x01(\t\"\xda\x01\n\x07\x42\x61\x63kend\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x1b\n\x13\x62\x61\x63kend_host_header\x18\x02 \x01(\t\x12\x15\n\renabled_state\x18\x03 \x01(\t\x12\x11\n\thttp_port\x18\x04 \x01(\x05\x12\x12\n\nhttps_port\x18\x05 \x01(\x05\x12\x10\n\x08priority\x18\x06 \x01(\x05\x12\x1a\n\x12private_link_alias\x18\x07 \x01(\t\x12%\n\x1dprivate_link_approval_message\x18\x08 \x01(\t\x12\x0e\n\x06weight\x18\t \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'azure.azure_microsoft_network_frontdoor_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FRONTDOORWEBAPPLICATIONFIREWALLPOLICIES_TAGSENTRY._options = None
  _FRONTDOORWEBAPPLICATIONFIREWALLPOLICIES_TAGSENTRY._serialized_options = b'8\001'
  _FRONTDOORS_TAGSENTRY._options = None
  _FRONTDOORS_TAGSENTRY._serialized_options = b'8\001'
  _MICROSOFT_NETWORK_FRONTDOOR._serialized_start=118
  _MICROSOFT_NETWORK_FRONTDOOR._serialized_end=476
  _LOADBALANCINGSETTINGS._serialized_start=479
  _LOADBALANCINGSETTINGS._serialized_end=651
  _HEALTHPROBESETTINGS._serialized_start=654
  _HEALTHPROBESETTINGS._serialized_end=838
  _FRONTDOORWEBAPPLICATIONFIREWALLPOLICIES._serialized_start=841
  _FRONTDOORWEBAPPLICATIONFIREWALLPOLICIES._serialized_end=1470
  _FRONTDOORWEBAPPLICATIONFIREWALLPOLICIES_TAGSENTRY._serialized_start=1427
  _FRONTDOORWEBAPPLICATIONFIREWALLPOLICIES_TAGSENTRY._serialized_end=1470
  _SKU._serialized_start=1472
  _SKU._serialized_end=1491
  _POLICYSETTINGS._serialized_start=1494
  _POLICYSETTINGS._serialized_end=1648
  _MANAGEDRULESETLIST._serialized_start=1650
  _MANAGEDRULESETLIST._serialized_end=1760
  _MANAGEDRULESET._serialized_start=1763
  _MANAGEDRULESET._serialized_end=2045
  _MANAGEDRULEGROUPOVERRIDE._serialized_start=2048
  _MANAGEDRULEGROUPOVERRIDE._serialized_end=2271
  _MANAGEDRULEOVERRIDE._serialized_start=2274
  _MANAGEDRULEOVERRIDE._serialized_end=2440
  _MANAGEDRULEEXCLUSION._serialized_start=2442
  _MANAGEDRULEEXCLUSION._serialized_end=2539
  _CUSTOMRULELIST._serialized_start=2541
  _CUSTOMRULELIST._serialized_end=2631
  _CUSTOMRULE._serialized_start=2634
  _CUSTOMRULE._serialized_end=2895
  _MATCHCONDITION._serialized_start=2898
  _MATCHCONDITION._serialized_end=3041
  _FRONTDOORSRULESENGINES._serialized_start=3044
  _FRONTDOORSRULESENGINES._serialized_end=3242
  _RULESENGINERULE._serialized_start=3245
  _RULESENGINERULE._serialized_end=3511
  _RULESENGINEMATCHCONDITION._serialized_start=3514
  _RULESENGINEMATCHCONDITION._serialized_end=3707
  _RULESENGINEACTION._serialized_start=3710
  _RULESENGINEACTION._serialized_end=4021
  _HEADERACTION._serialized_start=4023
  _HEADERACTION._serialized_end=4101
  _FRONTDOORS._serialized_start=4104
  _FRONTDOORS._serialized_end=4965
  _FRONTDOORS_TAGSENTRY._serialized_start=1427
  _FRONTDOORS_TAGSENTRY._serialized_end=1470
  _ROUTINGRULE._serialized_start=4968
  _ROUTINGRULE._serialized_end=5475
  _ROUTINGRULEUPDATEPARAMETERSWEBAPPLICATIONFIREWALLPOLICYLINK._serialized_start=5477
  _ROUTINGRULEUPDATEPARAMETERSWEBAPPLICATIONFIREWALLPOLICYLINK._serialized_end=5550
  _ROUTECONFIGURATION._serialized_start=5552
  _ROUTECONFIGURATION._serialized_end=5586
  _FRONTENDENDPOINT._serialized_start=5589
  _FRONTENDENDPOINT._serialized_end=5914
  _FRONTENDENDPOINTUPDATEPARAMETERSWEBAPPLICATIONFIREWALLPOLICYLINK._serialized_start=5916
  _FRONTENDENDPOINTUPDATEPARAMETERSWEBAPPLICATIONFIREWALLPOLICYLINK._serialized_end=5994
  _BACKENDPOOLSSETTINGS._serialized_start=5996
  _BACKENDPOOLSSETTINGS._serialized_end=6093
  _BACKENDPOOL._serialized_start=6096
  _BACKENDPOOL._serialized_end=6435
  _BACKEND._serialized_start=6438
  _BACKEND._serialized_end=6656
# @@protoc_insertion_point(module_scope)
