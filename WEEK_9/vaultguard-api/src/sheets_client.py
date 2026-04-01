#!/usr/bin/env python3
"""
Google Sheets Client for VaultGuard API Server
"""

import os
from typing import Dict, List, Any
from datetime import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SheetsClient:
    """Client for interacting with Google Sheets API"""

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        creds = None

        # Check for existing token
        token_path = os.path.join(os.getcwd(), 'token.json')
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Use client secrets from environment or file
                client_secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
                client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')

                if client_id and client_secret:
                    # Use environment variables
                    flow = InstalledAppFlow.from_client_config(
                        {
                            "installed": {
                                "client_id": client_id,
                                "client_secret": client_secret,
                                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                            }
                        },
                        self.SCOPES
                    )
                else:
                    # Try to use credentials file
                    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
                    if os.path.exists(creds_path):
                        flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
                    else:
                        raise ValueError("Google credentials not found. Set GOOGLE_OAUTH_CLIENT_ID/SECRET or provide credentials.json")

                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        self.creds = creds
        self.service = build('sheets', 'v4', credentials=creds)

    async def create_spreadsheet(self, title: str) -> Dict[str, Any]:
        """
        Create a new Google Sheets spreadsheet

        Args:
            title: Title for the spreadsheet

        Returns:
            Spreadsheet metadata
        """
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                },
                'sheets': [{
                    'properties': {
                        'title': 'Invoices',
                        'sheetType': 'GRID',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 20
                        }
                    }
                }]
            }

            request = self.service.spreadsheets().create(body=spreadsheet)
            response = request.execute()

            # Add headers to the sheet
            headers = [
                ['Invoice ID', 'Serial Number', 'Safe Age (Years)', 'Labour Charge',
                 'Parts Cost', 'Total Amount', 'OOS Tier 1', 'OOS Tier 2',
                 'Technician Comment', 'Current Decision', 'AI Decision',
                 'Confidence', 'Reason', 'Key Signal', 'Flag for Review', 'Processed At']
            ]

            spreadsheet_id = response['spreadsheetId']
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Invoices!A1:P1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()

            return response

        except HttpError as e:
            raise Exception(f"Failed to create spreadsheet: {e}")

    async def write_invoice_batch(self, spreadsheet_id: str, sheet_name: str, results: List[Dict]) -> None:
        """
        Write invoice classification results to Google Sheets

        Args:
            spreadsheet_id: Google Sheets spreadsheet ID
            sheet_name: Name of the sheet
            results: List of invoice processing results
        """
        try:
            # Prepare data for writing
            values = []
            for result in results:
                invoice = result['invoice']
                decision = result['decision']

                row = [
                    invoice.get('invoice_id', ''),
                    invoice.get('serial_number', ''),
                    invoice.get('safe_age_yr', ''),
                    invoice.get('labour_charge', 0),
                    invoice.get('parts_cost', 0),
                    invoice.get('total_amount', 0),
                    invoice.get('oos_tier1', ''),
                    invoice.get('oos_tier2', ''),
                    invoice.get('comment', ''),
                    invoice.get('current_decision', ''),
                    decision.get('decision', ''),
                    decision.get('confidence', ''),
                    decision.get('reason', ''),
                    decision.get('key_signal', ''),
                    'YES' if decision.get('flag_for_review', False) else 'NO',
                    datetime.now().isoformat()
                ]
                values.append(row)

            # Find the next available row
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f'{sheet_name}!A:A'
            ).execute()

            existing_rows = len(result.get('values', []))
            start_row = existing_rows + 1

            # Write the data
            range_name = f'{sheet_name}!A{start_row}:P{start_row + len(values) - 1}'
            body = {'values': values}

            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

        except HttpError as e:
            raise Exception(f"Failed to write to spreadsheet: {e}")

    async def get_invoice_statistics(self, spreadsheet_id: str, sheet_name: str = "Invoices") -> Dict[str, Any]:
        """
        Get statistics from processed invoices

        Args:
            spreadsheet_id: Google Sheets spreadsheet ID
            sheet_name: Name of the sheet

        Returns:
            Dictionary with statistics
        """
        try:
            # Get all data from the sheet
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f'{sheet_name}!A2:P'
            ).execute()

            rows = result.get('values', [])
            if not rows:
                return {"total_invoices": 0, "billable": 0, "absorb": 0, "flagged_for_review": 0}

            total_invoices = len(rows)
            billable = sum(1 for row in rows if len(row) > 10 and row[10].upper() == 'YES')
            absorb = sum(1 for row in rows if len(row) > 10 and row[10].upper() == 'NO')
            flagged = sum(1 for row in rows if len(row) > 14 and row[14].upper() == 'YES')

            # Calculate potential savings
            total_labour = sum(float(row[3]) for row in rows if len(row) > 3 and row[3])
            billable_amount = sum(float(row[3]) for row in rows if len(row) > 10 and row[10].upper() == 'YES' and len(row) > 3 and row[3])

            return {
                "total_invoices": total_invoices,
                "billable_count": billable,
                "absorb_count": absorb,
                "flagged_for_review": flagged,
                "billable_percentage": round(billable / total_invoices * 100, 2) if total_invoices > 0 else 0,
                "total_labour_cost": total_labour,
                "billable_labour_cost": billable_amount,
                "absorbed_labour_cost": total_labour - billable_amount
            }

        except HttpError as e:
            raise Exception(f"Failed to get statistics: {e}")