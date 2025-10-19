# 🏗️ Architecture Finale - DataMeesh

**Data Mesh Platform - Implémentation Locale K8s**

---

## 🎯 Vue d'Ensemble

Architecture Data Mesh complète avec **Kubernetes local**, sans RBAC (projet académique).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        VOTRE MACHINE LOCALE                             │
│                     (Windows 10 + Docker Desktop)                       │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    KUBERNETES CLUSTER                             │ │
│  │                                                                   │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │  Namespace: jupyterhub                                   │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  📓 JupyterHub (Hub + Proxy)              │          │   │ │
│  │  │  │     • Port: 30080 (HTTP)                  │          │   │ │
│  │  │  │     • User: admin / admin                 │          │   │ │
│  │  │  │     • PVC: 5GB (notebooks)                │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │                                                          │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  👤 User Pod (Single User)                │          │   │ │
│  │  │  │     • Python + DBT + Trino CLI            │          │   │ │
│  │  │  │     • Git Extension                       │          │   │ │
│  │  │  │     • Scheduler Extension                 │          │   │ │
│  │  │  │     • Persistent Storage: 5GB             │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  │                                                                   │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │  Namespace: data-platform                                │   │ │
│  │  │                                                          │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🗄️  Trino (Coordinator)                 │          │   │ │
│  │  │  │     • Port: 30081 (Web UI)                │          │   │ │
│  │  │  │     • Port: 8080 (Query)                  │          │   │ │
│  │  │  │     • Catalogs: sales, marketing, hive    │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │            │                                             │   │ │
│  │  │            │ Queries                                     │   │ │
│  │  │            ▼                                             │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🗄️  PostgreSQL Sales                    │          │   │ │
│  │  │  │     • Port: 5432                          │          │   │ │
│  │  │  │     • Database: sales_db                  │          │   │ │
│  │  │  │     • Tables: customers, orders           │          │   │ │
│  │  │  │     • PVC: 5GB                            │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │                                                          │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🗄️  PostgreSQL Marketing                │          │   │ │
│  │  │  │     • Port: 5432                          │          │   │ │
│  │  │  │     • Database: marketing_db              │          │   │ │
│  │  │  │     • Tables: leads, campaigns            │          │   │ │
│  │  │  │     • PVC: 5GB                            │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │                                                          │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  📦 Minio (S3-compatible)                 │          │   │ │
│  │  │  │     • Port: 30082 (Console)               │          │   │ │
│  │  │  │     • Port: 9000 (API)                    │          │   │ │
│  │  │  │     • User: minioadmin / minioadmin       │          │   │ │
│  │  │  │     • Bucket: datalake                    │          │   │ │
│  │  │  │     • PVC: 10GB                           │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │            │                                             │   │ │
│  │  │            │ Metadata                                    │   │ │
│  │  │            ▼                                             │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🐝 Hive Metastore                        │          │   │ │
│  │  │  │     • Port: 9083                          │          │   │ │
│  │  │  │     • Backend: PostgreSQL                 │          │   │ │
│  │  │  │     • Manages Minio metadata              │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │                                                          │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  📊 Grafana                               │          │   │ │
│  │  │  │     • Port: 30083 (Web UI)                │          │   │ │
│  │  │  │     • User: admin / admin                 │          │   │ │
│  │  │  │     • Data Sources: PostgreSQL x2         │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  │                                                          │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🌐 Nginx (DBT Docs Server)               │          │   │ │
│  │  │  │     • Port: 30084 (HTTP)                  │          │   │ │
│  │  │  │     • Serves: DBT documentation           │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  │                                                                   │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │  Namespace: sales-domain                                 │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🗄️  PostgreSQL Sales Domain             │          │   │ │
│  │  │  │     • Port: 5432                          │          │   │ │
│  │  │  │     • Owner: Sales team                   │          │   │ │
│  │  │  │     • PVC: 5GB                            │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  │                                                                   │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │  Namespace: marketing-domain                             │   │ │
│  │  │  ┌────────────────────────────────────────────┐          │   │ │
│  │  │  │  🗄️  PostgreSQL Marketing Domain         │          │   │ │
│  │  │  │     • Port: 5432                          │          │   │ │
│  │  │  │     • Owner: Marketing team               │          │   │ │
│  │  │  │     • PVC: 5GB                            │          │   │ │
│  │  │  └────────────────────────────────────────────┘          │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  Docker Desktop                                               │ │
│  │  • RAM: 8GB alloué                                           │ │
│  │  • Disk: ~35GB utilisé                                       │ │
│  │  • Kubernetes: Enabled                                       │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Inventaire des Services

| Service | Namespace | Type | Port | Accès | Status |
|---------|-----------|------|------|-------|--------|
| **JupyterHub** | jupyterhub | NodePort | 30080 | http://localhost:30080 | ✅ Running |
| **Trino UI** | data-platform | NodePort | 30081 | http://localhost:30081 | ✅ Running |
| **Minio Console** | data-platform | NodePort | 30082 | http://localhost:30082 | ✅ Running |
| **Grafana** | data-platform | NodePort | 30083 | http://localhost:30083 | ✅ Running |
| **DBT Docs** | data-platform | NodePort | 30084 | http://localhost:30084 | ✅ Running |
| **PostgreSQL Sales** | data-platform | ClusterIP | 5432 | Internal only | ✅ Running |
| **PostgreSQL Marketing** | data-platform | ClusterIP | 5432 | Internal only | ✅ Running |
| **Hive Metastore** | data-platform | ClusterIP | 9083 | Internal only | ✅ Running |
| **PostgreSQL (Sales Domain)** | sales-domain | ClusterIP | 5432 | Internal only | ✅ Running |
| **PostgreSQL (Marketing Domain)** | marketing-domain | ClusterIP | 5432 | Internal only | ✅ Running |

---

## 🔄 Flux de Données

### 1️⃣ Ingestion de Données

```
Data Scientist (JupyterHub)
           │
           ├──► Upload CSV/Parquet
           │         │
           │         ▼
           │    Minio Bucket (datalake/)
           │         │
           │         ├──► raw/
           │         ├──► processed/
           │         └──► curated/
           │
           ├──► Insert to PostgreSQL
           │         │
           │         ├──► Sales DB (customers, orders)
           │         └──► Marketing DB (leads, campaigns)
           │
           └──► Hive Metastore (metadata catalog)
```

### 2️⃣ Transformation avec DBT

```
JupyterHub Terminal
           │
           ▼
     dbt run --profiles-dir ~/dbt_projects
           │
           ├──► Staging Models
           │    ├── stg_sales__customers
           │    ├── stg_sales__orders
           │    └── stg_marketing__leads
           │
           ├──► Mart Models
           │    ├── mart_sales__customer_lifetime_value
           │    └── mart_lead_to_customer_journey
           │
           └──► Quality Tests
                ├── Not null checks
                ├── Unique checks
                └── Relationship checks
```

### 3️⃣ Requêtes Fédérées avec Trino

```
User (JupyterHub / Trino CLI)
           │
           ▼
    Trino Coordinator
           │
           ├──► Catalog: sales
           │    └── PostgreSQL Sales DB
           │
           ├──► Catalog: marketing
           │    └── PostgreSQL Marketing DB
           │
           └──► Catalog: hive
                └── Minio Data Lake
                    └── Hive Metastore
```

**Exemple de Requête Cross-Domain:**
```sql
SELECT 
    s.customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as revenue,
    m.campaign_name
FROM sales.public.customers s
JOIN sales.public.orders o ON s.customer_id = o.customer_id
LEFT JOIN marketing.public.leads l ON s.email = l.email
LEFT JOIN marketing.public.campaigns m ON l.campaign_id = m.campaign_id
GROUP BY s.customer_name, m.campaign_name
ORDER BY revenue DESC
```

### 4️⃣ Visualisation avec Grafana

```
Grafana Dashboard
           │
           ├──► Data Source: PostgreSQL Sales
           │    └── Query: Customer metrics
           │
           └──► Data Source: PostgreSQL Marketing
                └── Query: Campaign performance
```

---

## 🗂️ Structure de Stockage

### Persistent Volume Claims (PVC)

| PVC | Namespace | Size | Usage | Mounté sur |
|-----|-----------|------|-------|------------|
| `jupyterhub-hub-pvc` | jupyterhub | 1GB | Hub config | `/srv/jupyterhub` |
| `claim-admin` | jupyterhub | 5GB | User notebooks | `/home/jovyan` |
| `postgres-sales-pvc` | data-platform | 5GB | Sales DB data | `/var/lib/postgresql/data` |
| `postgres-marketing-pvc` | data-platform | 5GB | Marketing DB data | `/var/lib/postgresql/data` |
| `minio-pvc` | data-platform | 10GB | Data lake | `/data` |
| `postgres-hive-pvc` | data-platform | 2GB | Hive metadata | `/var/lib/postgresql/data` |
| `postgres-sales-domain-pvc` | sales-domain | 5GB | Sales domain DB | `/var/lib/postgresql/data` |
| `postgres-marketing-domain-pvc` | marketing-domain | 5GB | Marketing domain DB | `/var/lib/postgresql/data` |

**Total PVC:** ~38GB

### Structure dans JupyterHub (`/home/jovyan`)

```
/home/jovyan/
├── dbt_projects/               # DBT project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   │   ├── sales/
│   │   │   └── marketing/
│   │   └── marts/
│   │       ├── sales/
│   │       ├── marketing/
│   │       └── cross_domain/
│   └── target/                 # DBT compiled models
│       └── docs/                # DBT documentation
├── notebooks/                  # Jupyter notebooks
│   ├── 01_explore_data.ipynb
│   ├── 02_trino_queries.ipynb
│   └── 03_analysis.ipynb
├── data/                       # Local data files
│   ├── uploads/
│   └── exports/
└── scripts/                    # Python scripts
    └── utils.py
```

### Structure dans Minio (`s3://datalake`)

```
datalake/
├── raw/                        # Raw ingested data
│   ├── sales/
│   │   ├── customers.csv
│   │   └── orders.csv
│   └── marketing/
│       ├── leads.csv
│       └── campaigns.csv
├── processed/                  # Cleaned data
│   ├── sales/
│   └── marketing/
├── curated/                    # Business-ready data
│   ├── customer_360/
│   └── campaign_analytics/
└── notebooks/                  # Saved notebooks
    └── analysis_2024.ipynb
```

---

## 🔌 Connectivité et Réseau

### URLs d'Accès (depuis votre machine)

| Service | URL | Credentials |
|---------|-----|-------------|
| JupyterHub | http://localhost:30080 | admin / admin |
| Trino Web UI | http://localhost:30081 | - |
| Minio Console | http://localhost:30082 | minioadmin / minioadmin |
| Grafana | http://localhost:30083 | admin / admin |
| DBT Docs | http://localhost:30084 | - |

### Connexions Internes (dans K8s)

**Depuis JupyterHub vers PostgreSQL:**
```python
import psycopg2

# Sales DB
conn = psycopg2.connect(
    host='postgres-sales.data-platform.svc.cluster.local',
    port=5432,
    database='sales_db',
    user='admin',
    password='admin123'
)
```

**Depuis JupyterHub vers Trino:**
```python
from trino.dbapi import connect

conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin'
)
```

**Depuis JupyterHub vers Minio:**
```python
from minio import Minio

client = Minio(
    'minio.data-platform.svc.cluster.local:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)
```

---

## 🛠️ Technologies Utilisées

### Infrastructure
- **Kubernetes:** Orchestration (Docker Desktop)
- **Docker:** Containerization
- **Helm:** JupyterHub deployment

### Data Platform
- **JupyterHub:** Multi-user notebooks
- **PostgreSQL:** Transactional databases (4 instances)
- **Minio:** Object storage (S3-compatible)
- **Hive Metastore:** Data lake metadata
- **Trino:** Federated SQL query engine

### Data Engineering
- **DBT (Data Build Tool):** Transformations
- **Python:** Data processing (pandas, psycopg2)
- **SQL:** Data queries

### Visualization
- **Grafana:** Dashboards
- **Nginx:** DBT docs server

---

## 📦 Composants Détaillés

### 1. JupyterHub (Namespace: jupyterhub)

**Hub Pod:**
- Image: `quay.io/jupyterhub/k8s-hub:3.3.8`
- Resources: 512MB RAM, 0.5 CPU
- Function: User management, spawning

**Proxy Pod:**
- Image: `quay.io/jupyterhub/configurable-http-proxy:4.6.1`
- Resources: 256MB RAM, 0.25 CPU
- Function: Reverse proxy

**User Pod (Single User):**
- Image: Custom `jupyterhub-dbt:latest`
- Includes:
  - JupyterLab
  - Python 3.11
  - DBT Core + Trino adapter
  - Trino CLI
  - Minio CLI
  - Git extension
  - Scheduler extension
- Resources: 2GB RAM, 1 CPU
- Storage: 5GB PVC

### 2. Trino (Namespace: data-platform)

**Coordinator:**
- Image: `trinodb/trino:435`
- Resources: 2GB RAM, 1 CPU
- Function: Query planning, coordination

**Catalogs:**
```properties
# sales.properties
connector.name=postgresql
connection-url=jdbc:postgresql://postgres-sales:5432/sales_db

# marketing.properties
connector.name=postgresql
connection-url=jdbc:postgresql://postgres-marketing:5432/marketing_db

# hive.properties
connector.name=hive
hive.metastore.uri=thrift://hive-metastore:9083
hive.s3.endpoint=http://minio:9000
```

### 3. PostgreSQL Instances

**4 Instances Total:**
1. **Sales (data-platform)** - Main sales data
2. **Marketing (data-platform)** - Main marketing data
3. **Sales Domain (sales-domain)** - Domain-specific
4. **Marketing Domain (marketing-domain)** - Domain-specific

**Configuration par instance:**
- Image: `postgres:15`
- Resources: 512MB RAM, 0.5 CPU
- Storage: 5GB PVC (2GB for Hive)
- Environment:
  - `POSTGRES_USER=admin`
  - `POSTGRES_PASSWORD=admin123`

### 4. Minio (Namespace: data-platform)

**Configuration:**
- Image: `minio/minio:latest`
- Resources: 1GB RAM, 0.5 CPU
- Storage: 10GB PVC
- Buckets:
  - `datalake` (main storage)

### 5. Hive Metastore (Namespace: data-platform)

**Configuration:**
- Image: `apache/hive:3.1.3`
- Resources: 512MB RAM, 0.5 CPU
- Backend: PostgreSQL (dedicated instance)
- Function: Catalog for Minio/S3 data

### 6. Grafana (Namespace: data-platform)

**Configuration:**
- Image: `grafana/grafana:latest`
- Resources: 512MB RAM, 0.5 CPU
- Data Sources:
  - PostgreSQL Sales
  - PostgreSQL Marketing

### 7. Nginx (Namespace: data-platform)

**Configuration:**
- Image: `nginx:alpine`
- Resources: 128MB RAM, 0.1 CPU
- Function: Serve DBT documentation

---

## 💾 Utilisation des Ressources

### Actuelle (Monitoring)

```bash
# Vérifier les ressources
kubectl top nodes
kubectl top pods -A
```

**Estimation:**
| Resource | Usage | Total | Pourcentage |
|----------|-------|-------|-------------|
| **Disk** | ~35GB | 60GB+ | ~58% |
| **RAM** | ~7.6GB | 8GB | ~95% |
| **CPU** | ~3 cores | 4+ cores | ~75% |

**Recommandations Docker Desktop:**
- Disk: 60-70GB
- RAM: 8-10GB
- CPU: 4-6 cores
- Swap: 2GB

---

## 🚀 Déploiement Complet

### Script Principal

```bash
# Déployer tout
python setup/deploy_complete_stack.py

# Étapes:
# 1. Deploy PostgreSQL databases (2x)
# 2. Deploy Minio + Hive Metastore
# 3. Deploy Trino with catalogs
# 4. Deploy JupyterHub (Helm)
# 5. Deploy Grafana
# 6. Deploy Nginx for DBT docs
# 7. Load sample data
# 8. Setup DBT in JupyterHub
```

### Vérification

```bash
# Vérifier les pods
kubectl get pods -n data-platform
kubectl get pods -n jupyterhub
kubectl get pods -n sales-domain
kubectl get pods -n marketing-domain

# Vérifier les services
kubectl get svc -n data-platform
kubectl get svc -n jupyterhub

# Vérifier les PVC
kubectl get pvc -A
```

---

## 🔍 Tests et Validation

### 1. Test JupyterHub
```bash
# Accéder
open http://localhost:30080

# Login: admin / admin
# Créer notebook
# Test connexion Trino
```

### 2. Test Trino
```bash
# Accéder à un pod
kubectl exec -it -n data-platform <trino-pod> -- trino

# Requêtes de test
trino> SHOW CATALOGS;
trino> SHOW SCHEMAS FROM sales;
trino> SELECT * FROM sales.public.customers LIMIT 5;
```

### 3. Test DBT
```bash
# Dans JupyterHub terminal
cd ~/dbt_projects
dbt run --profiles-dir .
dbt test --profiles-dir .
dbt docs generate --profiles-dir .
```

### 4. Test Minio
```bash
# Accéder console
open http://localhost:30082

# Login: minioadmin / minioadmin
# Upload fichier dans bucket "datalake"
```

### 5. Test Grafana
```bash
# Accéder
open http://localhost:30083

# Login: admin / admin
# Vérifier data sources PostgreSQL
```

---

## 🧹 Nettoyage

### Nettoyage Complet
```bash
python setup/cleanup.py
```

### Nettoyage Sélectif
```bash
# Supprimer un namespace
kubectl delete namespace data-platform

# Supprimer JupyterHub
helm uninstall jupyterhub -n jupyterhub

# Nettoyer Docker cache
python setup/cleanup_docker_cache.py
```

---

## 📖 Principes Data Mesh Appliqués

### ✅ 1. Domain-Oriented Decentralization
- Namespace `sales-domain` avec PostgreSQL dédié
- Namespace `marketing-domain` avec PostgreSQL dédié
- Ownership clair par domaine

### ✅ 2. Data as a Product
- DBT models = data products
- Documentation automatique (dbt docs)
- Tests de qualité (dbt test)
- Versioning via Git

### ✅ 3. Self-Service Platform
- JupyterHub pour tous les data scientists
- Trino pour queries fédérées
- Minio pour stockage libre-service
- Grafana pour visualisations

### ✅ 4. Federated Governance
- Trino = point d'accès unique
- Hive Metastore = catalogue centralisé
- DBT = transformations standardisées
- (RBAC optionnel pour gouvernance avancée)

---

## 🎓 Cas d'Usage Démonstration

### Scénario 1: Analyse Cross-Domain
```python
# Dans JupyterHub
from trino.dbapi import connect

conn = connect(host='trino-coordinator.data-platform.svc.cluster.local', port=8080, user='admin')
cursor = conn.cursor()

# Requête Sales + Marketing
cursor.execute("""
    SELECT 
        c.customer_name,
        COUNT(o.order_id) as orders,
        SUM(o.total_amount) as revenue,
        l.source as lead_source
    FROM sales.public.customers c
    JOIN sales.public.orders o ON c.customer_id = o.customer_id
    LEFT JOIN marketing.public.leads l ON c.email = l.email
    GROUP BY c.customer_name, l.source
    ORDER BY revenue DESC
    LIMIT 10
""")

results = cursor.fetchall()
print(results)
```

### Scénario 2: Upload vers Data Lake
```python
# Upload CSV vers Minio
from minio import Minio
import pandas as pd

client = Minio('minio.data-platform.svc.cluster.local:9000',
               access_key='minioadmin',
               secret_key='minioadmin',
               secure=False)

df = pd.read_csv('data.csv')
df.to_parquet('/tmp/data.parquet')

client.fput_object('datalake', 'raw/data.parquet', '/tmp/data.parquet')
print("✅ Uploaded to data lake")
```

### Scénario 3: Transformation DBT
```sql
-- models/marts/sales/mart_customer_360.sql
{{
  config(
    materialized='view'
  )
}}

WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(total_amount) as lifetime_value
    FROM {{ ref('stg_sales__orders') }}
    GROUP BY customer_id
),

customer_leads AS (
    SELECT 
        email,
        MIN(created_at) as first_contact
    FROM {{ source('marketing', 'leads') }}
    GROUP BY email
)

SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    co.order_count,
    co.lifetime_value,
    cl.first_contact,
    DATEDIFF('day', cl.first_contact, c.created_at) as days_to_convert
FROM {{ ref('stg_sales__customers') }} c
LEFT JOIN customer_orders co ON c.customer_id = co.customer_id
LEFT JOIN customer_leads cl ON c.email = cl.email
```

---

## 📚 Documentation Associée

| Document | Description |
|----------|-------------|
| `README.md` | Vue d'ensemble du projet |
| `docs/DEPLOYMENT_GUIDE.md` | Guide de déploiement |
| `docs/CLEANUP_GUIDE.md` | Guide de nettoyage |
| `docs/guides/COMPLETE_GUIDE.md` | Guide utilisateur complet |
| `docs/guides/HIVE_METASTORE_GUIDE.md` | Guide Hive Metastore |
| `docs/guides/JUPYTERHUB_STORAGE_GUIDE.md` | Guide stockage JupyterHub |
| `docs/guides/RBAC_ACCESS_CONTROL.md` | Guide RBAC (optionnel) |
| `docs/guides/AWS_HYBRID_ARCHITECTURE.md` | Architecture hybride AWS |
| `docs/architecture/DATA_MODEL.md` | Modèle de données |
| `docs/architecture/DEPLOYMENT_STATUS.md` | Status déploiement |

---

## ✅ Résumé: Ce Qui Fonctionne

### ✅ Infrastructure
- Kubernetes local (Docker Desktop)
- 5 namespaces organisés
- ~35GB de stockage utilisé
- 8 PVC persistants

### ✅ Services Déployés
- JupyterHub (1 hub + 1 user pod)
- Trino (federated queries)
- PostgreSQL x4 (2 data-platform + 2 domains)
- Minio (data lake)
- Hive Metastore (catalog)
- Grafana (visualization)
- Nginx (docs server)

### ✅ Fonctionnalités
- Notebooks Python interactifs
- DBT transformations
- Requêtes SQL fédérées
- Upload/download S3
- Dashboards Grafana
- Documentation automatique

### ✅ Accès
- Tout accessible via localhost:300XX
- Un seul utilisateur (admin)
- Pas de RBAC (projet académique)

---

## 🎯 Prochaines Évolutions Possibles

### Option 1: AWS Hybrid (200 USD)
- Migrer PostgreSQL vers RDS
- Utiliser S3 au lieu de Minio
- IAM pour RBAC gratuit
- Voir: `docs/guides/AWS_HYBRID_ARCHITECTURE.md`

### Option 2: RBAC Local
- 3 users (admin, sales, marketing)
- +20GB stockage
- +900MB RAM
- Voir: `docs/guides/RBAC_ACCESS_CONTROL.md`

### Option 3: DataHub (Metadata Platform)
- Nécessite 16GB RAM
- ~10GB stockage
- Data lineage, discovery
- Déploiement séparé: `setup/datahub/`

---

## 🎓 Pour Présentation Académique

### Points Forts
1. **Architecture complète** - Tous les composants Data Mesh
2. **Production-like** - Technologies réelles (Trino, DBT, Kubernetes)
3. **Scalable** - Design pensé pour évolution (AWS, RBAC)
4. **Best practices** - Documentation, tests, monitoring

### Démo Live
1. Accéder JupyterHub → Créer notebook
2. Query cross-domain avec Trino
3. Montrer DBT transformations
4. Afficher dashboard Grafana
5. Explorer data lake Minio

### Slide Key
```
"Data Mesh Local Platform
 • 🔧 7 Services K8s
 • 📊 4 PostgreSQL databases
 • 🚀 Federated queries (Trino)
 • 📓 Data Science (JupyterHub + DBT)
 • 💾 Data Lake (Minio + Hive)
 • 📈 Visualization (Grafana)
 
 Budget: 0 EUR (local only)
 Evolution: +200 USD → AWS Hybrid"
```

---

**🎉 Votre Data Mesh est complet et prêt pour démonstration académique!**

