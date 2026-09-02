{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CallerIdentity",
      "Effect": "Allow",
      "Action": ["sts:GetCallerIdentity"],
      "Resource": "*"
    },
    {
      "Sid": "ReadDiscovery",
      "Effect": "Allow",
      "Action": [
        "sso:Describe*",
        "sso:Get*",
        "sso:List*",
        "identitystore:Describe*",
        "identitystore:Get*",
        "identitystore:List*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CreateOnlyTaggedPermissionSets",
      "Effect": "Allow",
      "Action": ["sso:CreatePermissionSet"],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestTag/managed-by": "aws-identity-access-terraform"
        }
      }
    },
    {
      "Sid": "MutateOnlyManagedResources",
      "Effect": "Allow",
      "Action": [
        "sso:UpdatePermissionSet",
        "sso:DeletePermissionSet",
        "sso:AttachManagedPolicyToPermissionSet",
        "sso:DetachManagedPolicyFromPermissionSet",
        "sso:PutInlinePolicyToPermissionSet",
        "sso:DeleteInlinePolicyFromPermissionSet",
        "sso:CreateAccountAssignment",
        "sso:DeleteAccountAssignment",
        "sso:ProvisionPermissionSet",
        "sso:TagResource",
        "sso:UntagResource"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/managed-by": "aws-identity-access-terraform"
        }
      }
    },
    {
      "Sid": "StateAndLockfileWithinRootPrefix",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "${state_objects_arn}"
    },
    {
      "Sid": "StateBucketListWithinPrefix",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "${state_bucket_arn}",
      "Condition": { "StringLike": { "s3:prefix": "${state_prefix}" } }
    },
    {
      "Sid": "EncryptedEvidenceGetPut",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "${evidence_objects_arn}"
    },
    {
      "Sid": "KmsDataPlaneViaS3",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:Encrypt",
        "kms:GenerateDataKey",
        "kms:DescribeKey"
      ],
      "Resource": "${kms_key_arn}",
      "Condition": {
        "StringEquals": { "kms:ViaService": "s3.us-east-1.amazonaws.com" }
      }
    }
  ]
}
