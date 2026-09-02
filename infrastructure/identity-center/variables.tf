variable "plan_context_file" {
  description = "Path to the retrieved T09 #12 plan-context evidence document (the snapshot envelope carrying the alias-to-account binding). The lab-plan workflow retrieves it from the non-public evidence store and hands the path to terraform plan; it is the sole alias-resolution source (T15 #10 d5 - exactly one non-public binding record). Without it the root fails closed; the saved plan the lab environment applies already carries every resolved value, so apply never re-reads it (T20 #22 d4)."
  type        = string
  nullable    = false
}
