"""INV-PUBLIC-LEAK - the single canonical public-serialization leak rule
(T14 #19 d4b).

Detects live, account-local, or generated identifier shapes in public
content. The only ARN-shaped exemption is the T21 #20 d2 partition-qualified
AWS-managed-policy vocabulary (arn:aws:iam::aws:policy/...); it never exempts
account-local, generated, live, import, principal, assignment, instance,
store, or role identifiers. Redaction is by omission: the offending value is
never carried into the serialized finding.

The shapes below are deterministic and conservative. Identifier families
whose grammar could collide with ordinary kebab-case prose (o-/r-/ou-
Organizations IDs) additionally require at least one digit in the token -
a documented deterministic narrowing that keeps the real alias-only tree
clean while every synthetic format-valid specimen (which carries digits)
still fires.
"""

import re

EXEMPT_ARN = re.compile(r"^arn:aws:iam::aws:policy/[A-Za-z0-9+=,.@_/-]+$")

_PATTERNS = (
    ("arn", re.compile(r"arn:[a-z0-9-]*:[a-z0-9-]*:[a-z0-9-]*:[a-z0-9-]*:[^\s\"',]+")),
    ("account-id", re.compile(r"(?<![0-9A-Za-z.-])[0-9]{12}(?![0-9A-Za-z.-])")),
    ("organization-id", re.compile(r"\bo-[a-z0-9]{10,32}\b")),
    ("root-id", re.compile(r"\br-[a-z0-9]{4,32}\b")),
    ("ou-id", re.compile(r"\bou-[a-z0-9]{4,32}-[a-z0-9]{8,32}\b")),
    ("identity-store-id", re.compile(r"\bd-[0-9a-f]{10}\b")),
    ("reserved-sso-role", re.compile(r"AWSReservedSSO_[A-Za-z0-9_+=,.@-]+")),
    ("uuid", re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")),
    ("e-mail", re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")),
)

_NEEDS_DIGIT = {"organization-id", "root-id", "ou-id"}


def scan_text(text):
    """Yield (line_number, kind, token) for every leak-shaped token.

    One finding per underlying token: a token wholly inside an
    already-matched span (an account ID inside an ARN) is not a second
    finding - dual emission for one root cause is rejected (T14 #19 d4).
    """
    for line_no, line in enumerate(text.split("\n"), start=1):
        spans = []
        for kind, pattern in _PATTERNS:
            for match in pattern.finditer(line):
                token = match.group(0)
                if kind == "arn" and EXEMPT_ARN.match(token):
                    continue
                if kind in _NEEDS_DIGIT and not any(c.isdigit() for c in token):
                    continue
                if any(match.start() >= s and match.end() <= e for s, e in spans):
                    continue
                spans.append((match.start(), match.end()))
                yield line_no, kind, token


def check_tree(ctx):
    """Scan every decodable file of the target tree (committed public
    content, T15 #10 d12); locators are canonical line numbers (C14)."""
    for rel in ctx.files():
        try:
            text = ctx.read_bytes(rel).decode("utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, kind, _token in scan_text(text):
            ctx.emit(
                "INV-PUBLIC-LEAK",
                file_path=rel,
                field_path=f"L{line_no}",
                value=None,
                message=f"{kind}-shaped identifier in public content; "
                        "redacted by omission",
            )
