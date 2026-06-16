---
name: it-provisioning
description: BTS-Synthetic IT provisioning catalogue for Hire-to-Onboard. Use whenever generating a hardware and accounts checklist for a new hire. Covers laptop specs, peripherals, core accounts, role-specific tools, access groups, and lead times. Trigger on any request to provision, set up, or prepare IT access for a new starter.
---

# IT Provisioning Catalogue

Use this to generate a complete, role-appropriate provisioning checklist for a new hire.

## 1. Hardware

Select hardware based on role family and location.

### Laptop

| Role family | Standard spec | Notes |
| --- | --- | --- |
| Engineering / Data / ML | MacBook Pro 14" M4 Pro, 36GB RAM, 1TB SSD | Order 10 business days ahead |
| Analytics / BI | MacBook Pro 14" M4, 24GB RAM, 512GB SSD | Order 7 business days ahead |
| Corporate (Finance, Legal, HR, Ops) | MacBook Air 15" M4, 16GB RAM, 512GB SSD | Order 5 business days ahead |
| Executive (Director+) | MacBook Pro 16" M4 Max, 48GB RAM, 1TB SSD | Requires IT Director approval |
| Windows required (specific tools) | Dell XPS 15, i9, 32GB RAM, 1TB SSD | Flag to IT — non-standard, 10 days |

**All laptops ship with:** Full-disk encryption enabled, MDM enrolment (Jamf), corporate VPN client pre-installed, approved browser (Chrome + Firefox), password manager (1Password).

### Peripherals

Standard kit for all hires:

- USB-C hub (7-in-1)
- Logitech MX Keys keyboard
- Logitech MX Master 3 mouse

Additional for role / location:

| Item | When to include |
| --- | --- |
| 27" 4K monitor | Office-based hires or hybrid with assigned desk |
| Second monitor (same spec) | Engineering, Data, and Analytics roles |
| Webcam (Logitech Brio) | Remote-first hires without monitor |
| Headset (Jabra Evolve2 55) | Customer-facing roles, Support, Sales |
| Mobile phone (iPhone 15) | Roles with on-call duties or field work; requires manager approval |
| YubiKey (x2) | Engineering, IT, Security, and Finance roles |

### Lead times summary

| Item | Lead time |
| --- | --- |
| Standard laptop (Mac) | 5–7 business days |
| High-spec Mac (M4 Pro / Max) | 10 business days |
| Windows laptop | 10 business days |
| Peripherals (standard) | 3 business days |
| Mobile phone | 5 business days |
| YubiKey | 3 business days |

Flag any item where the lead time exceeds the time until start date.

## 2. Core accounts (all hires)

Every new hire gets these accounts on or before day 1:

| System | Account type | Notes |
| --- | --- | --- |
| Google Workspace | Corporate email + Drive + Calendar | Username format: firstname.lastname@company.com |
| Slack | Full member | Add to #general, #announcements, and team channel |
| HRIS (Workday) | Employee self-service | Payroll, leave, and personal details |
| 1Password | Individual vault | Invite via email; team vault access per role |
| Confluence | Full member | Default space: New Starter Hub |
| Jira | Full member (or viewer for non-technical) | Role determines project access |
| Zoom | Licensed account | SSO via Google |
| Greenhouse (ATS) | Recruiter/interviewer roles only | |

## 3. Role-specific tools

### Engineering
- GitHub (org member, team-appropriate repos)
- AWS / GCP / Azure console access (dev environment only; prod requires separate approval)
- Docker Hub
- DataDog (developer access)
- PagerDuty (on-call roles only)
- Retool (internal tooling team only)

### Data / Analytics
- Snowflake (role-appropriate warehouse and database access)
- dbt Cloud (developer seat)
- Looker (developer or viewer — confirm with manager)
- Airflow / Prefect (data engineering only)
- DataDog (read-only unless data platform team)

### Product
- Figma (full seat)
- Amplitude / Mixpanel (analyst seat)
- ProductBoard
- LaunchDarkly (feature flag access)

### Sales / Account Management
- Salesforce CRM (standard user)
- Outreach / Salesloft
- Gong (call recording — licensed seat)
- LinkedIn Sales Navigator

### Finance / Legal / HR
- Xero / NetSuite (finance only — role-specific permissions)
- DocuSign (corporate account)
- Ironclad (legal only)
- Greenhouse (HR / recruiters only)

### Marketing
- HubSpot
- Canva (team account)
- Semrush / Ahrefs
- Hootsuite / Sprout Social

## 4. Access groups and permissions

| Group | Who gets it | What it grants |
| --- | --- | --- |
| all-staff | Everyone | Read access to shared drives, Confluence New Starter Hub |
| engineering | Engineering hires | GitHub org, dev AWS/GCP, DataDog |
| data-platform | Data Engineering | All data-platform repos, prod-read Snowflake |
| analytics | Analytics hires | Snowflake read, Looker, dbt viewer |
| finance-ops | Finance | NetSuite, Xero, restricted Slack channels |
| people-ops | HR | Workday full access, Greenhouse, restricted payroll data |
| it-admin | IT only | Jamf console, Okta admin, 1Password admin |

**Items requiring manager approval before provisioning:**
- Any prod environment access (even read-only)
- Mobile phone
- Executive-spec hardware
- PagerDuty on-call rotation
- Admin access to any system

## 5. Output format

```
IT PROVISIONING CHECKLIST — [Hire Name] | [Role] | [Start Date]

HARDWARE
  Laptop: [Spec] — order by [date] (lead time: X days)
  Peripherals: [List items]
  [Flag any item at risk of not arriving by start date]

CORE ACCOUNTS (all required by day 1)
  [ ] Google Workspace — firstname.lastname@company.com
  [ ] Slack — add to #general, #announcements, #[team-channel]
  [ ] Workday
  [ ] 1Password
  [ ] Confluence
  [ ] Jira ([Full / Viewer])
  [ ] Zoom

ROLE-SPECIFIC TOOLS
  [ ] [Tool 1] — [access level]
  [ ] [Tool 2] — [access level]
  [List all applicable tools]

ACCESS GROUPS
  [ ] all-staff
  [ ] [role-specific group]
  [List all applicable groups]

ITEMS REQUIRING MANAGER APPROVAL
  - [List any items needing sign-off]

RISKS / FLAGS
  - [Any lead-time issues or blockers]
```
