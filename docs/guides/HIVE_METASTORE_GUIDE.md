# 🗂️ Hive Metastore Guide

**Understanding Hive Metastore in the DataMeesh Platform**

---

## 📋 What is Hive Metastore?

**Hive Metastore** is a centralized metadata repository that stores information about:
- Table schemas (columns, data types)
- Partition information
- Storage locations (in Minio S3)
- File formats (Parquet, ORC, CSV, JSON)

Think of it as a **catalog** for your data lake.

---

## 🎯 Why Do We Need It?

Without Hive Metastore:
```
❌ Query engine doesn't know what tables exist
❌ No schema information for data lake files
❌ Can't query Minio/S3 like a database
```

With Hive Metastore:
```
✅ Trino knows all available tables
✅ Schema is managed and versioned
✅ Query Minio/S3 with standard SQL
✅ Metadata survives data lake changes
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│            TRINO QUERY ENGINE               │
│  SELECT * FROM hive.default.customer_events │
└────────────────┬────────────────────────────┘
                 │
                 ▼
         ┌──────────────┐
         │     HIVE     │
         │  METASTORE   │  ← Stores table metadata
         │   Port 9083  │
         └──────┬───────┘
                │
      ┌─────────┴─────────┐
      ▼                   ▼
┌─────────────┐     ┌──────────┐
│    MINIO    │     │  HIVE    │
│  (Storage)  │     │PostgreSQL│
│             │     │(Metadata)│
└─────────────┘     └──────────┘
```

### Components:

1. **Hive PostgreSQL**
   - Stores metadata (table definitions)
   - Database: `metastore`
   - User: `hive` / `hivepassword`

2. **Hive Metastore Service**
   - Listens on port 9083 (Thrift)
   - Manages metadata operations
   - Connects to Hive PostgreSQL

3. **Minio**
   - Stores actual data files
   - S3-compatible API
   - Connected via Hive Metastore

---

## 🔌 How Trino Uses It

### Trino Catalog Configuration

In `config/minio-trino-hive.yaml`, Trino is configured with a `hive` catalog:

```properties
connector.name=hive
hive.metastore.uri=thrift://hive-metastore:9083
hive.s3.endpoint=http://minio:9000
hive.s3.path-style-access=true
hive.s3.aws-access-key=minioadmin
hive.s3.aws-secret-key=minioadmin
hive.non-managed-table-writes-enabled=true
```

### Query Flow

```sql
-- User runs query in Trino
SELECT * FROM hive.default.customer_events;
```

**What happens:**
1. Trino asks Hive Metastore: "Where is `customer_events`?"
2. Metastore replies: "s3://datalake/customer_events/"
3. Trino reads files from Minio at that location
4. Trino applies schema from Metastore
5. Returns results to user

---

## 📊 Example Use Cases

### 1. Store Raw Event Data

```sql
-- Create external table pointing to Minio
CREATE TABLE hive.default.customer_events (
    event_id VARCHAR,
    customer_id VARCHAR,
    event_type VARCHAR,
    event_date DATE,
    event_data VARCHAR
)
WITH (
    external_location = 's3a://datalake/events/',
    format = 'PARQUET'
);
```

### 2. Query Data Lake

```sql
-- Query Minio data via Hive
SELECT 
    event_type,
    COUNT(*) as event_count
FROM hive.default.customer_events
WHERE event_date = CURRENT_DATE
GROUP BY event_type;
```

### 3. Cross-Domain with Data Lake

```sql
-- Join Sales PostgreSQL with Data Lake
SELECT 
    c.customer_name,
    e.event_type,
    COUNT(*) as event_count
FROM sales.public.customers c
JOIN hive.default.customer_events e 
    ON c.customer_id = e.customer_id
GROUP BY 1, 2;
```

---

## 🔧 Verify Hive is Running

```bash
# Check Hive pods
kubectl get pods -n data-platform | grep hive

# Expected:
# hive-postgres-0       1/1   Running
# hive-metastore-xxxxx  1/1   Running

# Check Hive service
kubectl get svc -n data-platform hive-metastore

# Test connection (from JupyterHub)
from trino.dbapi import connect

conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin',
    catalog='hive',
    schema='default'
)

cursor = conn.cursor()
cursor.execute("SHOW SCHEMAS")
print(cursor.fetchall())
```

---

## 🐛 Troubleshooting

### Issue: "Hive metastore connection failed"

**Solution:**
```bash
# Check Hive Metastore logs
kubectl logs -n data-platform <hive-metastore-pod>

# Restart Hive Metastore
kubectl delete pod -n data-platform <hive-metastore-pod>
```

### Issue: "Cannot connect to Hive PostgreSQL"

**Solution:**
```bash
# Check Hive PostgreSQL
kubectl get pods -n data-platform hive-postgres-0

# Test connection
kubectl exec -it -n data-platform hive-postgres-0 -- psql -U hive -d metastore
```

### Issue: "Table not found in Hive catalog"

**Solution:**
```sql
-- List available schemas
SHOW SCHEMAS FROM hive;

-- List tables in default schema
SHOW TABLES FROM hive.default;

-- Create schema if needed
CREATE SCHEMA IF NOT EXISTS hive.default;
```

---

## 📚 Common Operations

### Create Database/Schema

```sql
CREATE SCHEMA IF NOT EXISTS hive.analytics;
```

### Create External Table

```sql
CREATE TABLE hive.analytics.sales_data (
    order_id BIGINT,
    customer_id BIGINT,
    total_amount DOUBLE,
    order_date DATE
)
WITH (
    external_location = 's3a://datalake/sales/',
    format = 'PARQUET'
);
```

### Insert Data

```sql
-- Copy from Sales PostgreSQL to Data Lake
INSERT INTO hive.analytics.sales_data
SELECT 
    order_id,
    customer_id,
    total_amount,
    order_date
FROM sales.public.orders;
```

### Drop Table

```sql
-- Drop table (keeps data in Minio)
DROP TABLE hive.analytics.sales_data;
```

---

## 🎓 Key Concepts

### Managed vs External Tables

**Managed Tables:**
- Hive controls both metadata AND data
- `DROP TABLE` deletes metadata + data

**External Tables:**
- Hive controls only metadata
- `DROP TABLE` deletes only metadata
- Data remains in Minio

### Partitioning

```sql
CREATE TABLE hive.default.events_partitioned (
    event_id VARCHAR,
    event_type VARCHAR
)
WITH (
    external_location = 's3a://datalake/events/',
    format = 'PARQUET',
    partitioned_by = ARRAY['event_date']
);
```

---

## 🌐 Access Points

| Component | Endpoint | Protocol |
|-----------|----------|----------|
| Hive Metastore | `hive-metastore:9083` | Thrift |
| Hive PostgreSQL | `hive-postgres:5432` | PostgreSQL |
| Minio API | `minio:9000` | S3 |
| Trino Hive Catalog | `trino-coordinator:8080` | HTTP/SQL |

---

## 📖 Resources

- [Apache Hive Documentation](https://hive.apache.org/)
- [Trino Hive Connector](https://trino.io/docs/current/connector/hive.html)
- [Minio Documentation](https://min.io/docs/)

---

## 🎯 Summary

**Hive Metastore is essential for:**
- ✅ Querying data lake (Minio) with SQL
- ✅ Managing table schemas and metadata
- ✅ Enabling Trino to access S3-compatible storage
- ✅ Providing a unified view of structured and unstructured data

**Without it:** Minio is just file storage  
**With it:** Minio becomes a queryable data lake! 🚀

---

**Ready to explore your data lake?**

```sql
-- Start querying!
SELECT * FROM hive.default.your_table LIMIT 10;
```

