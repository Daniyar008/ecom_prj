# ================================
# Docker PostgreSQL Initialization
# ================================
# Этот скрипт выполняется при первом запуске PostgreSQL

-- Создание базы данных (если еще не создана)
SELECT 'CREATE DATABASE ecomprj_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ecomprj_db')\gexec

-- Создание расширений
\c ecomprj_db;

-- UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Full text search
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Geo support (если нужно для location features)
CREATE EXTENSION IF NOT EXISTS "postgis" CASCADE;

-- Вывод информации
\echo '✅ PostgreSQL initialization completed!'
\echo 'Database: ecomprj_db'
\echo 'Extensions: uuid-ossp, pg_trgm, postgis'
