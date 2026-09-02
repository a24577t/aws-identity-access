# Spec 8.1 pins (T15 #10 d13; changes only via platform-change PR):
# Terraform 1.15.7 exact; hashicorp/aws = 6.53.0 with the committed
# dependency lock carrying the T21 #20 F2 h1 hash.
terraform {
  required_version = "1.15.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 6.53.0"
    }
  }

  # T15 #10 d16: state object aws-identity-access/lab/identity-center/terraform.tfstate
  # with its native lockfile (use_lockfile=true) in the existing state
  # bucket, us-east-1. Partial configuration by design: the merged R4 #29
  # lab-plan/lab-apply workflows supply every value at init, because the
  # name of the state bucket is a live lab identifier that never enters
  # committed content (T15 #10 d12).
  backend "s3" {}
}
