from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any

# This is creating a simple router for the API endpoints

router = APIRouter(prefix="/api")

# GET /api/endpoints?org_id=xxx
# Returns: { "orgName": "...", "endpoints": [...], "totalEndpoints": 2 }
# Lists all storage endpoints for an organization
@router.get("/endpoints")
async def list_endpoints(request: Request, org_id: str) -> Dict[str, Any]:
    """
    GET /api/endpoints?org_id=...
    Returns list of endpoints for the org.
    """
    service = request.app.state.service  
    return await service.get_endpoints_for_org(org_id)

# POST /api/endpoints?org_id=xxx&provider=AWS&name=my-bucket&region=us-east-1
# Returns: { "orgName": "...", "endpointId": "...", "provider": "AWS", "name": "...", "region": "..." }
# Creates a new storage endpoint for the organization
@router.post("/endpoints")
async def create_endpoint(request: Request, org_id: str, provider: str, name: str, region: str = None, credentials_arn: str = None) -> Dict[str, Any]:
    """
    POST /api/endpoints
    Creates a new endpoint and returns the created record.
    """
    service = request.app.state.service  
    return await service.create_endpoint(org_id, provider, name, region, credentials_arn)

# DELETE /api/endpoints/{endpoint_id}?org_id=xxx
# Returns: { "message": "Endpoint deleted", "endpoint_id": "..." }
# Deletes a storage endpoint
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

# GET /api/security/policies?org_id=xxx
# Returns: { "orgName": "...", "endpoints": [{ "endpointId": "...", "securityStatus": "secure", "issueCount": 0 }] }
# Shows security status (secure/insecure) for all endpoints
@router.get("/security/policies")
async def get_policies_summary(request: Request, org_id: str) -> Dict[str, Any]:
    """
    GET /api/security/policies?org_id=...
    Returns policy summary for all endpoints in org.
    """
    service = request.app.state.service  
    return await service.get_policies_summary(org_id)

# GET /api/security/policies/{endpoint_id}?org_id=xxx
# Returns: { "orgName": "...", "endpointId": "...", "securityStatus": "insecure", "issueCount": 3 }
# Shows detailed security information for a specific endpoint
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
    return detail

# GET /api/events?org_id=xxx&limit=50
# Returns: { "orgName": "...", "totalEvents": 187, "events": [{ "eventId": "...", "eventType": "security_issue", "severity": "high" }] }
# Lists recent security and configuration events
@router.get("/events")
async def get_recent_events(request: Request, org_id: str, limit: int = 50) -> Dict[str, Any]:
    """
    GET /api/events?org_id=...&limit=50
    Returns recent events for the org.
    """
    service = request.app.state.service  
    return await service.get_recent_events(org_id, limit)

# GET /api/security/private-data?org_id=xxx
# Returns: { "orgName": "...", "endpoints": [{ "endpointId": "...", "hasPrivateData": true, "dataTypes": ["SSN", "credit-card"] }] }
# Shows which endpoints contain sensitive private data (SSN, credit cards, etc.)
@router.get("/security/private-data")
async def get_private_data_summary(request: Request, org_id: str) -> Dict[str, Any]:
    """
    GET /api/security/private-data?org_id=...
    Returns private data summary for all endpoints in org.
    """
    service = request.app.state.service  
    return await service.get_private_data_summary(org_id)

# GET /api/events/summary?org_id=xxx
# Returns: { "orgName": "...", "totalEvents": 187 }
# Shows total count of all events for the organization
@router.get("/events/summary")
async def get_events_summary(request: Request, org_id: str) -> Dict[str, Any]:
    """
    GET /api/events/summary?org_id=...
    Returns total event count for org.
    """
    service = request.app.state.service  
    return await service.get_events_count(org_id)

# GET /api/storage/size?org_id=xxx
# Returns: { "orgName": "...", "endpoints": [{ "endpointId": "...", "name": "...", "sizeGB": 505.5 }], "totalSizeGB": 505.5 }
# Shows storage size in GB for each endpoint and total
@router.get("/storage/size")
async def get_storage_sizes(request: Request, org_id: str) -> Dict[str, Any]:
    """
    GET /api/storage/size?org_id=...
    Returns storage size per endpoint.
    """
    service = request.app.state.service  
    return await service.get_storage_sizes(org_id)

# GET /api/providers?org_id=xxx
# Returns: { "orgName": "...", "providers": [{ "name": "AWS", "endpointCount": 15, "totalStorageGB": 2500.5 }] }
# Shows breakdown of cloud providers used (AWS, Azure, GCP) with endpoint count and storage
@router.get("/providers")
async def get_providers_summary(request: Request, org_id: str) -> Dict[str, Any]:
    """
    GET /api/providers?org_id=...
    Returns provider summary (count and storage per provider).
    """
    service = request.app.state.service  
    return await service.get_providers_summary(org_id)