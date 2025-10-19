# 🗂️ DataHub Guide - DataMeesh Platform

## 📚 Table of Contents

1. [Access DataHub](#access-datahub)
2. [Ingest Metadata](#ingest-metadata)
3. [Explore Your Data](#explore-your-data)
4. [Data Lineage](#data-lineage)
5. [Advanced Features](#advanced-features)

---

## 🌐 Access DataHub

### Login

**URL**: http://localhost:9002

```
Username: datahub
Password: datahub
```

### First Login

You'll see the DataHub home page with:
- 📊 Search bar
- 📈 Recent activity
- 👥 Popular datasets
- 🔍 Browse by platform

---

## 🔄 Ingest Metadata

### 1. Ingest from Trino (Sales + Marketing)

This will catalog all your PostgreSQL tables.

```powershell
# In PowerShell Windows
datahub ingest -c datahub_trino_recipe.yml
```

Or in WSL:
```bash
wsl datahub ingest -c datahub_trino_recipe.yml
```

**What gets ingested:**
- ✅ sales.public.customers
- ✅ sales.public.products
- ✅ sales.public.orders
- ✅ sales.public.order_items
- ✅ marketing.public.campaigns
- ✅ marketing.public.leads
- ✅ marketing.public.campaign_metrics
- ✅ marketing.public.website_traffic

---

### 2. Ingest from DBT (Transformations + Lineage)

This will show your DBT models and their dependencies.

#### Step 2.1: Copy DBT artifacts from JupyterHub

```powershell
kubectl cp jupyterhub/jupyter-admin:/home/jovyan/dbt_projects/datamesh/target ./dbt_target
```

#### Step 2.2: Update datahub_dbt_recipe.yml

Edit the file to point to the copied artifacts:

```yaml
source:
  type: dbt
  config:
    manifest_path: "./dbt_target/manifest.json"
    catalog_path: "./dbt_target/catalog.json"
    target_platform: "postgres"
    
sink:
  type: datahub-rest
  config:
    server: "http://localhost:8080"
```

#### Step 2.3: Ingest

```powershell
datahub ingest -c datahub_dbt_recipe.yml
```

**What gets ingested:**
- ✅ stg_sales__customers (staging model)
- ✅ stg_sales__orders (staging model)
- ✅ mart_sales__customer_lifetime_value (mart)
- ✅ DBT tests and documentation
- ✅ **Data Lineage** (how models depend on each other)

---

## 🔍 Explore Your Data

### Search for a Dataset

1. Click the **Search bar** at the top
2. Type: `customers`
3. You'll see:
   - `sales.public.customers` (source table)
   - `stg_sales__customers` (DBT staging model)

### View Dataset Details

Click on `sales.public.customers` to see:

```
┌────────────────────────────────────────────────┐
│  sales.public.customers                        │
├────────────────────────────────────────────────┤
│  📊 Schema                                     │
│     • customer_id (INTEGER) - Primary Key     │
│     • customer_name (VARCHAR)                  │
│     • email (VARCHAR)                          │
│     • country (VARCHAR)                        │
│     • industry (VARCHAR)                       │
│     • created_at (TIMESTAMP)                   │
│                                                │
│  📝 Documentation                              │
│     Customer master data containing...         │
│                                                │
│  🏷️ Tags                                       │
│     #sales #customer-data                      │
│                                                │
│  👤 Owners                                     │
│     sales-team@company.com                     │
│                                                │
│  📈 Usage Statistics                           │
│     • Last accessed: Today                     │
│     • Query count: 15 this week                │
└────────────────────────────────────────────────┘
```

---

## 🔗 Data Lineage

### View Lineage Graph

1. Go to any dataset (e.g., `mart_sales__customer_lifetime_value`)
2. Click the **"Lineage"** tab
3. You'll see the full dependency graph:

```
┌─────────────────────────────────────────────────────┐
│              DATA LINEAGE GRAPH                     │
└─────────────────────────────────────────────────────┘

[sales.public.customers] ─────┐
                              │
                              ▼
                    [stg_sales__customers]
                              │
                              │
                              ▼
[sales.public.orders] ────────┼──────────────┐
                              │              │
                              ▼              │
                    [stg_sales__orders]      │
                              │              │
                              │              │
                              ▼              │
          [mart_sales__customer_lifetime_value]
```

### Impact Analysis

Click **"Impact"** to see:
- Which downstream models depend on this dataset
- Who will be affected if you change this table

### Upstream Dependencies

Click **"Upstream"** to see:
- Which source tables feed into this model
- The complete data flow

---

## 📊 Browse by Platform

### View All Datasets by Source

1. Click **"Browse"** in the navigation
2. Select **"Platforms"**
3. You'll see:

```
📁 PostgreSQL (Sales)
   ├── customers (15 rows)
   ├── products (10 rows)
   ├── orders (20 rows)
   └── order_items (45 rows)

📁 PostgreSQL (Marketing)
   ├── campaigns (8 rows)
   ├── leads (15 rows)
   ├── campaign_metrics (8 rows)
   └── website_traffic (50 rows)

📁 DBT
   ├── stg_sales__customers (view)
   ├── stg_sales__orders (view)
   └── mart_sales__customer_lifetime_value (table)
```

---

## 🏷️ Advanced Features

### 1. Add Tags

Tags help organize and discover data.

```
Example tags:
  • #pii - Personal Identifiable Information
  • #customer-facing
  • #high-value
  • #daily-refresh
  • #sales-kpi
```

**How to add:**
1. Go to a dataset
2. Click **"Add Tag"**
3. Type tag name
4. Save

### 2. Add Documentation

Improve discoverability with good docs.

**How to add:**
1. Go to a dataset
2. Click **"Edit Description"**
3. Write in Markdown:

```markdown
# Customer Lifetime Value

## Purpose
This model calculates key customer metrics including:
- Total lifetime value
- Order frequency
- RFM scores

## Usage
Use this for:
- Executive dashboards
- Customer segmentation
- Churn prediction

## Refresh
Updated daily at 2 AM UTC via DBT job
```

### 3. Set Ownership

**How to add:**
1. Click **"Edit Owners"**
2. Add:
   - `sales-team@company.com`
   - `data-team@company.com`
3. Save

### 4. Add Terms (Glossary)

Create business glossary terms:

```
Term: Customer Lifetime Value (CLV)
Definition: Total revenue from a customer over their entire relationship
Owner: Finance Team
Related: customers, orders, revenue
```

### 5. Data Quality

Add data quality rules:

```
✅ Assertions:
  • customer_id is unique
  • email is valid format
  • created_at not null
  • No duplicate emails
```

---

## 🔄 Scheduled Ingestion

### Setup Daily Ingestion

Create a cron job to refresh metadata daily:

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Task
3. Trigger: Daily at 3 AM
4. Action: `wsl datahub ingest -c datahub_trino_recipe.yml`

**Or use Airflow/Scheduler**:
```python
# In JupyterHub
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG('datahub_ingest', schedule_interval='@daily')

ingest_trino = BashOperator(
    task_id='ingest_trino',
    bash_command='datahub ingest -c /path/to/datahub_trino_recipe.yml',
    dag=dag
)

ingest_dbt = BashOperator(
    task_id='ingest_dbt',
    bash_command='datahub ingest -c /path/to/datahub_dbt_recipe.yml',
    dag=dag
)

ingest_trino >> ingest_dbt
```

---

## 📚 Use Cases

### 1. Data Discovery

**Scenario**: A data scientist wants to find customer data.

```
1. Search: "customer"
2. See all customer-related datasets
3. Check lineage to understand data flow
4. Read documentation
5. Contact owner if questions
```

### 2. Impact Analysis

**Scenario**: You want to change the `customers` table schema.

```
1. Go to sales.public.customers
2. Click "Lineage" → "Downstream"
3. See all affected models:
   - stg_sales__customers
   - mart_sales__customer_lifetime_value
   - Any Grafana dashboards
4. Plan migration carefully
```

### 3. Data Governance

**Scenario**: Identify all tables with PII.

```
1. Browse → Tags
2. Filter by #pii
3. See all PII datasets
4. Verify access controls
5. Document compliance
```

### 4. Cross-Domain Analysis

**Scenario**: Find all marketing data that feeds into sales reports.

```
1. Search: "campaign"
2. View: marketing.public.campaigns
3. Click: "Impact"
4. See if any sales models use it
5. Understand cross-domain dependencies
```

---

## 🔧 Troubleshooting

### DataHub not accessible

```powershell
# Check if running
wsl docker ps | findstr datahub

# View logs
wsl docker-compose -f ~/.datahub/quickstart/docker-compose.yml logs datahub-gms

# Restart
wsl datahub docker quickstart --stop
wsl datahub docker quickstart
```

### Ingestion fails

```powershell
# Check connection to Trino
kubectl port-forward -n data-platform trino-coordinator-xxx 30808:8080

# Test manually
curl http://localhost:30808/v1/info

# Run ingestion with debug
datahub ingest -c datahub_trino_recipe.yml --debug
```

### Missing metadata

```
Check:
1. Ingestion completed successfully?
2. Correct server URL in recipe? (http://localhost:8080)
3. DataHub GMS running? (docker ps)
4. Elasticsearch healthy?
```

---

## 🎯 Quick Commands Reference

```powershell
# Start DataHub
wsl datahub docker quickstart

# Stop DataHub
wsl datahub docker quickstart --stop

# Ingest Trino
datahub ingest -c datahub_trino_recipe.yml

# Ingest DBT
datahub ingest -c datahub_dbt_recipe.yml

# Check version
datahub version

# View help
datahub ingest --help

# Clean up everything
wsl datahub docker nuke
```

---

## 📖 Additional Resources

- **Official Docs**: https://datahubproject.io/docs/
- **GitHub**: https://github.com/datahub-project/datahub
- **Slack Community**: https://datahubspace.slack.com

---

## ✅ Checklist

After setup, you should have:

- [ ] DataHub accessible at http://localhost:9002
- [ ] Ingested Trino metadata (Sales + Marketing tables)
- [ ] Ingested DBT metadata (models + lineage)
- [ ] Viewed data lineage graph
- [ ] Added tags to key datasets
- [ ] Set ownership on critical tables
- [ ] Documented important models
- [ ] Tested search functionality

---

**Your Data Mesh platform now has a complete metadata catalog!** 🎉

