# STUB — infrastructure/terraform/: backend on the existing lab backend + KMS key with an isolated aws-identity-access state-key prefix (T02); exact Terraform + AWS-provider pins (T15); resources for slice A only.
# Naming boundary (T04-d5, Eric): stable keys under access/ are never environment-prefixed. Deployed permission-set name = <resource_name_prefix><permission-set-key>, derived here.
#   - T15/T16 select the exact non-empty lab/POC prefix. The target-estate prefix is NOT decided by T04 — T19 decides target naming during brownfield discovery/import/migration planning.
#   - POC-created permission sets also carry a managed-by/project marker when the selected provider pin supports the tagging operation (T21 verifies).
#   - Prefix and tags are defense-in-depth coexistence markers, not reconciliation-ownership authority.
#   - Account assignments are not assumed taggable: their protected scope = governed assignment tuple + association with POC-managed permission sets + isolated state.
#   - Plan guard (T15): reject any create/import/update/delete outside the explicitly derived POC-managed resource and assignment set; pre-existing lab resources are never imported, modified, or destroyed by the first slice.
