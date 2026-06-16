---
name: recruiter-checklist
description: BTS-Synthetic recruiter checklist for Hire-to-Onboard. Use whenever confirming a new hire's offer terms and pre-employment check status before day 1. Covers offer confirmation, reference checks, background screening, and contract status. Trigger on any request to review, confirm, or flag pre-employment readiness.
---

# Recruiter Checklist

Use this to verify a new hire is fully cleared and offer terms are locked before day 1.

## 1. Offer terms confirmation

Every item below must be confirmed in writing before the hire is marked ready.

| Item | Source of truth | Status options |
| --- | --- | --- |
| Role title | Signed offer letter | Confirmed / Mismatch / Pending |
| Level / grade | HRIS system | Confirmed / Mismatch / Pending |
| Start date | Offer letter + calendar invite | Confirmed / Pending |
| Base salary | Offer letter | Confirmed / Pending |
| Bonus / incentive structure | Offer letter or incentive plan doc | Confirmed / N/A / Pending |
| Equity (if applicable) | Equity award letter | Confirmed / N/A / Pending |
| Location / work arrangement | Offer letter | Confirmed / Mismatch / Pending |
| Reporting line | Offer letter + org chart | Confirmed / Pending |

**Flag any mismatch** between the offer letter and HRIS as a blocker. Do not mark offer confirmed until the HRIS reflects the agreed terms.

## 2. Reference checks

**Our standard:** Three references required — two professional (former managers preferred), one character reference acceptable as third.

| Reference | Type | Outcome options |
| --- | --- | --- |
| Reference 1 | Professional | Complete / Pending / Waived |
| Reference 2 | Professional | Complete / Pending / Waived |
| Reference 3 | Professional / Character | Complete / Pending / Waived |

**Waiver conditions:** References may be waived only when:
- Internal transfer (existing employee)
- Rehire within 2 years with clean prior exit
- Senior leadership sign-off with documented reason

Flag pending references as a risk if they are not resolved 5 or more business days before start date.

## 3. Background check

Managed via the third-party screening provider. Standard checks by hire type:

### Standard (all hires)
- Identity verification
- Right-to-work / work authorisation
- Criminal record check (jurisdiction-appropriate)
- Education verification (highest qualification claimed)

### Enhanced (roles with financial, data, or systems access)
- Credit check (financial roles only — requires candidate consent)
- Employment history verification (last 5 years)
- Professional licence verification (if role requires one)

### Executive (Director level and above)
- All standard + enhanced checks
- Media / adverse press search
- Global sanctions screening

**Status options per check:** Clear / Pending / Refer (requires HR review) / Failed (escalate to HR Director)

Any "Refer" or "Failed" status must be escalated before an offer is considered confirmed. HR Director must sign off on any conditional start.

## 4. Contract and documentation

| Document | Required? | Status options |
| --- | --- | --- |
| Signed offer letter | Always | Signed / Unsigned / Sent |
| Employment contract | Always | Signed / Unsigned / Sent |
| Confidentiality / NDA | Always | Signed / Unsigned / Sent |
| Non-compete (if applicable) | Role-dependent | Signed / N/A / Pending |
| IP assignment agreement | Engineering / Product / Data roles | Signed / N/A / Pending |
| Work authorisation docs | Non-citizens | Verified / N/A / Pending |
| Superannuation / pension nomination | All permanent hires | Complete / Pending |

All documents must be in the HRIS document vault before day 1. Unsigned documents are a day-1 blocker.

## 5. Day-1 readiness blockers

Mark the hire as **not ready** if any of the following are unresolved:

- Offer terms mismatch between letter and HRIS
- Any background check in Refer or Failed status
- Employment contract unsigned
- Right-to-work verification incomplete
- Start date not confirmed with hiring manager

## How to structure your output

```
OFFER CONFIRMATION SUMMARY — [Hire Name]

Role: [Title] | Level: [Grade] | Start: [Date] | Location: [City / Remote]
Salary: [$X] | Bonus: [X% target or N/A] | Equity: [X units or N/A]

REFERENCE CHECKS
  Ref 1: [Name, Company] — [Complete / Pending / Waived]
  Ref 2: [Name, Company] — [Complete / Pending / Waived]
  Ref 3: [Name, Company] — [Complete / Pending / Waived]

BACKGROUND CHECK
  Identity: [Clear / Pending]
  Right-to-work: [Clear / Pending]
  Criminal: [Clear / Pending / Refer]
  Education: [Clear / Pending]
  [Enhanced checks if applicable]

DOCUMENTATION
  Offer letter: [Signed / Pending]
  Contract: [Signed / Pending]
  NDA: [Signed / Pending]
  [Other docs as applicable]

BLOCKERS (if any):
  - [Description of each unresolved item]

OVERALL STATUS: READY / NOT READY
```
