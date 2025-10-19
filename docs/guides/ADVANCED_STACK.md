# DataMeesh - Advanced Stack Deployment Guide

## 🎯 Overview

The **Advanced Stack** adds enterprise-grade federated query capabilities to your Data Mesh platform:

```
Core Stack                    Advanced Stack
├── Sales Domain              ├── Trino (Federated SQL)
├── Marketing Domain          ├── Minio (S3 Object Storage)
├── PostgreSQL Databases      ├── Hive Metastore (Schema Registry)
└── JupyterHub                └── Custom Image (Trino CLI, tools)
```

---

## 🚀 Quick Start

### Prerequisites

1. **Core Data Mesh deployed:**
   ```bash
   python3 setup/deploy_cluster.py
   python3 setup/addons/install_helm.py
   python3 setup/addons/deploy_jupyterhub.py
   python3 setup/addons/setup_sample_data.py
   ```

2. **Verify everything is running:**
   ```bash
   kubectl get pods -A
   ```

---

### Step 1: Deploy Advanced Stack

```bash
python3 setup/addons/advanced/deploy_advanced_stack.py
```

**What it deploys:**
- ✅ **Minio**: S3-compatible object storage (10GB)
- ✅ **Hive Metastore**: Schema/metadata management
- ✅ **Hive PostgreSQL**: Metastore backend database
- ✅ **Trino Coordinator**: Query coordinator (1 replica)
- ✅ **Trino Workers**: Query workers (2 replicas)

⏱️ **Deployment time: 3-5 minutes**

---

### Step 2: Build Custom JupyterHub Image (Optional)

The custom image includes Trino CLI, MinIO CLI, and additional tools.

**On Linux/WSL:**
```bash
chmod +x setup/addons/advanced/build_custom_image.sh
./setup/addons/advanced/build_custom_image.sh
```

**On Windows (PowerShell):**
```powershell
cd setup\addons\advanced
docker build -f Dockerfile.jupyterhub -t datamesh-jupyter:latest .
```

**Then update JupyterHub** (if you built custom image):
```bash
# Edit setup/addons/jupyterhub-values.yaml
# Change:
#   singleuser:
#     image:
#       name: datamesh-jupyter
#       tag: latest

# Upgrade JupyterHub
helm upgrade jupyterhub jupyterhub/jupyterhub \
  -n jupyterhub \
  --values setup/addons/jupyterhub-values.yaml
```

---

## 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Trino Web UI** | http://localhost:30808 | No auth |
| **Minio Console** | http://localhost:30901 | minioadmin / minioadmin |
| **Minio API** | http://localhost:30900 | minioadmin / minioadmin |
| **JupyterHub** | http://localhost:30080 | admin / datamesh2024 |

---

## 📊 Using Trino for Federated Queries

### From JupyterHub Notebook

```python
from trino.dbapi import connect
import pandas as pd

# Connect to Trino
conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin'
)

# Federated query across Sales + Marketing domains!
query = """
SELECT 
    c.customer_name,
    c.lifetime_value,
    c.country,
    l.lead_source,
    l.campaign_name,
    l.lead_score
FROM sales.sales_db.customers c
INNER JOIN marketing.marketing_db.leads l 
    ON c.email = l.email
WHERE l.status = 'Converted'
ORDER BY c.lifetime_value DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)
print(df)
```

### From Trino CLI

```bash
# In JupyterHub terminal (if custom image) or any pod with Trino CLI
trino --server http://trino-coordinator.data-platform.svc.cluster.local:8080

# Show available data sources
trino> SHOW CATALOGS;

# Explore Sales domain
trino> SHOW SCHEMAS FROM sales;
trino> SHOW TABLES FROM sales.sales_db;

# Run federated query
trino> SELECT 
    s.customer_name,
    m.lead_source,
    COUNT(*) as order_count
FROM sales.sales_db.customers s
JOIN marketing.marketing_db.leads m ON s.email = m.email
WHERE m.status = 'Converted'
GROUP BY s.customer_name, m.lead_source;
```

---

## 📁 Working with Minio (S3 Storage)

### Upload Data to Minio

**Method 1: MinIO Console (Web UI)**
1. Open: http://localhost:30901
2. Login: minioadmin / minioadmin
3. Navigate to buckets: `sales-data`, `marketing-data`, `data-lake`
4. Upload CSV/Parquet files

**Method 2: From JupyterHub (if custom image)**
```bash
# Configure mc client
mc alias set minio http://minio.data-platform.svc.cluster.local:9000 minioadmin minioadmin

# List buckets
mc ls minio/

# Upload file
mc cp mydata.csv minio/data-lake/mydata.csv

# Download file
mc cp minio/data-lake/mydata.csv ./local-copy.csv
```

**Method 3: Python (boto3)**
```python
import boto3
import pandas as pd

# Configure S3 client for Minio
s3_client = boto3.client(
    's3',
    endpoint_url='http://minio.data-platform.svc.cluster.local:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

# Upload DataFrame as CSV
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
csv_buffer = df.to_csv(index=False)
s3_client.put_object(
    Bucket='data-lake',
    Key='test/mydata.csv',
    Body=csv_buffer
)

# Read CSV from Minio
obj = s3_client.get_object(Bucket='data-lake', Key='test/mydata.csv')
df = pd.read_csv(obj['Body'])
```

---

## 🗄️ Creating Tables in Hive/Trino

### Create Schema

```sql
CREATE SCHEMA IF NOT EXISTS hive.sales_reports
WITH (location = 's3a://sales-data/reports/');
```

### Create External Table (CSV)

```sql
CREATE TABLE hive.sales_reports.daily_summary (
    report_date DATE,
    region VARCHAR,
    total_orders INTEGER,
    total_revenue DECIMAL(12,2)
)
WITH (
    external_location = 's3a://sales-data/reports/daily/',
    format = 'CSV',
    csv_separator = ',',
    skip_header_line_count = 1
);
```

### Create External Table (Parquet)

```sql
CREATE TABLE hive.data_lake.customer_360 (
    customer_id INTEGER,
    customer_name VARCHAR,
    lifetime_value DECIMAL(12,2),
    lead_source VARCHAR,
    country VARCHAR
)
WITH (
    external_location = 's3a://data-lake/customer_360/',
    format = 'PARQUET'
);
```

### Export Query Results to S3

```sql
-- Create table and export data in one step
CREATE TABLE hive.data_lake.high_value_customers
WITH (
    external_location = 's3a://data-lake/analytics/high_value/',
    format = 'PARQUET'
)
AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value
FROM sales.sales_db.customers c
LEFT JOIN sales.sales_db.orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email, c.country
HAVING SUM(o.total_amount) > 100000;
```

---

## 🎓 Available Trino Catalogs

| Catalog | Type | Description | Example |
|---------|------|-------------|---------|
| **sales** | PostgreSQL | Sales domain database | `sales.sales_db.customers` |
| **marketing** | PostgreSQL | Marketing domain database | `marketing.marketing_db.campaigns` |
| **hive** | Hive/S3 | Data lake on Minio | `hive.data_lake.analytics` |
| **system** | System | Trino metadata | `system.runtime.queries` |

---

## 🔥 Advanced Use Cases

### 1. **Cross-Domain Analytics Dashboard**

```python
import pandas as pd
from trino.dbapi import connect
import matplotlib.pyplot as plt

conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin'
)

# Get cross-domain KPIs
kpi_query = """
SELECT 
    DATE_TRUNC('month', o.order_date) as month,
    COUNT(DISTINCT o.customer_id) as customers,
    COUNT(o.order_id) as orders,
    SUM(o.total_amount) as revenue,
    (SELECT SUM(spent) 
     FROM marketing.marketing_db.campaigns 
     WHERE DATE_TRUNC('month', start_date) = DATE_TRUNC('month', o.order_date)) as marketing_spend
FROM sales.sales_db.orders o
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month
"""

df = pd.read_sql(kpi_query, conn)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].plot(df['month'], df['revenue']/1000)
axes[0, 0].set_title('Revenue Over Time ($K)')

axes[0, 1].plot(df['month'], df['customers'])
axes[0, 1].set_title('Unique Customers')

axes[1, 0].plot(df['month'], df['orders'])
axes[1, 0].set_title('Total Orders')

axes[1, 1].plot(df['month'], df['marketing_spend']/1000)
axes[1, 1].set_title('Marketing Spend ($K)')

plt.tight_layout()
plt.show()
```

### 2. **Real-time Data Pipeline**

```python
# Extract from multiple sources
sales_df = pd.read_sql(
    "SELECT * FROM sales.sales_db.orders WHERE order_date = CURRENT_DATE",
    conn
)

# Transform
sales_df['profit'] = sales_df['total_amount'] * 0.3

# Load to S3/Minio via Trino
from sqlalchemy import create_engine

trino_engine = create_engine(
    'trino://admin@trino-coordinator.data-platform.svc.cluster.local:8080/hive/data_lake'
)

sales_df.to_sql('daily_orders', trino_engine, if_exists='append', index=False)
```

### 3. **Data Quality Checks**

```sql
-- Check for data quality issues across domains
WITH quality_checks AS (
    SELECT 
        'Sales - Null Emails' as check_name,
        COUNT(*) as issue_count
    FROM sales.sales_db.customers
    WHERE email IS NULL
    
    UNION ALL
    
    SELECT 
        'Marketing - Orphan Leads',
        COUNT(*)
    FROM marketing.marketing_db.leads l
    LEFT JOIN sales.sales_db.customers c ON l.email = c.email
    WHERE c.customer_id IS NULL AND l.status = 'Converted'
    
    UNION ALL
    
    SELECT 
        'Sales - Orders Without Items',
        COUNT(*)
    FROM sales.sales_db.orders o
    LEFT JOIN sales.sales_db.order_items oi ON o.order_id = oi.order_id
    WHERE oi.item_id IS NULL
)
SELECT * FROM quality_checks
WHERE issue_count > 0;
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER (Data Scientist)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  JupyterHub  │
                  │  (Trino CLI) │
                  └──────┬───────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Trino Coordinator    │
            │  (Query Planning)      │
            └────────┬───────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Worker │  │ Worker │  │ Worker │
    │   1    │  │   2    │  │   N    │
    └───┬────┘  └───┬────┘  └───┬────┘
        │           │           │
        ▼           ▼           ▼
    ┌───────────────────────────────┐
    │      Data Sources             │
    ├───────────┬──────────┬────────┤
    │   Sales   │Marketing │  Hive  │
    │PostgreSQL │PostgreSQL│ (S3)   │
    └───────────┴──────────┴────────┘
```

---

## 🛠️ Troubleshooting

### Check Trino Status

```bash
kubectl get pods -n data-platform
kubectl logs -n data-platform -l app=trino,component=coordinator --tail=50
```

### Test Connectivity

```bash
# From JupyterHub terminal
curl http://trino-coordinator.data-platform.svc.cluster.local:8080/v1/info
```

### View Trino Logs

```bash
kubectl logs -n data-platform <trino-coordinator-pod> --tail=100
```

### Check Hive Metastore

```bash
kubectl logs -n data-platform -l app=hive-metastore --tail=50
```

### Reset Everything

```bash
# Delete advanced stack
kubectl delete -f config/minio-trino-hive.yaml

# Redeploy
python3 setup/addons/advanced/deploy_advanced_stack.py
```

---

## 📚 Documentation

- **Trino Guide**: `setup/addons/advanced/TRINO_GUIDE.md`
- **Sample Data**: `DATA_MODEL.md`
- **Core Setup**: `README.md`

---

## ✨ Summary

You now have a **production-grade federated query engine** that:

✅ Queries multiple PostgreSQL databases with ONE SQL statement  
✅ Accesses S3/Minio object storage  
✅ Manages schemas with Hive Metastore  
✅ Provides standard SQL interface (ANSI SQL)  
✅ Scales horizontally (add more workers)  
✅ Integrates with BI tools (Tableau, PowerBI, Grafana)  

**This is the architecture used by Netflix, LinkedIn, Uber, and other tech giants!** 🚀

---

**Ready to query?** See `setup/addons/advanced/TRINO_GUIDE.md` for examples!

