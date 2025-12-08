"""
FastAPI routes for endpoints and summaries.
Use the service layer and return JSON directly (FastAPI auto-serializes dicts/lists).
"""
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any

router = APIRouter(prefix="/api")

# Create a single shared DAC instance (you'll do this in main.py at startup)
# For now, assume `dac` is passed in or imported from a shared module
# Example: from backend.main import dac

@router.get("/endpoints")
async def list_endpoints(request: Request, org_id: str) -> List[Dict[str, Any]]:
    """
    GET /api/endpoints?org_id=...
    Returns list of endpoints for the org.
    """
    service = request.app.state.service  
    return await service.get_endpoints_for_org(org_id)


@router.post("/endpoints")
async def create_endpoint(request: Request, org_id: str, provider: str, name: str, region: str = None, credentials_arn: str = None) -> Dict[str, Any]:
    """
    POST /api/endpoints
    Creates a new endpoint and returns the created record.
    """
    service = request.app.state.service  
    return await service.create_endpoint(org_id, provider, name, region, credentials_arn)

@router.delete("/endpoints/{endpoint_id}")
async def delete_endpoint(request: Request, endpoint_id: str, org_id: str) -> Dict[str, str]:
    """
    DELETE /api/endpoints/{endpoint_id}?org_id=...
    Deletes the endpoint if found.
    """
    service = request.app.state.service  
    deleted = await service.delete_endpoint(endpoint_id, org_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return {"message": "Endpoint deleted", "endpoint_id": endpoint_id}


@router.get("/security/policies")
async def get_policies_summary(request: Request, org_id: str) -> List[Dict[str, Any]]:
    """
    GET /api/security/policies?org_id=...
    Returns policy summary for all endpoints in org.
    """
    service = request.app.state.service  
    return await service.get_policies_summary(org_id)


@router.get("/security/policies/{endpoint_id}")
async def get_policy_detail(request: Request, endpoint_id: str, org_id: str) -> Dict[str, Any]:
    """
    GET /api/security/policies/{endpoint_id}?org_id=...
    Returns policy detail for the endpoint.
    """
    service = request.app.state.service  
    detail = await service.get_policy_detail(endpoint_id, org_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Policy not found")
    return detail[0]


@router.get("/security/private-data")
async def get_private_data_summary(request: Request, org_id: str) -> List[Dict[str, Any]]:
    """
    GET /api/security/private-data?org_id=...
    Returns private data summary for all endpoints in org.
    """
    service = request.app.state.service  
    return await service.get_private_data_summary(org_id)


@router.get("/events/summary")
async def get_events_summary(request: Request, org_id: str) -> Dict[str, int]:
    """
    GET /api/events/summary?org_id=...
    Returns total event count for org.
    """
    service = request.app.state.service  
    count = await service.get_events_count(org_id)
    return {"total_events": count}


@router.get("/storage/size")
async def get_storage_sizes(request: Request, org_id: str) -> List[Dict[str, Any]]:
    """
    GET /api/storage/size?org_id=...
    Returns storage size per endpoint.
    """
    service = request.app.state.service  
    return await service.get_storage_sizes(org_id)


@router.get("/providers")
async def get_providers_summary(request: Request, org_id: str) -> List[Dict[str, Any]]:
    """
    GET /api/providers?org_id=...
    Returns provider summary (count and storage per provider).
    """
    service = request.app.state.service  
    return await service.get_providers_summary(org_id)