# Repository byte-identity amendment

Append-only repository policy record: how this repository defines byte identity for
hash-bound governance, and the root `.gitattributes` that enforces it. Produced as a
correction after the aborted narrow ⟦G-Accept⟧ transition (transition-start commit
`f9739daaaba3b9e5b27d9997f87b083b6d06ca56`; abort cleanup
`a3a2825e1e0eb3a92a8ca6fefa7764e6ec39ea5f`): that transaction's pre-PR verification
found the package's descriptive hashes identified a platform-specific CRLF
working-tree rendering of the accepted engineering specification and of the Status
Artifact instead of their canonical committed Git blobs. This record carries no
authority header (T23 #23 decision 4 scopes the normative-header rule to
`docs/architecture/` and `docs/guides/`; no accepted rule requires specification
frontmatter): its authority derives from its approving ⟦G-Accept⟧ record and this
repository placement.

## 1. Decision

1. **Hash authority is the canonical committed Git blob.** Wherever this repository
   binds an artifact by hash — gate authorizations, publication and review packages,
   catalog source verification (specification §7.1), evidence digests, manifest
   entries — the identity is the SHA-256 of the exact bytes of the Git blob in the
   object database (`git cat-file blob <oid>`), never a platform-specific
   working-tree rendering. A working-tree hash may be reported as a diagnostic only
   and is never authorization identity.
2. **Canonical text is LF.** The root `.gitattributes` accepted with this record
   declares `* text=auto eol=lf`: Git-managed text is stored LF and checks out LF on
   every platform.
3. **JSON is exact-byte.** `*.json -text` disables all conversion for JSON: staged
   bytes equal source bytes and checkout bytes equal blob bytes. The raw SRI source
   files (`governance/catalogs/sources/…`) and every generated JSON artifact keep
   their exact bytes end to end, so specification §7.1/§7.4 hash verification
   operates on identical bytes in the blob and in a conforming checkout.
4. **No bulk renormalization.** Existing committed blobs are not rewritten. The
   pre-adoption survey found every indexed blob already LF (or attribute-neutral),
   so this `.gitattributes` changes no existing object and no renormalizing commit
   exists. `git add --renormalize` and any unrelated file rewrite are outside this
   record and would require their own governance.
5. **New or changed files are verified from their staged or committed blobs** at the
   destination path (`git rev-parse :<path>` / `git show <commit>:<path>`), then
   reverified from the committed blob after commit — never accepted from an
   authoring working tree alone.

## 2. Canonical pre-state identities (recorded at adoption)

| Artifact | Git blob OID | Bytes | SHA-256 |
|---|---|---|---|
| accepted engineering specification (`docs/specifications/slice-a-engineering-specification.md`) | `97faf7cb658e1238c695dcfe6ab00e2b749a10a0` | 17,938 | `5679d79656052410e118b18a224b590e303315906c132fc8bdc92f72297557ad` |
| pre-amendment Status Artifact (`.ai/repository/state/STATUS.md`) | `d7a57c9064fa45ddefa8509e8aaad080f44d8dd0` | 2,304 | `8db3a4c62e5f43b35a2c9a3c35e55d3b5e2ddf376787e6153643dee92c3e8104` |

The superseded working-tree-rendering figures (specification 18,195 bytes, SHA-256
`f23bcad4c81f97864a63040a582f85efef7837ae794b58f455509789579e8fc4`; Status Artifact
2,349 bytes, SHA-256
`8b661f7ad308d8fb3ee277797a6ca69083ec67b9c5ea0b7d2803a7f80d973d53`) are recorded
here once as diagnostics of the corrected defect; they are not identity and must not
be cited as such.

## 3. Root `.gitattributes` (exact accepted content)

```
* text=auto eol=lf
*.json -text
```

## 4. Application

This policy governs the catalog verification of specification §7 (the item-6
producer hashes the committed source blobs; with `*.json -text` those equal the
on-disk bytes of a conforming checkout), every future hash-bound review package and
gate authorization, and all evidence digests. On any divergence between a
working-tree rendering and the committed blob, the blob prevails and the divergence
is surfaced, never silently resolved.
