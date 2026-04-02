**VAULTGUARD × SAFECORE**

**AI-Powered Maintenance Intelligence Platform**

Use Case Definition Document · IronHack AI Bootcamp Capstone · March 2026

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Project at a glance**                                                                                                                                                                                 |
|                                                                                                                                                                                                         |
| Industry: Cash management & fintech infrastructure · Company: VaultGuard Inc.                                                                                                                                |
|                                                                                                                                                                                                         |
| Problem: \$2.68M/year in reactive smart safe maintenance with no predictive capability, no contractor oversight, and systematic billing errors estimated at \$98,843 in client dispute risk.            |
|                                                                                                                                                                                                         |
| Solution: An AI-powered maintenance intelligence platform combining predictive failure scoring, automated billing validation, real-time fleet risk dashboards, and contractor accountability workflows. |
|                                                                                                                                                                                                         |
| Engagement type: External AI consulting · Primary contact: VP of Product                                                                                                              |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

+-------------------------+------------------------+-----------------------+--------------------------+
| **76,000**              | **\$2.68M**            | **\~50%**             | **\$1.35M**              |
|                         |                        |                       |                          |
| Smart safes in US fleet | 2024 maintenance spend | Target cost reduction | Estimated annual savings |
+-------------------------+------------------------+-----------------------+--------------------------+

  ------- ----------------------------------------------------------------------
  **1**   **Company profile --- VaultGuard Inc.**

  ------- ----------------------------------------------------------------------

  ---------------------- ---------------------------------------------------------------------------------------------------
  **Company**            VaultGuard Inc. --- subsidiary of VaultGuard Group (Sweden, publicly listed)

  **Industry**           Cash management, armored transport, smart safe services

  **Size**               \~200 US locations, 76,000 smart safeboxes deployed nationally

  **Revenue model**      Warranty contracts (\$270--\$600/unit/year) + CIT + armored transport services

  **Hardware fleet**     98% SafeCore Systems/NexCash Technologies hardware (SV-100, SV-200, SV-300, Titan C, Titan dual models)

  **Critical context**   SafeCore Systems acquired by ArmorGroup (direct VaultGuard competitor) via NexCash Technologies in February 2022 for \~C\$900M

  **Primary contact**    VP of Product

  **Engagement start**   March 2026 · Friday deliverable deadline
  ---------------------- ---------------------------------------------------------------------------------------------------

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **⚠️ Strategic context: competitor-owned hardware**                                                                                                                                                                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                                                                                                                                                                 |
| VaultGuard operates 76,000 smart safes of which 98% are manufactured by SafeCore Systems, now owned by ArmorGroup through NexCash Technologies since February 2022. ArmorGroup is a direct competitor in the cash services industry. This means VaultGuard is structurally dependent on a competitor-owned hardware manufacturer for its entire US smart safe fleet --- a strategic vulnerability that underpins the urgency of this engagement. |
|                                                                                                                                                                                                                                                                                                                                                                                                                 |
| The Italian EuroSafe AG units arriving in July 2026 (40 units) are also NexCash Technologies-owned, meaning diversification has not yet occurred in practice.                                                                                                                                                                                                                                                                     |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ------- ----------------------------------------------------------------------
  **2**   **Business problem definition**

  ------- ----------------------------------------------------------------------

VaultGuard\'s US smart safe operation runs almost entirely reactively. When a safe fails, a service call is dispatched, a contractor arrives, and an invoice is submitted. There is no mechanism to predict which safes are approaching failure, no structured oversight of contractor billing, and no system to validate whether service costs are correctly passed to the client or absorbed by VaultGuard. The result is a maintenance program that costs \$2.68M per year --- with significant portions of that spend attributable to preventable failures, inflated contractor invoices, and systematic billing errors.

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **The four root causes**                                                                                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                                                      |
| 1\. Reactive-only maintenance --- No predictive capability. Safes fail in the field before intervention. The 2014--2015 cohort (427 units) has already crossed its financial break-even point but remains in service generating the most expensive invoices.                                         |
|                                                                                                                                                                                                                                                                                                      |
| 2\. No contractor accountability --- Independent technicians submit invoices without structured oversight. 16.5% of 2024 invoices are flagged as Abused Part at an average cost of \$961 vs \$323 for normal visits. No technician ID is attached to service records.                                |
|                                                                                                                                                                                                                                                                                                      |
| 3\. Systematic billing errors --- AI assessment of 2025 data identified 456 billing discrepancies: \$98,843 in over-billing (client dispute risk) and \$22,915 in under-billing (revenue leak). The primary biller is not consistently applying warranty vs. customer-billable classification rules. |
|                                                                                                                                                                                                                                                                                                      |
| 4\. Zero data visibility from SafeCore Systems/NexCash Technologies --- SafeCore Systems is not sharing total incidents opened, making it impossible to calculate what proportion of service calls are absorbed under warranty vs. billed. This is a contractual visibility gap that must be escalated.                                  |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ---------------------------- -------------------------------------------------------------------
  **Current state**            100% reactive maintenance, no prediction, no contractor scoring

  **2024 total spend**         \$2,681,277 across 6,259 invoices and 5,129 unique safes

  **Average invoice**          \$428.39 (2024) · \$351.46 (2025 partial year, -18%)

  **Top cost driver 2024**     Bill validator failures: 37% of spend (\$988k, avg \$1,083/visit)

  **Top cost driver 2025**     Comms/modem issues: 54% of all invoices (new OOS classification)

  **Abuse-flagged invoices**   16.5% of 2024 invoices --- 3x the cost of normal visits

  **Billing discrepancies**    456 identified --- \$98,843 over-billing + \$22,915 under-billing

  **Fleet risk**               37 units score ≥85/100 --- recommend immediate replacement
  ---------------------------- -------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **3**   **Proposed AI-powered solution**

  ------- ----------------------------------------------------------------------

The proposed solution is an AI-powered maintenance intelligence platform with four integrated components. Each component addresses one of the four root causes identified above. The platform is designed to be deployed incrementally --- starting with the highest-impact, lowest-effort components and building toward a fully integrated fleet intelligence system.

+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **01** | **Predictive failure scoring**                                                                                                                                                                                                                                                                                                                  |
|        |                                                                                                                                                                                                                                                                                                                                                 |
|        | A polynomial regression model trained on 2024 invoice data (R²=0.84) scores each safe unit from 0--100 based on age, model type, failure history, and cost trajectory. Units scoring ≥71 are flagged as HIGH risk; ≥85 are recommended for immediate replacement. Deployed as a daily fleet risk dashboard updated from invoice data.           |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        |                                                                                                                                                                                                                                                                                                                                                 |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **02** | **Automated billing validation AI**                                                                                                                                                                                                                                                                                                             |
|        |                                                                                                                                                                                                                                                                                                                                                 |
|        | An LLM-based classification system reads OOS Tier 1/2 categories and invoice comments to assess whether each invoice should be billed to the customer or absorbed by VaultGuard. Achieves 84.3% match rate vs. current human biller on 2025 data. Flags all discrepancies for human review. POC built and validated.                                |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        |                                                                                                                                                                                                                                                                                                                                                 |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **03** | **Contractor accountability workflow (n8n POC)**                                                                                                                                                                                                                                                                                                |
|        |                                                                                                                                                                                                                                                                                                                                                 |
|        | An n8n automation workflow that ingests invoices, scores technician behaviour against baseline cost benchmarks, flags outliers for audit, and triggers an alert to the operations manager. Built as a no-code POC using n8n Schedule Trigger → HTTP Request → JS Code → IF branch → Gmail/Airtable. Demonstrated in Week 7 SilverTrust project. |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        |                                                                                                                                                                                                                                                                                                                                                 |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **04** | **Fleet intelligence dashboard (MVP)**                                                                                                                                                                                                                                                                                                          |
|        |                                                                                                                                                                                                                                                                                                                                                 |
|        | An interactive HTML/D3.js dashboard displaying real-time fleet risk scores, US conflict map by state, OOS failure category trends, break-even analysis by model (SV-100/SV-200/SV-300/Titan C/Titan dual), and billing accuracy KPIs. Deployed as a VP-facing presentation layer and an operational tool for the VaultGuard fleet team.                        |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  ------- ----------------------------------------------------------------------
  **4**   **Key stakeholders**

  ------- ----------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Role**               **Name / dept**         **Primary interest**                                                                                      **Impact**
  ---------------------- ----------------------- --------------------------------------------------------------------------------------------------------- -----------------
  **VP of Product**      VP of Product        Understand true cost of maintenance, validate billing accuracy, assess NexCash Technologies/ArmorGroup strategic risk   **HIGH**

  **Operations**         Field Operations Team   Reduce service call volume, improve contractor quality, receive early warning on at-risk safes            **HIGH**

  **Finance**            CFO / Finance Dept      Quantify \$1.35M savings case, validate ROI, ensure billing accuracy and revenue recovery                 **HIGH**

  **Legal**              General Counsel         Review NexCash Technologies contract for data sharing obligations and renegotiation rights post-acquisition             **HIGH**

  **IT / Engineering**   Tech Team               Integrate AI platform with existing VaultGuard systems, maintain n8n workflows and dashboard                  **MEDIUM**

  **Clients**            Retail / QSR chains     Confidence that billing is accurate; Whataburger, Speedway, Popeyes flagged as over-billed                **MEDIUM**

  **Contractors**        SafeCore Systems / independents    Awareness that invoices are being scored; behavioural change through accountability                       **LOW**

  **AI Consultant**      Pedro (IronHack)        Deliver analysis, POC, and strategic recommendations before Friday deadline                               **HIGH**
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------- ----------------------------------------------------------------------
  **5**   **Success criteria --- what "this works" looks like**

  ------- ----------------------------------------------------------------------

Success is defined across three horizons. Phase 1 (POC) criteria are measurable today from the data already analysed. Phase 2 (Pilot) criteria require a 90-day operational run. Phase 3 (Production) criteria define the long-term value case.

  -----------------------------------------------------------------------------------------------------------------------------------------------
  **Criterion**                            **Metric**                                      **Target threshold**                  **Owner**
  ---------------------------------------- ----------------------------------------------- ------------------------------------- ----------------
  **Phase 1 --- POC validated (now)**                                                                                            

  **Billing AI accuracy**                  Match rate vs human biller decisions            **≥84.3% (demonstrated)**             AI Consultant

  **Fleet risk scoring**                   Units correctly classified HIGH/MEDIUM/LOW      **Validated on 5,129 units**          AI Consultant

  **POC workflow**                         n8n automation end-to-end run                   **Zero manual steps required**        AI Consultant

  **Phase 2 --- Pilot (90 days)**                                                                                                

  **Billing dispute reduction**            Client billing disputes per month               **≥50% reduction vs baseline**        Operations

  **Abuse detection**                      Flagged invoices audited and resolved           **≥80% of HIGH flags actioned**       Operations

  **Preventive maintenance**               Reactive call rate on pilot cohort              **≥30% reduction vs control group**   Field Ops

  **Phase 3 --- Production (12 months)**                                                                                         

  **Annual cost reduction**                Total maintenance spend vs 2024 baseline        **≥\$1.35M saved (≥50%)**             Finance

  **Billing accuracy**                     Discrepancy rate on all invoices                **\<5% error rate**                   Operations

  **Fleet modernisation**                  Units past break-even retired or flagged        **427+ units addressed**              Fleet Mgmt

  **NexCash Technologies risk mitigation**               Contract renegotiated with data access clause   **Signed before next renewal**        Legal / VP
  -----------------------------------------------------------------------------------------------------------------------------------------------

*Use Case Definition · VaultGuard × SafeCore Capstone · IronHack AI Bootcamp · March 2026*
