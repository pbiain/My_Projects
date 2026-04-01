**VAULTGUARD × SAFECORE**

**Data Protection Impact Assessment**

Billing Validation AI System · Highest-Risk Processing Activity · March 2026

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Why this DPIA was conducted**                                                                                                                                                                                                                                               |
|                                                                                                                                                                                                                                                                               |
| This DPIA was conducted because the Billing Validation AI processes invoice free-text comments that contain names of real individuals --- store managers, VaultGuard staff, and contractors --- without those individuals' knowledge or consent.                                  |
|                                                                                                                                                                                                                                                                               |
| GDPR Article 35 requires a DPIA when processing is likely to result in a high risk to individuals' rights and freedoms. The combination of automated decision-making, sensitive operational data, and identifiable individuals through singling-out satisfies this threshold. |
|                                                                                                                                                                                                                                                                               |
| This assessment covers the highest-risk processing activity in the VaultGuard Maintenance Intelligence Platform. All other components have been assessed as lower risk in the GDPR Data Flows document.                                                                       |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ------- ----------------------------------------------------------------------
  **1**   **Description of processing**

  ------- ----------------------------------------------------------------------

  -------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **System name**            Billing Validation AI --- Component 2 of the VaultGuard Maintenance Intelligence Platform

  **Data controller**        VaultGuard Inc.

  **Purpose**                To classify each maintenance invoice as either billable to the client (customer abuse/OOS) or absorbed by VaultGuard (covered warranty service), replacing an error-prone manual billing process

  **Processing activity**    An LLM reads invoice data including free-text technician comments and outputs a binary YES/NO billing recommendation for human biller review

  **Trigger for DPIA**       Invoice comment field contains names of identifiable natural persons (store managers, VaultGuard staff, contractors) processed without their knowledge

  **Data subjects**          \(1\) Individual contractors identifiable by cross-referencing date, location, serial, and service description. (2) Named individuals in free-text comments (store managers, VaultGuard staff). (3) Human biller whose decisions are compared against AI output.

  **Volume**                 3,848 invoices processed in 2025 (partial year). \~6,000--8,000 per full year projected.

  **Outcome demonstrated**   84.3% match rate with current human biller on 2025 data. 456 discrepancies identified: \$98,843 over-billing risk + \$22,915 revenue leak.
  -------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **2**   **Necessity and proportionality assessment**

  ------- ----------------------------------------------------------------------

+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **The core tension**                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                                            |
| The billing AI can achieve approximately 80% accuracy using only structured fields (OOS Tier 1/2 categories, part codes, labour rate). Processing the free-text comment field improves accuracy to 84.3% --- a 4.3 percentage point gain.                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                            |
| The question under GDPR Article 5(1)(c) data minimisation is whether this 4.3pp accuracy improvement justifies processing personal data from invoice comments. The answer is nuanced: it does not satisfy data minimisation in its current form, but the processing is operationally necessary and cannot be made fully privacy-neutral without destroying system utility. |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**2.1 Legal basis**

Legal basis: Legitimate interests (GDPR Article 6(1)(f)). VaultGuard has a legitimate interest in accurate billing operations, fraud prevention, and client contract compliance. Processing invoice data including technician comments is necessary to achieve that interest.

**Three-part legitimate interests test:**

-   Purpose test --- Is the interest legitimate? Yes. Accurate billing is a core commercial obligation. Identifying over-billing (\$98,843 dispute risk) and under-billing (\$22,915 revenue leak) directly serves VaultGuard's operational and financial integrity.

-   Necessity test --- Is processing the comment field necessary? Partially. The structured OOS fields carry the primary classification signal. The comment field improves accuracy from \~80% to 84.3%. At 80% accuracy, approximately 770 invoices per year are misclassified --- creating real commercial harm. The comment field is therefore necessary to reach a commercially acceptable accuracy threshold, even if not strictly indispensable.

-   Balancing test --- Do the data subjects' interests override VaultGuard's? The individuals named in comments (store managers, staff) are mentioned incidentally in operational records. The processing does not target them --- they are collateral data. The harm from their names being processed is low. However, the balancing test is weakened by the fact that even pseudonymised comments retain identifying power through singling-out (date + location + serial number combination). This is documented as a residual risk below.

**2.2 Data minimisation assessment**

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Key finding --- identifiability survives pseudonymisation**                                                                                                                                                                                                                                                                                                                                                   |
|                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Even after removing names from the comment field, the combination of invoice date, client location, safe serial number, and service description is sufficient to single out a specific technician or staff member. GDPR defines personal data as any information relating to an identified OR identifiable person. Identifiability by combination means the data remains personal data even after name removal. |
|                                                                                                                                                                                                                                                                                                                                                                                                                 |
| The legitimate interests basis therefore does not fully survive the proportionality test. Processing is necessary for the stated purpose but cannot be made fully privacy-neutral. This DPIA documents that fact honestly and implements the strongest available mitigations.                                                                                                                                   |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Data minimisation measures required:**

-   Step 1 --- Pseudonymise before AI ingestion: Replace personal names in comment field with role descriptors ("spoke with \[STORE CONTACT\]", "called \[VAULTGUARD STAFF\]") before the text enters the AI model. This removes the most direct identification vector while preserving the factual content needed for classification.

-   Step 2 --- Two-layer architecture: The AI processing layer receives only OOS categories, part codes, labour rate, pseudonymised comment, and invoice number (as linking key). It never receives client name, client location, or safe serial number. The billing execution layer --- operated by the human biller --- holds the full invoice and uses the invoice number to retrieve it when executing charges.

-   Step 3 --- 2024 data exclusion: The 2024 invoice dataset has no structured OOS categories. The comment field is the only classification signal available. Under data minimisation principles, 2024 data cannot be used for AI training or validation without prior pseudonymisation of the comment field. Until pseudonymisation is applied, 2024 data must be excluded from AI processing.

  ------- ----------------------------------------------------------------------
  **3**   **Risk assessment**

  ------- ----------------------------------------------------------------------

Data subjects are ranked by risk exposure:

**(1) Individual contractors --- highest risk.** Identifiable by cross-referencing date, location, serial, and service description even without a name field. Not party to any contract with VaultGuard. No awareness their professional conduct is being evaluated by an AI system. An adverse flag could affect their assignment to future work dispatches.

**(2) Human biller at VaultGuard --- medium risk.** An existing employment relationship provides legal structure. The risk arises only if AI output is used to evaluate the biller's performance --- which is a prohibited use explicitly documented in the EU AI Act conformity assessment. If that prohibition is breached, the processing becomes High Risk under Annex III and this DPIA must be revised.

**(3) Named individuals in comments --- lower but real risk.** Store managers, VaultGuard staff, and customer names appear incidentally in technician notes. The processing does not target them. Realistic harm is low --- their names are processed in an internal billing system, not published or shared. Risk materialises only if the data is breached or used beyond its stated purpose.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Data subject / risk**                            **Description**                                                                                                                                                **Likelihood**   **Severity**   **Residual**   **Mitigation**
  -------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------- -------------- -------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Contractor --- identified without name field**   Technician identifiable by singling out through date + location + serial + description combination. No name needed.                                            **HIGH**         **MEDIUM**     **MEDIUM**     Pseudonymise comments. Restrict dashboard contractor flagging to authorised operations management only. Document retention limit.

  **Contractor --- unaware of AI evaluation**        No direct relationship with VaultGuard. Cannot exercise GDPR rights (access, objection) without knowing processing occurs.                                     **HIGH**         **MEDIUM**     **LOW**        VaultGuard requests SafeCore Systems includes GDPR disclosure in contractor onboarding, OR publishes publicly accessible privacy notice covering invoice processing.

  **Biller --- performance evaluation via AI**       If AI output is used to measure biller accuracy, it becomes a performance monitoring tool under Annex III --- triggering High Risk EU AI Act classification.   **LOW**          **HIGH**       **LOW**        Operational policy explicitly prohibits using billing AI output to evaluate biller performance. Documented in EU AI Act conformity assessment.

  **Named individuals in comments**                  Store managers, VaultGuard staff named in technician notes processed by AI without their knowledge.                                                                **HIGH**         **LOW**        **LOW**        Pseudonymise names before AI ingestion. Factual content (what happened) preserved; identifying names removed.

  **2024 data --- no structured OOS fields**         Comment field is the only signal in 2024 data. Processing it without pseudonymisation is disproportionate under data minimisation.                             **HIGH**         **MEDIUM**     **LOW**        Exclude 2024 data from AI training and validation until retroactive pseudonymisation is applied to comment field.

  **Residual singling-out after pseudonymisation**   Even after name removal, date + location + serial combination retains identifying power. Processing remains personal data under GDPR.                          **MEDIUM**       **LOW**        **LOW**        Accepted as residual risk proportionate to legitimate business purpose. Documented in processing register. Reviewed annually.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **4**   **Mitigation measures and residual risk**

  ------- ----------------------------------------------------------------------

**4.1 Technical measures**

1.  Pseudonymisation pipeline: Build an automated pre-processing step that identifies and replaces personal names in invoice comments before data enters the AI model. Replace with role descriptors: \[STORE MANAGER\], \[VAULTGUARD STAFF\], \[CONTRACTOR\], \[CUSTOMER\]. Preserve all factual content.

2.  Two-layer architecture: AI processing layer receives invoice number, OOS categories, part codes, labour rate, pseudonymised comment only. Billing execution layer retains full invoice, accessed by invoice number. Personal data never enters the AI model directly.

3.  Role-based access control on dashboard: The contractor flagging section of the fleet intelligence dashboard is restricted to authorised operations management personnel. Fleet data and billing KPIs are accessible to all authorised dashboard users.

4.  2024 data quarantine: 2024 invoice dataset flagged as requiring pseudonymisation before any AI use. Access restricted pending retroactive processing.

**4.2 Organisational measures**

5.  Operational policy document: Written policy prohibiting use of billing AI output for biller performance evaluation. Signed by relevant managers. Included in system governance documentation.

6.  Privacy notice: VaultGuard publishes a publicly accessible privacy notice stating that maintenance invoice data, including technician service notes, is processed for billing accuracy purposes. This addresses the data subject notification obligation for contractors with whom VaultGuard has no direct relationship.

7.  Data subject access request process: A DSAR process is established so that any individual who appears in invoice data can request access to, correction of, or erasure of their personal data. Responses within the statutory 30-day window.

**4.3 Retention limits**

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Data layer**                            **Retention limit**            **Justification**
  ----------------------------------------- ------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Full invoice (billing system)**         **7 years**                    US tax and audit record retention requirement. Overrides GDPR erasure requests where legal obligation applies.

  **AI training dataset (pseudonymised)**   **3 years or model refresh**   Retained only while model is in active use. Model must be retrained on fresh data within 3 years. Pseudonymised dataset deleted on model retirement.

  **AI model outputs (YES/NO flags)**       **12 months**                  Billing flags are operational outputs. Retained for audit and dispute resolution for one billing cycle. Deleted on annual rollover.

  **Contractor flagging dashboard data**    **90 days rolling**            Flags are operational management tools. Shortest defensible retention. After 90 days the flag has served its purpose --- either investigated or dismissed.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **5**   **Conclusion and sign-off**

  ------- ----------------------------------------------------------------------

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **DPIA conclusion**                                                                                                                                                                                                                                                 |
|                                                                                                                                                                                                                                                                     |
| Processing is necessary for a legitimate purpose and cannot be made fully privacy-neutral given the inherent identifying power of the invoice data combination. The legal basis (legitimate interests) is established and the three-part test is satisfied.         |
|                                                                                                                                                                                                                                                                     |
| The residual risk after mitigations is LOW. No identified risk requires suspension or prohibition of processing. The system may proceed to deployment subject to implementation of all mitigation measures in Section 4 before live data is processed.              |
|                                                                                                                                                                                                                                                                     |
| This DPIA must be reviewed if: (a) the AI output is used to evaluate biller performance; (b) contractor IDs are added to the dataset; (c) the system is extended to process data of a new category of individuals; (d) a data breach occurs involving invoice data. |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ------------------------------------------ ----------------------------------------------------------------------------------------------------------
  **Overall risk level (post-mitigation)**   LOW

  **Proceed to deployment?**                 YES --- subject to Section 4 mitigations being implemented first

  **DPA consultation required?**             No --- residual risk is LOW. Consultation required only if HIGH residual risk remains after mitigations.

  **Review trigger**                         Biller performance evaluation use / contractor ID addition / new data categories / data breach

  **Next scheduled review**                  March 2027 (12 months) or earlier if trigger condition met

  **Prepared by**                            Pedro --- AI Consultant, IronHack Bootcamp Capstone

  **Date**                                   March 2026
  ------------------------------------------ ----------------------------------------------------------------------------------------------------------

*DPIA · Billing Validation AI · VaultGuard Capstone · IronHack AI Bootcamp · March 2026*
