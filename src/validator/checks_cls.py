"""The CLS-* checks - plan-effect classification findings (R3 #28 row 9).

Validation stage: the changed-path arms. CLS-UNCOVERED-PATH fires for a
changed file matching no row of the T20 #22 d2 table; CLS-COMBINATION for a
prohibited class combination. The changed-path set arrives as explicit run
input (RunConfig.changed_paths at validation; plan_context["changed_paths"]
at plan/apply - the CI wiring of R4 #29 supplies both). Absent input means
no classification is attempted - hermetically nothing fires.

Plan/apply stage: the classifier consumes the synthetic-safe plan section of
the explicit plan-context input:

  plan: {resource_changes: [{address, type, change: {actions, before,
         after, after_unknown, importing}, target_alias?, protected?}],
         configuration: {removed_blocks: [address], import_blocks: [address],
         guard_removed: bool}}
  changed_paths: [repo-relative changed file]
  overlay: null | {kind, phase}   # the matched merged declaration
                                  # (GOV-DECL-MATCH owns the matching)
  revocation_acknowledgements: [{address, account, group, permission_set}]

Rows mirror plan-JSON resource_changes; assignment targets resolve to the
stable inventory alias (target_alias, or before/after target_id through the
snapshot's bindings). Deterministic evaluation order - one root cause, one
canonical code (T14 #19 d4):

  per row: unknown action list -> CLS-UNKNOWN-ACTION; no-op/read rows are
  separated (never mutation); a required-but-unknown/sensitive value ->
  CLS-UNRESOLVED-VALUE; protected marker or deployed Name outside the
  derived prefix -> CLS-PROTECTED; an effect targeting a deferred alias ->
  CLS-EFFECT; unattributable type or surface outside the matched classes ->
  CLS-UNATTRIBUTABLE; an action the matched surface class does not permit ->
  CLS-EFFECT (assignment deletes lacking their exact-entry acknowledgement
  -> CLS-REVOCATION-ACK).

  vector: a removed-block address planning anything but ["forget"] ->
  CLS-REPRESENTATION; a forget row combined with live mutation or lacking
  its one-to-one removed block -> CLS-FORGET-PATTERN; a well-formed
  state-removal pattern -> CLS-REPRESENTATION (spec 8.3: the pinned-provider
  forget representation is unverified - state-removal-only cannot activate;
  the condition is not advanced); import markers inconsistent with the
  aggregate -> CLS-MARKER-MISMATCH; a clean imports-only or
  guard-removal-no-live-change pattern computes its dormant T19 class, which
  no slice-A PR class permits -> CLS-EFFECT.
"""

from . import classifier, tree
from .checks_access import _fixture_accounts


def _changed_paths_validation(ctx):
    return ctx.config.changed_paths


def check_paths_validation(ctx):
    paths = _changed_paths_validation(ctx)
    if paths is None:
        return
    _emit_path_findings(ctx, paths)


def _emit_path_findings(ctx, paths):
    classes, uncovered = classifier.classify_paths(paths)
    for path in uncovered:
        ctx.emit("CLS-UNCOVERED-PATH", file_path=path,
                 message="changed file matches no row of the T20 #22 d2 "
                         "classification table - fail closed")
    reason = classifier.prohibited_combination(classes)
    if reason:
        ctx.emit("CLS-COMBINATION", message=reason)
    return classes


def _plan_section(ctx):
    raw = ctx.config.plan_context
    if isinstance(raw, dict):
        return raw
    # checks_plan already parses file-shaped contexts; reuse its loader.
    from .checks_plan import _context

    return _context(ctx)


def _alias_for(row, plan):
    """Resolve a row's target account alias: the explicit synthetic-safe
    target_alias, else target_id through the snapshot's bindings."""
    if "target_alias" in row:
        return row["target_alias"]
    change = row.get("change") or {}
    target_id = None
    for side in ("after", "before"):
        doc = change.get(side)
        if isinstance(doc, dict) and isinstance(doc.get("target_id"), str):
            target_id = doc["target_id"]
            break
    if target_id is None:
        return None
    body = (((plan.get("snapshot") or {}).get("envelope")) or {}).get("body")
    for entry in (body or {}).get("accounts") or []:
        if isinstance(entry, dict) and entry.get("account_id") == target_id:
            return entry.get("alias")
    return None


def _deployed_name(row):
    change = row.get("change") or {}
    unknown = change.get("after_unknown") or {}
    if unknown.get("name"):
        return None, True
    for side in ("after", "before"):
        doc = change.get(side)
        if isinstance(doc, dict) and isinstance(doc.get("name"), str):
            return doc["name"], False
    return None, False


def check_plan_classification(ctx):
    plan = _plan_section(ctx)
    if not isinstance(plan, dict):
        return
    section = plan.get("plan")
    changed_paths = plan.get("changed_paths")
    matched = None
    if changed_paths is not None:
        matched = _emit_path_findings(ctx, changed_paths)
    if not isinstance(section, dict):
        return
    rows = [r for r in section.get("resource_changes") or []
            if isinstance(r, dict)]
    configuration = section.get("configuration") or {}
    removed = set(configuration.get("removed_blocks") or ())
    imports = set(configuration.get("import_blocks") or ())
    guard_removed = bool(configuration.get("guard_removed"))
    overlay = plan.get("overlay")
    acks = plan.get("revocation_acknowledgements") or []
    accounts = _fixture_accounts(tree.model(ctx))

    live_classes = []
    forget_rows = []
    marked_rows = []
    unmarked_live = 0

    for row in rows:
        address = row.get("address")
        change = row.get("change") or {}
        cls = classifier.action_class(change.get("actions"))
        if cls is None:
            ctx.emit("CLS-UNKNOWN-ACTION", file_path=None,
                     field_path=str(address),
                     message="unknown or unsupported plan-JSON action list "
                             "- fail closed, never guessed")
            continue
        importing = "importing" in change
        if importing:
            marked_rows.append(row)
        if cls in ("no-op", "read"):
            # Read rows belong to the summary's separate read section;
            # no-op rows carry no effect. Neither joins the aggregate.
            continue
        if cls == "forget":
            forget_rows.append(row)
            continue
        unmarked_live += 0 if importing else 1
        live_classes.append(cls)

        if address in removed:
            # A removed-block address planning live mutation is owned by
            # the vector-level CLS-REPRESENTATION rule - one root cause,
            # one canonical code (T14 #19 d4).
            continue

        surface = classifier.RESOURCE_SURFACES.get(row.get("type"))
        # Required values first (T20 d5: classification that cannot be
        # established because required values are sensitive or unknown
        # fails closed).
        if row.get("type") in classifier.NAMED_TYPES:
            name, unknown = _deployed_name(row)
            if unknown or name is None:
                ctx.emit("CLS-UNRESOLVED-VALUE", field_path=str(address),
                         message="the deployed Name required for the "
                                 "protected-resource guard is sensitive or "
                                 "unknown - fail closed")
                continue
            if row.get("protected") or not name.startswith(
                    ctx.config.resource_name_prefix):
                ctx.emit("CLS-PROTECTED", field_path=str(address),
                         message="operation outside the derived POC-managed "
                                 "set or on a protected pre-existing "
                                 "resource (T15 #10 d7; ADR-0009)")
                continue
        elif row.get("protected"):
            ctx.emit("CLS-PROTECTED", field_path=str(address),
                     message="operation on a protected pre-existing "
                             "resource (T15 #10 d7; ADR-0009)")
            continue

        alias = _alias_for(row, plan)
        if accounts and alias is not None:
            entries = accounts.get(alias) or []
            if any(e.get("status") == "requested" for e in entries):
                ctx.emit("CLS-EFFECT", field_path=str(address), value=alias,
                         message="plan effect targeting a deferred alias - "
                                 "deferred is never an executable target "
                                 "(RD-08; T16 #11 d8)")
                continue

        if surface is None:
            ctx.emit("CLS-UNATTRIBUTABLE", field_path=str(address),
                     value=str(row.get("type")),
                     message="plan effect on a resource type attributable "
                             "to no slice-A changed surface - fail closed")
            continue
        if matched is not None and surface not in matched:
            ctx.emit("CLS-UNATTRIBUTABLE", field_path=str(address),
                     value=surface,
                     message="plan effect not attributable to an allowed "
                             "changed surface of a matched class "
                             "(T20 #22 d1/d5 composition)")
            continue

        permitted = classifier.PERMITTED_ACTIONS.get(surface, frozenset())
        if cls not in permitted and not classifier.overlay_permits(
                overlay, surface, cls):
            ctx.emit("CLS-EFFECT", field_path=str(address), value=cls,
                     message=f"{cls} is outside the matched classes' "
                             "permitted plan effects (T20 #22 d5 matrix)")
            continue
        if surface == "access-grant" and cls == "delete":
            if classifier.overlay_permits(overlay, surface, cls):
                continue
            acked = any(
                isinstance(a, dict)
                and a.get("address") == address
                and a.get("account") == alias
                for a in acks
            )
            if not acked:
                ctx.emit("CLS-REVOCATION-ACK", field_path=str(address),
                         value=alias,
                         message="assignment delete effect without the "
                                 "exact-entry access-revocation "
                                 "acknowledgement (T20 #22 d3/d5)")

    # --- Vector-level rules ---
    aggregate = classifier.aggregate_class(live_classes)

    for address in sorted(removed):
        row = next((r for r in rows if r.get("address") == address), None)
        if row is None:
            continue
        cls = classifier.action_class((row.get("change") or {}).get("actions"))
        if cls is not None and cls != "forget":
            ctx.emit("CLS-REPRESENTATION", field_path=str(address),
                     value=cls,
                     message="a removed-block resource planned a "
                             "representation other than [\"forget\"] - the "
                             "pinned toolchain must not emit this; fail "
                             "closed (T21 #20 F8)")

    if forget_rows:
        if live_classes:
            for row in forget_rows:
                ctx.emit("CLS-FORGET-PATTERN",
                         field_path=str(row.get("address")),
                         message="a forget row combined with live-mutation "
                                 "rows - outside the state-removal-only "
                                 "pattern, fail closed")
        else:
            unmatched = [r for r in forget_rows
                         if r.get("address") not in removed]
            if unmatched:
                for row in unmatched:
                    ctx.emit("CLS-FORGET-PATTERN",
                             field_path=str(row.get("address")),
                             message="a forget row lacking its one-to-one "
                                     "removed { destroy = false } block - "
                                     "fail closed")
            else:
                ctx.emit("CLS-REPRESENTATION",
                         message="state-removal-only cannot activate: the "
                                 "pinned-provider forget representation is "
                                 "unverified (specification 8.3) - fail "
                                 "closed without advancing the condition")

    if marked_rows:
        if unmarked_live or live_classes:
            ctx.emit("CLS-MARKER-MISMATCH",
                     message="import markers combined with live-mutation "
                             "rows - marker/aggregate inconsistency, fail "
                             "closed (T20 #22 d5 layer 2)")
        elif not forget_rows:
            # A clean imports-only pattern computes its contract class; the
            # T19 rehearsal family is dormant and no slice-A PR class
            # permits it (T20 d5 matrix).
            ctx.emit("CLS-EFFECT", value="imports-only",
                     message="imports-only is a dormant T19 rehearsal "
                             "class - permitted by no slice-A PR class "
                             "(T20 #22 d1/d5; T19 #14 d2)")

    if guard_removed:
        if aggregate != "empty" or forget_rows:
            ctx.emit("CLS-MARKER-MISMATCH",
                     message="guard configuration removed while the plan "
                             "carries effects - marker/aggregate "
                             "inconsistency, fail closed")
        else:
            ctx.emit("CLS-EFFECT", value="guard-removal-no-live-change",
                     message="guard-removal-no-live-change is a dormant "
                             "T19 rehearsal class - permitted by no "
                             "slice-A PR class (T20 #22 d5)")
