# VaultGuard Billing Classification Criteria

This document defines the rules the AI uses to decide whether a SafeCore maintenance invoice should be billed to the client or absorbed by VaultGuard. These rules come directly from the White Glove Service Contract.

---

## The core question

For every invoice, the AI answers one question:

> Was this problem caused by the client, or is it something VaultGuard is responsible for under the service contract?

If the client caused it → **YES** (bill the client, GL 440134)
If it's a warranty/contract issue → **NO** (VaultGuard absorbs, GL 440133)

---

## Bill the client — YES

These situations are the client's responsibility:

| Situation | Examples from technician notes |
|---|---|
| **Physical damage** | "cracked screen", "broken display", "bent components" |
| **Liquid spillage** | "liquid damage", "wet inside unit", "drink spilled" |
| **Abuse or vandalism** | "unit was kicked", "deliberate damage", "vandalism" |
| **Foreign objects** | "coins jammed in acceptor", "debris in slot", "paper stuck" |
| **Infestation** | "cockroach infestation", "rodent damage", "insect nest" |
| **Burglary damage** | "break-in attempt", "pry marks on door", "safe attacked" |
| **Access refused** | "customer refused entry", "no access", "cancelled after dispatch" |
| **Negligence** | "customer dropped unit", "improper handling" |

---

## VaultGuard absorbs — NO

These situations are covered under the service contract:

| Situation | Examples from technician notes |
|---|---|
| **Normal wear and tear** | "validator spring worn", "component reached end of life" |
| **Communications failure** | "modem replaced", "SIM card issue", "no signal" |
| **Network / connectivity** | "phone line fault", "broadband issue", "network error" |
| **Software / firmware** | "firmware updated", "software reset", "configuration error" |
| **Programming error** | "user set wrong denomination", "till settings incorrect" |
| **No fault found** | "safe working fine on arrival", "could not replicate issue" |
| **Printer issues** | "paper jam", "receipt paper loaded incorrectly" |
| **Equipment reset** | "power cycle resolved issue", "safe reset remotely" |

---

## How the AI uses the labour charge

The dollar amount of the labour charge tells the AI which zone the visit was in:

| Amount | Zone | What it means |
|---|---|---|
| $186 or $189 | Zone 1–3 | Standard OOS rate — visit was Out of Scope |
| $621 or $630 | Zone 4 | Remote/high-cost OOS rate — visit was Out of Scope |

Both amounts confirm the technician classified the visit as Out of Scope. This supports but does not override the decision — the technician note and OOS categories are the primary signal.

---

## Confidence levels

The AI assigns a confidence level to every decision:

| Level | Meaning | Action |
|---|---|---|
| **HIGH** | Clear signal in the note or OOS categories | Auto-classify, no review needed |
| **MEDIUM** | Signal present but some ambiguity | Classify, human may want to spot-check |
| **LOW** | Comment is vague, missing, or contradicts the OOS category | Flag for human review |

---

## When the AI flags for human review

An invoice is flagged (`flag_for_review: true`) when:

- Confidence is LOW
- The technician note is empty or says nothing useful
- The OOS Tier 1 and Tier 2 categories are both missing
- The technician note and the OOS categories contradict each other (e.g. note says "no fault found" but OOS category says "physical damage")

Flagged invoices appear in the urgent alert email and are highlighted in the Working sheet. A human biller makes the final call before the Oracle upload.

---

## What the AI does NOT do

- It does not make the final billing decision — a human reviews and confirms before any upload
- It does not store or retain customer data — PII is pseudonymised before the invoice reaches the AI
- It does not override the human biller — its output is a recommendation, not an instruction
- It does not classify 2024-format invoices reliably — those lack structured OOS categories and should be reviewed manually

---

## Output fields

Every classification returns:

| Field | Values | Meaning |
|---|---|---|
| `decision` | YES / NO / UNKNOWN | Billing recommendation |
| `confidence` | HIGH / MEDIUM / LOW | How certain the AI is |
| `reason` | Plain text | One sentence explaining the decision |
| `key_signal` | Plain text | The word or phrase that drove the decision |
| `flag_for_review` | true / false | Whether a human must review before upload |
| `gl_code` | 440134 / 440133 | Oracle GL code (YES=440134, NO=440133) |
