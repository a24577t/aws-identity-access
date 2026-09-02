# Live lab identifiers reach this root only as input values at the
# separately authorized local apply (T15 #10 d15) - never as committed
# bytes (T15 #10 d12). Both inputs are marked sensitive so no rendered
# diagnostic or output carries them.

variable "state_bucket" {
  description = "Name of the existing CMK-encrypted state bucket that holds the isolated aws-identity-access prefixes (T15 #10 d16). Supplied at the one-time local apply; never committed."
  type        = string
  sensitive   = true
  nullable    = false

  validation {
    condition     = length(var.state_bucket) > 0 && !strcontains(var.state_bucket, "/")
    error_message = "fail closed: state_bucket must be a bare S3 bucket name, not a path or URI."
  }
}

variable "state_kms_key_arn" {
  description = "ARN of the existing customer-managed key that encrypts the state bucket. Scopes both pipeline roles' KMS data-plane access to exactly this key (T15 #10 d6); key and key-policy administration stay denied (d7). Supplied at the one-time local apply; never committed."
  type        = string
  sensitive   = true
  nullable    = false

  validation {
    condition     = startswith(var.state_kms_key_arn, "arn:")
    error_message = "fail closed: state_kms_key_arn must be a key ARN."
  }
}
