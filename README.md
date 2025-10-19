# 🏗️ DataMeesh Platform

**A Modern, Production-Ready Data Mesh Platform on Kubernetes**

[![Platform](https://img.shields.io/badge/Platform-Kubernetes-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Data Mesh](https://img.shields.io/badge/Architecture-Data%20Mesh-FF6B6B)](https://martinfowler.com/articles/data-mesh-principles.html)

> Complete Data Mesh implementation with federated queries, self-service analytics, data transformation, and metadata management.

---

## 🎯 What is DataMeesh?

A **production-grade Data Mesh platform** demonstrating modern data engineering:

- ✅ **Domain-Oriented** - Sales & Marketing domains with clear ownership
- ✅ **Federated Queries** - Trino for cross-domain analytics
- ✅ **Self-Service** - JupyterHub for data scientists
- ✅ **Data Transformation** - DBT for ELT pipelines
- ✅ **Visualization** - Grafana dashboards
- ✅ **Data Lake** - Minio S3-compatible storage
- ✅ **Metadata Management** - Hive Metastore for data lake tables
- ✅ **Metadata Catalog** - DataHub (optional, requires 10-12GB RAM)

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop with Kubernetes enabled
- Python 3.8+
- 8-10GB RAM

### Deploy (One Command!)

```bash
# 1. Verify system
python setup/verify_prerequisites.py

# 2. Deploy everything
python setup/deploy_complete_stack.py
```

**Time:** ~15 minutes  
**Result:** Full Data Mesh platform ready to use!

---

## 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **JupyterHub** | http://localhost:30080 | admin / datamesh2024 |
| **Trino Web UI** | http://localhost:30808 | - |
| **Minio Console** | http://localhost:30901 | minioadmin / minioadmin |
| **Grafana** | http://localhost:30030 | admin / datamesh2024 |
| **DBT Docs** | http://localhost:30082 | - |
| **DataHub** (optional) | http://localhost:9002 | datahub / datahub |

---

## 📂 Project Structure

```
DataMeesh/
├── README.md                    # This file
│
├── config/                      # Kubernetes manifests
│   ├── datamesh.yaml           # Core domains
│   ├── minio-trino-hive.yaml   # Analytics stack
│   ├── grafana.yaml            # Visualization
│   └── nginx-dbt-docs.yaml     # Documentation
│
├── setup/                       # Deployment scripts
│   ├── verify_prerequisites.py # Check system
│   ├── deploy_complete_stack.py# Deploy everything
│   ├── cleanup.py              # Remove all
│   │
│   ├── kubernetes/             # Core deployments
│   ├── helm/                   # JupyterHub
│   ├── trino/                  # Federated queries
│   ├── grafana/                # Dashboards
│   ├── dbt/                    # Data transformation
│   ├── data/                   # Sample data
│   ├── datahub/                # DataHub (optional)
│   └── docker/                 # Custom images
│
├── docs/                        # Documentation
│   ├── DEPLOYMENT_GUIDE.md     # Deployment guide
│   ├── CLEANUP_GUIDE.md        # Cleanup guide
│   │
│   ├── guides/                 # User guides
│   │   ├── COMPLETE_GUIDE.md
│   │   ├── DATAHUB_GUIDE.md
│   │   └── ADVANCED_STACK.md
│   │
│   ├── architecture/           # Architecture docs
│   │   ├── DATA_MODEL.md
│   │   └── DEPLOYMENT_STATUS.md
│   │
│   └── summaries/              # Summary reports
│       ├── DEPLOYMENT_SUMMARY.md
│       └── FINAL_SUMMARY.md
│
├── recipes/                     # DataHub ingestion
│   ├── datahub_trino_recipe.yml
│   └── datahub_dbt_recipe.yml
│
└── examples/                    # Example code
    ├── trino_queries.sql
    └── jupyter_notebook_example.py
```

---

## 🎓 Key Features

### 1. Domain-Oriented Architecture

```
┌─────────────────┐       ┌─────────────────┐
│  Sales Domain   │       │Marketing Domain │
├─────────────────┤       ├─────────────────┤
│ • PostgreSQL    │       │ • PostgreSQL    │
│ • REST APIs     │       │ • REST APIs     │
│ • 15 Customers  │       │ • 8 Campaigns   │
│ • 20 Orders     │       │ • 15 Leads      │
└────────┬────────┘       └────────┬────────┘
         │                         │
         └──────────┬──────────────┘
                    │
            ┌───────▼────────┐
            │  Trino Engine  │
            │ Federated SQL  │
            └────────────────┘
```

### 2. Federated Queries (Trino + Hive)

Query across domains and data lake seamlessly:

```sql
-- Cross-domain: Marketing campaigns → Sales revenue
SELECT 
    c.campaign_name,
    COUNT(DISTINCT l.lead_id) as leads,
    SUM(o.total_amount) as revenue
FROM marketing.public.campaigns c
JOIN marketing.public.leads l ON c.campaign_id = l.campaign_id
JOIN sales.public.customers cust ON l.email = cust.email
JOIN sales.public.orders o ON cust.customer_id = o.customer_id
GROUP BY 1;

-- Query data lake via Hive Metastore
SELECT * FROM hive.default.customer_events
WHERE event_date = CURRENT_DATE;
```

**Catalogs available:**
- `sales` - Sales PostgreSQL
- `marketing` - Marketing PostgreSQL  
- `hive` - Minio data lake (via Hive Metastore)

### 3. Self-Service Analytics (JupyterHub)

```python
from trino.dbapi import connect

conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin'
)

df = pd.read_sql("SELECT * FROM sales.public.customers", conn)
df.head()
```

### 4. Data Transformation (DBT)

```
Raw Data → DBT Staging → DBT Marts → Analytics
```

**Models:**
- `stg_sales__customers` - Clean customer data
- `stg_sales__orders` - Standardized orders
- `mart_sales__customer_lifetime_value` - CLV + RFM scores

---

## 📊 Architecture

### Components

| Layer | Component | Purpose | Resources |
|-------|-----------|---------|-----------|
| **Storage** | PostgreSQL (Sales) | Customer, Order data | 256MB |
| **Storage** | PostgreSQL (Marketing) | Campaign, Lead data | 128MB |
| **Query** | Trino | Federated queries | 3GB |
| **Storage** | Minio | Data lake (S3) | 256MB |
| **Metadata** | Hive Metastore | Data lake metadata | 512MB |
| **Analytics** | JupyterHub | Notebooks | 900MB |
| **Transform** | DBT | Data pipelines | - |
| **Visualization** | Grafana | Dashboards | 256MB |
| **Catalog** | DataHub (optional) | Metadata | 2-3GB |

**Total:** ~6.5GB (or ~9GB with DataHub)

---

## 🔧 Management Commands

```bash
# Verify prerequisites
python setup/verify_prerequisites.py

# Deploy everything
python setup/deploy_complete_stack.py

# Check status
kubectl get pods --all-namespaces

# View logs
kubectl logs -n <namespace> <pod-name>

# Clean up
python setup/cleanup.py

# Deploy DataHub (optional - requires 10-12GB RAM)
python setup/datahub/deploy_datahub.py
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [**Deployment Guide**](docs/DEPLOYMENT_GUIDE.md) | Step-by-step deployment |
| [**Cleanup Guide**](docs/CLEANUP_GUIDE.md) | Resource cleanup |
| [**Complete Guide**](docs/guides/COMPLETE_GUIDE.md) | Comprehensive user guide |
| [**Hive Metastore Guide**](docs/guides/HIVE_METASTORE_GUIDE.md) | Data lake metadata |
| [**Architecture**](docs/architecture/) | Technical details |
| [**Setup Details**](setup/README.md) | Setup folder guide |

---

## 🎯 Use Cases

### 1. Marketing Attribution

Track leads from campaigns to revenue:

```python
query = """
SELECT 
    c.campaign_name,
    COUNT(DISTINCT l.lead_id) as leads,
    SUM(o.total_amount) as revenue
FROM marketing.public.campaigns c
JOIN marketing.public.leads l ON c.campaign_id = l.campaign_id
JOIN sales.public.customers cust ON l.email = cust.email
JOIN sales.public.orders o ON cust.customer_id = o.customer_id
GROUP BY 1
"""
df = pd.read_sql(query, trino_conn)
```

### 2. Customer Lifetime Value

```sql
SELECT 
    customer_id,
    SUM(total_amount) as lifetime_value,
    COUNT(*) as total_orders,
    CASE 
        WHEN SUM(total_amount) >= 100000 THEN 'High Value'
        ELSE 'Medium Value'
    END as segment
FROM orders
GROUP BY customer_id
```

### 3. Cross-Domain Analytics

Analyze marketing campaign impact on sales.

---

## 🏆 What Makes This Special?

✅ **Production-Ready**
- Resource limits & requests
- Health checks, Auto-scaling
- High availability, Security (RBAC, Secrets)

✅ **Best Practices**
- Infrastructure as Code
- Kubernetes orchestration
- Modern data stack

✅ **Complete**
- End-to-end platform
- Sample data included
- Full documentation

✅ **Portable**
- Cross-platform (Windows, WSL, macOS, Linux)
- One-command deployment
- Easy to redeploy

---

## 🧹 Cleanup

```bash
# Standard cleanup
python setup/cleanup.py

# Deep Docker cleanup (removes ALL Docker resources)
python setup/cleanup_docker_cache.py
```

---

## 🤝 Contributing

This is a demonstration project. Feel free to:
- Fork and extend
- Add more domains
- Implement additional DBT models
- Create more dashboards

---

## 📞 Support

- **Deployment issues?** → Check [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- **Cleanup questions?** → Check [Cleanup Guide](docs/CLEANUP_GUIDE.md)
- **Usage questions?** → Check [Complete Guide](docs/guides/COMPLETE_GUIDE.md)

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Built With

Amazing open-source technologies:
- [Kubernetes](https://kubernetes.io/)
- [Trino](https://trino.io/)
- [Apache Hive](https://hive.apache.org/)
- [JupyterHub](https://jupyter.org/hub)
- [DBT](https://www.getdbt.com/)
- [Grafana](https://grafana.com/)
- [Minio](https://min.io/)

---

**Ready to explore modern data engineering?** 🚀

```bash
python setup/deploy_complete_stack.py
```
