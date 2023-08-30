"""
Type annotations for fsx service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/literals/)

Usage::

    ```python
    from mypy_boto3_fsx.literals import AdministrativeActionTypeType

    data: AdministrativeActionTypeType = "FILE_SYSTEM_ALIAS_ASSOCIATION"
    ```
"""
import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AdministrativeActionTypeType",
    "AliasLifecycleType",
    "AutoImportPolicyTypeType",
    "AutocommitPeriodTypeType",
    "BackupLifecycleType",
    "BackupTypeType",
    "DataCompressionTypeType",
    "DataRepositoryLifecycleType",
    "DataRepositoryTaskFilterNameType",
    "DataRepositoryTaskLifecycleType",
    "DataRepositoryTaskTypeType",
    "DeleteFileSystemOpenZFSOptionType",
    "DeleteOpenZFSVolumeOptionType",
    "DescribeBackupsPaginatorName",
    "DescribeFileSystemsPaginatorName",
    "DescribeStorageVirtualMachinesPaginatorName",
    "DescribeVolumesPaginatorName",
    "DiskIopsConfigurationModeType",
    "DriveCacheTypeType",
    "EventTypeType",
    "FileCacheLifecycleType",
    "FileCacheLustreDeploymentTypeType",
    "FileCacheTypeType",
    "FileSystemLifecycleType",
    "FileSystemMaintenanceOperationType",
    "FileSystemTypeType",
    "FilterNameType",
    "FlexCacheEndpointTypeType",
    "InputOntapVolumeTypeType",
    "ListTagsForResourcePaginatorName",
    "LustreAccessAuditLogLevelType",
    "LustreDeploymentTypeType",
    "NfsVersionType",
    "OntapDeploymentTypeType",
    "OntapVolumeTypeType",
    "OpenZFSCopyStrategyType",
    "OpenZFSDataCompressionTypeType",
    "OpenZFSDeploymentTypeType",
    "OpenZFSQuotaTypeType",
    "PrivilegedDeleteType",
    "ReportFormatType",
    "ReportScopeType",
    "ResourceTypeType",
    "RestoreOpenZFSVolumeOptionType",
    "RetentionPeriodTypeType",
    "SecurityStyleType",
    "SnaplockTypeType",
    "SnapshotFilterNameType",
    "SnapshotLifecycleType",
    "StatusType",
    "StorageTypeType",
    "StorageVirtualMachineFilterNameType",
    "StorageVirtualMachineLifecycleType",
    "StorageVirtualMachineRootVolumeSecurityStyleType",
    "StorageVirtualMachineSubtypeType",
    "TieringPolicyNameType",
    "UnitType",
    "VolumeFilterNameType",
    "VolumeLifecycleType",
    "VolumeTypeType",
    "WindowsAccessAuditLogLevelType",
    "WindowsDeploymentTypeType",
    "FSxServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)


AdministrativeActionTypeType = Literal[
    "FILE_SYSTEM_ALIAS_ASSOCIATION",
    "FILE_SYSTEM_ALIAS_DISASSOCIATION",
    "FILE_SYSTEM_UPDATE",
    "IOPS_OPTIMIZATION",
    "RELEASE_NFS_V3_LOCKS",
    "SNAPSHOT_UPDATE",
    "STORAGE_OPTIMIZATION",
    "STORAGE_TYPE_OPTIMIZATION",
    "THROUGHPUT_OPTIMIZATION",
    "VOLUME_RESTORE",
    "VOLUME_UPDATE",
]
AliasLifecycleType = Literal["AVAILABLE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING"]
AutoImportPolicyTypeType = Literal["NEW", "NEW_CHANGED", "NEW_CHANGED_DELETED", "NONE"]
AutocommitPeriodTypeType = Literal["DAYS", "HOURS", "MINUTES", "MONTHS", "NONE", "YEARS"]
BackupLifecycleType = Literal[
    "AVAILABLE", "COPYING", "CREATING", "DELETED", "FAILED", "PENDING", "TRANSFERRING"
]
BackupTypeType = Literal["AUTOMATIC", "AWS_BACKUP", "USER_INITIATED"]
DataCompressionTypeType = Literal["LZ4", "NONE"]
DataRepositoryLifecycleType = Literal[
    "AVAILABLE", "CREATING", "DELETING", "FAILED", "MISCONFIGURED", "UPDATING"
]
DataRepositoryTaskFilterNameType = Literal[
    "data-repository-association-id", "file-cache-id", "file-system-id", "task-lifecycle"
]
DataRepositoryTaskLifecycleType = Literal[
    "CANCELED", "CANCELING", "EXECUTING", "FAILED", "PENDING", "SUCCEEDED"
]
DataRepositoryTaskTypeType = Literal[
    "AUTO_RELEASE_DATA",
    "EXPORT_TO_REPOSITORY",
    "IMPORT_METADATA_FROM_REPOSITORY",
    "RELEASE_DATA_FROM_FILESYSTEM",
]
DeleteFileSystemOpenZFSOptionType = Literal["DELETE_CHILD_VOLUMES_AND_SNAPSHOTS"]
DeleteOpenZFSVolumeOptionType = Literal["DELETE_CHILD_VOLUMES_AND_SNAPSHOTS"]
DescribeBackupsPaginatorName = Literal["describe_backups"]
DescribeFileSystemsPaginatorName = Literal["describe_file_systems"]
DescribeStorageVirtualMachinesPaginatorName = Literal["describe_storage_virtual_machines"]
DescribeVolumesPaginatorName = Literal["describe_volumes"]
DiskIopsConfigurationModeType = Literal["AUTOMATIC", "USER_PROVISIONED"]
DriveCacheTypeType = Literal["NONE", "READ"]
EventTypeType = Literal["CHANGED", "DELETED", "NEW"]
FileCacheLifecycleType = Literal["AVAILABLE", "CREATING", "DELETING", "FAILED", "UPDATING"]
FileCacheLustreDeploymentTypeType = Literal["CACHE_1"]
FileCacheTypeType = Literal["LUSTRE"]
FileSystemLifecycleType = Literal[
    "AVAILABLE",
    "CREATING",
    "DELETING",
    "FAILED",
    "MISCONFIGURED",
    "MISCONFIGURED_UNAVAILABLE",
    "UPDATING",
]
FileSystemMaintenanceOperationType = Literal["BACKING_UP", "PATCHING"]
FileSystemTypeType = Literal["LUSTRE", "ONTAP", "OPENZFS", "WINDOWS"]
FilterNameType = Literal[
    "backup-type",
    "data-repository-type",
    "file-cache-id",
    "file-cache-type",
    "file-system-id",
    "file-system-type",
    "volume-id",
]
FlexCacheEndpointTypeType = Literal["CACHE", "NONE", "ORIGIN"]
InputOntapVolumeTypeType = Literal["DP", "RW"]
ListTagsForResourcePaginatorName = Literal["list_tags_for_resource"]
LustreAccessAuditLogLevelType = Literal["DISABLED", "ERROR_ONLY", "WARN_ERROR", "WARN_ONLY"]
LustreDeploymentTypeType = Literal["PERSISTENT_1", "PERSISTENT_2", "SCRATCH_1", "SCRATCH_2"]
NfsVersionType = Literal["NFS3"]
OntapDeploymentTypeType = Literal["MULTI_AZ_1", "SINGLE_AZ_1"]
OntapVolumeTypeType = Literal["DP", "LS", "RW"]
OpenZFSCopyStrategyType = Literal["CLONE", "FULL_COPY"]
OpenZFSDataCompressionTypeType = Literal["LZ4", "NONE", "ZSTD"]
OpenZFSDeploymentTypeType = Literal["MULTI_AZ_1", "SINGLE_AZ_1", "SINGLE_AZ_2"]
OpenZFSQuotaTypeType = Literal["GROUP", "USER"]
PrivilegedDeleteType = Literal["DISABLED", "ENABLED", "PERMANENTLY_DISABLED"]
ReportFormatType = Literal["REPORT_CSV_20191124"]
ReportScopeType = Literal["FAILED_FILES_ONLY"]
ResourceTypeType = Literal["FILE_SYSTEM", "VOLUME"]
RestoreOpenZFSVolumeOptionType = Literal["DELETE_CLONED_VOLUMES", "DELETE_INTERMEDIATE_SNAPSHOTS"]
RetentionPeriodTypeType = Literal[
    "DAYS", "HOURS", "INFINITE", "MINUTES", "MONTHS", "SECONDS", "UNSPECIFIED", "YEARS"
]
SecurityStyleType = Literal["MIXED", "NTFS", "UNIX"]
SnaplockTypeType = Literal["COMPLIANCE", "ENTERPRISE"]
SnapshotFilterNameType = Literal["file-system-id", "volume-id"]
SnapshotLifecycleType = Literal["AVAILABLE", "CREATING", "DELETING", "PENDING"]
StatusType = Literal["COMPLETED", "FAILED", "IN_PROGRESS", "PENDING", "UPDATED_OPTIMIZING"]
StorageTypeType = Literal["HDD", "SSD"]
StorageVirtualMachineFilterNameType = Literal["file-system-id"]
StorageVirtualMachineLifecycleType = Literal[
    "CREATED", "CREATING", "DELETING", "FAILED", "MISCONFIGURED", "PENDING"
]
StorageVirtualMachineRootVolumeSecurityStyleType = Literal["MIXED", "NTFS", "UNIX"]
StorageVirtualMachineSubtypeType = Literal[
    "DEFAULT", "DP_DESTINATION", "SYNC_DESTINATION", "SYNC_SOURCE"
]
TieringPolicyNameType = Literal["ALL", "AUTO", "NONE", "SNAPSHOT_ONLY"]
UnitType = Literal["DAYS"]
VolumeFilterNameType = Literal["file-system-id", "storage-virtual-machine-id"]
VolumeLifecycleType = Literal[
    "AVAILABLE", "CREATED", "CREATING", "DELETING", "FAILED", "MISCONFIGURED", "PENDING"
]
VolumeTypeType = Literal["ONTAP", "OPENZFS"]
WindowsAccessAuditLogLevelType = Literal[
    "DISABLED", "FAILURE_ONLY", "SUCCESS_AND_FAILURE", "SUCCESS_ONLY"
]
WindowsDeploymentTypeType = Literal["MULTI_AZ_1", "SINGLE_AZ_1", "SINGLE_AZ_2"]
FSxServiceName = Literal["fsx"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "arc-zonal-shift",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "backup-gateway",
    "backupstorage",
    "batch",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcases",
    "connectparticipant",
    "controltower",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "entityresolution",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "gamesparks",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector2",
    "internetmonitor",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot-roborunner",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "m2",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "managedblockchain-query",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "medical-imaging",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "oam",
    "omics",
    "opensearch",
    "opensearchserverless",
    "opsworks",
    "opsworkscm",
    "organizations",
    "osis",
    "outposts",
    "panorama",
    "payment-cryptography",
    "payment-cryptography-data",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "privatenetworks",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "resiliencehub",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "simspaceweaver",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "support-app",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "describe_backups",
    "describe_file_systems",
    "describe_storage_virtual_machines",
    "describe_volumes",
    "list_tags_for_resource",
]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ca-central-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
