# This file is maintained automatically by "terraform init".
# Manual edits may be lost in future updates.
#
# Authored from the recorded pin (spec 8.1; T21 #20 F2) under R5 #30's
# zero-execution rule - no terraform init ran to produce it. The h1 hash
# is exactly the one the accepted specification requires the committed
# entry to carry; platform coverage beyond it is verified empirically at
# the first designated lab-CI run (the open provider-execution
# condition, spec 8.3).

provider "registry.terraform.io/hashicorp/aws" {
  version     = "6.53.0"
  constraints = "6.53.0"
  hashes = [
    "h1:eD0xCJQCp+iQQKpU/SpMk/pGRrkF16UUJAEMCXvWCWo=",
  ]
}
