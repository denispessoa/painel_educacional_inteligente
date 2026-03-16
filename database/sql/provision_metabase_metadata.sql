\set ON_ERROR_STOP on

SELECT format(
    'DO $do$ BEGIN
       IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = %L) THEN
         CREATE ROLE %I LOGIN PASSWORD %L;
       ELSE
         ALTER ROLE %I LOGIN PASSWORD %L;
       END IF;
     END $do$;',
    :'METABASE_DB_USER',
    :'METABASE_DB_USER',
    :'METABASE_DB_PASS',
    :'METABASE_DB_USER',
    :'METABASE_DB_PASS'
) \gexec

SELECT format(
    'CREATE DATABASE %I OWNER %I',
    :'METABASE_DB_NAME',
    :'METABASE_DB_USER'
)
WHERE NOT EXISTS (
    SELECT 1 FROM pg_database WHERE datname = :'METABASE_DB_NAME'
) \gexec

SELECT format(
    'GRANT ALL PRIVILEGES ON DATABASE %I TO %I',
    :'METABASE_DB_NAME',
    :'METABASE_DB_USER'
) \gexec
