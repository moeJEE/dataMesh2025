# 🎨 DataMeesh - Architecture Diagrams

**Visual Guide to Platform Architecture**

---

## 📐 Diagram 1: Complete Technical Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                          🌐 USER ACCESS LAYER                                         ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

    Browser                Browser              Browser               Browser
   (Admin)              (Data Scientist)     (Sales User)        (Marketing User)
      │                      │                    │                    │
      │ :30080              │ :30080             │ :30030             │ :30030
      └──────────┬───────────┘                    └────────┬───────────┘
                 │                                         │
                 ▼                                         ▼
    ┌────────────────────────┐                ┌────────────────────────┐
    │     JupyterHub         │                │       Grafana          │
    │   (Self-Service)       │                │    (Visualization)     │
    │                        │                │                        │
    │  • Python 3.11         │                │  • Pre-built dashboards│
    │  • Jupyter Notebooks   │                │  • Query builder       │
    │  • DBT CLI             │                │  • Alerting            │
    │  • Trino Python Client │                │  • User permissions    │
    │  • Pandas, Matplotlib  │                │  • Export (PDF/PNG)    │
    │                        │                │                        │
    │  PVC: 10Gi (persistent)│                │  Data Sources:         │
    │  Port: 30080           │                │    - Sales DB          │
    └────────────┬───────────┘                │    - Marketing DB      │
                 │                             │    - Sales API DB      │
                 │                             └────────────┬───────────┘
                 │                                          │
                 │                                          │
╔════════════════▼══════════════════════════════════════════▼═══════════════════════════╗
║                          🔗 QUERY & FEDERATION LAYER                                  ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

                 │                                          │
                 └──────────┬───────────────────────────────┘
                            │
                            │ SQL Queries
                            ▼
                ┌───────────────────────┐
                │   Trino Coordinator   │
                │   :30808 (Web UI)     │
                │   :8080  (JDBC)       │
                │                       │
                │  • Query Planning     │
                │  • Query Optimization │
                │  • Result Aggregation │
                │  • Catalog Management │
                └───────────┬───────────┘
                            │
                            │ Distribute Work
                            ▼
                ┌───────────────────────┐
                │    Trino Worker       │
                │                       │
                │  • Query Execution    │
                │  • Data Processing    │
                │  • Result Caching     │
                └───────────┬───────────┘
                            │
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        │         Catalogs Configuration        │
        │                                       │
        ▼                                       ▼
┌───────────────┐                      ┌────────────────┐
│ PostgreSQL    │                      │     Hive       │
│  Connector    │                      │   Connector    │
│               │                      │                │
│ • sales       │                      │ • hive         │
│ • marketing   │                      │   (data lake)  │
└───────┬───────┘                      └────────┬───────┘
        │                                       │
        │                                       │
╔═══════▼═══════════════════════════════════════▼═══════════════════════════════════════╗
║                       💾 STORAGE & METADATA LAYER                                     ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

        │                                       │
        │                              ┌────────▼────────┐
        │                              │ Hive Metastore  │
        │                              │   :9083         │
        │                              │                 │
        │                              │ • Table schemas │
        │                              │ • Partitions    │
        │                              │ • Locations     │
        │                              │ • Statistics    │
        │                              │                 │
        │                              │ Backend DB:     │
        │                              │  PostgreSQL     │
        │                              └────────┬────────┘
        │                                       │
        │                                       │ Metadata
        │                                       │
┌───────┴────────────────────┐         ┌────────▼────────┐
│                            │         │                 │
│    Domain Databases        │         │  Data Lake      │
│                            │         │                 │
│  ┌──────────────────┐     │         │  ┌───────────┐  │
│  │   Sales Domain   │     │         │  │   Minio   │  │
│  │   PostgreSQL     │     │         │  │    S3     │  │
│  │   :5432          │     │         │  │  :9000    │  │
│  │                  │     │         │  │           │  │
│  │ Tables:          │     │         │  │ Buckets:  │  │
│  │  • customers     │     │         │  │  • datalake│ │
│  │  • orders        │     │         │  │  • backups │ │
│  │                  │     │         │  │           │  │
│  │ PVC: 5Gi         │     │         │  │ Console:  │  │
│  └──────────────────┘     │         │  │  :30901   │  │
│                            │         │  │           │  │
│  ┌──────────────────┐     │         │  │ PVC: 20Gi │  │
│  │ Marketing Domain │     │         │  └───────────┘  │
│  │   PostgreSQL     │     │         │                 │
│  │   :5432          │     │         └─────────────────┘
│  │                  │     │
│  │ Tables:          │     │
│  │  • leads         │     │
│  │  • campaigns     │     │
│  │                  │     │
│  │ PVC: 5Gi         │     │
│  └──────────────────┘     │
│                            │
│  ┌──────────────────┐     │
│  │ Sales API Domain │     │
│  │   PostgreSQL     │     │
│  │   :5432          │     │
│  │                  │     │
│  │ Tables:          │     │
│  │  • api_logs      │     │
│  │  • metrics       │     │
│  │                  │     │
│  │ PVC: 2Gi         │     │
│  └──────────────────┘     │
│                            │
│  ┌──────────────────┐     │
│  │  Grafana DB      │     │
│  │   PostgreSQL     │     │
│  │   :5432          │     │
│  │                  │     │
│  │ PVC: 1Gi         │     │
│  └──────────────────┘     │
│                            │
└────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                         🔧 TRANSFORMATION LAYER                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

         JupyterHub ──────────────────┐
              │                       │
              │ dbt run               │ dbt docs generate
              ▼                       ▼
    ┌─────────────────┐      ┌────────────────┐
    │  DBT Models     │      │   DBT Docs     │
    │                 │      │   (Nginx)      │
    │ • Staging       │      │   :30082       │
    │ • Marts         │      │                │
    │ • Cross-domain  │      │ • Lineage      │
    │                 │      │ • Tests        │
    │ Sources:        │      │ • Catalog      │
    │  sales DB ──────┼──────┤                │
    │  marketing DB   │      └────────────────┘
    │                 │
    │ Target:         │
    │  Trino/PgSQL    │
    └─────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                      🏗️ INFRASTRUCTURE LAYER (Kubernetes)                             ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

    ┌────────────────────────────────────────────────────────────────────────┐
    │                        Kubernetes Cluster                              │
    │                                                                        │
    │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
    │  │   Namespace:     │  │   Namespace:     │  │   Namespace:     │   │
    │  │  data-platform   │  │  sales-domain    │  │ marketing-domain │   │
    │  │                  │  │                  │  │                  │   │
    │  │ • JupyterHub     │  │ • Sales DB       │  │ • Marketing DB   │   │
    │  │ • Trino          │  │ • Sales API      │  │                  │   │
    │  │ • Minio          │  │ • Sales API DB   │  │                  │   │
    │  │ • Hive           │  │                  │  │                  │   │
    │  │ • Grafana        │  │                  │  │                  │   │
    │  │ • Nginx          │  │                  │  │                  │   │
    │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
    │                                                                        │
    │  Services (NodePort):                                                 │
    │  • JupyterHub:  30080                                                 │
    │  • Trino UI:    30808                                                 │
    │  • Minio:       30900 (API), 30901 (Console)                          │
    │  • Grafana:     30030                                                 │
    │  • DBT Docs:    30082                                                 │
    │  • Sales API:   30081                                                 │
    │                                                                        │
    │  Persistent Volumes:                                                  │
    │  • jupyterhub-pvc:       10Gi                                         │
    │  • minio-pvc:            20Gi                                         │
    │  • sales-db-pvc:         5Gi                                          │
    │  • marketing-db-pvc:     5Gi                                          │
    │  • sales-api-db-pvc:     2Gi                                          │
    │  • grafana-pvc:          1Gi                                          │
    │  • hive-metastore-pvc:   2Gi                                          │
    └────────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                         📦 OPTIONAL COMPONENTS                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

    ┌─────────────────────────────────────────────────────────────────┐
    │  DataHub (Optional - Docker Compose)                            │
    │  Requires: 10-12GB RAM                                          │
    │                                                                 │
    │  • datahub-gms          (Metadata Service)                      │
    │  • datahub-frontend     (Web UI :9002)                          │
    │  • datahub-mae-consumer (Event Consumer)                        │
    │  • datahub-mce-consumer (Change Consumer)                       │
    │  • elasticsearch        (Search)                                │
    │  • neo4j                (Graph)                                 │
    │  • kafka/zookeeper      (Event Bus)                             │
    │  • schema-registry      (Avro Schemas)                          │
    │                                                                 │
    │  Integration:                                                   │
    │    JupyterHub ──► DBT ──► DataHub (metadata ingestion)          │
    └─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Diagram 2: Data Flow Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                     DATA FLOW: User Query to Results                                  ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

 STEP 1: User writes federated query
┌─────────────────────────────────────┐
│  Data Scientist @ JupyterHub        │
│                                     │
│  from trino.dbapi import connect    │
│                                     │
│  query = """                        │
│    SELECT                           │
│      s.customer_name,               │
│      m.campaign_name,               │
│      SUM(s.revenue)                 │
│    FROM sales.public.customers s    │◄─── Query spans 2 domains!
│    JOIN marketing.public.leads m    │
│      ON s.email = m.email           │
│    GROUP BY 1, 2                    │
│  """                                │
│                                     │
│  cursor.execute(query)              │
└─────────────┬───────────────────────┘
              │
              │ ① Submit SQL
              ▼
┌─────────────────────────────────────┐
│     Trino Coordinator               │
│                                     │
│  [Query Parser]                     │
│    └──► Parse SQL                   │
│                                     │
│  [Query Planner]                    │
│    └──► Create execution plan       │
│         • Identify tables           │
│         • Determine join strategy   │
│         • Optimize query            │
│                                     │
│  [Catalog Manager]                  │
│    └──► Resolve table locations     │
└─────────────┬───────────────────────┘
              │
              │ ② Distributed execution plan
              ▼
┌─────────────────────────────────────┐
│       Trino Worker                  │
│                                     │
│  Stage 1: Scan Sales DB             │
│    ┌────────────────────┐           │
│    │ SELECT customer_id,│           │
│    │   customer_name,   │◄──────────┼─── ③ Query sales.customers
│    │   email, revenue   │           │
│    │ FROM customers     │           │
│    └────────────────────┘           │
│           │                         │
│           │ Results: 1000 rows      │
│           ▼                         │
│    ┌────────────────────┐           │
│    │  Memory Buffer     │           │
│    └────────────────────┘           │
│                                     │
│  Stage 2: Scan Marketing DB         │
│    ┌────────────────────┐           │
│    │ SELECT lead_id,    │◄──────────┼─── ④ Query marketing.leads
│    │   email,           │           │
│    │   campaign_name    │           │
│    │ FROM leads         │           │
│    └────────────────────┘           │
│           │                         │
│           │ Results: 2500 rows      │
│           ▼                         │
│    ┌────────────────────┐           │
│    │  Memory Buffer     │           │
│    └────────────────────┘           │
│                                     │
│  Stage 3: Hash Join                 │
│    ┌────────────────────┐           │
│    │ Join on email      │           │
│    │ • Build hash table │           │
│    │ • Probe & match    │           │
│    └────────┬───────────┘           │
│             │                       │
│             │ Results: 850 rows     │
│             ▼                       │
│  Stage 4: Aggregation               │
│    ┌────────────────────┐           │
│    │ GROUP BY           │           │
│    │ customer_name,     │           │
│    │ campaign_name      │           │
│    │                    │           │
│    │ SUM(revenue)       │           │
│    └────────┬───────────┘           │
│             │                       │
│             │ Final: 45 rows        │
└─────────────┼───────────────────────┘
              │
              │ ⑤ Return results
              ▼
┌─────────────────────────────────────┐
│     Trino Coordinator               │
│                                     │
│  [Result Aggregator]                │
│    └──► Combine worker results      │
│                                     │
│  [Result Cache]                     │
│    └──► Cache for reuse             │
└─────────────┬───────────────────────┘
              │
              │ ⑥ Send results
              ▼
┌─────────────────────────────────────┐
│    JupyterHub (Data Scientist)      │
│                                     │
│  df = pd.DataFrame(                 │
│      cursor.fetchall(),             │
│      columns=[...]                  │
│  )                                  │
│                                     │
│  # Results ready in 2.3 seconds!    │
│                                     │
│  df.head()                          │
│    customer_name  campaign  revenue │
│  0 Alice Johnson  Spring    $5,230  │
│  1 Bob Smith      Black Fr  $3,890  │
│  2 Carol White    Spring    $4,120  │
└─────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                    DATA FLOW: DBT Transformation Pipeline                             ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

 STEP 1: Data Scientist runs DBT
┌─────────────────────────────────────┐
│  JupyterHub Terminal                │
│                                     │
│  $ cd ~/dbt_projects                │
│  $ dbt run --profiles-dir .         │
└─────────────┬───────────────────────┘
              │
              │ ① Execute DBT
              ▼
┌─────────────────────────────────────┐
│         DBT Core                    │
│                                     │
│  [Dependency Resolver]              │
│    └──► Analyze model dependencies  │
│         • Read dbt_project.yml      │
│         • Build DAG                 │
│                                     │
│  [Execution Order]                  │
│    1. sources (raw tables)          │
│    2. staging models                │
│    3. marts models                  │
└─────────────┬───────────────────────┘
              │
              │ ② Compiled SQL
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Model: stg_sales__customers                                │
│  Target: sales_analytics.staging                            │
│                                                             │
│  CREATE OR REPLACE VIEW staging.stg_sales__customers AS     │
│  SELECT                                                     │
│    customer_id,                                             │
│    LOWER(TRIM(customer_name)) as customer_name,             │
│    LOWER(TRIM(email)) as email,                             │
│    phone,                                                   │
│    created_at                                               │
│  FROM sales.public.customers                                │
│  WHERE created_at >= CURRENT_DATE - INTERVAL '1 year'       │
└─────────────┬───────────────────────────────────────────────┘
              │
              │ ③ Execute on target
              ▼
       ┌──────────────┐
       │ PostgreSQL   │◄─── Creates view/table
       │ (Sales DB)   │
       └──────────────┘
              │
              │ ④ Success (0.45s)
              ▼
┌─────────────────────────────────────┐
│  Model: mart_customer_journey       │
│  Target: sales_analytics.marts      │
│                                     │
│  Dependencies:                      │
│    • stg_sales__customers ✅        │
│    • stg_marketing__leads ✅        │
└─────────────┬───────────────────────┘
              │
              │ ⑤ Execute complex transformation
              ▼
       ┌──────────────┐
       │   Trino      │◄─── Federated query execution
       │              │
       │ Reads from:  │
       │  • Sales DB  │
       │  • Marketing │
       │              │
       │ Writes to:   │
       │  • Marts DB  │
       └──────────────┘
              │
              │ ⑥ Model built successfully
              ▼
┌─────────────────────────────────────┐
│         DBT Summary                 │
│                                     │
│  Completed successfully             │
│                                     │
│  Done. PASS=8 WARN=0 ERROR=0 SKIP=0 │
│                                     │
│  Models updated:                    │
│    ✅ stg_sales__customers          │
│    ✅ stg_marketing__leads          │
│    ✅ mart_customer_journey         │
│                                     │
│  Tests passed: 12/12                │
└─────────────────────────────────────┘
```

---

## 🌐 Diagram 3: Network & Ports Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                     NETWORK TOPOLOGY & PORT MAPPING                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

                              🌐 EXTERNAL ACCESS (localhost)
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        │ :30080                        │ :30808                       │ :30901
        │ JupyterHub                    │ Trino UI                     │ Minio Console
        │                               │                               │
        │ :30030                        │ :30082                       │ :30081
        │ Grafana                       │ DBT Docs                     │ Sales API
        │                               │                               │
╔═══════▼═══════════════════════════════▼═══════════════════════════════▼═══════════════╗
║                        KUBERNETES SERVICES (NodePort)                                 ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────────────┐
│  NAMESPACE: data-platform                                                            │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Service: proxy-public (JupyterHub)                                                 │
│    • Type: NodePort                                                                 │
│    • Port: 80                                                                       │
│    • NodePort: 30080                                                                │
│    • Target: hub:8000                                                               │
│         └──► Pod: hub-xxxxxxxxx                                                     │
│              └──► Container: hub:8000                                               │
│                   └──► Container: jupyter-user:8888 (spawned)                       │
│                                                                                      │
│  Service: trino-coordinator                                                         │
│    • Type: ClusterIP + NodePort                                                     │
│    • Ports:                                                                         │
│      - 8080  (JDBC/API)                                                             │
│      - 30808 (Web UI - NodePort)                                                    │
│    • Target: trino-coordinator                                                      │
│         └──► Pod: trino-coordinator-0                                               │
│              └──► Container: trinodb/trino:435                                      │
│                                                                                      │
│  Service: trino-worker                                                              │
│    • Type: ClusterIP                                                                │
│    • Port: 8080 (Internal)                                                          │
│    • Target: trino-worker                                                           │
│         └──► Pod: trino-worker-0                                                    │
│              └──► Container: trinodb/trino:435                                      │
│                                                                                      │
│  Service: minio                                                                     │
│    • Type: NodePort                                                                 │
│    • Ports:                                                                         │
│      - 9000  → 30900 (S3 API)                                                       │
│      - 9001  → 30901 (Console)                                                      │
│    • Target: minio                                                                  │
│         └──► Pod: minio-xxxxxxxxx                                                   │
│              └──► Container: minio/minio:latest                                     │
│                                                                                      │
│  Service: hive-metastore                                                            │
│    • Type: ClusterIP (Internal only)                                                │
│    • Port: 9083 (Thrift)                                                            │
│    • Target: hive-metastore                                                         │
│         └──► Pod: hive-metastore-xxxxxxxxx                                          │
│              └──► Container: apache/hive:3.1.3                                      │
│                                                                                      │
│  Service: grafana                                                                   │
│    • Type: NodePort                                                                 │
│    • Port: 3000 → 30030                                                             │
│    • Target: grafana                                                                │
│         └──► Pod: grafana-xxxxxxxxx                                                 │
│              └──► Container: grafana/grafana:latest                                 │
│                                                                                      │
│  Service: nginx-dbt-docs                                                            │
│    • Type: NodePort                                                                 │
│    • Port: 80 → 30082                                                               │
│    • Target: nginx                                                                  │
│         └──► Pod: nginx-dbt-docs-xxxxxxxxx                                          │
│              └──► Container: nginx:alpine                                           │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────┐
│  NAMESPACE: sales-domain                                                             │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Service: sales-db                                                                  │
│    • Type: ClusterIP (Internal only)                                                │
│    • Port: 5432 (PostgreSQL)                                                        │
│    • Target: sales-db                                                               │
│         └──► Pod: sales-db-xxxxxxxxx                                                │
│              └──► Container: postgres:15                                            │
│                   └──► DB: sales_data                                               │
│                        └──► Tables: customers, orders                               │
│                                                                                      │
│  Service: sales-api                                                                 │
│    • Type: NodePort                                                                 │
│    • Port: 5000 → 30081                                                             │
│    • Target: sales-api                                                              │
│         └──► Pod: sales-api-xxxxxxxxx                                               │
│              └──► Container: python:3.11-slim (Flask)                               │
│                                                                                      │
│  Service: sales-api-db                                                              │
│    • Type: ClusterIP (Internal only)                                                │
│    • Port: 5432 (PostgreSQL)                                                        │
│    • Target: sales-api-db                                                           │
│         └──► Pod: sales-api-db-xxxxxxxxx                                            │
│              └──► Container: postgres:15                                            │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────┐
│  NAMESPACE: marketing-domain                                                         │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Service: marketing-db                                                              │
│    • Type: ClusterIP (Internal only)                                                │
│    • Port: 5432 (PostgreSQL)                                                        │
│    • Target: marketing-db                                                           │
│         └──► Pod: marketing-db-xxxxxxxxx                                            │
│              └──► Container: postgres:15                                            │
│                   └──► DB: marketing_data                                           │
│                        └──► Tables: leads, campaigns                                │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                         INTERNAL COMMUNICATION PATHS                                  ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

JupyterHub User Pod
    │
    ├──► Trino Coordinator
    │    (trino-coordinator.data-platform.svc.cluster.local:8080)
    │
    ├──► DBT → Trino
    │    (Same connection as above)
    │
    └──► Direct DB access (if needed)
         └──► sales-db.sales-domain.svc.cluster.local:5432
         └──► marketing-db.marketing-domain.svc.cluster.local:5432

Trino Coordinator
    │
    ├──► Trino Worker
    │    (trino-worker.data-platform.svc.cluster.local:8080)
    │
    ├──► Sales DB (via PostgreSQL connector)
    │    (sales-db.sales-domain.svc.cluster.local:5432)
    │
    ├──► Marketing DB (via PostgreSQL connector)
    │    (marketing-db.marketing-domain.svc.cluster.local:5432)
    │
    └──► Hive Metastore (via Hive connector)
         (hive-metastore.data-platform.svc.cluster.local:9083)
              │
              └──► Minio (S3 API)
                   (minio.data-platform.svc.cluster.local:9000)

Grafana
    │
    ├──► Sales DB
    │    (sales-db.sales-domain.svc.cluster.local:5432)
    │
    ├──► Marketing DB
    │    (marketing-db.marketing-domain.svc.cluster.local:5432)
    │
    └──► Sales API DB
         (sales-api-db.sales-domain.svc.cluster.local:5432)

Hive Metastore
    │
    └──► PostgreSQL (metadata backend)
         (hive-metastore-db.data-platform.svc.cluster.local:5432)
```

---

## 🎭 Diagram 4: User Personas & Access Patterns

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                          USER PERSONAS & WORKFLOWS                                    ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  👨‍💻 PERSONA 1: Data Scientist (Alex)                                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Daily Workflow:                                                                    │
│                                                                                     │
│  09:00  Login to JupyterHub                                                         │
│         └──► http://localhost:30080                                                 │
│              Username: alex                                                         │
│                                                                                     │
│  09:05  Create new notebook: customer_analysis.ipynb                                │
│         └──► File → New → Notebook                                                  │
│                                                                                     │
│  09:10  Explore data with Trino                                                     │
│         ┌────────────────────────────────────────┐                                  │
│         │ from trino.dbapi import connect        │                                  │
│         │ conn = connect(                        │                                  │
│         │   host='trino-coordinator...',         │                                  │
│         │   port=8080                            │                                  │
│         │ )                                      │                                  │
│         │ cursor = conn.cursor()                 │                                  │
│         │ cursor.execute("SHOW CATALOGS")        │                                  │
│         └────────────────────────────────────────┘                                  │
│                  │                                                                   │
│                  ├──► Access: sales.public.customers                                 │
│                  ├──► Access: marketing.public.leads                                 │
│                  └──► Access: hive.default.* (data lake)                             │
│                                                                                     │
│  09:30  Write federated query                                                       │
│         └──► Query spans Sales + Marketing domains                                  │
│              Results in < 3 seconds                                                 │
│                                                                                     │
│  10:00  Build DBT model for reusability                                             │
│         ┌────────────────────────────────────────┐                                  │
│         │ $ cd ~/dbt_projects                    │                                  │
│         │ $ dbt run --models mart_*              │                                  │
│         │ $ dbt test                             │                                  │
│         │ $ dbt docs generate                    │                                  │
│         └────────────────────────────────────────┘                                  │
│                                                                                     │
│  10:30  Create visualizations                                                       │
│         └──► matplotlib/seaborn in notebook                                         │
│              OR                                                                     │
│         └──► Share query with Grafana team                                          │
│                                                                                     │
│  11:00  Upload results to data lake                                                 │
│         ┌────────────────────────────────────────┐                                  │
│         │ import boto3                           │                                  │
│         │ s3 = boto3.client('s3',                │                                  │
│         │   endpoint='minio:9000')               │                                  │
│         │ s3.upload_file('results.parquet',      │                                  │
│         │   'datalake', 'analytics/...')         │                                  │
│         └────────────────────────────────────────┘                                  │
│                                                                                     │
│  Tools Used:                                                                        │
│    ✅ JupyterHub (workspace)                                                        │
│    ✅ Trino (federated queries)                                                     │
│    ✅ DBT (transformations)                                                         │
│    ✅ Python (pandas, matplotlib)                                                   │
│    ✅ Minio (data lake storage)                                                     │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  👔 PERSONA 2: Business Analyst (Sarah)                                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Daily Workflow:                                                                    │
│                                                                                     │
│  08:30  Login to Grafana                                                            │
│         └──► http://localhost:30030                                                 │
│              Username: sarah                                                        │
│                                                                                     │
│  08:35  Open pre-built dashboards                                                   │
│         ├──► Sales Performance Dashboard                                            │
│         ├──► Marketing Campaign ROI                                                 │
│         └──► Customer Journey Analytics                                             │
│                                                                                     │
│  09:00  Explore metrics                                                             │
│         └──► Filter by date range                                                   │
│         └──► Drill down by campaign                                                 │
│         └──► Export to PDF for meeting                                              │
│                                                                                     │
│  10:00  Create new visualization                                                    │
│         ┌────────────────────────────────────────┐                                  │
│         │ Add Panel → Query Builder              │                                  │
│         │   Data Source: PostgreSQL (Sales)      │                                  │
│         │   Query: SELECT ... FROM               │                                  │
│         │     mart_customer_journey              │                                  │
│         │   Visualization: Time Series           │                                  │
│         └────────────────────────────────────────┘                                  │
│                                                                                     │
│  11:00  Set up alerts                                                               │
│         └──► Alert if conversion rate < 20%                                         │
│         └──► Notify via email                                                       │
│                                                                                     │
│  Tools Used:                                                                        │
│    ✅ Grafana (visualization)                                                       │
│    ✅ DBT marts (pre-built by data team)                                            │
│    ❌ No need for JupyterHub/Python!                                                │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  🔧 PERSONA 3: Data Engineer (Mike)                                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Daily Workflow:                                                                    │
│                                                                                     │
│  08:00  Check system health                                                         │
│         ├──► Trino Web UI (query performance)                                       │
│         ├──► Minio Console (storage usage)                                          │
│         └──► Grafana (system metrics)                                               │
│                                                                                     │
│  09:00  Deploy new DBT models                                                       │
│         ┌────────────────────────────────────────┐                                  │
│         │ $ kubectl exec -it                     │                                  │
│         │   jupyter-admin -n data-platform       │                                  │
│         │   -- bash                              │                                  │
│         │ $ cd ~/dbt_projects                    │                                  │
│         │ $ dbt run --full-refresh               │                                  │
│         └────────────────────────────────────────┘                                  │
│                                                                                     │
│  10:00  Add new data source                                                         │
│         └──► Edit Trino catalog configuration                                       │
│         └──► Create new PostgreSQL connector                                        │
│         └──► Update Hive metadata                                                   │
│                                                                                     │
│  11:00  Monitor data quality                                                        │
│         └──► Run DBT tests                                                          │
│         └──► Check test results                                                     │
│         └──► Fix issues if any                                                      │
│                                                                                     │
│  14:00  Optimize Trino queries                                                      │
│         └──► Analyze slow queries                                                   │
│         └──► Add table statistics                                                   │
│         └──► Create partitions if needed                                            │
│                                                                                     │
│  Tools Used:                                                                        │
│    ✅ kubectl (Kubernetes management)                                               │
│    ✅ Trino Web UI (monitoring)                                                     │
│    ✅ JupyterHub (DBT development)                                                  │
│    ✅ Minio Console (storage management)                                            │
│    ✅ DBT (pipeline orchestration)                                                  │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  👑 PERSONA 4: Executive (Emma)                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Daily Workflow:                                                                    │
│                                                                                     │
│  09:00  Login to Grafana (read-only)                                                │
│         └──► http://localhost:30030                                                 │
│                                                                                     │
│  09:05  View Executive Dashboard                                                    │
│         ├──► KPI Overview (Revenue, Customers, Conversion)                          │
│         ├──► Trend Analysis (Week-over-week, Month-over-month)                      │
│         └──► Department Performance (Sales vs Marketing)                            │
│                                                                                     │
│  09:15  Export report for board meeting                                             │
│         └──► Export as PDF                                                          │
│         └──► Share via email                                                        │
│                                                                                     │
│  Tools Used:                                                                        │
│    ✅ Grafana only (no technical skills needed!)                                    │
│    ❌ Never touches JupyterHub, Trino, or DBT                                       │
│                                                                                     │
│  Benefits:                                                                          │
│    • Real-time data                                                                 │
│    • No waiting for IT                                                              │
│    • Self-service insights                                                          │
│    • No SQL knowledge required                                                      │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Diagram 5: Security & Access Control

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                       SECURITY LAYERS & ACCESS CONTROL                                ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: Network Security                                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Kubernetes Network Policies:                                                       │
│                                                                                     │
│    ┌──────────────────────────────────────────────────────────────┐                │
│    │  Default: Deny all traffic                                   │                │
│    └──────────────────────────────────────────────────────────────┘                │
│                                                                                     │
│    Allowed ingress:                                                                 │
│      ✅ data-platform → sales-domain (DB access)                                    │
│      ✅ data-platform → marketing-domain (DB access)                                │
│      ✅ JupyterHub → Trino (query execution)                                        │
│      ✅ Trino → Hive (metadata)                                                     │
│      ✅ Trino → Minio (data lake)                                                   │
│      ✅ Grafana → All databases (read-only)                                         │
│                                                                                     │
│    Blocked:                                                                         │
│      ❌ sales-domain ↔ marketing-domain (direct communication)                      │
│      ❌ External → Internal databases (no direct access)                            │
│                                                                                     │
│  Port Exposure:                                                                     │
│      NodePort (external):  30xxx                                                    │
│      ClusterIP (internal): Service ports only                                       │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LAYER 2: Authentication                                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  JupyterHub Authentication:                                                         │
│    • Username/Password (admin / datamesh2024)                                       │
│    • Can be extended to:                                                            │
│      - LDAP/Active Directory                                                        │
│      - OAuth (Google, GitHub)                                                       │
│      - SAML                                                                         │
│                                                                                     │
│  Grafana Authentication:                                                            │
│    • Username/Password (admin / datamesh2024)                                       │
│    • Built-in user management                                                       │
│    • Role-based access (Viewer, Editor, Admin)                                      │
│                                                                                     │
│  Minio Authentication:                                                              │
│    • Access Key / Secret Key                                                        │
│    • S3 signature authentication                                                    │
│    • Bucket policies                                                                │
│                                                                                     │
│  Database Authentication:                                                           │
│    • PostgreSQL: username/password                                                  │
│    • Trino: pass-through to connectors                                              │
│    • Hive: Kerberos (optional, not enabled)                                         │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LAYER 3: Authorization (Data Access)                                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Current Setup (Academic):                                                          │
│    • All authenticated users have full access                                       │
│    • No row-level security                                                          │
│    • No column masking                                                              │
│                                                                                     │
│  Production-Ready Options (can be added):                                           │
│                                                                                     │
│    ┌────────────────────────────────────────────────────────────┐                  │
│    │  Trino Access Control                                      │                  │
│    ├────────────────────────────────────────────────────────────┤                  │
│    │                                                            │                  │
│    │  File-based:                                               │                  │
│    │    • access-control.properties                             │                  │
│    │    • rules.json                                            │                  │
│    │                                                            │                  │
│    │  Example rules:                                            │                  │
│    │    {                                                       │                  │
│    │      "catalogs": [                                         │                  │
│    │        {                                                   │                  │
│    │          "user": "sales_team",                             │                  │
│    │          "catalog": "sales",                               │                  │
│    │          "allow": "all"                                    │                  │
│    │        },                                                  │                  │
│    │        {                                                   │                  │
│    │          "user": "sales_team",                             │                  │
│    │          "catalog": "marketing",                           │                  │
│    │          "allow": "read-only"                              │                  │
│    │        }                                                   │                  │
│    │      ]                                                     │                  │
│    │    }                                                       │                  │
│    └────────────────────────────────────────────────────────────┘                  │
│                                                                                     │
│    PostgreSQL Row-Level Security (RLS):                                             │
│      • Can restrict rows based on user                                              │
│      • Example: Users only see their department's data                              │
│                                                                                     │
│    Ranger Integration (Advanced):                                                   │
│      • Centralized access control                                                   │
│      • Fine-grained policies                                                        │
│      • Audit logging                                                                │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LAYER 4: Data Encryption                                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  In Transit:                                                                        │
│    Current:  ❌ HTTP (local development)                                            │
│    Production: ✅ HTTPS/TLS (recommended)                                           │
│      • Add TLS certificates                                                         │
│      • Configure Ingress with TLS                                                   │
│      • Enable HTTPS in all services                                                 │
│                                                                                     │
│  At Rest:                                                                           │
│    Current:  ⚠️  Kubernetes PVC (default storage)                                   │
│    Production: ✅ Encrypted volumes                                                 │
│      • Enable volume encryption                                                     │
│      • Use encrypted storage class                                                  │
│      • Encrypt database backups                                                     │
│                                                                                     │
│  Secrets Management:                                                                │
│    Current:  ⚠️  Kubernetes Secrets (base64)                                        │
│    Production: ✅ Vault or Sealed Secrets                                           │
│      • HashiCorp Vault integration                                                  │
│      • Sealed Secrets (encrypted at rest)                                           │
│      • Rotate credentials regularly                                                 │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LAYER 5: Audit & Monitoring                                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Query Auditing:                                                                    │
│    • Trino query history (UI)                                                       │
│    • PostgreSQL query logs                                                          │
│    • DBT run logs                                                                   │
│                                                                                     │
│  Access Logs:                                                                       │
│    • JupyterHub access logs                                                         │
│    • Grafana audit trail                                                            │
│    • Kubernetes audit logs                                                          │
│                                                                                     │
│  Can be enhanced with:                                                              │
│    • Elasticsearch + Kibana (log aggregation)                                       │
│    • Prometheus + Grafana (metrics)                                                 │
│    • DataHub lineage (who accessed what)                                            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

**📚 How to Use These Diagrams:**

1. **Diagram 1**: Show overall technical architecture
2. **Diagram 2**: Explain data flow during queries
3. **Diagram 3**: Reference for network configuration
4. **Diagram 4**: Present user workflows to stakeholders
5. **Diagram 5**: Discuss security with IT/compliance team

**💡 Tip:** These diagrams are also great for:
- Academic presentations
- Technical documentation
- Onboarding new team members
- Architecture review meetings

