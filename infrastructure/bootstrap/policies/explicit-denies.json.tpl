{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyIamMutationSurface",
      "Effect": "Deny",
      "Action": ["iam:*"],
      "Resource": "*"
    },
    {
      "Sid": "DenyOrganizationsMutation",
      "Effect": "Deny",
      "Action": [
        "organizations:Accept*",
        "organizations:Attach*",
        "organizations:Cancel*",
        "organizations:Close*",
        "organizations:Create*",
        "organizations:Decline*",
        "organizations:Delete*",
        "organizations:Deregister*",
        "organizations:Detach*",
        "organizations:Disable*",
        "organizations:Enable*",
        "organizations:Invite*",
        "organizations:Leave*",
        "organizations:Move*",
        "organizations:Put*",
        "organizations:Register*",
        "organizations:Remove*",
        "organizations:Tag*",
        "organizations:Untag*",
        "organizations:Update*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyS3ControlPlane",
      "Effect": "Deny",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:PutBucketPolicy",
        "s3:DeleteBucketPolicy",
        "s3:PutBucketAcl",
        "s3:PutBucketVersioning",
        "s3:PutBucketPublicAccessBlock",
        "s3:PutEncryptionConfiguration",
        "s3:PutLifecycleConfiguration",
        "s3:PutReplicationConfiguration",
        "s3:PutBucketOwnershipControls",
        "s3:PutBucketObjectLockConfiguration"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyS3OutsideAuthorizedPrefixes",
      "Effect": "Deny",
      "Action": ["s3:*"],
      "NotResource": [
        "${state_bucket_arn}",
        "${state_objects_arn}",
        "${evidence_objects_arn}"
      ]
    },
    {
      "Sid": "DenyKmsControlPlane",
      "Effect": "Deny",
      "Action": [
        "kms:Create*",
        "kms:Delete*",
        "kms:Disable*",
        "kms:Enable*",
        "kms:ImportKeyMaterial",
        "kms:PutKeyPolicy",
        "kms:ReplicateKey",
        "kms:RetireGrant",
        "kms:RevokeGrant",
        "kms:CreateGrant",
        "kms:ScheduleKeyDeletion",
        "kms:CancelKeyDeletion",
        "kms:TagResource",
        "kms:UntagResource",
        "kms:Update*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyIdentityCenterPlatformMutation",
      "Effect": "Deny",
      "Action": [
        "sso:CreateInstance",
        "sso:DeleteInstance",
        "sso:UpdateInstance",
        "sso:CreateInstanceAccessControlAttributeConfiguration",
        "sso:DeleteInstanceAccessControlAttributeConfiguration",
        "sso:UpdateInstanceAccessControlAttributeConfiguration",
        "sso:CreateApplication",
        "sso:DeleteApplication",
        "sso:UpdateApplication",
        "sso:PutApplicationAccessScope",
        "sso:PutApplicationAssignmentConfiguration",
        "sso:PutApplicationAuthenticationMethod",
        "sso:PutApplicationGrant",
        "sso:CreateApplicationAssignment",
        "sso:DeleteApplicationAssignment",
        "sso:CreateTrustedTokenIssuer",
        "sso:DeleteTrustedTokenIssuer",
        "sso:UpdateTrustedTokenIssuer",
        "identitystore:Create*",
        "identitystore:Delete*",
        "identitystore:Update*",
        "sso-directory:*"
      ],
      "Resource": "*"
    }
  ]
}
