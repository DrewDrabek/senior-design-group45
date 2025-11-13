# Creating the service layer - there is not going to be any business logic here yet

# There will need to be a dac object that is passed into the service layer

# This is what will allow it to call the dac - Will need to be tested as I do not know if that is correct

from typing import Any, Dict, List, Optional
from backend.app.database.sqlalc_dac import SQLAlchemyDAC


class Servies:

    def __init__(self, dac: SQLAlchemyDAC):
        self.dac = dac

    async def get_endpoints_for_org(self, org_id: str) -> List[Dict[str, Any]]:
        return await self.dac.get_endpoints_for_org(org_id)
    
    async def create_endpoint(self, org_id: str, provider: str, name: str, region: Optional[str], credentials_arn: Optional[str]) -> Dict[str, Any]:
        return await self.dac.create_endpoint(org_id, provider, name, region, credentials_arn)
    
    async def delete_endpoint(self, endpoint_id: str, org_id: str) -> bool:
        return await self.dac.delete_endpoint(endpoint_id, org_id)

    async def get_policies_summary(self, org_id: str) -> List[Dict[str, Any]]:
        return await self.dac.get_policies_summary(org_id)

    async def get_policy_detail(self, endpoint_id: str, org_id: str) -> List[Dict[str, Any]]:
        return await self.dac.get_policy_detail(endpoint_id, org_id)

    async def get_private_data_summary(self, org_id: str) -> List[Dict[str, Any]]:
        return await self.dac.get_private_data_summary(org_id)

    async def get_events_count(self, org_id: str) -> int:
        return await self.dac.get_events_count(org_id)

    async def get_recent_events(self, org_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.dac.get_recent_events(org_id, limit)

    async def get_storage_sizes(self, org_id: str) -> List[Dict[str, Any]]:
        return await self.dac.get_storage_sizes(org_id)

    async def get_total_storage(self, org_id: str) -> Dict[str, Any]:
        return await self.dac.get_total_storage(org_id)

    async def get_providers_summary(self, org_id: str) -> List[Dict[str, Any]]:
        return await self.dac.get_providers_summary(org_id)
    
    # these do not to be used since they are not used by the frontend - they will be used in backgroup ta

    # async def insert_policy(self, endpoint_id: str, security_status: str, issue_count: int) -> None:
    #     await self.dac.insert_policy(endpoint_id, security_status, issue_count)

    # async def insert_private_data(self, endpoint_id: str, has_private: bool, data_types: List[str]) -> None:
    #     await self.dac.insert_private_data(endpoint_id, has_private, data_types)

    # async def insert_event(self, endpoint_id: str, org_id: str, event_type: str, description: str, severity: str) -> Dict[str, Any]:
    #     return await self.dac.insert_event(endpoint_id, org_id, event_type, description, severity)

    # async def update_endpoint_storage(self, endpoint_id: str, storage_bytes: int) -> Dict[str, Any]:
    #     return await self.dac.update_endpoint_storage(endpoint_id, storage_bytes)
