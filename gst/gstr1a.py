# Updated router.py
# (Add these new endpoints to your existing router.py file)

from fastapi import APIRouter, Query, Header, HTTPException
import httpx
from typing import Dict, Any, Optional, List
import asyncio

router = APIRouter(prefix="/gstr1a", tags=["gstr1a"])  # Prefix to match the GSTR1A path

# Define valid endpoints to validate user input
VALID_ENDPOINTS = [
    'retsum', 'dociss', 'cdnra', 'b2cl', 'b2ba', 'ata', 'txp', 'supeco', 'supecoa',
    'ecom', 'ecoma', 'b2b', 'b2cla', 'b2csa', 'cdnr', 'at', 'expa', 'b2cs', 'exp',
    'nil', 'hsnsum', 'cdnur', 'cdnura', 'txpa'
]

async def fetch_gstr1a_endpoint(client: httpx.AsyncClient, base_url: str, endpoint: str, headers: Dict[str, str], params: Dict[str, str]) -> Dict[str, Any]:
    """
    Helper to fetch a single GSTR1A endpoint asynchronously.
    """
    url = f"{base_url}/gstr1a/{endpoint}"
    try:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {endpoint: response.json()}
    except httpx.HTTPStatusError as e:
        return {endpoint: {'error': f"API Error: {e.response.status_code} - {e.response.text}"}}
    except Exception as e:
        return {endpoint: {'error': f"Request failed: {str(e)}"}}

@router.get("/json_returns")
async def get_gstr1a_json_returns(
    gstin: str = Query(..., description="GSTIN of the taxpayer"),
    retperiod: str = Query(..., description="Return Period format MMYYYY"),
    email: str = Query(..., description="Email"),
    base_url: str = Query(..., description="Base URL for the external API, e.g., https://api.whitebooks.in"),
    endpoints_str: Optional[str] = Query(None, description="Comma-separated list of endpoints to fetch, e.g., 'retsum,b2b,nil'. If not provided, fetches all valid endpoints."),
    gst_username: str = Header(..., description="GST UserName"),
    state_cd: str = Header(..., description="State Code"),
    ip_address: str = Header(..., description="IP Address"),
    txn: str = Header(..., description="Transaction"),
    client_id: str = Header(..., description="Client ID"),
    client_secret: str = Header(..., description="Client Secret")
):
    """
    Aggregates specified GSTR1A data from user-selected endpoints into a single JSON response.
    If no endpoints are specified, fetches data from all valid endpoints.
    Forwards requests to the external GST API endpoints and combines the results.
    """
    
    headers = {
        "gst_username": gst_username,
        "state_cd": state_cd,
        "ip_address": ip_address,
        "txn": txn,
        "client_id": client_id,
        "client_secret": client_secret,
        "Content-Type": "application/json"
    }
    
    params = {
        "gstin": gstin,
        "retperiod": retperiod,
        "email": email
    }
    
    # Determine endpoints based on user input
    if endpoints_str:
        requested_endpoints = [e.strip() for e in endpoints_str.split(',') if e.strip()]
        invalid_endpoints = [e for e in requested_endpoints if e not in VALID_ENDPOINTS]
        if invalid_endpoints:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid endpoints provided: {', '.join(invalid_endpoints)}. Valid endpoints are: {', '.join(VALID_ENDPOINTS)}"
            )
        endpoints = requested_endpoints
    else:
        endpoints = VALID_ENDPOINTS.copy()
    
    async with httpx.AsyncClient() as client:
        try:
            # Fetch all endpoints in parallel for efficiency
            tasks = [fetch_gstr1a_endpoint(client, base_url, endpoint, headers, params) for endpoint in endpoints]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine responses
            combined_data = {}
            for resp in responses:
                if isinstance(resp, dict):
                    combined_data.update(resp)
                else:
                    # Handle any exceptions in gather
                    combined_data['fetch_error'] = {'error': str(resp)}
            
            return {
                "success": True,
                "message": f"GSTR1A data aggregated successfully for endpoints: {', '.join(endpoints)}",
                "data": combined_data
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Aggregation failed: {str(e)}")