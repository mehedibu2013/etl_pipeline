{{ config(materialized='view') }}

SELECT
  id,
  name,
  email,
  company_name  -- Already flattened, no need for JSONB accessor
FROM raw_users
WHERE email IS NOT NULL