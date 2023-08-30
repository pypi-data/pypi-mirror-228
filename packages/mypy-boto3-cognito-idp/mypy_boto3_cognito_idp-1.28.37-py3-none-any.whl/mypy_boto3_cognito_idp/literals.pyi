"""
Type annotations for cognito-idp service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/literals/)

Usage::

    ```python
    from mypy_boto3_cognito_idp.literals import AccountTakeoverEventActionTypeType

    data: AccountTakeoverEventActionTypeType = "BLOCK"
    ```
"""
import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AccountTakeoverEventActionTypeType",
    "AdminListGroupsForUserPaginatorName",
    "AdminListUserAuthEventsPaginatorName",
    "AdvancedSecurityModeTypeType",
    "AliasAttributeTypeType",
    "AttributeDataTypeType",
    "AuthFlowTypeType",
    "ChallengeNameType",
    "ChallengeNameTypeType",
    "ChallengeResponseType",
    "CompromisedCredentialsEventActionTypeType",
    "CustomEmailSenderLambdaVersionTypeType",
    "CustomSMSSenderLambdaVersionTypeType",
    "DefaultEmailOptionTypeType",
    "DeletionProtectionTypeType",
    "DeliveryMediumTypeType",
    "DeviceRememberedStatusTypeType",
    "DomainStatusTypeType",
    "EmailSendingAccountTypeType",
    "EventFilterTypeType",
    "EventResponseTypeType",
    "EventSourceNameType",
    "EventTypeType",
    "ExplicitAuthFlowsTypeType",
    "FeedbackValueTypeType",
    "IdentityProviderTypeTypeType",
    "ListGroupsPaginatorName",
    "ListIdentityProvidersPaginatorName",
    "ListResourceServersPaginatorName",
    "ListUserPoolClientsPaginatorName",
    "ListUserPoolsPaginatorName",
    "ListUsersInGroupPaginatorName",
    "ListUsersPaginatorName",
    "LogLevelType",
    "MessageActionTypeType",
    "OAuthFlowTypeType",
    "PreventUserExistenceErrorTypesType",
    "RecoveryOptionNameTypeType",
    "RiskDecisionTypeType",
    "RiskLevelTypeType",
    "StatusTypeType",
    "TimeUnitsTypeType",
    "UserImportJobStatusTypeType",
    "UserPoolMfaTypeType",
    "UserStatusTypeType",
    "UsernameAttributeTypeType",
    "VerifiedAttributeTypeType",
    "VerifySoftwareTokenResponseTypeType",
    "CognitoIdentityProviderServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)

AccountTakeoverEventActionTypeType = Literal[
    "BLOCK", "MFA_IF_CONFIGURED", "MFA_REQUIRED", "NO_ACTION"
]
AdminListGroupsForUserPaginatorName = Literal["admin_list_groups_for_user"]
AdminListUserAuthEventsPaginatorName = Literal["admin_list_user_auth_events"]
AdvancedSecurityModeTypeType = Literal["AUDIT", "ENFORCED", "OFF"]
AliasAttributeTypeType = Literal["email", "phone_number", "preferred_username"]
AttributeDataTypeType = Literal["Boolean", "DateTime", "Number", "String"]
AuthFlowTypeType = Literal[
    "ADMIN_NO_SRP_AUTH",
    "ADMIN_USER_PASSWORD_AUTH",
    "CUSTOM_AUTH",
    "REFRESH_TOKEN",
    "REFRESH_TOKEN_AUTH",
    "USER_PASSWORD_AUTH",
    "USER_SRP_AUTH",
]
ChallengeNameType = Literal["Mfa", "Password"]
ChallengeNameTypeType = Literal[
    "ADMIN_NO_SRP_AUTH",
    "CUSTOM_CHALLENGE",
    "DEVICE_PASSWORD_VERIFIER",
    "DEVICE_SRP_AUTH",
    "MFA_SETUP",
    "NEW_PASSWORD_REQUIRED",
    "PASSWORD_VERIFIER",
    "SELECT_MFA_TYPE",
    "SMS_MFA",
    "SOFTWARE_TOKEN_MFA",
]
ChallengeResponseType = Literal["Failure", "Success"]
CompromisedCredentialsEventActionTypeType = Literal["BLOCK", "NO_ACTION"]
CustomEmailSenderLambdaVersionTypeType = Literal["V1_0"]
CustomSMSSenderLambdaVersionTypeType = Literal["V1_0"]
DefaultEmailOptionTypeType = Literal["CONFIRM_WITH_CODE", "CONFIRM_WITH_LINK"]
DeletionProtectionTypeType = Literal["ACTIVE", "INACTIVE"]
DeliveryMediumTypeType = Literal["EMAIL", "SMS"]
DeviceRememberedStatusTypeType = Literal["not_remembered", "remembered"]
DomainStatusTypeType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
EmailSendingAccountTypeType = Literal["COGNITO_DEFAULT", "DEVELOPER"]
EventFilterTypeType = Literal["PASSWORD_CHANGE", "SIGN_IN", "SIGN_UP"]
EventResponseTypeType = Literal["Fail", "InProgress", "Pass"]
EventSourceNameType = Literal["userNotification"]
EventTypeType = Literal["ForgotPassword", "PasswordChange", "ResendCode", "SignIn", "SignUp"]
ExplicitAuthFlowsTypeType = Literal[
    "ADMIN_NO_SRP_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH",
    "ALLOW_CUSTOM_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "CUSTOM_AUTH_FLOW_ONLY",
    "USER_PASSWORD_AUTH",
]
FeedbackValueTypeType = Literal["Invalid", "Valid"]
IdentityProviderTypeTypeType = Literal[
    "Facebook", "Google", "LoginWithAmazon", "OIDC", "SAML", "SignInWithApple"
]
ListGroupsPaginatorName = Literal["list_groups"]
ListIdentityProvidersPaginatorName = Literal["list_identity_providers"]
ListResourceServersPaginatorName = Literal["list_resource_servers"]
ListUserPoolClientsPaginatorName = Literal["list_user_pool_clients"]
ListUserPoolsPaginatorName = Literal["list_user_pools"]
ListUsersInGroupPaginatorName = Literal["list_users_in_group"]
ListUsersPaginatorName = Literal["list_users"]
LogLevelType = Literal["ERROR"]
MessageActionTypeType = Literal["RESEND", "SUPPRESS"]
OAuthFlowTypeType = Literal["client_credentials", "code", "implicit"]
PreventUserExistenceErrorTypesType = Literal["ENABLED", "LEGACY"]
RecoveryOptionNameTypeType = Literal["admin_only", "verified_email", "verified_phone_number"]
RiskDecisionTypeType = Literal["AccountTakeover", "Block", "NoRisk"]
RiskLevelTypeType = Literal["High", "Low", "Medium"]
StatusTypeType = Literal["Disabled", "Enabled"]
TimeUnitsTypeType = Literal["days", "hours", "minutes", "seconds"]
UserImportJobStatusTypeType = Literal[
    "Created", "Expired", "Failed", "InProgress", "Pending", "Stopped", "Stopping", "Succeeded"
]
UserPoolMfaTypeType = Literal["OFF", "ON", "OPTIONAL"]
UserStatusTypeType = Literal[
    "ARCHIVED",
    "COMPROMISED",
    "CONFIRMED",
    "FORCE_CHANGE_PASSWORD",
    "RESET_REQUIRED",
    "UNCONFIRMED",
    "UNKNOWN",
]
UsernameAttributeTypeType = Literal["email", "phone_number"]
VerifiedAttributeTypeType = Literal["email", "phone_number"]
VerifySoftwareTokenResponseTypeType = Literal["ERROR", "SUCCESS"]
CognitoIdentityProviderServiceName = Literal["cognito-idp"]
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
    "admin_list_groups_for_user",
    "admin_list_user_auth_events",
    "list_groups",
    "list_identity_providers",
    "list_resource_servers",
    "list_user_pool_clients",
    "list_user_pools",
    "list_users",
    "list_users_in_group",
]
RegionName = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
