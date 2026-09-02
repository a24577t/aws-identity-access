# Alias-only, deterministic outputs (T15 #10 d12): the derived deployed
# names for the governed permission-set keys. No live identifier and no
# generated identifier is ever output.

output "deployed_permission_set_names" {
  description = "Deployed Name per governed permission-set key (T15 #10 d8 derivation)."
  value = {
    for key, ps in local.permission_sets :
    key => "${local.resource_name_prefix}${ps.key}"
  }
}
