# Creating the service layer - there is not going to be any business logic here yet

# There will need to be a dac object that is passed into the service layer

# This is what will allow it to call the dac - Will need to be tested as I do not know if that is correct

from typing import Any, Dict, List, Optional
from app.database.sqlalc_dac import Sql_Alc_DAC


class Services:

    def __init__(self, dac: Sql_Alc_DAC):
        self.dac = dac

    # Gets all endpoints for an org and formats as JSON with org name and total count
    async def get_endpoints_for_org(self, org_id: str) -> Dict[str, Any]:
        """Returns formatted endpoint list with org name and total count."""
        org_name = await self.dac.get_org_name(org_id)
        endpoints = await self.dac.get_endpoints_for_org(org_id)
        
        # Format endpoints to match expected structure
        formatted_endpoints = [
            {
                "endpointId": str(ep.get("endpoint_id")),
                "provider": ep.get("provider"),
                "name": ep.get("name"),
                "region": ep.get("region")
            }
            for ep in endpoints
        ]
        
        return {
            "orgName": org_name,
            "endpoints": formatted_endpoints,
            "totalEndpoints": len(formatted_endpoints)
        }
    
    # Creates a new storage endpoint and returns formatted response with org name
    async def create_endpoint(self, org_id: str, provider: str, name: str, region: Optional[str], credentials_arn: Optional[str]) -> Dict[str, Any]:
        """Creates endpoint and returns formatted response."""
        org_name = await self.dac.get_org_name(org_id)
        result = await self.dac.create_endpoint(org_id, provider, name, region, credentials_arn)
        
        return {
            "orgName": org_name,
            "endpointId": str(result.get("endpoint_id")),
            "provider": result.get("provider"),
            "name": result.get("name"),
            "region": result.get("region"),
            "onboardedAt": result.get("onboarded_at").isoformat() if result.get("onboarded_at") else None
        }
    
    # Deletes an endpoint - returns True if successful, False if not found
    async def delete_endpoint(self, endpoint_id: str, org_id: str) -> bool:
        return await self.dac.delete_endpoint(endpoint_id, org_id)

    # Gets security status for all endpoints (secure/insecure) and formats as JSON
    async def get_policies_summary(self, org_id: str) -> Dict[str, Any]:
        """Returns formatted security policies summary."""
        org_name = await self.dac.get_org_name(org_id)
        policies = await self.dac.get_policies_summary(org_id)
        
        formatted_endpoints = [
            {
                "endpointId": str(p.get("endpoint_id")),
                "name": p.get("name"),
                "provider": p.get("provider"),
                "securityStatus": p.get("security_status"),
                "issueCount": p.get("issue_count")
            }
            for p in policies
        ]
        
        return {
            "orgName": org_name,
            "endpoints": formatted_endpoints
        }

    # Gets detailed security info for a specific endpoint
    async def get_policy_detail(self, endpoint_id: str, org_id: str) -> Dict[str, Any]:
        """Returns formatted policy detail for an endpoint."""
        org_name = await self.dac.get_org_name(org_id)
        detail = await self.dac.get_policy_detail(endpoint_id, org_id)
        
        if not detail:
            return {}
        
        d = detail[0]
        return {
            "orgName": org_name,
            "endpointId": str(d.get("endpoint_id")),
            "provider": d.get("provider"),
            "name": d.get("name"),
            "securityStatus": d.get("security_status"),
            "issueCount": d.get("issue_count"),
            "lastScannedAt": d.get("last_scanned_at").isoformat() if d.get("last_scanned_at") else None
        }

    # Shows which endpoints contain sensitive private data (SSN, credit cards, etc.)
    async def get_private_data_summary(self, org_id: str) -> Dict[str, Any]:
        """Returns formatted private data summary."""
        org_name = await self.dac.get_org_name(org_id)
        data = await self.dac.get_private_data_summary(org_id)
        
        formatted_endpoints = [
            {
                "endpointId": str(d.get("endpoint_id")),
                "name": d.get("name"),
                "provider": d.get("provider"),
                "hasPrivateData": d.get("has_private"),
                "dataTypes": d.get("data_types", [])
            }
            for d in data
        ]
        
        return {
            "orgName": org_name,
            "endpoints": formatted_endpoints
        }

    # Returns total count of all security/configuration events for the org
    async def get_events_count(self, org_id: str) -> Dict[str, Any]:
        """Returns formatted events summary."""
        org_name = await self.dac.get_org_name(org_id)
        count = await self.dac.get_events_count(org_id)
        
        return {
            "orgName": org_name,
            "totalEvents": count
        }

    # Gets recent security and configuration events with full details
    async def get_recent_events(self, org_id: str, limit: int = 50) -> Dict[str, Any]:
        """Returns formatted recent events list."""
        org_name = await self.dac.get_org_name(org_id)
        events = await self.dac.get_recent_events(org_id, limit)
        
        formatted_events = [
            {
                "eventId": str(e.get("event_id")),
                "endpointId": str(e.get("endpoint_id")),
                "eventType": e.get("event_type"),
                "severity": e.get("severity"),
                "description": e.get("description"),
                "foundAt": e.get("found_at").isoformat() if e.get("found_at") else None
            }
            for e in events
        ]
        
        return {
            "orgName": org_name,
            "totalEvents": len(formatted_events),
            "events": formatted_events
        }

    # Gets storage size in GB for each endpoint plus total storage across all endpoints
    async def get_storage_sizes(self, org_id: str) -> Dict[str, Any]:
        """Returns formatted storage sizes with total."""
        org_name = await self.dac.get_org_name(org_id)
        sizes = await self.dac.get_storage_sizes(org_id)
        total = await self.dac.get_total_storage(org_id)
        
        formatted_endpoints = [
            {
                "endpointId": str(s.get("endpoint_id")),
                "name": s.get("name"),
                "provider": s.get("provider"),
                "sizeGB": float(s.get("size_gb", 0))
            }
            for s in sizes
        ]
        
        return {
            "orgName": org_name,
            "endpoints": formatted_endpoints,
            "totalSizeGB": float(total.get("total_size_gb", 0))
        }

    # Gets raw total storage data (used internally by get_storage_sizes)
    async def get_total_storage(self, org_id: str) -> Dict[str, Any]:
        return await self.dac.get_total_storage(org_id)

    # Shows breakdown of cloud providers in use (AWS, Azure, GCP) with endpoint counts and storage
    async def get_providers_summary(self, org_id: str) -> Dict[str, Any]:
        """Returns formatted providers summary."""
        org_name = await self.dac.get_org_name(org_id)
        providers = await self.dac.get_providers_summary(org_id)
        
        formatted_providers = [
            {
                "name": p.get("provider"),
                "endpointCount": p.get("endpoint_count"),
                "totalStorageGB": float(p.get("total_storage_gb", 0))
            }
            for p in providers
        ]
        
        return {
            "orgName": org_name,
            "providers": formatted_providers
        }