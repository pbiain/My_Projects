
VAULTGUARD × SAFECORE
GDPR Compliance Documentation
Data Flows · Legal Basis · Data Subject Rights · Third-Party Processors  ·  March 2026


| Document scope This document identifies all personal data processed by the VaultGuard Maintenance Intelligence Platform, documents the legal basis for each processing activity, assesses data subject rights, and maps third-party processor relationships. Regulation: GDPR (EU) 2016/679  ·  Controller: VaultGuard Inc.  ·  Processor: AI Consultant (IronHack capstone)  ·  Date: March 2026 |
| --- |


| 1 | Controller and processor identification |
| --- | --- |


| Data controller | VaultGuard Inc. — determines the purposes and means of processing maintenance invoice data across its 76,000-unit smart safe fleet |
| --- | --- |
| Data processor | AI Consultant (IronHack capstone project) — processes data on behalf of VaultGuard to build and validate the AI models |
| Third-party processor | Microsoft Corporation — Power BI, Teams, Outlook used for dashboard and notifications. Covered under existing VaultGuard enterprise Microsoft 365 DPA. EU-US Data Privacy Framework adequacy applies. |
| Data used in project | Synthetic/mock dataset based on real invoice structure. No real personal data used for model training or POC demonstration in this capstone project. |



| 2 | Personal data inventory by component |
| --- | --- |


| Key finding The highest-risk personal data processing in the platform occurs in the billing validation AI and the contractor accountability workflow. Both components process data from which natural persons (named individuals in invoice comments, and individual technicians identifiable by cross-referencing invoice fields) can be identified. The predictive failure scoring and fleet dashboard — in their fleet data sections — process no personal data. |
| --- |


| Component 1 — Predictive failure scoring |
| --- |


| Data field | Personal? | Reason | Legal basis | Risk |
| --- | --- | --- | --- | --- |
| Safe unit serial number | NO | Identifies a machine, not a person | N/A | NONE |
| Safe manufacture year | NO | Machine attribute | N/A | NONE |
| Maintenance cost history | NO | Relates to equipment, not individuals | N/A | NONE |
| Risk score output (0–100) | NO | Score on a machine. No natural person is the subject. | N/A | NONE |


| Component 2 — Billing validation AI  — HIGHEST RISK |
| --- |


| Data field | Personal? | Reason | Legal basis | Risk |
| --- | --- | --- | --- | --- |
| Invoice total amount | CONDITIONAL | Personal data if technician is a sole trader (their commercial activity). Not personal if contractor is a legal entity. | Legitimate interests Art. 6(1)(f) | LOW |
| Component / parts data | NO | Machine and product codes only. No individual identified. | N/A | NONE |
| Labour charge | CONDITIONAL | Personal if linked to named individual technician. Not personal if contractor is a company. | Legitimate interests Art. 6(1)(f) | LOW |
| Date + location + serial | YES — indirect | Combination can single out a specific technician at a specific location on a specific date (identifiability by combination — GDPR Art. 4(1)). | Legitimate interests Art. 6(1)(f) | MEDIUM |
| Invoice comment (free text) | YES — HIGH RISK | Named individuals appear routinely in technician notes (store managers, client staff, customer names). AI reads this field to make billing classification. | Legitimate interests Art. 6(1)(f) | HIGH |
| OOS Tier 1/2 category | NO | Structured category codes. No individual identified directly. | N/A | NONE |
| Output: YES/NO billing flag | CONDITIONAL | Personal if used internally to evaluate biller performance. Not personal if attached to business client account only. | Legitimate interests Art. 6(1)(f) | MEDIUM |


| Component 3 — Contractor accountability workflow |
| --- |


| Data field | Personal? | Reason | Legal basis | Risk |
| --- | --- | --- | --- | --- |
| Invoice content (input) | YES — indirect | Technician identifiable by cross-referencing date, location, serial, service description even without a name field. | Legitimate interests Art. 6(1)(f) | MEDIUM |
| Cost deviation flag | YES | Output relates to an identifiable individual's professional conduct. Operations manager can use it to identify the technician. | Legitimate interests Art. 6(1)(f) | HIGH |
| Power BI / Teams notification | YES | Personal data transmitted to Microsoft as third-party processor. Covered under existing enterprise Microsoft 365 DPA. | Legitimate interests Art. 6(1)(f) | MEDIUM |
| Dashboard flag (internal) | YES | Contractor identifiable to manager reviewing the flag. Role-based access control required (data minimisation Art. 5(1)(c)). | Legitimate interests Art. 6(1)(f) | MEDIUM |


| Known limitation — data subject notification GDPR requires data subjects to be informed that their data is being processed (Articles 13–14). The individual technicians are contracted to SafeCore Systems (the hardware manufacturer), not directly to VaultGuard. VaultGuard has no direct contact relationship with them. This makes data subject notification practically difficult. Proposed mitigation: VaultGuard requests that SafeCore Systems includes a GDPR disclosure in technician onboarding documentation stating that invoice data may be processed by VaultGuard clients for quality assurance purposes. Alternatively, VaultGuard publishes a publicly accessible privacy notice covering contractor invoice processing. |
| --- |


| Component 4 — Fleet intelligence dashboard |
| --- |


| Data field | Personal? | Reason | Legal basis | Risk |
| --- | --- | --- | --- | --- |
| Fleet risk scores | NO | Safe unit scores. Machine data only. | N/A | NONE |
| OOS category trends | NO | Aggregate operational statistics. No individuals identified. | N/A | NONE |
| Billing accuracy KPIs | NO | Aggregate percentages. No individual decisions displayed. | N/A | NONE |
| Contractor flagging section | YES — conditional | Individual contractor identifiable to manager from flagged invoice data. Personal data under GDPR. | Legitimate interests Art. 6(1)(f) | MEDIUM |


| Data minimisation obligation — role-based access control The contractor flagging section must be restricted to authorised operations management personnel only (GDPR Article 5(1)(c) — data minimisation). Fleet data, OOS trends, and billing KPIs may be accessible to all authorised dashboard users. Unrestricted access to contractor flagging data would violate data minimisation principles. |
| --- |



| 3 | Data subject rights |
| --- | --- |


| Who are the data subjects? Data subjects in this system are: (1) Individual technicians identifiable through invoice cross-referencing — primary data subjects, highest risk. (2) Named individuals appearing in invoice free-text comments (store managers, client staff, customer names) — incidental data subjects, lower risk. (3) The human biller at VaultGuard, if the billing AI output is used to evaluate their performance — conditional data subject. |
| --- |


| Right (GDPR Article) | Applies? | How the system supports it |
| --- | --- | --- |
| Right to be informed (Art. 13–14) | YES | Difficult to implement directly — no direct relationship with technicians. Proposed mitigation: SafeCore Systems includes GDPR disclosure in contractor onboarding, or VaultGuard publishes a public privacy notice. |
| Right of access (Art. 15) | YES | VaultGuard must be able to provide a technician with all invoice data held about them upon request. Requires a data subject access request (DSAR) process to be established. |
| Right to erasure (Art. 17) | YES — limited | Applies to personal data in invoice comments and flags. May conflict with VaultGuard’s legitimate interest in retaining billing audit records. Legal obligation to retain financial records (typically 7 years) may override erasure requests. |
| Right to object (Art. 21) | YES | Technicians may object to processing under legitimate interests. VaultGuard must demonstrate compelling legitimate grounds that override the individual’s interests. Quality control and fraud prevention are strong grounds. |
| Right to data portability (Art. 20) | NO | Portability applies only when processing is based on consent or contract performance. Processing here is based on legitimate interests. Right to portability does not apply. |


| 4 | Third-party data processors |
| --- | --- |


| Processor | Service used | Transfer mechanism | DPA status |
| --- | --- | --- | --- |
| Microsoft Corporation | Power BI, Teams, Outlook (Microsoft 365) | EU–US Data Privacy Framework adequacy decision | Covered under existing VaultGuard enterprise Microsoft 365 DPA. No additional agreement required. |
| SafeCore Systems (hardware manufacturer) | Invoice data provision — source of raw data | Covered under existing service contract | Data Processing Addendum to be added to master service contract at next renewal. Recommended action. |
| Anthropic (Claude AI) | LLM used for billing classification and analysis | Anonymised/synthetic data used in capstone. Production deployment requires DPA. | Data Processing Agreement required before processing real personal data in production. NDA with AI-specific clauses (no training on confidential data) required. |



GDPR Data Flows & Assessment  ·  VaultGuard × SafeCore Capstone  ·  IronHack AI Bootcamp  ·  March 2026