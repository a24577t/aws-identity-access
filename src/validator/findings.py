"""The redaction-safe finding-record contract (T14 #19 d9, C12/C14).

Every finding carries code, severity, stage, file_path, field_path, ordered
rule_ids, a sanitized value (the fixed "[omitted]" sentinel standing in when
absent or redacted by omission), and a sanitized message. Severity is derived
from the catalogue - it is serialized but never an ordering key and never
authorable per finding (no silent downgrade, T14 #19 d1). Canonical ordering
is total and deterministic over the seven distinguishing fields in order:
file_path, code, field_path, stage, rule_ids, value, message; identical
findings collapse deterministically before serialization; no occurrence index
exists. A global finding (no owning file) uses file_path "-", field_path "-".
The serialization format (JSON below) is the S6 implementation choice whose
output preserves this contract.
"""

import json

from . import catalogue

OMITTED = "[omitted]"
GLOBAL = "-"


class ContractViolation(Exception):
    """A use of the finding contract the catalogue does not permit."""


def _sanitize(text):
    """Render escaped and unambiguous: no raw control characters ever."""
    if text is None:
        return None
    out = []
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\x{:02x}".format(ord(ch)))
        else:
            out.append(ch)
    return "".join(out)


class Finding:
    __slots__ = ("code", "stage", "file_path", "field_path", "rule_ids",
                 "value", "message")

    def __init__(self, code, stage, file_path, field_path, rule_ids, value,
                 message):
        entry = catalogue.CATALOGUE.get(code)
        if entry is None:
            raise ContractViolation(f"code {code!r} is not in the catalogue")
        if stage not in entry.stages:
            raise ContractViolation(
                f"{code} does not enumerate stage {stage!r} "
                f"(allowed: {', '.join(entry.stages)})"
            )
        self.code = code
        self.stage = stage
        self.file_path = GLOBAL if file_path is None else str(file_path)
        self.field_path = GLOBAL if field_path is None else str(field_path)
        self.rule_ids = tuple(rule_ids)
        self.value = _sanitize(value)
        self.message = _sanitize(message)

    @property
    def severity(self):
        return catalogue.CATALOGUE[self.code].severity

    def _key(self):
        # C14: the seven serialized distinguishing fields, in order; the
        # sentinel stands in for an absent or omitted value. severity is
        # derivable from code and never distinguishes findings.
        return (
            self.file_path,
            self.code,
            self.field_path,
            self.stage,
            self.rule_ids,
            self.value if self.value is not None else OMITTED,
            self.message or "",
        )

    def __eq__(self, other):
        return isinstance(other, Finding) and self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return f"Finding({self.code} {self.file_path} {self.field_path} {self.stage})"

    def to_record(self):
        return {
            "code": self.code,
            "severity": self.severity,
            "stage": self.stage,
            "file_path": self.file_path,
            "field_path": self.field_path,
            "rule_ids": list(self.rule_ids),
            "value": self.value if self.value is not None else OMITTED,
            "message": self.message or "",
        }


def canonical(items):
    """Collapse identical findings, then order by the C14 total key."""
    unique = {}
    for finding in items:
        unique.setdefault(finding._key(), finding)
    return [unique[key] for key in sorted(unique)]


def serialize(items):
    """Byte-deterministic serialization of the canonical finding list.

    UTF-8, LF, two-space indent, ASCII-escaped: identical inputs produce
    identical bytes in every environment (specification 8.2).
    """
    doc = {"findings": [finding.to_record() for finding in canonical(items)]}
    return (json.dumps(doc, indent=2, ensure_ascii=True) + "\n").encode("ascii")
