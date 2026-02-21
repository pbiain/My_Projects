# mcp_langchain.py
# Lab: Using MCP in LangChain
# Week 3 - Day 5

import asyncio
import traceback
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

DOCUMENTS_PATH = r"C:\Users\pbiai\Desktop\IRONHACK-BOOTCAMP\WEEK_3\Day_5\documents"

SYSTEM_PROMPT = """You are a document analysis assistant with access to a documents directory.
You can read, search, and analyze files using your available tools.
Always read the actual file content before answering questions about it.
When referring to files, always use the full relative path: documents/filename.txt
Be concise, structured, and professional in your responses."""

async def run_query(agent, query: str) -> None:
    """Send a single query to the agent and print the response."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    response = await agent.ainvoke({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    })
    print(f"Answer:\n{response['messages'][-1].content}")

async def main():
    print("Connecting to MCP server...")
    client = MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    DOCUMENTS_PATH
                ],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()
    print(f"[OK] {len(tools)} tools loaded!")

    print("\nLoading MCP resources...")
    try:
        resources = await client.get_resources()
        print(f"[OK] {len(resources)} resources found")
    except Exception as e:
        print("[WARNING] Resources not available (filesystem server does not support them)")
        resources = []

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools)
    print("\n[OK] Document Analysis Agent ready!")

    queries = [
        "What documents are available? List all files in the documents folder.",
        "Read documents/project_beta.txt and extract the 3 most important lessons learned.",
        "Read both documents/project_alpha.txt and documents/project_beta.txt. Create a brief executive summary covering both projects in 5 bullet points.",
        "Search for any files that contain the word pipeline in their name or content.",
    ]

    for query in queries:
        await run_query(agent, query)

    print(f"\n{'='*60}")
    print("Document analysis complete!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        traceback.print_exc()