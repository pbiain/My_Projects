# VaultGuard MCP Server

AI-powered maintenance intelligence platform for smart safe billing validation.

## Overview

VaultGuard MCP is a Model Context Protocol (MCP) server that provides AI-powered tools for processing and classifying maintenance invoices for smart safes. It uses OpenAI's GPT-4o for intelligent billing decisions and Google Sheets for data storage and reporting.

## Features

- **Invoice Classification**: Automatically determine whether maintenance costs should be billed to clients or absorbed by VaultGuard
- **Google Sheets Integration**: Store and analyze invoice data in Google Sheets
- **Batch Processing**: Process multiple invoices simultaneously
- **Statistics Dashboard**: Generate insights from processed invoices
- **Evaluation Framework**: Test and validate classification accuracy

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vaultguard-mcp
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables in `.env`:
```bash
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret
```

## Usage

### Running the MCP Server

```bash
vaultguard-mcp
```

Or with SSE transport:
```bash
vaultguard-mcp --transport sse --port 8000
```

### Available Tools

#### 1. `classify_invoice`
Classify a single invoice for billing decision.

**Parameters:**
- `invoice_data`: JSON string with invoice information

**Example:**
```json
{
  "invoice_id": "INV-001",
  "serial_number": "SV100-12345",
  "labour_charge": 186.0,
  "parts_cost": 0.0,
  "comment": "Screen damaged by customer",
  "oos_tier1": "Physical Damage"
}
```

#### 2. `process_invoice_batch`
Process multiple invoices and write results to Google Sheets.

**Parameters:**
- `invoice_batch`: JSON array of invoice objects
- `spreadsheet_id`: Google Sheets ID
- `sheet_name`: Sheet name (default: "Invoices")

#### 3. `get_invoice_statistics`
Get statistics from processed invoices.

**Parameters:**
- `spreadsheet_id`: Google Sheets ID
- `sheet_name`: Sheet name (default: "Invoices")

#### 4. `create_invoice_spreadsheet`
Create a new Google Sheets spreadsheet for invoice tracking.

**Parameters:**
- `title`: Spreadsheet title (default: "VaultGuard Invoices")

## Decision Rules

The AI classifies invoices based on these rules:

**Bill Client (YES):**
- Abuse, misuse, vandalism, or negligence
- Liquid spillage onto equipment
- Physical damage (broken/cracked screen, bent components)
- Foreign objects in bill acceptors
- Infestation (insects, rodents)
- Safe burglary or robbery attempt damage
- Customer refused access or cancelled after dispatch

**Absorb (NO):**
- Normal wear and tear
- Communications/connectivity/modem failure
- Software or firmware issues
- Network or phone line problems
- User programming errors
- No problem found on site
- Printer jams or paper loading
- Equipment resets

## Evaluation

Run the evaluation suite to test classification accuracy:

```bash
python -m src.evals
```

This will create sample test cases and evaluate the model's performance.

## Google Sheets Setup

1. Create a Google Cloud Project
2. Enable the Google Sheets API
3. Create OAuth 2.0 credentials
4. Add the credentials to your `.env` file
5. Run the server - it will prompt for authentication on first use

## Development

### Project Structure
```
vaultguard-mcp/
├── src/
│   ├── mcp_server.py      # Main MCP server
│   ├── llm_client.py       # OpenAI integration
│   ├── sheets_client.py    # Google Sheets integration
│   ├── invoice_processor.py # Invoice processing logic
│   └── evals.py           # Evaluation utilities
├── evals/
│   └── invoice_examples.json # Test cases
├── n8n_config/
│   └── vaultguard_mcp.json  # n8n workflow config
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables
└── .gitignore            # Git ignore rules
```

### Adding New Tools

1. Define the tool function in `mcp_server.py` with the `@app.tool()` decorator
2. Add proper type hints and docstrings
3. Implement the logic using the available clients

## License

[Add license information]