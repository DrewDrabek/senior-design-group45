# This is the dac class that manages and creates connections to the database

# before you do this you need to make sure that you have the connection information for the database
# Make sure that local database or remote database if we end up having to use one is up and running
# If it is hosted somewhere make sure that we can access it from laptop via network
# In the connection string need to include the username, password, host, port, and database name in the format:
# postgresql+asyncpg://username:password@host:port/database_name - this needs to be tested just got from documentation
# I added in type hints

from typing import Any, Dict, List, Optional
import json
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

class Sql_Alc_DAC:

    # This is just the constructor for the class. This gets called anytime the class is called and then the options that are passed are used to create the attributes for the class
    # for example the creation an object would be - 
    # dac = sql_Alc_DAC(database_url="postgresql+asyncpg://username:password@host:port/database_name", echo=True)
    # The engine is set to none since in the methods on the class check if is none and do certain things
    # Here is a good example and where I found a lot of the ideas for this class - https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html
    # Please note that this example creates a database if there is not one - we are not doing that here I am just assuming that the db exists where needed
    # the methods might not be the best way to do this either 

    def __init__(self, database_url: str, echo: bool = False):
        self.database_url = database_url
        self.echo = echo
        self._engine: Optional[AsyncEngine] = None 

    # This is the method that creates the connection
    # This is an example of why the engine is set to none at first in the constructor 

    # This is the connection method and this should be run on the startup of the fastapi app

    async def connect(self):
        if self._engine is None:
            self._engine = create_async_engine(self.database_url, echo=self.echo)

    # This is the disconnect method for the db connection and will called when the app is shutting down to clean up the connection that is made earlier on startup

    async def disconnect(self):
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None

    # This is a helper method that we can use to call a sql query and then return the result it is easier doing this then having to write the same code over and over
    # params here is a dictionary of params that can be passes to the query to be used 
    # sql is the sql query that is being ran
    async def query(self, sql_query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        async with AsyncSession(self._engine) as session:
            async with session.begin():
                result = await session.execute(text(sql_query), params or {})
                return [dict(r) for r in result.mappings().all()]

    # These now just run the querys for the database using the query method
    async def get_endpoints_for_org(self, org_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT endpoint_id, provider, name, region, storage_bytes,
               ROUND((storage_bytes::numeric / 1024 / 1024 / 1024)::numeric, 3) AS storage_gb,
               credentials_arn, onboarded_at, last_scanned_at
        FROM endpoints
        WHERE org_id = :org_id
        ORDER BY name;
        """
        return await self.query(sql, {"org_id": org_id})
    
    async def create_endpoint(self, org_id: str, provider: str, name: str, region: Optional[str], credentials_arn: Optional[str]) -> Dict[str, Any]:
        sql = """
        INSERT INTO endpoints (org_id, provider, name, region, credentials_arn, onboarded_at)
        VALUES (:org_id, :provider, :name, :region, :credentials_arn, now())
        RETURNING endpoint_id, org_id, provider, name, region, storage_bytes, onboarded_at, last_scanned_at;
        """
        result = await self.query(sql, {
            "org_id": org_id,
            "provider": provider,
            "name": name,
            "region": region,
            "credentials_arn": credentials_arn,
        })
        return result[0] if result else {}

    async def delete_endpoint(self, endpoint_id: str, org_id: str) -> bool:
        sql = "DELETE FROM endpoints WHERE endpoint_id = :endpoint_id AND org_id = :org_id RETURNING endpoint_id;"
        result = await self.query(sql, {"endpoint_id": endpoint_id, "org_id": org_id})
        return bool(result)


    async def get_policies_summary(self, org_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT e.endpoint_id, e.name, e.provider,
               COALESCE(p.security_status, 'unknown') AS security_status,
               COALESCE(p.issue_count, 0) AS issue_count,
               p.last_scanned_at
        FROM endpoints e
        LEFT JOIN policies p ON p.endpoint_id = e.endpoint_id
        WHERE e.org_id = :org_id
        ORDER BY e.name;
        """
        return await self.query(sql, {"org_id": org_id})

    async def get_policy_detail(self, endpoint_id: str, org_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT e.endpoint_id, e.provider, e.name, p.security_status, p.issue_count, p.last_scanned_at
        FROM endpoints e
        LEFT JOIN policies p ON p.endpoint_id = e.endpoint_id
        WHERE e.endpoint_id = :endpoint_id AND e.org_id = :org_id;
        """
        return await self.query(sql, {"endpoint_id": endpoint_id, "org_id": org_id})

    async def get_private_data_summary(self, org_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT e.endpoint_id, e.name, e.provider,
               COALESCE(pd.has_private, false) AS has_private,
               COALESCE(pd.data_types, '[]'::jsonb) AS data_types,
               pd.found_at
        FROM endpoints e
        LEFT JOIN private_data pd ON pd.endpoint_id = e.endpoint_id
        WHERE e.org_id = :org_id
        ORDER BY e.name;
        """
        return await self.query(sql, {"org_id": org_id})

    async def get_events_count(self, org_id: str) -> int:
        sql = "SELECT COUNT(*)::int AS total_events FROM events WHERE org_id = :org_id;"
        row = await self.query(sql, {"org_id": org_id})
        return int(row[0]["total_events"]) if row and "total_events" in row[0] else 0

    async def get_recent_events(self, org_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        sql = """
        SELECT event_id, endpoint_id, event_type, severity, description, found_at
        FROM events
        WHERE org_id = :org_id
        ORDER BY found_at DESC
        LIMIT :limit;
        """
        return await self.query(sql, {"org_id": org_id, "limit": limit})

    async def get_storage_sizes(self, org_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT endpoint_id, name, provider, storage_bytes,
               ROUND((storage_bytes::numeric / 1024 / 1024 / 1024)::numeric, 3) AS size_gb,
               last_scanned_at
        FROM endpoints
        WHERE org_id = :org_id
        ORDER BY storage_bytes DESC;
        """
        return await self.query(sql, {"org_id": org_id})

    async def get_total_storage(self, org_id: str) -> Dict[str, Any]:
        sql = """
        SELECT COALESCE(SUM(storage_bytes), 0) AS total_size_bytes,
               ROUND((COALESCE(SUM(storage_bytes),0)::numeric / 1024 / 1024 / 1024)::numeric, 3) AS total_size_gb
        FROM endpoints
        WHERE org_id = :org_id;
        """
        result = await self.query(sql, {"org_id": org_id})
        return result[0] if result else {"total_size_bytes": 0, "total_size_gb": 0.0}

    async def get_providers_summary(self, org_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT provider,
               COUNT(*) AS endpoint_count,
               COALESCE(SUM(storage_bytes), 0) AS total_storage_bytes,
               ROUND((COALESCE(SUM(storage_bytes),0)::numeric / 1024 / 1024 / 1024)::numeric, 3) AS total_storage_gb
        FROM endpoints
        WHERE org_id = :org_id
        GROUP BY provider
        ORDER BY endpoint_count DESC;
        """
        return await self.query(sql, {"org_id": org_id})

    async def insert_policy(self, endpoint_id: str, security_status: str, issue_count: int) -> None:
        sql = """
        INSERT INTO policies (policy_id, endpoint_id, security_status, issue_count, last_scanned_at)
        VALUES (uuidv7(), :endpoint_id, :security_status, :issue_count, now())
        ON CONFLICT (endpoint_id) DO UPDATE
          SET security_status = EXCLUDED.security_status,
              issue_count = EXCLUDED.issue_count,
              last_scanned_at = EXCLUDED.last_scanned_at;
        """
        await self.query(sql, {"endpoint_id": endpoint_id, "security_status": security_status, "issue_count": issue_count})

    async def insert_private_data(self, endpoint_id: str, has_private: bool, data_types: List[str]) -> None:
        sql = """
        INSERT INTO private_data (private_id, endpoint_id, has_private, data_types, found_at)
        VALUES (uuidv7(), :endpoint_id, :has_private, :data_types::jsonb, now())
        ON CONFLICT (endpoint_id) DO UPDATE
          SET has_private = EXCLUDED.has_private,
              data_types = EXCLUDED.data_types,
              found_at = EXCLUDED.found_at;
        """
        await self.query(sql, {"endpoint_id": endpoint_id, "has_private": has_private, "data_types": json.dumps(data_types)})

    async def insert_event(self, endpoint_id: str, org_id: str, event_type: str, description: str, severity: str) -> Dict[str, Any]:
        sql = """
        INSERT INTO events (event_id, endpoint_id, org_id, event_type, description, severity, found_at)
        VALUES (uuidv7(), :endpoint_id, :org_id, :event_type, :description, :severity, now())
        RETURNING event_id, found_at;
        """
        result = await self.query(sql, {"endpoint_id": endpoint_id, "org_id": org_id, "event_type": event_type, "description": description, "severity": severity})
        return result[0] if result else {}

    async def update_endpoint_storage(self, endpoint_id: str, storage_bytes: int) -> Dict[str, Any]:
        sql = """
        UPDATE endpoints
        SET storage_bytes = :storage_bytes, last_scanned_at = now()
        WHERE endpoint_id = :endpoint_id
        RETURNING endpoint_id, storage_bytes, last_scanned_at;
        """
        result = await self.query(sql, {"endpoint_id": endpoint_id, "storage_bytes": storage_bytes})
        return result[0] if result else {}
