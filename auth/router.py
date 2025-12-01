# Updated auth/router.py
# (Add these new endpoints to your existing router.py file)

from fastapi import APIRouter, Query, Header
import httpx  # You'll need to install if not already: pip install httpx
from typing import Optional

router = APIRouter(prefix="/authentication", tags=["auth"])  # Prefix to match the external API path
base_url = "https://api.whitebooks.in"
@router.get("/otprequest")
async def request_otp(
    
    email: str = Header(..., description="GST UserName"),
    gst_username: str = Header(..., description="GST UserName"),
    state_cd: str = Header(..., description="State Code"),
    ip_address: str = Header(..., description="IP Address"),
    client_id: str = Header(..., description="Client ID"),
    client_secret: str = Header(..., description="Client Secret")
):
    print(email, gst_username, state_cd, ip_address, client_id, client_secret)
    """
    Request for OTP. Forwards the request to the external GST API.
    After successful verification, the GST system sends OTP via Email and SMS.
    """

    url = f"{base_url}/authentication/otprequest"
    
    headers = {
        "gst_username": gst_username,
        "state_cd": state_cd,
        "ip_address": ip_address,
        "client_id": client_id,
        "client_secret": client_secret,
        # Add any other common headers if needed, e.g., "Content-Type": "application/json"
    }
    
    params = {
        "email": email
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPException for bad responses
            return {
                "success": True,
                "message": "OTP requested successfully",
                "data": response.json()  # Assuming the response is JSON; adjust if needed
            }
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "message": f"API Error: {e.response.status_code} - {e.response.text}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Request failed: {str(e)}"
            }

@router.get("/authtoken")
async def request_auth_token(
    email: str = Header(..., description="User Email"),
    otp: str = Header(..., description="GST User Received OTP (Default for Sandbox: 575757)"),
    gst_username: str = Header(..., description="GST UserName"),
    state_cd: str = Header(..., description="State Code"),
    ip_address: str = Header(..., description="IP Address"),
    txn: str = Header(..., description="Transaction ID (from OTP request response)"),
    client_id: str = Header(..., description="Client ID"),
    client_secret: str = Header(..., description="Client Secret")
):
    """
    Request for Authorization Token. Forwards the request to the external GST API.
    Used after OTP verification to obtain the auth token.
    """
   
    url = f"{base_url}/authentication/authtoken"
    
    headers = {
        "gst_username": gst_username,
        "state_cd": state_cd,
        "ip_address": ip_address,
        "txn": txn,
        "client_id": client_id,
        "client_secret": client_secret,
        # Add any other common headers if needed, e.g., "Content-Type": "application/json"
    }
    
    params = {
        "email": email,
        "otp": otp
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPException for bad responses
            return {
                "success": True,
                "message": "Authorization token requested successfully",
                "data": response.json()  # Assuming the response is JSON; adjust if needed (e.g., extract token)
            }
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "message": f"API Error: {e.response.status_code} - {e.response.text}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Request failed: {str(e)}"
            }

@router.get("/refreshtoken")
async def refresh_auth_token(
    email: str = Query(..., description="User Email"),
    gst_username: str = Header(..., description="GST UserName"),
    state_cd: str = Header(..., description="State Code"),
    ip_address: str = Header(..., description="IP Address"),
    txn: str = Header(..., description="Transaction ID (from previous auth request)"),
    client_id: str = Header(..., description="Client ID"),
    client_secret: str = Header(..., description="Client Secret")
):
    """
    Request for Refresh Token. Forwards the request to the external GST API.
    Used by GSP to extend access through Authorization code without user intervention.
    """
   
    url = f"{base_url}/authentication/refreshtoken"
    
    headers = {
        "gst_username": gst_username,
        "state_cd": state_cd,
        "ip_address": ip_address,
        "txn": txn,
        "client_id": client_id,
        "client_secret": client_secret,
        # Add any other common headers if needed, e.g., "Content-Type": "application/json"
    }
    
    params = {
        "email": email
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPException for bad responses
            return {
                "success": True,
                "message": "Refresh token requested successfully",
                "data": response.json()  # Assuming the response is JSON; adjust if needed
            }
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "message": f"API Error: {e.response.status_code} - {e.response.text}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Request failed: {str(e)}"
            }

@router.get("/logout")
async def user_logout(
    email: str = Query(..., description="User Email"),
    gst_username: str = Header(..., description="GST UserName"),
    state_cd: str = Header(..., description="State Code"),
    ip_address: str = Header(..., description="IP Address"),
    txn: str = Header(..., description="Transaction ID (from auth request)"),
    client_id: str = Header(..., description="Client ID"),
    client_secret: str = Header(..., description="Client Secret")
):
    """
    Request for Logout. Forwards the request to the external GST API.
    Used for user logout.
    """
    base_url = " https://api.whitebooks.in"
    url = f"{base_url}/authentication/logout"
    
    headers = {
        "gst_username": gst_username,
        "state_cd": state_cd,
        "ip_address": ip_address,
        "txn": txn,
        "client_id": client_id,
        "client_secret": client_secret,
        # Add any other common headers if needed, e.g., "Content-Type": "application/json"
    }
    
    params = {
        "email": email
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPException for bad responses
            return {
                "success": True,
                "message": "Logout successful",
                "data": response.json()  # Assuming the response is JSON; adjust if needed
            }
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "message": f"API Error: {e.response.status_code} - {e.response.text}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Request failed: {str(e)}"
            }

