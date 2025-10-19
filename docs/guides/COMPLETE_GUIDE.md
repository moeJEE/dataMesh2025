# 🚀 DataMeesh - Complete Data Mesh Platform Guide

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Components](#components)
5. [DBT Workflow](#dbt-workflow)
6. [Grafana Dashboards](#grafana-dashboards)
7. [DataHub Setup](#datahub-setup)
8. [Advanced Use Cases](#advanced-use-cases)
9. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                   COMPLETE DATA MESH PLATFORM                    │
└──────────────────────────────────────────────────────────────────┘

                        👥 DATA USERS
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
  ┌──────────┐         ┌──────────┐        ┌──────────┐
  │JupyterHub│         │ Grafana  │        │  Nginx   │
  │+ DBT     │         │Dashboards│        │DBT Docs  │
  │+ Git     │         │          │        │          │
  │+Scheduler│         │          │        │          │
  └────┬─────┘         └────┬─────┘        └────┬─────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
                      ┌──────────┐
                      │  TRINO   │
                      │Federated │
                      │  Queries │
                      └─────┬────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌───────────┐       ┌───────────┐      ┌──────────┐
  │   Sales   │       │ Marketing │      │   HIVE   │
  │PostgreSQL │       │PostgreSQL │      │Metastore │
  └───────────┘       └───────────┘      └────┬─────┘
                                               │
                                         ┌─────▼─────┐
                                         │   Minio   │
                                         │Data Lake  │
                                         │    (S3)   │
                                         └───────────┘
```

---

## ✅ Prerequisites

### Already Deployed (from previous steps):
- ✅ Docker Desktop with Kubernetes enabled
- ✅ kubectl configured
- ✅ Helm installed
- ✅ Core Data Mesh (Sales + Marketing PostgreSQL)
- ✅ Trino + Minio + Hive Metastore
- ✅ JupyterHub
- ✅ Sample data loaded

### Memory Requirements:
- **Total Available**: 7.6GB
- **Currently Used**: ~6.2GB
- **Available**: ~1.4GB

---

## 🚀 Quick Start

### Step 1: Verify All Services

```powershell
# Check all pods
kubectl get pods --all-namespaces

# Expected namespaces:
# - sales-domain
# - marketing-domain
# - data-platform (Trino, Minio, Hive)
# - jupyterhub
# - monitoring (Grafana)
# - dbt-docs (Nginx)
```

### Step 2: Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **JupyterHub** | http://localhost:30080 | any username / `datamesh2024` |
| **Trino Web UI** | http://localhost:30808 | No auth |
| **Minio Console** | http://localhost:30901 | `minioadmin` / `minioadmin` |
| **Grafana** | http://localhost:30030 | `admin` / `datamesh2024` |
| **DBT Docs** | http://localhost:30082 | No auth |

---

## 🧩 Components

### 1. **Sales Domain** (`sales-domain` namespace)
- **PostgreSQL**: Customer, product, and order data
- **API**: REST API for data access
- **Data**: 15 customers, 10 products, 20 orders

### 2. **Marketing Domain** (`marketing-domain` namespace)
- **PostgreSQL**: Campaign, lead, and metrics data
- **API**: REST API for data access
- **Data**: 8 campaigns, 15 leads, performance metrics

### 3. **Data Platform** (`data-platform` namespace)
- **Trino**: Federated SQL query engine (coordinator + worker)
- **Minio**: S3-compatible object storage (data lake)
- **Hive PostgreSQL**: Metadata database
- **Hive Metastore**: Data lake metadata management (port 9083)

**Trino Catalogs:**
- `sales` → Sales PostgreSQL
- `marketing` → Marketing PostgreSQL
- `hive` → Minio data lake (via Hive Metastore)

### 4. **JupyterHub** (`jupyterhub` namespace)
- **Hub**: Multi-user notebook server
- **Extensions**: Git, Scheduler
- **Pre-installed**: DBT, psycopg2, pandas, trino-python-client

### 5. **Monitoring** (`monitoring` namespace)
- **Grafana**: Visualization and dashboards
- **Data Sources**: Sales + Marketing PostgreSQL

### 6. **DBT Docs** (`dbt-docs` namespace)
- **Nginx**: Static file server for DBT documentation

---

## 🔄 DBT Workflow

### Project Structure

```
setup/addons/dbt/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Connection profiles
└── models/
    ├── staging/
    │   ├── sales/
    │   │   ├── _sales__sources.yml
    │   │   ├── stg_sales__customers.sql
    │   │   └── stg_sales__orders.sql
    │   └── marketing/
    │       └── _marketing__sources.yml
    └── marts/
        ├── sales/
        │   └── mart_sales__customer_lifetime_value.sql
        └── cross_domain/
            └── mart_lead_to_customer_journey.sql
```

### Using DBT in JupyterHub

1. **Open JupyterHub**: http://localhost:30080
2. **Login**: any username / `datamesh2024`
3. **Open Terminal** in JupyterHub
4. **Copy DBT project**:

```bash
# In JupyterHub terminal
cp -r /path/to/dbt setup/addons/dbt ~/dbt_projects/datamesh
cd ~/dbt_projects/datamesh

# Copy profiles
cp setup/addons/dbt/profiles.yml ~/.dbt/profiles.yml
```

5. **Run DBT commands**:

```bash
# Test connection
dbt debug

# Run data quality tests
dbt test

# Build models
dbt run

# Build specific model
dbt run --select mart_sales__customer_lifetime_value

# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve --port 8001
```

### Key DBT Models

#### 1. Customer Lifetime Value
```sql
-- Location: models/marts/sales/mart_sales__customer_lifetime_value.sql
-- Purpose: Calculate CLV, segmentation, and status
-- Materialization: Incremental
-- Output: customer_id, lifetime_value, total_orders, customer_segment, customer_status
```

#### 2. Lead to Customer Journey
```sql
-- Location: models/marts/cross_domain/mart_lead_to_customer_journey.sql
-- Purpose: Track marketing leads through to sales revenue
-- Materialization: Table
-- Cross-Domain: Joins marketing.leads + sales.customers + sales.orders
-- Output: lead_id, email, is_converted, days_to_conversion, total_revenue
```

### DBT Tests

```bash
# Run all tests
dbt test

# Test specific model
dbt test --select mart_lead_to_customer_journey

# Test sources only
dbt test --select source:*
```

---

## 📊 Grafana Dashboards

### Access Grafana
- **URL**: http://localhost:30030
- **Login**: `admin` / `datamesh2024`

### Pre-configured Data Sources
1. **Sales PostgreSQL**: Connected to `sales-domain`
2. **Marketing PostgreSQL**: Connected to `marketing-domain`

### Example Queries

#### Sales Dashboard

**Revenue by Month**:
```sql
SELECT 
  to_char(order_date, 'YYYY-MM') as month,
  sum(total_amount) as revenue
FROM orders
WHERE order_date >= NOW() - INTERVAL '6 months'
GROUP BY 1
ORDER BY 1
```

**Top 10 Customers by Revenue**:
```sql
SELECT 
  c.customer_name,
  count(o.order_id) as total_orders,
  sum(o.total_amount) as lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY lifetime_value DESC
LIMIT 10
```

#### Marketing Dashboard

**Campaign Performance**:
```sql
SELECT 
  c.campaign_name,
  c.channel,
  c.budget,
  m.impressions,
  m.clicks,
  m.conversions,
  ROUND(m.clicks::numeric / NULLIF(m.impressions, 0) * 100, 2) as ctr,
  ROUND(m.conversions::numeric / NULLIF(m.clicks, 0) * 100, 2) as conversion_rate
FROM campaigns c
LEFT JOIN campaign_metrics m ON c.campaign_id = m.campaign_id
WHERE c.status IN ('active', 'completed')
ORDER BY m.conversions DESC
```

**Lead Funnel**:
```sql
SELECT 
  lead_stage,
  count(*) as total_leads,
  ROUND(avg(lead_score), 1) as avg_score
FROM leads
GROUP BY lead_stage
ORDER BY 
  CASE lead_stage
    WHEN 'new' THEN 1
    WHEN 'contacted' THEN 2
    WHEN 'qualified' THEN 3
    WHEN 'converted' THEN 4
    WHEN 'lost' THEN 5
  END
```

---

## 🗂️ DataHub Setup

DataHub provides metadata cataloging and data lineage. Due to resource constraints, we recommend running DataHub using Docker Compose **outside** of Kubernetes.

### Installation

```bash
# Install DataHub CLI
pip install acryl-datahub

# Quick start with docker-compose
datahub docker quickstart
```

This will start:
- DataHub GMS (Metadata Service)
- DataHub Frontend
- MySQL (metadata storage)
- Elasticsearch (search & graph)
- Kafka (event streaming)

**Access**: http://localhost:9002
**Login**: `datahub` / `datahub`

### Ingesting Trino Metadata

Create `trino_ingestion.yml`:

```yaml
source:
  type: trino
  config:
    host_port: "localhost:30808"
    database: sales
    username: ""  # No auth in demo
    
sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
```

Run ingestion:
```bash
datahub ingest -c trino_ingestion.yml
```

### Ingesting DBT Metadata

```bash
# In your DBT project directory
cd ~/dbt_projects/datamesh

# Generate DBT artifacts
dbt docs generate

# Create DataHub ingestion config
cat > datahub_dbt.yml << EOF
source:
  type: dbt
  config:
    manifest_path: ./target/manifest.json
    catalog_path: ./target/catalog.json
    sources_path: ./target/sources.json
    
sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
EOF

# Run ingestion
datahub ingest -c datahub_dbt.yml
```

---

## 🎯 Advanced Use Cases

### 1. Federated Queries with Trino

```sql
-- Query across Sales and Marketing
SELECT 
  s.customer_name,
  s.total_revenue,
  m.lead_source,
  m.campaign_name
FROM sales.public.customers s
JOIN marketing.public.leads m ON s.email = m.email
WHERE m.lead_stage = 'converted'
```

### 2. Incremental DBT Models

```sql
-- models/marts/sales/daily_sales_summary.sql
{{ config(
    materialized='incremental',
    unique_key='date'
) }}

SELECT 
  DATE(order_date) as date,
  COUNT(*) as total_orders,
  SUM(total_amount) as total_revenue
FROM {{ source('sales', 'orders') }}

{% if is_incremental() %}
  WHERE order_date > (SELECT MAX(date) FROM {{ this }})
{% endif %}

GROUP BY 1
```

### 3. Scheduled DBT Jobs in JupyterHub

In JupyterHub, right-click on a notebook → **Schedule**:

```python
# dbt_daily_refresh.ipynb
import subprocess
import os

os.chdir('/home/jovyan/dbt_projects/datamesh')

# Run DBT
result = subprocess.run(['dbt', 'run'], capture_output=True, text=True)
print(result.stdout)

# Run tests
result = subprocess.run(['dbt', 'test'], capture_output=True, text=True)
print(result.stdout)
```

Schedule: `0 2 * * *` (daily at 2 AM)

---

## 🔧 Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl get pods -n <namespace>

# Describe pod for events
kubectl describe pod <pod-name> -n <namespace>

# Check logs
kubectl logs <pod-name> -n <namespace>
```

### DBT Connection Issues

```bash
# Test DBT connection
dbt debug

# Common issues:
# 1. Wrong host: Use K8s service names (e.g., trino-coordinator.data-platform.svc.cluster.local)
# 2. Wrong credentials: Check profiles.yml
# 3. Network policies: Ensure namespaces can communicate
```

### Grafana Data Source Not Working

```bash
# Test PostgreSQL connection from Grafana pod
kubectl exec -it -n monitoring <grafana-pod> -- \
  psql -h sales-postgres.sales-domain.svc.cluster.local -U sales_user -d sales_db
```

### Out of Memory

```bash
# Check node resources
kubectl top nodes

# Scale down non-critical components
kubectl scale deployment trino-worker -n data-platform --replicas=0
```

---

## 📚 Additional Resources

- **DBT Documentation**: https://docs.getdbt.com/
- **Trino Documentation**: https://trino.io/docs/current/
- **DataHub Documentation**: https://datahubproject.io/docs/
- **Grafana Documentation**: https://grafana.com/docs/

---

## 🎉 What You've Built

✅ **Complete Data Mesh Platform**:
- Domain-driven data architecture
- Federated query engine (Trino)
- Data transformation framework (DBT)
- Self-service analytics (JupyterHub)
- Visualization layer (Grafana)
- Metadata catalog (DataHub)
- CI/CD for data (Git + Scheduler)

**This is a production-grade modern data platform!** 🚀

---

**Need help?** Check the logs, review configurations, or consult the official documentation for each component.

