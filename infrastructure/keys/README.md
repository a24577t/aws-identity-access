# infrastructure/keys

Public encryption material for the saved-plan pipeline (T15 #10 d9).

`lab-plan-encryption.pub` — the public half of the plan-encryption
keypair the merged `lab-plan` workflow uses to encrypt the applicable
saved plan (RSA-OAEP/SHA-256 key wrapping over an AES-256 session key);
the workflow references it at exactly this path
(`PLAN_ENCRYPTION_PUBLIC_KEY`).

**Not yet committed — deliberately.** Generating the keypair is part of
the separately authorized R6 #31 activation that registers the private
half as the `lab` environment secret (`LAB_PLAN_DECRYPTION_KEY`,
referenced by name only — T15 #10 d9); the public half is committed by
that same separately authorized act. R5 #30 authors no key material of
either kind (no private key material may ever enter the repository, and
a placeholder public key would dishonestly satisfy the preflight).
Until the key lands, the `lab-plan` job's preflight fails closed naming
this path — exactly as authored in R4 #29.
