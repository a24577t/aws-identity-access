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
      "Sid": "ReadOnlyDiscovery",
      "Effect": "Allow",
      "Action": [
        "organizations:Describe*",
        "organizations:List*",
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
      "Sid": "StateBucketListWithinPrefix",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "${state_bucket_arn}",
      "Condition": { "StringLike": { "s3:prefix": "${state_prefix}" } }
    },
    {
      "Sid": "StateObjectReadOnly",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "${state_object_arn}"
    },
    {
      "Sid": "NativeLockfileOnly",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "${state_lock_arn}"
    },
    {
      "Sid": "EncryptedPlanEvidenceGetPut",
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
