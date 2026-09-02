"""ADO-PHASE - the mechanism-defined greenfield/adoption boundary
(R3 #28 allocation reconciliation; T19 #14 d2).

Slice A contains no `import` block and no `moved`/`removed` state surgery
of any kind; adoption exists only inside the distinct import-rehearsal
phase - entered only after POC acceptance and separate authorization, and
additionally gated on the open import-redaction verification (T20 #22 d7).
Until that phase is authorized, any adoption-shaped Terraform configuration
in the governed tree is a validation error at its canonical layer.

Detection is textual and deterministic over `*.tf` files: a top-level
`import`/`moved`/`removed` block opener. ADO-MANIFEST stays dormant with
its recorded activation condition and is never checked here.
"""

import re

_BLOCK_RE = re.compile(r"^\s*(import|moved|removed)\s*\{", re.MULTILINE)


def check_ado(ctx):
    for rel in ctx.files():
        if not rel.endswith(".tf"):
            continue
        try:
            text = ctx.read_bytes(rel).decode("utf-8")
        except UnicodeDecodeError:
            continue
        for match in _BLOCK_RE.finditer(text):
            line_no = text.count("\n", 0, match.start()) + 1
            ctx.emit("ADO-PHASE", file_path=rel, field_path=f"L{line_no}",
                     value=match.group(1),
                     message=f"{match.group(1)} block outside an authorized "
                             "rehearsal phase - adoption-shaped change "
                             "rejected (T19 #14 d2; slice A performs no "
                             "state surgery)")
