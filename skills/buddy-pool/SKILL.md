---
name: buddy-pool
description: BTS-Synthetic onboarding buddy pool for Hire-to-Onboard. Use whenever matching a new hire to an onboarding buddy. Contains the current list of eligible buddies, their team and seniority, and availability status. Trigger on any request to recommend, assign, or match an onboarding buddy.
---

# Onboarding Buddy Pool

Use this to select the best onboarding buddy for a new hire. Prioritise team or adjacent-team matches, then seniority alignment, then recency of last buddy assignment.

## Matching criteria (in priority order)

1. **Team alignment** — same team is best; adjacent team is acceptable; cross-functional only as last resort
2. **Seniority alignment** — buddy should be 1–2 levels above the new hire; peers can work for senior hires
3. **Recency** — prefer buddies who have not onboarded anyone in the last 60 days
4. **Availability** — buddy must not be on leave or in a heavy delivery period in the new hire's first two weeks

## Buddy pool

### Engineering

| Name | Role | Level | Team | Last buddy assignment | Available |
| --- | --- | --- | --- | --- | --- |
| Marcus Webb | Senior Software Engineer | L5 | Platform | 90 days ago | Yes |
| Priya Nair | Software Engineer | L4 | Backend | 45 days ago | Yes |
| James Okafor | Staff Engineer | L6 | Platform | Never | Yes |
| Sophie Laurent | Software Engineer | L4 | Frontend | 120 days ago | Yes |
| Daniel Kim | Senior Software Engineer | L5 | Mobile | 20 days ago | Limited — in sprint crunch until week 3 |
| Fatima Al-Hassan | Engineering Manager | M1 | Data Platform | 60 days ago | Yes — good for senior engineering hires |

### Data & Analytics

| Name | Role | Level | Team | Last buddy assignment | Available |
| --- | --- | --- | --- | --- | --- |
| Anika Sharma | Senior Data Analyst | D4 | Growth Analytics | 80 days ago | Yes |
| Tom Bergstrom | Analytics Engineer | D3 | Data Platform | 30 days ago | Yes |
| Yuki Tanaka | Staff Data Scientist | D6 | ML Platform | Never | Yes — prefers senior DS hires |
| Chloe Martin | Data Engineer | D3 | Data Platform | 55 days ago | On leave weeks 1–2; available from week 3 |

### Product

| Name | Role | Level | Team | Last buddy assignment | Available |
| --- | --- | --- | --- | --- | --- |
| Ravi Patel | Senior Product Manager | P5 | Growth | 70 days ago | Yes |
| Ingrid Holmberg | Product Manager | P4 | Core Platform | 10 days ago | Limited — product launch week 2 |
| Leon Osei | Principal PM | P6 | Enterprise | Never | Yes — senior PM hires only |

### Design

| Name | Role | Level | Team | Last buddy assignment | Available |
| --- | --- | --- | --- | --- | --- |
| Maya Chen | Senior Product Designer | De4 | Growth | 90 days ago | Yes |
| Oliver Ruiz | Product Designer | De3 | Core Platform | 40 days ago | Yes |

### Sales & Account Management

| Name | Role | Level | Team | Last buddy assignment | Available |
| --- | --- | --- | --- | --- | --- |
| Natalie Brooks | Senior Account Executive | S5 | Enterprise | 60 days ago | Yes |
| Sam Oduya | Account Executive | S4 | Mid-Market | 15 days ago | Yes |
| Zeynep Yilmaz | Sales Development Manager | SM1 | SDR Team | 50 days ago | Yes — SDR hires only |

### Corporate (Finance, HR, Legal, Ops)

| Name | Role | Level | Team | Last buddy assignment | Available |
| --- | --- | --- | --- | --- | --- |
| Grace Adeyemi | Senior HR Business Partner | C5 | People Ops | 100 days ago | Yes |
| Ben Whitfield | Finance Business Partner | C4 | FP&A | 35 days ago | Yes |
| Amara Diallo | Legal Counsel | C5 | Legal | Never | Yes — legal hires preferred |

## Buddy responsibilities (first week)

Brief the recommended buddy to cover:

1. **Day 1 welcome** — meet the new hire at the office entrance or kick off a video call; walk them through the day
2. **Team introductions** — make informal intros to the immediate team and key cross-functional contacts
3. **Unwritten rules** — how the team actually works (stand-ups, async norms, Slack etiquette, escalation paths)
4. **Tools walkthrough** — where to find things (Confluence, Jira, Slack channels, shared drives)
5. **Lunch / coffee in week 1** — at least one informal social touchpoint
6. **Check-in at end of week 1** — 30-minute debrief: what's clear, what's confusing, what do they need

## Scheduling conflicts to flag

- Buddy on leave in the first 2 weeks → recommend backup as primary instead
- Buddy in a sprint crunch or major product deadline → note the constraint and confirm with their manager
- Buddy has onboarded someone in the last 30 days → flag, but don't disqualify if best match

## Output format

```
BUDDY RECOMMENDATION — [Hire Name] | [Role] | [Team] | [Start Date]

PRIMARY BUDDY
  Name: [Name]
  Role: [Role], [Team]
  Why: [1–2 sentences on why they're the best fit]
  Last assignment: [X days ago / Never]
  Availability: [Confirmed / Limited — note constraint]

BACKUP BUDDY
  Name: [Name]
  Role: [Role], [Team]
  Why: [1–2 sentences]
  Availability: [Confirmed / Limited — note constraint]

FIRST-WEEK PRIORITIES FOR BUDDY
  1. [Specific thing relevant to this hire's role/team]
  2. [Specific thing]
  3. [Specific thing]

FLAGS / SCHEDULING NOTES
  - [Any conflicts or concerns to resolve before day 1]
```
