"""Validation-stage DOC-* checks - the T23 #23 header contracts (R2 #27
row 4).

Applicability boundary (T23 #23 d4): docs/architecture/** and docs/guides/**
Markdown files, excluding docs/generated/** (T20's generated-metadata schema
governs there; GEN detection lands with R3 #28). Every other documentation
tree (adr, wayfinding, research, agents), the root README, and CONTEXT.md
carry their own established forms and are outside this boundary.
"""

import re

import yaml

NORMATIVE_REQUIRED = {"status", "authority", "scope", "decision_owner"}
BOUNDARY_PREFIXES = ("docs/architecture/", "docs/guides/")

_ADR_ID_RE = re.compile(r"^ADR-([0-9]{4})$")
_URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://\S+$")


def _frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    try:
        header = yaml.safe_load(text[4:end + 1])
    except Exception:
        return None
    return header if isinstance(header, dict) else None


def _resolvable(entry, ctx):
    """derives_from entries resolve to a repository path, a domain ADR
    identifier, or an immutable pinned platform identifier/URL (T23 d2).
    The resolution domain is the repository: a staged-subdomain run supplies
    the committed path inventory as RunConfig.resolution_paths (R4 #29 CI
    wiring); absent, the target tree is the domain."""
    if not isinstance(entry, str) or not entry:
        return False
    if _URL_RE.match(entry):
        return True
    paths = ctx.config.resolution_paths
    universe = ctx.files() if paths is None else paths
    match = _ADR_ID_RE.match(entry)
    if match:
        prefix = f"docs/adr/{match.group(1)}-"
        return any(rel.startswith(prefix) for rel in universe)
    return entry in universe


def check_docs(ctx):
    for rel in ctx.files():
        if not rel.endswith(".md"):
            continue
        if rel.startswith("docs/generated/"):
            continue
        if not any(rel.startswith(p) for p in BOUNDARY_PREFIXES):
            continue
        try:
            text = ctx.read_bytes(rel).decode("utf-8")
        except UnicodeDecodeError:
            ctx.emit("DOC-SCOPE", file_path=rel,
                     message="file inside the header boundary is not "
                             "readable documentation")
            continue
        header = _frontmatter(text)
        if header is None:
            ctx.emit("DOC-SCOPE", file_path=rel,
                     message="file inside the applicability boundary is "
                             "missing its class header")
            continue
        if "supersedes" in header:
            ctx.emit("DOC-SCOPE", file_path=rel, field_path="/supersedes",
                     message="supersedes is register-exclusive and never "
                             "appears on a document header")
            continue
        authority = header.get("authority")
        if authority == "normative":
            _check_normative(ctx, rel, header)
        elif authority == "informative":
            _check_informative(ctx, rel, header)
        else:
            ctx.emit("DOC-SCOPE", file_path=rel, field_path="/authority",
                     value=str(authority),
                     message="header carries neither class's form "
                             "(authority must be normative or informative)")


def _check_normative(ctx, rel, header):
    allowed = NORMATIVE_REQUIRED | {"decided"}
    unknown = sorted(set(header) - allowed)
    for field in unknown:
        ctx.emit("DOC-NORMATIVE", file_path=rel, field_path=f"/{field}",
                 message="unknown header field is prohibited")
    for field in sorted(NORMATIVE_REQUIRED - set(header)):
        ctx.emit("DOC-NORMATIVE", file_path=rel, field_path=f"/{field}",
                 message="missing required normative-header field")
    status = header.get("status")
    if "status" in header and status not in ("proposed", "accepted"):
        ctx.emit("DOC-NORMATIVE", file_path=rel, field_path="/status",
                 value=str(status),
                 message="status outside the closed set proposed|accepted")
    if status == "proposed" and "decided" in header:
        ctx.emit("DOC-NORMATIVE", file_path=rel, field_path="/decided",
                 message="decided is absent while proposed")
    if status == "accepted" and "decided" not in header:
        ctx.emit("DOC-NORMATIVE", file_path=rel, field_path="/decided",
                 message="decided is required when accepted (added atomically "
                         "in the acceptance-gate merge)")


def _check_informative(ctx, rel, header):
    unknown = sorted(set(header) - {"authority", "derives_from"})
    for field in unknown:
        ctx.emit("DOC-INFORMATIVE", file_path=rel, field_path=f"/{field}",
                 message="unknown header field is prohibited")
    derives = header.get("derives_from")
    if not isinstance(derives, list) or not derives:
        ctx.emit("DOC-INFORMATIVE", file_path=rel, field_path="/derives_from",
                 message="derives_from must be a non-empty list")
        return
    seen = set()
    for index, entry in enumerate(derives):
        pointer = f"/derives_from/{index}"
        key = str(entry)
        if key in seen:
            ctx.emit("DOC-INFORMATIVE", file_path=rel, field_path=pointer,
                     value=key, message="duplicated derives_from entry")
            continue
        seen.add(key)
        if not _resolvable(entry, ctx):
            ctx.emit("DOC-INFORMATIVE", file_path=rel, field_path=pointer,
                     value=key, message="unresolvable derives_from entry")
