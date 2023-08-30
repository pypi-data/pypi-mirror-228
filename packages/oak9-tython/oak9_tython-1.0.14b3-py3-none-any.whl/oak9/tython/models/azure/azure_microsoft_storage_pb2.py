# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: azure/azure_microsoft_storage.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#azure/azure_microsoft_storage.proto\x12#oak9.tython.azure.microsoft_storage\x1a\x13shared/shared.proto\"\x8c\x07\n\x11Microsoft_Storage\x12N\n\x10storage_accounts\x18\x01 \x01(\x0b\x32\x34.oak9.tython.azure.microsoft_storage.StorageAccounts\x12h\n\x1estorage_accounts_blob_services\x18\x02 \x03(\x0b\x32@.oak9.tython.azure.microsoft_storage.StorageAccountsBlobServices\x12}\n)storage_accounts_blob_services_containers\x18\x03 \x03(\x0b\x32J.oak9.tython.azure.microsoft_storage.StorageAccountsBlobServicesContainers\x12h\n\x1estorage_accounts_file_services\x18\x04 \x03(\x0b\x32@.oak9.tython.azure.microsoft_storage.StorageAccountsFileServices\x12t\n$storage_accounts_management_policies\x18\x05 \x03(\x0b\x32\x46.oak9.tython.azure.microsoft_storage.StorageAccountsManagementPolicies\x12\x85\x01\n-storage_accounts_private_endpoint_connections\x18\x06 \x03(\x0b\x32N.oak9.tython.azure.microsoft_storage.StorageAccountsPrivateEndpointConnections\x12j\n\x1fstorage_accounts_queue_services\x18\x07 \x03(\x0b\x32\x41.oak9.tython.azure.microsoft_storage.StorageAccountsQueueServices\x12j\n\x1fstorage_accounts_table_services\x18\x08 \x03(\x0b\x32\x41.oak9.tython.azure.microsoft_storage.StorageAccountsTableServices\"k\n\"StorageAccountsTableServicesTables\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x9c\x02\n\x1cStorageAccountsTableServices\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12<\n\x04\x63ors\x18\x03 \x01(\x0b\x32..oak9.tython.azure.microsoft_storage.CorsRules\x12w\n&storage_accounts_table_services_tables\x18\x04 \x03(\x0b\x32G.oak9.tython.azure.microsoft_storage.StorageAccountsTableServicesTables\"\x85\x02\n\"StorageAccountsQueueServicesQueues\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12g\n\x08metadata\x18\x03 \x03(\x0b\x32U.oak9.tython.azure.microsoft_storage.StorageAccountsQueueServicesQueues.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x9c\x02\n\x1cStorageAccountsQueueServices\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12<\n\x04\x63ors\x18\x03 \x01(\x0b\x32..oak9.tython.azure.microsoft_storage.CorsRules\x12w\n&storage_accounts_queue_services_queues\x18\x04 \x03(\x0b\x32G.oak9.tython.azure.microsoft_storage.StorageAccountsQueueServicesQueues\"\xd5\x02\n)StorageAccountsPrivateEndpointConnections\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12N\n\x10private_endpoint\x18\x03 \x01(\x0b\x32\x34.oak9.tython.azure.microsoft_storage.PrivateEndpoint\x12u\n%private_link_service_connection_state\x18\x04 \x01(\x0b\x32\x46.oak9.tython.azure.microsoft_storage.PrivateLinkServiceConnectionState\x12\x1a\n\x12provisioning_state\x18\x05 \x01(\t\"a\n!PrivateLinkServiceConnectionState\x12\x17\n\x0f\x61\x63tion_required\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\"\x1f\n\x0fPrivateEndpoint\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xf7\x01\n(StorageAccountsObjectReplicationPolicies\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1b\n\x13\x64\x65stination_account\x18\x03 \x01(\t\x12O\n\x05rules\x18\x04 \x03(\x0b\x32@.oak9.tython.azure.microsoft_storage.ObjectReplicationPolicyRule\x12\x16\n\x0esource_account\x18\x05 \x01(\t\"\xbc\x01\n\x1bObjectReplicationPolicyRule\x12\x1d\n\x15\x64\x65stination_container\x18\x01 \x01(\t\x12S\n\x07\x66ilters\x18\x02 \x01(\x0b\x32\x42.oak9.tython.azure.microsoft_storage.ObjectReplicationPolicyFilter\x12\x0f\n\x07rule_id\x18\x03 \x01(\t\x12\x18\n\x10source_container\x18\x04 \x01(\t\"P\n\x1dObjectReplicationPolicyFilter\x12\x19\n\x11min_creation_time\x18\x01 \x01(\t\x12\x14\n\x0cprefix_match\x18\x02 \x03(\t\"\xb7\x01\n!StorageAccountsManagementPolicies\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12K\n\x06policy\x18\x03 \x01(\x0b\x32;.oak9.tython.azure.microsoft_storage.ManagementPolicySchema\"b\n\x16ManagementPolicySchema\x12H\n\x05rules\x18\x01 \x03(\x0b\x32\x39.oak9.tython.azure.microsoft_storage.ManagementPolicyRule\"\x98\x01\n\x14ManagementPolicyRule\x12S\n\ndefinition\x18\x01 \x01(\x0b\x32?.oak9.tython.azure.microsoft_storage.ManagementPolicyDefinition\x12\x0f\n\x07\x65nabled\x18\x02 \x01(\x08\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\"\xb8\x01\n\x1aManagementPolicyDefinition\x12L\n\x07\x61\x63tions\x18\x01 \x01(\x0b\x32;.oak9.tython.azure.microsoft_storage.ManagementPolicyAction\x12L\n\x07\x66ilters\x18\x02 \x01(\x0b\x32;.oak9.tython.azure.microsoft_storage.ManagementPolicyFilter\"\x8c\x01\n\x16ManagementPolicyFilter\x12H\n\x10\x62lob_index_match\x18\x01 \x03(\x0b\x32..oak9.tython.azure.microsoft_storage.TagFilter\x12\x12\n\nblob_types\x18\x02 \x03(\t\x12\x14\n\x0cprefix_match\x18\x03 \x03(\t\"4\n\tTagFilter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02op\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x8a\x02\n\x16ManagementPolicyAction\x12P\n\tbase_blob\x18\x01 \x01(\x0b\x32=.oak9.tython.azure.microsoft_storage.ManagementPolicyBaseBlob\x12O\n\x08snapshot\x18\x02 \x01(\x0b\x32=.oak9.tython.azure.microsoft_storage.ManagementPolicySnapShot\x12M\n\x07version\x18\x03 \x01(\x0b\x32<.oak9.tython.azure.microsoft_storage.ManagementPolicyVersion\"\x80\x02\n\x17ManagementPolicyVersion\x12\x46\n\x06\x64\x65lete\x18\x01 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.DateAfterCreation\x12O\n\x0ftier_to_archive\x18\x02 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.DateAfterCreation\x12L\n\x0ctier_to_cool\x18\x03 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.DateAfterCreation\"\x81\x02\n\x18ManagementPolicySnapShot\x12\x46\n\x06\x64\x65lete\x18\x01 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.DateAfterCreation\x12O\n\x0ftier_to_archive\x18\x02 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.DateAfterCreation\x12L\n\x0ctier_to_cool\x18\x03 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.DateAfterCreation\"=\n\x11\x44\x61teAfterCreation\x12(\n days_after_creation_greater_than\x18\x01 \x01(\x01\"\xb8\x02\n\x18ManagementPolicyBaseBlob\x12J\n\x06\x64\x65lete\x18\x01 \x01(\x0b\x32:.oak9.tython.azure.microsoft_storage.DateAfterModification\x12)\n!enable_auto_tier_to_hot_from_cool\x18\x02 \x01(\x08\x12S\n\x0ftier_to_archive\x18\x03 \x01(\x0b\x32:.oak9.tython.azure.microsoft_storage.DateAfterModification\x12P\n\x0ctier_to_cool\x18\x04 \x01(\x0b\x32:.oak9.tython.azure.microsoft_storage.DateAfterModification\"w\n\x15\x44\x61teAfterModification\x12\x30\n(days_after_last_access_time_greater_than\x18\x01 \x01(\x01\x12,\n$days_after_modification_greater_than\x18\x02 \x01(\x01\"\xa8\x03\n\x19StorageAccountsLocalUsers\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0ehas_shared_key\x18\x03 \x01(\x08\x12\x13\n\x0bhas_ssh_key\x18\x04 \x01(\x08\x12\x18\n\x10has_ssh_password\x18\x05 \x01(\x08\x12\x16\n\x0ehome_directory\x18\x06 \x01(\t\x12O\n\x11permission_scopes\x18\x07 \x03(\x0b\x32\x34.oak9.tython.azure.microsoft_storage.PermissionScope\x12N\n\x13ssh_authorized_keys\x18\x08 \x03(\x0b\x32\x31.oak9.tython.azure.microsoft_storage.SshPublicKey\x12\x44\n\x0bsystem_data\x18\t \x01(\x0b\x32/.oak9.tython.azure.microsoft_storage.SystemData\"0\n\x0cSshPublicKey\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\"N\n\x0fPermissionScope\x12\x13\n\x0bpermissions\x18\x01 \x01(\t\x12\x15\n\rresource_name\x18\x02 \x01(\t\x12\x0f\n\x07service\x18\x03 \x01(\t\"\xff\x01\n StorageAccountsInventoryPolicies\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12N\n\x06policy\x18\x03 \x01(\x0b\x32>.oak9.tython.azure.microsoft_storage.BlobInventoryPolicySchema\x12\x44\n\x0bsystem_data\x18\x04 \x01(\x0b\x32/.oak9.tython.azure.microsoft_storage.SystemData\"\xa0\x01\n\nSystemData\x12\x12\n\ncreated_at\x18\x01 \x01(\t\x12\x12\n\ncreated_by\x18\x02 \x01(\t\x12\x17\n\x0f\x63reated_by_type\x18\x03 \x01(\t\x12\x18\n\x10last_modified_at\x18\x04 \x01(\t\x12\x18\n\x10last_modified_by\x18\x05 \x01(\t\x12\x1d\n\x15last_modified_by_type\x18\x06 \x01(\t\"\x87\x01\n\x19\x42lobInventoryPolicySchema\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\x12K\n\x05rules\x18\x02 \x03(\x0b\x32<.oak9.tython.azure.microsoft_storage.BlobInventoryPolicyRule\x12\x0c\n\x04type\x18\x03 \x01(\t\"\xa5\x01\n\x17\x42lobInventoryPolicyRule\x12V\n\ndefinition\x18\x01 \x01(\x0b\x32\x42.oak9.tython.azure.microsoft_storage.BlobInventoryPolicyDefinition\x12\x13\n\x0b\x64\x65stination\x18\x02 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x03 \x01(\x08\x12\x0c\n\x04name\x18\x04 \x01(\t\"\xbe\x01\n\x1d\x42lobInventoryPolicyDefinition\x12O\n\x07\x66ilters\x18\x01 \x01(\x0b\x32>.oak9.tython.azure.microsoft_storage.BlobInventoryPolicyFilter\x12\x0e\n\x06\x66ormat\x18\x02 \x01(\t\x12\x13\n\x0bobject_type\x18\x03 \x01(\t\x12\x10\n\x08schedule\x18\x04 \x01(\t\x12\x15\n\rschema_fields\x18\x05 \x03(\t\"\x7f\n\x19\x42lobInventoryPolicyFilter\x12\x12\n\nblob_types\x18\x01 \x03(\t\x12\x1d\n\x15include_blob_versions\x18\x02 \x01(\x08\x12\x19\n\x11include_snapshots\x18\x03 \x01(\x08\x12\x14\n\x0cprefix_match\x18\x04 \x03(\t\"\xb0\x03\n!StorageAccountsFileServicesShares\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x61\x63\x63\x65ss_tier\x18\x03 \x01(\t\x12\x19\n\x11\x65nabled_protocols\x18\x04 \x01(\t\x12\x66\n\x08metadata\x18\x05 \x03(\x0b\x32T.oak9.tython.azure.microsoft_storage.StorageAccountsFileServicesShares.MetadataEntry\x12\x13\n\x0broot_squash\x18\x06 \x01(\t\x12\x13\n\x0bshare_quota\x18\x07 \x01(\x05\x12Q\n\x12signed_identifiers\x18\x08 \x03(\x0b\x32\x35.oak9.tython.azure.microsoft_storage.SignedIdentifier\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"h\n\x10SignedIdentifier\x12H\n\raccess_policy\x18\x01 \x01(\x0b\x32\x31.oak9.tython.azure.microsoft_storage.AccessPolicy\x12\n\n\x02id\x18\x02 \x01(\t\"K\n\x0c\x41\x63\x63\x65ssPolicy\x12\x13\n\x0b\x65xpiry_time\x18\x01 \x01(\t\x12\x12\n\npermission\x18\x02 \x01(\t\x12\x12\n\nstart_time\x18\x03 \x01(\t\"\xce\x03\n\x1bStorageAccountsFileServices\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12<\n\x04\x63ors\x18\x03 \x01(\x0b\x32..oak9.tython.azure.microsoft_storage.CorsRules\x12P\n\x11protocol_settings\x18\x04 \x01(\x0b\x32\x35.oak9.tython.azure.microsoft_storage.ProtocolSettings\x12\x61\n\x1dshare_delete_retention_policy\x18\x05 \x01(\x0b\x32:.oak9.tython.azure.microsoft_storage.DeleteRetentionPolicy\x12u\n%storage_accounts_file_services_shares\x18\x06 \x03(\x0b\x32\x46.oak9.tython.azure.microsoft_storage.StorageAccountsFileServicesShares\"P\n\x10ProtocolSettings\x12<\n\x03smb\x18\x01 \x01(\x0b\x32/.oak9.tython.azure.microsoft_storage.SmbSetting\"\xc7\x01\n\nSmbSetting\x12\x1e\n\x16\x61uthentication_methods\x18\x01 \x01(\t\x12\x1a\n\x12\x63hannel_encryption\x18\x02 \x01(\t\x12\"\n\x1akerberos_ticket_encryption\x18\x03 \x01(\t\x12G\n\x0cmultichannel\x18\x04 \x01(\x0b\x32\x31.oak9.tython.azure.microsoft_storage.Multichannel\x12\x10\n\x08versions\x18\x05 \x01(\t\"\x1f\n\x0cMultichannel\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\"\x98\x02\n\x1fStorageAccountsEncryptionScopes\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x64\n\x14key_vault_properties\x18\x03 \x01(\x0b\x32\x46.oak9.tython.azure.microsoft_storage.EncryptionScopeKeyVaultProperties\x12)\n!require_infrastructure_encryption\x18\x04 \x01(\x08\x12\x0e\n\x06source\x18\x05 \x01(\t\x12\r\n\x05state\x18\x06 \x01(\t\"4\n!EncryptionScopeKeyVaultProperties\x12\x0f\n\x07key_uri\x18\x01 \x01(\t\"\x88\x02\n9StorageAccountsBlobServicesContainersImmutabilityPolicies\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x1d\x61llow_protected_append_writes\x18\x03 \x01(\x08\x12)\n!allow_protected_append_writes_all\x18\x04 \x01(\x08\x12\x32\n*immutability_period_since_creation_in_days\x18\x05 \x01(\x05\"\xcb\x05\n%StorageAccountsBlobServicesContainers\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12 \n\x18\x64\x65\x66\x61ult_encryption_scope\x18\x03 \x01(\t\x12&\n\x1e\x64\x65ny_encryption_scope_override\x18\x04 \x01(\x08\x12 \n\x18\x65nable_nfs_v3_all_squash\x18\x05 \x01(\x08\x12!\n\x19\x65nable_nfs_v3_root_squash\x18\x06 \x01(\x08\x12n\n!immutable_storage_with_versioning\x18\x07 \x01(\x0b\x32\x43.oak9.tython.azure.microsoft_storage.ImmutableStorageWithVersioning\x12j\n\x08metadata\x18\x08 \x03(\x0b\x32X.oak9.tython.azure.microsoft_storage.StorageAccountsBlobServicesContainers.MetadataEntry\x12\x15\n\rpublic_access\x18\t \x01(\t\x12\xa7\x01\n?storage_accounts_blob_services_containers_immutability_policies\x18\n \x03(\x0b\x32^.oak9.tython.azure.microsoft_storage.StorageAccountsBlobServicesContainersImmutabilityPolicies\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"1\n\x1eImmutableStorageWithVersioning\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\"\xda\x05\n\x1bStorageAccountsBlobServices\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12)\n!automatic_snapshot_policy_enabled\x18\x03 \x01(\x08\x12\x44\n\x0b\x63hange_feed\x18\x04 \x01(\x0b\x32/.oak9.tython.azure.microsoft_storage.ChangeFeed\x12\x65\n!container_delete_retention_policy\x18\x05 \x01(\x0b\x32:.oak9.tython.azure.microsoft_storage.DeleteRetentionPolicy\x12<\n\x04\x63ors\x18\x06 \x01(\x0b\x32..oak9.tython.azure.microsoft_storage.CorsRules\x12\x1f\n\x17\x64\x65\x66\x61ult_service_version\x18\x07 \x01(\t\x12[\n\x17\x64\x65lete_retention_policy\x18\x08 \x01(\x0b\x32:.oak9.tython.azure.microsoft_storage.DeleteRetentionPolicy\x12\x1d\n\x15is_versioning_enabled\x18\t \x01(\x08\x12k\n last_access_time_tracking_policy\x18\n \x01(\x0b\x32\x41.oak9.tython.azure.microsoft_storage.LastAccessTimeTrackingPolicy\x12T\n\x0erestore_policy\x18\x0b \x01(\x0b\x32<.oak9.tython.azure.microsoft_storage.RestorePolicyProperties\"8\n\x17RestorePolicyProperties\x12\x0c\n\x04\x64\x61ys\x18\x01 \x01(\x05\x12\x0f\n\x07\x65nabled\x18\x02 \x01(\x08\"u\n\x1cLastAccessTimeTrackingPolicy\x12\x11\n\tblob_type\x18\x01 \x03(\t\x12\x0e\n\x06\x65nable\x18\x02 \x01(\x08\x12\x0c\n\x04name\x18\x03 \x01(\t\x12$\n\x1ctracking_granularity_in_days\x18\x04 \x01(\x05\"N\n\tCorsRules\x12\x41\n\ncors_rules\x18\x01 \x03(\x0b\x32-.oak9.tython.azure.microsoft_storage.CorsRule\"\x8a\x01\n\x08\x43orsRule\x12\x17\n\x0f\x61llowed_headers\x18\x01 \x03(\t\x12\x17\n\x0f\x61llowed_methods\x18\x02 \x03(\t\x12\x17\n\x0f\x61llowed_origins\x18\x03 \x03(\t\x12\x17\n\x0f\x65xposed_headers\x18\x04 \x03(\t\x12\x1a\n\x12max_age_in_seconds\x18\x05 \x01(\x05\"6\n\x15\x44\x65leteRetentionPolicy\x12\x0c\n\x04\x64\x61ys\x18\x01 \x01(\x05\x12\x0f\n\x07\x65nabled\x18\x02 \x01(\x08\"8\n\nChangeFeed\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\x12\x19\n\x11retention_in_days\x18\x02 \x01(\x05\"\xe0\x0f\n\x0fStorageAccounts\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12P\n\x11\x65xtended_location\x18\x02 \x01(\x0b\x32\x35.oak9.tython.azure.microsoft_storage.ExtendedLocation\x12?\n\x08identity\x18\x03 \x01(\x0b\x32-.oak9.tython.azure.microsoft_storage.Identity\x12\x0c\n\x04kind\x18\x04 \x01(\t\x12\x10\n\x08location\x18\x05 \x01(\t\x12\x0c\n\x04name\x18\x06 \x01(\t\x12\x13\n\x0b\x61\x63\x63\x65ss_tier\x18\x07 \x01(\t\x12 \n\x18\x61llow_blob_public_access\x18\x08 \x01(\x08\x12&\n\x1e\x61llow_cross_tenant_replication\x18\t \x01(\x08\x12\x1a\n\x12\x61llowed_copy_scope\x18\n \x01(\t\x12\x1f\n\x17\x61llow_shared_key_access\x18\x0b \x01(\x08\x12}\n)azure_files_identity_based_authentication\x18\x0c \x01(\x0b\x32J.oak9.tython.azure.microsoft_storage.AzureFilesIdentityBasedAuthentication\x12H\n\rcustom_domain\x18\r \x01(\x0b\x32\x31.oak9.tython.azure.microsoft_storage.CustomDomain\x12(\n default_to_o_auth_authentication\x18\x0e \x01(\x08\x12\x43\n\nencryption\x18\x0f \x01(\x0b\x32/.oak9.tython.azure.microsoft_storage.Encryption\x12g\n!immutable_storage_with_versioning\x18\x10 \x01(\x0b\x32<.oak9.tython.azure.microsoft_storage.ImmutableStorageAccount\x12\x16\n\x0eis_hns_enabled\x18\x11 \x01(\x08\x12\x1d\n\x15is_local_user_enabled\x18\x12 \x01(\x08\x12\x19\n\x11is_nfs_v3_enabled\x18\x13 \x01(\x08\x12\x17\n\x0fis_sftp_enabled\x18\x14 \x01(\x08\x12\x42\n\nkey_policy\x18\x15 \x01(\x0b\x32..oak9.tython.azure.microsoft_storage.KeyPolicy\x12\x1f\n\x17large_file_shares_state\x18\x16 \x01(\t\x12\x1b\n\x13minimum_tls_version\x18\x17 \x01(\t\x12I\n\x0cnetwork_acls\x18\x18 \x01(\x0b\x32\x33.oak9.tython.azure.microsoft_storage.NetworkRuleSet\x12\x1d\n\x15public_network_access\x18\x19 \x01(\t\x12R\n\x12routing_preference\x18\x1a \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.RoutingPreference\x12\x42\n\nsas_policy\x18\x1b \x01(\x0b\x32..oak9.tython.azure.microsoft_storage.SasPolicy\x12#\n\x1bsupports_https_traffic_only\x18\x1c \x01(\x08\x12\x35\n\x03sku\x18\x1d \x01(\x0b\x32(.oak9.tython.azure.microsoft_storage.Sku\x12L\n\x04tags\x18\x1e \x03(\x0b\x32>.oak9.tython.azure.microsoft_storage.StorageAccounts.TagsEntry\x12r\n#storage_accounts_inventory_policies\x18\x1f \x03(\x0b\x32\x45.oak9.tython.azure.microsoft_storage.StorageAccountsInventoryPolicies\x12\x83\x01\n,storage_accounts_object_replication_policies\x18  \x03(\x0b\x32M.oak9.tython.azure.microsoft_storage.StorageAccountsObjectReplicationPolicies\x12\x64\n\x1cstorage_accounts_local_users\x18! \x03(\x0b\x32>.oak9.tython.azure.microsoft_storage.StorageAccountsLocalUsers\x12p\n\"storage_accounts_encryption_scopes\x18\" \x03(\x0b\x32\x44.oak9.tython.azure.microsoft_storage.StorageAccountsEncryptionScopes\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"!\n\x03Sku\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04tier\x18\x02 \x01(\t\"E\n\tSasPolicy\x12\x19\n\x11\x65xpiration_action\x18\x01 \x01(\t\x12\x1d\n\x15sas_expiration_period\x18\x02 \x01(\t\"t\n\x11RoutingPreference\x12\"\n\x1apublish_internet_endpoints\x18\x01 \x01(\x08\x12#\n\x1bpublish_microsoft_endpoints\x18\x02 \x01(\x08\x12\x16\n\x0erouting_choice\x18\x03 \x01(\t\"\xa7\x02\n\x0eNetworkRuleSet\x12\x0e\n\x06\x62ypass\x18\x01 \x01(\t\x12\x16\n\x0e\x64\x65\x66\x61ult_action\x18\x02 \x01(\t\x12=\n\x08ip_rules\x18\x03 \x03(\x0b\x32+.oak9.tython.azure.microsoft_storage.IPRule\x12V\n\x15resource_access_rules\x18\x04 \x03(\x0b\x32\x37.oak9.tython.azure.microsoft_storage.ResourceAccessRule\x12V\n\x15virtual_network_rules\x18\x05 \x03(\x0b\x32\x37.oak9.tython.azure.microsoft_storage.VirtualNetworkRule\"?\n\x12VirtualNetworkRule\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\"<\n\x12ResourceAccessRule\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\x12\x11\n\ttenant_id\x18\x02 \x01(\t\"\'\n\x06IPRule\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"2\n\tKeyPolicy\x12%\n\x1dkey_expiration_period_in_days\x18\x01 \x01(\x05\"\x91\x01\n\x17ImmutableStorageAccount\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\x12\x65\n\x13immutability_policy\x18\x02 \x01(\x0b\x32H.oak9.tython.azure.microsoft_storage.AccountImmutabilityPolicyProperties\"\x8f\x01\n#AccountImmutabilityPolicyProperties\x12%\n\x1d\x61llow_protected_append_writes\x18\x01 \x01(\x08\x12\x32\n*immutability_period_since_creation_in_days\x18\x02 \x01(\x05\x12\r\n\x05state\x18\x03 \x01(\t\"\xb6\x02\n\nEncryption\x12I\n\x08identity\x18\x01 \x01(\x0b\x32\x37.oak9.tython.azure.microsoft_storage.EncryptionIdentity\x12\x12\n\nkey_source\x18\x02 \x01(\t\x12S\n\x12keyvaultproperties\x18\x03 \x01(\x0b\x32\x37.oak9.tython.azure.microsoft_storage.KeyVaultProperties\x12)\n!require_infrastructure_encryption\x18\x04 \x01(\x08\x12I\n\x08services\x18\x05 \x01(\x0b\x32\x37.oak9.tython.azure.microsoft_storage.EncryptionServices\"\xae\x02\n\x12\x45ncryptionServices\x12\x44\n\x04\x62lob\x18\x01 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.EncryptionService\x12\x44\n\x04\x66ile\x18\x02 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.EncryptionService\x12\x45\n\x05queue\x18\x03 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.EncryptionService\x12\x45\n\x05table\x18\x04 \x01(\x0b\x32\x36.oak9.tython.azure.microsoft_storage.EncryptionService\"6\n\x11\x45ncryptionService\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\x12\x10\n\x08key_type\x18\x02 \x01(\t\"N\n\x12KeyVaultProperties\x12\x0f\n\x07keyname\x18\x01 \x01(\t\x12\x13\n\x0bkeyvaulturi\x18\x02 \x01(\t\x12\x12\n\nkeyversion\x18\x03 \x01(\t\"Z\n\x12\x45ncryptionIdentity\x12$\n\x1c\x66\x65\x64\x65rated_identity_client_id\x18\x01 \x01(\t\x12\x1e\n\x16user_assigned_identity\x18\x02 \x01(\t\"9\n\x0c\x43ustomDomain\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1b\n\x13use_sub_domain_name\x18\x02 \x01(\x08\"\xd1\x01\n%AzureFilesIdentityBasedAuthentication\x12\x63\n\x1b\x61\x63tive_directory_properties\x18\x01 \x01(\x0b\x32>.oak9.tython.azure.microsoft_storage.ActiveDirectoryProperties\x12 \n\x18\x64\x65\x66\x61ult_share_permission\x18\x02 \x01(\t\x12!\n\x19\x64irectory_service_options\x18\x03 \x01(\t\"\xd7\x01\n\x19\x41\x63tiveDirectoryProperties\x12\x14\n\x0c\x61\x63\x63ount_type\x18\x01 \x01(\t\x12\x19\n\x11\x61zure_storage_sid\x18\x02 \x01(\t\x12\x13\n\x0b\x64omain_guid\x18\x03 \x01(\t\x12\x13\n\x0b\x64omain_name\x18\x04 \x01(\t\x12\x12\n\ndomain_sid\x18\x05 \x01(\t\x12\x13\n\x0b\x66orest_name\x18\x06 \x01(\t\x12\x1c\n\x14net_bios_domain_name\x18\x07 \x01(\t\x12\x18\n\x10sam_account_name\x18\x08 \x01(\t\"\xc4\x01\n\x08Identity\x12\x0c\n\x04type\x18\x01 \x01(\t\x12k\n\x18user_assigned_identities\x18\x02 \x03(\x0b\x32I.oak9.tython.azure.microsoft_storage.Identity.UserAssignedIdentitiesEntry\x1a=\n\x1bUserAssignedIdentitiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\".\n\x10\x45xtendedLocation\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'azure.azure_microsoft_storage_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STORAGEACCOUNTSQUEUESERVICESQUEUES_METADATAENTRY._options = None
  _STORAGEACCOUNTSQUEUESERVICESQUEUES_METADATAENTRY._serialized_options = b'8\001'
  _STORAGEACCOUNTSFILESERVICESSHARES_METADATAENTRY._options = None
  _STORAGEACCOUNTSFILESERVICESSHARES_METADATAENTRY._serialized_options = b'8\001'
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERS_METADATAENTRY._options = None
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERS_METADATAENTRY._serialized_options = b'8\001'
  _STORAGEACCOUNTS_TAGSENTRY._options = None
  _STORAGEACCOUNTS_TAGSENTRY._serialized_options = b'8\001'
  _IDENTITY_USERASSIGNEDIDENTITIESENTRY._options = None
  _IDENTITY_USERASSIGNEDIDENTITIESENTRY._serialized_options = b'8\001'
  _MICROSOFT_STORAGE._serialized_start=98
  _MICROSOFT_STORAGE._serialized_end=1006
  _STORAGEACCOUNTSTABLESERVICESTABLES._serialized_start=1008
  _STORAGEACCOUNTSTABLESERVICESTABLES._serialized_end=1115
  _STORAGEACCOUNTSTABLESERVICES._serialized_start=1118
  _STORAGEACCOUNTSTABLESERVICES._serialized_end=1402
  _STORAGEACCOUNTSQUEUESERVICESQUEUES._serialized_start=1405
  _STORAGEACCOUNTSQUEUESERVICESQUEUES._serialized_end=1666
  _STORAGEACCOUNTSQUEUESERVICESQUEUES_METADATAENTRY._serialized_start=1619
  _STORAGEACCOUNTSQUEUESERVICESQUEUES_METADATAENTRY._serialized_end=1666
  _STORAGEACCOUNTSQUEUESERVICES._serialized_start=1669
  _STORAGEACCOUNTSQUEUESERVICES._serialized_end=1953
  _STORAGEACCOUNTSPRIVATEENDPOINTCONNECTIONS._serialized_start=1956
  _STORAGEACCOUNTSPRIVATEENDPOINTCONNECTIONS._serialized_end=2297
  _PRIVATELINKSERVICECONNECTIONSTATE._serialized_start=2299
  _PRIVATELINKSERVICECONNECTIONSTATE._serialized_end=2396
  _PRIVATEENDPOINT._serialized_start=2398
  _PRIVATEENDPOINT._serialized_end=2429
  _STORAGEACCOUNTSOBJECTREPLICATIONPOLICIES._serialized_start=2432
  _STORAGEACCOUNTSOBJECTREPLICATIONPOLICIES._serialized_end=2679
  _OBJECTREPLICATIONPOLICYRULE._serialized_start=2682
  _OBJECTREPLICATIONPOLICYRULE._serialized_end=2870
  _OBJECTREPLICATIONPOLICYFILTER._serialized_start=2872
  _OBJECTREPLICATIONPOLICYFILTER._serialized_end=2952
  _STORAGEACCOUNTSMANAGEMENTPOLICIES._serialized_start=2955
  _STORAGEACCOUNTSMANAGEMENTPOLICIES._serialized_end=3138
  _MANAGEMENTPOLICYSCHEMA._serialized_start=3140
  _MANAGEMENTPOLICYSCHEMA._serialized_end=3238
  _MANAGEMENTPOLICYRULE._serialized_start=3241
  _MANAGEMENTPOLICYRULE._serialized_end=3393
  _MANAGEMENTPOLICYDEFINITION._serialized_start=3396
  _MANAGEMENTPOLICYDEFINITION._serialized_end=3580
  _MANAGEMENTPOLICYFILTER._serialized_start=3583
  _MANAGEMENTPOLICYFILTER._serialized_end=3723
  _TAGFILTER._serialized_start=3725
  _TAGFILTER._serialized_end=3777
  _MANAGEMENTPOLICYACTION._serialized_start=3780
  _MANAGEMENTPOLICYACTION._serialized_end=4046
  _MANAGEMENTPOLICYVERSION._serialized_start=4049
  _MANAGEMENTPOLICYVERSION._serialized_end=4305
  _MANAGEMENTPOLICYSNAPSHOT._serialized_start=4308
  _MANAGEMENTPOLICYSNAPSHOT._serialized_end=4565
  _DATEAFTERCREATION._serialized_start=4567
  _DATEAFTERCREATION._serialized_end=4628
  _MANAGEMENTPOLICYBASEBLOB._serialized_start=4631
  _MANAGEMENTPOLICYBASEBLOB._serialized_end=4943
  _DATEAFTERMODIFICATION._serialized_start=4945
  _DATEAFTERMODIFICATION._serialized_end=5064
  _STORAGEACCOUNTSLOCALUSERS._serialized_start=5067
  _STORAGEACCOUNTSLOCALUSERS._serialized_end=5491
  _SSHPUBLICKEY._serialized_start=5493
  _SSHPUBLICKEY._serialized_end=5541
  _PERMISSIONSCOPE._serialized_start=5543
  _PERMISSIONSCOPE._serialized_end=5621
  _STORAGEACCOUNTSINVENTORYPOLICIES._serialized_start=5624
  _STORAGEACCOUNTSINVENTORYPOLICIES._serialized_end=5879
  _SYSTEMDATA._serialized_start=5882
  _SYSTEMDATA._serialized_end=6042
  _BLOBINVENTORYPOLICYSCHEMA._serialized_start=6045
  _BLOBINVENTORYPOLICYSCHEMA._serialized_end=6180
  _BLOBINVENTORYPOLICYRULE._serialized_start=6183
  _BLOBINVENTORYPOLICYRULE._serialized_end=6348
  _BLOBINVENTORYPOLICYDEFINITION._serialized_start=6351
  _BLOBINVENTORYPOLICYDEFINITION._serialized_end=6541
  _BLOBINVENTORYPOLICYFILTER._serialized_start=6543
  _BLOBINVENTORYPOLICYFILTER._serialized_end=6670
  _STORAGEACCOUNTSFILESERVICESSHARES._serialized_start=6673
  _STORAGEACCOUNTSFILESERVICESSHARES._serialized_end=7105
  _STORAGEACCOUNTSFILESERVICESSHARES_METADATAENTRY._serialized_start=1619
  _STORAGEACCOUNTSFILESERVICESSHARES_METADATAENTRY._serialized_end=1666
  _SIGNEDIDENTIFIER._serialized_start=7107
  _SIGNEDIDENTIFIER._serialized_end=7211
  _ACCESSPOLICY._serialized_start=7213
  _ACCESSPOLICY._serialized_end=7288
  _STORAGEACCOUNTSFILESERVICES._serialized_start=7291
  _STORAGEACCOUNTSFILESERVICES._serialized_end=7753
  _PROTOCOLSETTINGS._serialized_start=7755
  _PROTOCOLSETTINGS._serialized_end=7835
  _SMBSETTING._serialized_start=7838
  _SMBSETTING._serialized_end=8037
  _MULTICHANNEL._serialized_start=8039
  _MULTICHANNEL._serialized_end=8070
  _STORAGEACCOUNTSENCRYPTIONSCOPES._serialized_start=8073
  _STORAGEACCOUNTSENCRYPTIONSCOPES._serialized_end=8353
  _ENCRYPTIONSCOPEKEYVAULTPROPERTIES._serialized_start=8355
  _ENCRYPTIONSCOPEKEYVAULTPROPERTIES._serialized_end=8407
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERSIMMUTABILITYPOLICIES._serialized_start=8410
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERSIMMUTABILITYPOLICIES._serialized_end=8674
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERS._serialized_start=8677
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERS._serialized_end=9392
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERS_METADATAENTRY._serialized_start=1619
  _STORAGEACCOUNTSBLOBSERVICESCONTAINERS_METADATAENTRY._serialized_end=1666
  _IMMUTABLESTORAGEWITHVERSIONING._serialized_start=9394
  _IMMUTABLESTORAGEWITHVERSIONING._serialized_end=9443
  _STORAGEACCOUNTSBLOBSERVICES._serialized_start=9446
  _STORAGEACCOUNTSBLOBSERVICES._serialized_end=10176
  _RESTOREPOLICYPROPERTIES._serialized_start=10178
  _RESTOREPOLICYPROPERTIES._serialized_end=10234
  _LASTACCESSTIMETRACKINGPOLICY._serialized_start=10236
  _LASTACCESSTIMETRACKINGPOLICY._serialized_end=10353
  _CORSRULES._serialized_start=10355
  _CORSRULES._serialized_end=10433
  _CORSRULE._serialized_start=10436
  _CORSRULE._serialized_end=10574
  _DELETERETENTIONPOLICY._serialized_start=10576
  _DELETERETENTIONPOLICY._serialized_end=10630
  _CHANGEFEED._serialized_start=10632
  _CHANGEFEED._serialized_end=10688
  _STORAGEACCOUNTS._serialized_start=10691
  _STORAGEACCOUNTS._serialized_end=12707
  _STORAGEACCOUNTS_TAGSENTRY._serialized_start=12664
  _STORAGEACCOUNTS_TAGSENTRY._serialized_end=12707
  _SKU._serialized_start=12709
  _SKU._serialized_end=12742
  _SASPOLICY._serialized_start=12744
  _SASPOLICY._serialized_end=12813
  _ROUTINGPREFERENCE._serialized_start=12815
  _ROUTINGPREFERENCE._serialized_end=12931
  _NETWORKRULESET._serialized_start=12934
  _NETWORKRULESET._serialized_end=13229
  _VIRTUALNETWORKRULE._serialized_start=13231
  _VIRTUALNETWORKRULE._serialized_end=13294
  _RESOURCEACCESSRULE._serialized_start=13296
  _RESOURCEACCESSRULE._serialized_end=13356
  _IPRULE._serialized_start=13358
  _IPRULE._serialized_end=13397
  _KEYPOLICY._serialized_start=13399
  _KEYPOLICY._serialized_end=13449
  _IMMUTABLESTORAGEACCOUNT._serialized_start=13452
  _IMMUTABLESTORAGEACCOUNT._serialized_end=13597
  _ACCOUNTIMMUTABILITYPOLICYPROPERTIES._serialized_start=13600
  _ACCOUNTIMMUTABILITYPOLICYPROPERTIES._serialized_end=13743
  _ENCRYPTION._serialized_start=13746
  _ENCRYPTION._serialized_end=14056
  _ENCRYPTIONSERVICES._serialized_start=14059
  _ENCRYPTIONSERVICES._serialized_end=14361
  _ENCRYPTIONSERVICE._serialized_start=14363
  _ENCRYPTIONSERVICE._serialized_end=14417
  _KEYVAULTPROPERTIES._serialized_start=14419
  _KEYVAULTPROPERTIES._serialized_end=14497
  _ENCRYPTIONIDENTITY._serialized_start=14499
  _ENCRYPTIONIDENTITY._serialized_end=14589
  _CUSTOMDOMAIN._serialized_start=14591
  _CUSTOMDOMAIN._serialized_end=14648
  _AZUREFILESIDENTITYBASEDAUTHENTICATION._serialized_start=14651
  _AZUREFILESIDENTITYBASEDAUTHENTICATION._serialized_end=14860
  _ACTIVEDIRECTORYPROPERTIES._serialized_start=14863
  _ACTIVEDIRECTORYPROPERTIES._serialized_end=15078
  _IDENTITY._serialized_start=15081
  _IDENTITY._serialized_end=15277
  _IDENTITY_USERASSIGNEDIDENTITIESENTRY._serialized_start=15216
  _IDENTITY_USERASSIGNEDIDENTITIESENTRY._serialized_end=15277
  _EXTENDEDLOCATION._serialized_start=15279
  _EXTENDEDLOCATION._serialized_end=15325
# @@protoc_insertion_point(module_scope)
