# SQL Notes

This where notes on the sql side of thing will go. This will be things like sql scripts and so on. This needs to include information about where the DB is going to live and how, if needed, we can restart the database somewhere new.


Go through and document each one and figure out all of the operations and make sure that his covers the minium

## Table strucuture

```sql
-- organizations information here just stores what we need to store about the org
CREATE TABLE organizations (
  org_id UUID PRIMARY KEY DEFAULT uuidv7(),
  org_name TEXT NOT NULL UNIQUE,
  join_date DATE DEFAULT CURRENT_DATE
);

-- endpoints, this is the information for the endpoint. I think we should just store the arn for the secrets from like secret manager and then we can pull them in. This would be a cred store we manage.
CREATE TABLE endpoints (
  endpoint_id UUID PRIMARY KEY DEFAULT uuidv7(),
  org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
  provider TEXT NOT NULL, -- this will be azure, aws, or google but cleaning for this will happen on bussinesse logic              
  name TEXT NOT NULL,
  region TEXT,
  storage_bytes BIGINT DEFAULT 0 NOT NULL,
  credentials_arn TEXT,                 
  onboarded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_scanned_at TIMESTAMPTZ,
  CONSTRAINT uq_endpoint_per_org UNIQUE (org_id, provider, name) -- this prevents us from getting duplicates
);

-- policy information - we dont actually need to store the policy just what we find
CREATE TABLE policies (
  policy_id UUID PRIMARY KEY DEFAULT uuidv7(),
  endpoint_id UUID NOT NULL REFERENCES endpoints(endpoint_id) ON DELETE CASCADE,
  security_status TEXT DEFAULT 'unknown', -- secure, insecure, unknown this will be clean on business logic as well 
  issue_count INT DEFAULT 0,
  last_scanned_at TIMESTAMPTZ,
  CONSTRAINT uq_policy_per_endpoint UNIQUE (endpoint_id)
);

-- private data found table we might not need this was just writing out the database had this - cant remember why at this point. The events table might cover every we need there.
CREATE TABLE private_data (
  private_id UUID PRIMARY KEY DEFAULT uuidv7(),
  endpoint_id UUID NOT NULL REFERENCES endpoints(endpoint_id) ON DELETE CASCADE,
  has_private BOOLEAN NOT NULL DEFAULT false,
  data_types JSONB DEFAULT '[]'::jsonb,
  found_at TIMESTAMPTZ,
  CONSTRAINT uq_privatedata_per_endpoint UNIQUE (endpoint_id)
);

-- events table 
CREATE TABLE events (
  event_id UUID PRIMARY KEY DEFAULT uuidv7(),
  endpoint_id UUID REFERENCES endpoints(endpoint_id) ON DELETE SET NULL,
  org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  description TEXT,
  severity TEXT DEFAULT 'low',
  found_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

```sql


-- These are just the queries cleaned up so that we can test them these dont need to be stored in the db they are stored in the dac and then ran there

GET /api/endpoints

Params: $1 = org_id (UUID)

SELECT endpoint_id,
       provider,
       name,
       region,
       storage_bytes,
       ROUND((storage_bytes::numeric / 1024 / 1024 / 1024)::numeric, 3) AS storage_gb,
       credentials_arn,
       onboarded_at,
       last_scanned_at
FROM endpoints
WHERE org_id = $1
ORDER BY name;


POST /api/endpoints

Params: $1 = org_id, $2 = provider, $3 = name, $4 = region, $5 = credentials_arn


INSERT INTO endpoints (org_id, provider, name, region, credentials_arn, onboarded_at)
VALUES ($1, $2, $3, $4, $5, now())
RETURNING endpoint_id, org_id, provider, name, region, storage_bytes, onboarded_at, last_scanned_at;

DELETE /api/endpoints/{endpointId}

Params: $1 = endpoint_id, $2 = org_id

DELETE /api/endpoints/{endpointId}
DELETE FROM endpoints
WHERE endpoint_id = $1 AND org_id = $2
RETURNING endpoint_id;

GET /api/security/policies

SELECT e.endpoint_id,
       e.name,
       e.provider,
       COALESCE(p.security_status, 'unknown') AS security_status,
       COALESCE(p.issue_count, 0) AS issue_count,
       p.last_scanned_at
FROM endpoints e
LEFT JOIN policies p ON p.endpoint_id = e.endpoint_id
WHERE e.org_id = $1
ORDER BY e.name;

GET /api/security/policies/{endpointId}
Params: $1 = endpoint_id, $2 = org_id

SELECT e.endpoint_id,
       e.provider,
       e.name,
       p.security_status,
       p.issue_count,
       p.last_scanned_at
FROM endpoints e
LEFT JOIN policies p ON p.endpoint_id = e.endpoint_id
WHERE e.endpoint_id = $1 AND e.org_id = $2;


GET /api/security/private-data
Params: $1 = org_id


SELECT e.endpoint_id,
       e.name,
       e.provider,
       COALESCE(pd.has_private, false) AS has_private,
       COALESCE(pd.data_types, '[]'::jsonb) AS data_types,
       pd.found_at
FROM endpoints e
LEFT JOIN private_data pd ON pd.endpoint_id = e.endpoint_id
WHERE e.org_id = $1
ORDER BY e.name;

GET /api/events/summary
Params: $1 = org_id
SELECT COUNT(*) AS total_events
FROM events ev
WHERE ev.org_id = $1;

GET /api/storage/size
params: $1 = org_id

SELECT endpoint_id,
       name,
       provider,
       storage_bytes,
       ROUND((storage_bytes::numeric / 1024 / 1024 / 1024)::numeric, 3) AS size_gb,
       last_scanned_at
FROM endpoints
WHERE org_id = $1
ORDER BY storage_bytes DESC;

GET /api/providers

Params: $1 = org_id

SELECT provider,
       COUNT(*) AS endpoint_count,
       COALESCE(SUM(storage_bytes), 0) AS total_storage_bytes,
       ROUND((COALESCE(SUM(storage_bytes),0)::numeric / 1024 / 1024 / 1024)::numeric, 3) AS total_storage_gb
FROM endpoints
WHERE org_id = $1
GROUP BY provider
ORDER BY endpoint_count DESC;

```