\# n8n Jira Integration — Lab Documentation  
\*\*Project:\*\* Smart Resource Scheduler (SRS)    
\*\*Tool:\*\* n8n \+ Jira Cloud  
\---  
\#\# What I Built  
I connected n8n to my Jira project and built a workflow that automatically creates a Jira ticket when triggered. The trigger fires manually (or via webhook), and n8n calls the Jira API to create a new issue in the SRS project. I tested it and it worked — ticket SRS-10 was created successfully.  
\---  
\#\# Workflow Diagram  
\*(paste your n8n screenshot here)\*  
\*\*Nodes:\*\*  
1\. \*\*Manual Trigger\*\* — starts the workflow when you click "Execute"  
2\. \*\*Create Issue (Jira)\*\* — sends a request to Jira and creates a new ticket in the SRS project  
\---  
\#\# User Story Mapping  
| User Story | What it needs | Category |  
|---|---|---|  
| SRS-4: Real-time capacity data | Scheduled API fetch → update dashboard | Category 1 |  
| SRS-5: Unified view of allocations | Pull data → push to Jira automatically | Category 1 |  
| SRS-7: Flag over-allocation | Check a rule → create alert ticket | Category 1 |  
| SRS-6: Optimal team suggestions | AI reasoning about skills & fit | Category 2 |  
| SRS-8: Match to mentor assignments | Intelligent matching | Category 2 |  
| SRS-9: Skill gap reports | AI analysis & interpretation | Category 2 |  
\---  
\#\# What's Category 1 vs Category 2?  
\*\*Category 1\*\* is what n8n handles natively — moving data, calling APIs, following simple rules. No AI needed. That's what I built.  
\*\*Category 2\*\* needs AI to make smart decisions — like figuring out the best team composition or generating a meaningful skill gap report. n8n alone can't do that; you'd need to plug in something like OpenAI or LangChain.  
\---  
\#\# What I'd Build Next  
Talking with Isabella about prioritization, the approach I'd follow is: start with something visible and quick to deliver, so the company sees results fast.  
That means I'd start with \*\*SRS-4 or SRS-5\*\* — they're straightforward Category 1 automations (fetching data, keeping views updated) that are easy to build and easy to demo. Something tangible the client can see on day one.  
For \*\*SRS-7\*\* (over-allocation alerts), it's meaningful and still Category 1, but it requires a bit more logic — checking conditions, triggering at the right moment. I'd plan it carefully and build it shortly after, once there's already something to show.  
In parallel, I'd start scoping the \*\*Category 2 stories\*\* (SRS-6, SRS-8, SRS-9). These need AI and are more complex, so they take longer — but they're also the ones that deliver the most value long-term. The idea is not to wait for them, but to run them alongside the quick wins.  
\---  
\#\# Limitations  
\- n8n can move and react to data, but it can't \*understand\* it — that's where Category 2 starts  
\- The current workflow is triggered manually; in production it would need a real trigger (form, webhook, or schedule)  
\- Jira custom fields (like epic links) require extra configuration in n8n  
