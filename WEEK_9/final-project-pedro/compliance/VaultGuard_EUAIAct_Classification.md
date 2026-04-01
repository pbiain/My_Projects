**VAULTGUARD × SAFECORE**

**EU AI Act Compliance Documentation**

Risk Classification · Conformity Assessment Summary · Technical Documentation Outline · March 2026

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Document scope**                                                                                                                                                                                                                                                                            |
|                                                                                                                                                                                                                                                                                               |
| This document classifies the four AI components of the VaultGuard Maintenance Intelligence Platform under the EU AI Act (Regulation 2024/1689). It provides step-by-step classification reasoning, a conformity assessment summary, and a technical documentation outline for each component. |
|                                                                                                                                                                                                                                                                                               |
| Consultant: Pedro (IronHack AI Bootcamp) · Client: VaultGuard Inc. (cash management) · Primary contact: Alex Navarro, VP of Product                                                                                                                                                           |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ------- ----------------------------------------------------------------------
  **1**   **AI system overview**

  ------- ----------------------------------------------------------------------

  ------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------
  System name               VaultGuard Maintenance Intelligence Platform

  Deployer                  VaultGuard Inc. --- internal operational deployment

  Provider                  AI Consultant (IronHack Capstone Project)

  Purpose                   Predict smart safe failures, validate maintenance billing decisions, monitor contractor invoice quality, and visualise fleet risk across 76,000 deployed units

  Deployment context        Internal B2B cash management operations. No direct interaction with consumers or members of the public.

  Number of AI components   4 --- assessed individually below
  ------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **2**   **Risk classification summary**

  ------- ----------------------------------------------------------------------

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Classification methodology**                                                                                                                                                                                                                                                        |
|                                                                                                                                                                                                                                                                                       |
| Each component is assessed using the EU AI Act four-step classification process: (1) check for prohibited practices under Article 5; (2) check Annex III high-risk categories; (3) check Article 50 limited risk transparency obligations; (4) default to minimal risk if none apply. |
|                                                                                                                                                                                                                                                                                       |
| The system as a whole is classified as LIMITED RISK. No component reaches Unacceptable or High Risk as designed. Escalation conditions are documented for each component where applicable.                                                                                            |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Component**                            **Risk level**        **Article**                            **Key reason**
  ---------------------------------------- --------------------- -------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------
  **Predictive failure scoring**           **MINIMAL**           No specific obligation                 Scores machines (safe units), not people. No natural person's rights affected.

  **Billing validation AI**                **LIMITED**           Art. 50 --- transparency               AI-assisted commercial decision. Transparency obligation if output is client-facing. Human biller retains override authority.

  **Contractor accountability workflow**   **MINIMAL→LIMITED**   Art. 50 if output reaches contractor   Flags for human review only. Final decision remains with operations manager. Escalates to Limited Risk if output reaches contractor directly.

  **Fleet intelligence dashboard**         **MINIMAL**           No specific obligation                 Visualisation tool. No automated decisions. Role-based access control required for contractor flagging section.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **3**   **Step-by-step classification reasoning**

  ------- ----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **Component 1 --- Predictive failure scoring \| MINIMAL RISK**

  -----------------------------------------------------------------------

-   Step 1 --- Prohibited practices (Article 5): Does the system manipulate behaviour subliminally, exploit vulnerabilities, conduct real-time biometric surveillance, or perform social scoring? No. The system scores inanimate objects (safe units) based on age, model type, and maintenance cost history. No natural person is the subject of any score.

-   Step 2 --- High Risk (Annex III): Does the system fall under any Annex III category? The relevant categories to check are: (4) employment and workers management, (5) access to essential services. The system does not make decisions about people's employment or access to services. It flags machines for maintenance or replacement. Annex III does not apply.

-   Step 3 --- Escalation condition identified: If the scoring model were extended to evaluate technician performance based on the safes they service (e.g. flagging a technician whose assigned safes have abnormally high failure rates), it would fall under Annex III item 4 (employment, task allocation, performance evaluation). This extension is NOT part of the current design.

-   Step 4 --- Limited Risk (Article 50): Does the system generate synthetic content, interact with users in a way that could be mistaken for human interaction, or produce deep fakes? No. It outputs a numerical risk score consumed internally. Article 50 does not apply.

-   Conclusion: MINIMAL RISK. No specific EU AI Act obligations apply. Voluntary best practice: document the model architecture and training data in internal technical documentation.

  -----------------------------------------------------------------------
  **Component 2 --- Billing validation AI \| LIMITED RISK**

  -----------------------------------------------------------------------

-   Step 1 --- Prohibited practices (Article 5): No manipulation, no biometric surveillance, no social scoring. The system reads invoice data and outputs a binary billing recommendation. Not prohibited.

-   Step 2 --- High Risk (Annex III): The system makes recommendations about whether to charge a business client for a maintenance visit. The client is a legal entity (QSR chain, gas station network), not a natural person. Annex III high-risk categories require impact on natural persons' fundamental rights. Charging a business more or less for a service call does not meet this threshold. Annex III does not apply.

-   Step 2a --- Escalation condition identified: If the system output is used to evaluate the human biller's performance --- measuring how often the biller's decisions align with the AI recommendation --- then it becomes a performance monitoring tool under Annex III item 4 (employment, task allocation, performance evaluation of workers). This would trigger High Risk classification, mandatory conformity assessment, and human oversight documentation. This escalation is NOT part of the current deployment design but must be explicitly prohibited in the system's operational policy.

-   Step 3 --- Limited Risk (Article 50): If billing decisions validated by the AI are communicated to clients without disclosing that AI was involved in the decision, a transparency obligation arises under Article 50(1) by analogy. Clients interacting with AI-generated billing outputs should be informed. This is the conservative compliant position.

-   Conclusion: LIMITED RISK. Obligation: disclose to clients that billing decisions are AI-assisted. Operational policy must prohibit using AI output to evaluate biller performance.

  ----------------------------------------------------------------------------------
  **Component 3 --- Contractor accountability workflow \| MINIMAL → LIMITED RISK**

  ----------------------------------------------------------------------------------

-   Step 1 --- Prohibited practices (Article 5): No manipulation, no biometric surveillance, no social scoring. The system analyses invoice patterns, not personal attributes. Not prohibited.

-   Step 2 --- High Risk (Annex III): The system flags invoices for human review and notifies an operations manager. It does NOT make the final decision on contractor assignment, suspension, or termination. The operations manager retains full authority. Because the final decision is human-made, the system does not cross into High Risk employment category. Annex III does not apply as designed.

-   Step 2a --- Escalation condition: If the workflow output were connected to an automated contractor de-listing or assignment restriction system, it would cross into High Risk under Annex III item 4. This connection must be explicitly prevented in the system architecture.

-   Step 3 --- Limited Risk (Article 50): As designed, the output goes to an internal operations manager dashboard (Power BI / Microsoft 365). The contractor does not interact with the system or receive its output directly. Article 50 does not currently apply. However, if VaultGuard were to notify contractors directly ("your invoices have been flagged"), that notification would be AI-generated content about an individual, triggering Article 50 transparency obligations.

-   Conclusion: MINIMAL RISK in current design. Escalates to LIMITED RISK if output reaches the contractor directly. Operational policy must restrict output to internal management use only.

  -----------------------------------------------------------------------
  **Component 4 --- Fleet intelligence dashboard \| MINIMAL RISK**

  -----------------------------------------------------------------------

-   Step 1 --- Prohibited practices (Article 5): Not applicable. Visualisation tool only.

-   Step 2 --- High Risk (Annex III): The dashboard displays fleet data, OOS category trends, billing accuracy KPIs, and contractor flagging summaries. It does not make decisions. It is a human-facing analytical tool. Annex III does not apply.

-   Step 3 --- Limited Risk (Article 50): The dashboard does not generate synthetic content or interact with users as if it were human. Article 50 does not apply.

-   Risk note --- data minimisation: The contractor flagging section of the dashboard displays information from which individual contractors may be identifiable. Role-based access control must restrict this section to authorised operations management personnel only. Unrestricted access would create a GDPR data minimisation issue, not an EU AI Act issue.

-   Conclusion: MINIMAL RISK. No EU AI Act obligations. GDPR access control obligation applies to contractor flagging section.

  ------- ----------------------------------------------------------------------
  **4**   **Conformity assessment summary**

  ------- ----------------------------------------------------------------------

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **What this document certifies**                                                                                                                                                                                                                                                                                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| This conformity assessment summary states what the VaultGuard Maintenance Intelligence Platform does, its risk classification under the EU AI Act, and what obligations apply. It does not constitute a full conformity assessment under Article 43 (which is only required for High Risk systems). It documents the reasoning by which the system avoids High Risk classification and the controls in place to maintain that classification. |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ----------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  System name             VaultGuard Maintenance Intelligence Platform

  Overall risk class      LIMITED RISK (system level) · Two components at Minimal, two at Limited

  Prohibited practices    None --- confirmed through Article 5 assessment of all four components

  High Risk triggers      None active --- two escalation conditions documented and mitigated by design

  Article 50 obligation   Billing AI: disclose AI involvement to clients in billing communications

  Human oversight         Human biller retains override on billing AI. Operations manager retains final authority on contractor flags. No autonomous decisions affecting natural persons.

  Prohibited uses         \(1\) Using billing AI output to evaluate biller performance. (2) Connecting contractor workflow to automated assignment restriction. (3) Sending contractor flags directly to contractors without disclosure.

  Registration required   No --- EU AI Act database registration is mandatory only for High Risk systems (Article 51). Not applicable here.

  Review trigger          This classification must be reviewed if: (a) technician ID is added to the dataset; (b) workflow output is connected to automated contractor management; (c) billing AI is used for biller performance evaluation.
  ----------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **5**   **Technical documentation outline (Annex IV skeleton)**

  ------- ----------------------------------------------------------------------

+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Note on scope**                                                                                                                                                                                                                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                                |
| Full Annex IV technical documentation is mandatory only for High Risk AI systems. This outline is provided as a voluntary best practice for the Limited Risk components, demonstrating compliance-aware development. If either escalation condition is triggered and the system reaches High Risk, this outline becomes the mandatory documentation framework. |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Ref**   **Section**                    **Contents (current status)**
  --------- ------------------------------ -----------------------------------------------------------------------------------------------------------------------------------------------------------
  **1.**    **General description**        System name, purpose, version, deployer identity, intended use, geographic scope --- COMPLETE in Use Case Definition document

  **2.**    **Design specifications**      Polynomial regression model architecture (R²=0.84), LLM classification logic for billing AI, n8n workflow architecture, dashboard data model --- PARTIAL

  **3.**    **Training data**              Synthetic/mock data based on 2024 maintenance invoice structure. No real personal data used in model training --- COMPLETE

  **4.**    **Validation & testing**       Billing AI: 84.3% match rate on 2025 test data (2,906 classified invoices). Failure scoring: validated on 5,129 units. --- PARTIAL

  **5.**    **Human oversight measures**   Human biller reviews all billing AI outputs. Operations manager reviews all contractor flags. No autonomous decisions affecting individuals. --- COMPLETE

  **6.**    **Transparency measures**      Client disclosure template for AI-assisted billing (to be drafted). Internal policy prohibiting prohibited uses. --- TO DO

  **7.**    **Accuracy & robustness**      84.3% billing accuracy. 24.5% unclear classification rate requiring human review. Failure scoring R²=0.84. Known limitations documented. --- PARTIAL

  **8.**    **Post-market monitoring**     Monthly accuracy review of billing AI classifications. Quarterly review of contractor flagging rates. Annual classification review. --- TO DO
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

*EU AI Act Classification · VaultGuard × SafeCore Capstone · IronHack AI Bootcamp · March 2026*
