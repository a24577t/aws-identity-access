---
name: wayfinder-repo-owner
description: Repository-owned specialization of /wayfinder for architecture-bearing efforts. Requires /grill-with-docs when authoritative documents govern a proposed convention or decision; preserves Wayfinder charting and one-ticket stop boundaries.
disable-model-invocation: true
---

# wayfinder — repository-owner specialization

**Base skill:** the installed Matt Pocock [`wayfinder`](../wayfinder/SKILL.md). Use its
map, frontier, ticket, and fog-of-war behavior wherever this file does not override it.
Do not duplicate its text here; do not modify it there.

> Repository-owner skills specialize upstream behavior without replacing it. Skills
> prepare decisions and changes; repository authority changes only at Repository Gates.

## Document-grounded decision rule

Invoke [`grill-with-docs`](../grill-with-docs/SKILL.md) whenever charting or resolving
a Wayfinder ticket requires any of the following:

- classifying a convention as inherited from, compatible with, absent from, or contrary
  to an authoritative document;
- interpreting the scope or consequence of an accepted rule or decision;
- choosing among proposals constrained by authoritative documents;
- proposing a deviation, amendment, refinement, or supersession of documented authority.

Use `grilling` and `domain-modeling` for the human decision exchange; use
`grill-with-docs` to test the proposal and its premises against the governing texts.
Document reading or keyword search alone does not satisfy this rule.

Do not invoke `grill-with-docs` merely because documentation exists. Pure provenance
research, tracker administration, and decisions with no governing-document claim retain
their normal Wayfinder route.

## Evidence in the ticket

Record the document-grounded result in the affected ticket, identifying:

- the governing document and stable rule or decision identifier;
- the claim tested;
- whether the result is inherited, compatible, absent, conflicting, or unresolved;
- any question that must return to the authoritative source as an amendment or refinement.

The result informs the ticket resolution but does not itself accept architecture.

## Stop boundaries

- **Publication:** Publishing or materially rewriting the map or its child tickets requires
  explicit repository-owner authorization. Charting may prepare the complete publication
  set, but stops for owner review before creating or changing tracker artifacts.
- **Charting:** create or revise the map, tickets, dependencies, and frontier; do not
  resolve HITL tickets or begin implementation.
- **Working the map:** resolve at most one HITL ticket per session, preserving the base
  skill's research exception.
- **Architecture-bearing map completion:** stop at S4, the Architecture Grill. Nothing
  becomes authoritative until the applicable Repository Gates authorize it.
