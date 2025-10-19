# ☁️ Architecture Hybride AWS + Local

**Maximiser 200 USD de crédits AWS pour un projet académique Data Mesh**

---

## 🎯 Stratégie

### ✅ Local (Votre Machine - Gratuit)
- JupyterHub (développement)
- Trino (queries)
- Grafana (dashboards)
- Outils de développement

### ☁️ AWS (Cloud - 200 USD)
- RDS PostgreSQL (bases de données production-like)
- S3 (data lake au lieu de Minio)
- IAM (authentication production)
- CloudWatch (monitoring)
- Optionnel: EC2 pour services lourds

---

## 💰 Estimation Budget AWS (200 USD)

### 📊 Configuration Recommandée

| Service | Spécifications | Coût/Mois | Durée | Total |
|---------|---------------|-----------|-------|-------|
| **RDS PostgreSQL (Sales)** | db.t3.micro (2vCPU, 1GB RAM) | $15 | 3 mois | $45 |
| **RDS PostgreSQL (Marketing)** | db.t3.micro (2vCPU, 1GB RAM) | $15 | 3 mois | $45 |
| **S3 Storage** | 50GB + 10K requests | $5 | 3 mois | $15 |
| **EC2 (Optionnel)** | t3.medium (2vCPU, 4GB RAM) | $30 | 2 mois | $60 |
| **CloudWatch** | Logs + Metrics | $5 | 3 mois | $15 |
| **Data Transfer** | Sortant vers votre machine | $5 | 3 mois | $15 |
| **TOTAL** | | | | **$195** |

**Marge restante:** 5 USD

---

## 🏗️ Architecture Hybride Détaillée

```
┌──────────────────────────────────────────────────────────────────┐
│                    VOTRE MACHINE LOCALE                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  JupyterHub  │  │    Trino     │  │   Grafana    │          │
│  │ (Dev & Query)│  │ (Federated)  │  │ (Dashboards) │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                    📡 Internet (HTTPS)
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                         AWS CLOUD                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🗄️  RDS PostgreSQL (Sales)                             │   │
│  │     • Endpoint: sales.xxxxx.rds.amazonaws.com            │   │
│  │     • Port: 5432                                         │   │
│  │     • Storage: 20GB SSD                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🗄️  RDS PostgreSQL (Marketing)                         │   │
│  │     • Endpoint: marketing.xxxxx.rds.amazonaws.com        │   │
│  │     • Port: 5432                                         │   │
│  │     • Storage: 20GB SSD                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  📦 S3 Bucket (Data Lake)                                │   │
│  │     • Bucket: datamesh-datalake-[votre-nom]              │   │
│  │     • Region: us-east-1                                  │   │
│  │     • Storage: 50GB                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🔐 IAM (Users & Roles)                                  │   │
│  │     • admin (full access)                                │   │
│  │     • sales_analyst (Sales DB only)                      │   │
│  │     • marketing_analyst (Marketing DB only)              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  📊 CloudWatch (Monitoring)                              │   │
│  │     • DB Performance Insights                            │   │
│  │     • Query Logs                                         │   │
│  │     • Cost Tracking                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Plan de Déploiement

### Étape 1: Configuration AWS (1-2 heures)

#### 1.1 Créer les RDS PostgreSQL

```bash
# Sales Database
aws rds create-db-instance \
    --db-instance-identifier datamesh-sales \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password YourSecurePassword123! \
    --allocated-storage 20 \
    --publicly-accessible \
    --backup-retention-period 7 \
    --tags Key=Project,Value=DataMeesh

# Marketing Database
aws rds create-db-instance \
    --db-instance-identifier datamesh-marketing \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password YourSecurePassword123! \
    --allocated-storage 20 \
    --publicly-accessible \
    --backup-retention-period 7 \
    --tags Key=Project,Value=DataMeesh
```

#### 1.2 Créer S3 Bucket

```bash
# Data Lake
aws s3 mb s3://datamesh-datalake-votrenom --region us-east-1

# Configure public access (démo seulement)
aws s3api put-bucket-versioning \
    --bucket datamesh-datalake-votrenom \
    --versioning-configuration Status=Enabled
```

#### 1.3 Créer IAM Users

```bash
# Admin user
aws iam create-user --user-name datamesh-admin

# Sales analyst
aws iam create-user --user-name datamesh-sales-analyst

# Marketing analyst
aws iam create-user --user-name datamesh-marketing-analyst

# Créer access keys
aws iam create-access-key --user-name datamesh-admin
```

---

### Étape 2: Configuration Locale (30 minutes)

#### 2.1 Mettre à jour Trino pour AWS

**Créer:** `config/trino-catalogs-aws.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-catalogs-aws
  namespace: data-platform
data:
  # Sales RDS PostgreSQL
  sales.properties: |
    connector.name=postgresql
    connection-url=jdbc:postgresql://sales.xxxxx.us-east-1.rds.amazonaws.com:5432/sales_db
    connection-user=admin
    connection-password=YourSecurePassword123!
    
  # Marketing RDS PostgreSQL
  marketing.properties: |
    connector.name=postgresql
    connection-url=jdbc:postgresql://marketing.xxxxx.us-east-1.rds.amazonaws.com:5432/marketing_db
    connection-user=admin
    connection-password=YourSecurePassword123!
    
  # S3 Data Lake (via Hive)
  hive.properties: |
    connector.name=hive
    hive.metastore=glue  # AWS Glue Catalog (gratuit avec free tier)
    hive.s3.aws-access-key=AKIAIOSFODNN7EXAMPLE
    hive.s3.aws-secret-key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    hive.s3.region=us-east-1
    hive.non-managed-table-writes-enabled=true
```

#### 2.2 Script de Connexion Python

**Créer:** `examples/connect_aws.py`

```python
#!/usr/bin/env python3
"""
Connect to AWS RDS from local JupyterHub
"""

import psycopg2
from trino.dbapi import connect
import boto3

# ============================================
# 1. Connect to AWS RDS PostgreSQL
# ============================================

def connect_sales_rds():
    """Connect to Sales RDS"""
    conn = psycopg2.connect(
        host='sales.xxxxx.us-east-1.rds.amazonaws.com',
        port=5432,
        database='sales_db',
        user='admin',
        password='YourSecurePassword123!'
    )
    return conn

def connect_marketing_rds():
    """Connect to Marketing RDS"""
    conn = psycopg2.connect(
        host='marketing.xxxxx.us-east-1.rds.amazonaws.com',
        port=5432,
        database='marketing_db',
        user='admin',
        password='YourSecurePassword123!'
    )
    return conn

# ============================================
# 2. Query via Trino (Federated)
# ============================================

def query_via_trino():
    """Federated query across AWS RDS databases"""
    conn = connect(
        host='trino-coordinator.data-platform.svc.cluster.local',
        port=8080,
        user='admin'
    )
    
    cursor = conn.cursor()
    
    # Cross-domain query (Sales + Marketing on AWS)
    cursor.execute("""
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
        LIMIT 10
    """)
    
    results = cursor.fetchall()
    return results

# ============================================
# 3. Upload to S3 Data Lake
# ============================================

def upload_to_s3(file_path, s3_key):
    """Upload file to S3 data lake"""
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
        aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        region_name='us-east-1'
    )
    
    bucket = 'datamesh-datalake-votrenom'
    s3.upload_file(file_path, bucket, s3_key)
    
    print(f"✅ Uploaded to s3://{bucket}/{s3_key}")

# ============================================
# 4. Query S3 via Trino
# ============================================

def query_s3_data():
    """Query data lake on S3 via Trino"""
    conn = connect(
        host='trino-coordinator.data-platform.svc.cluster.local',
        port=8080,
        user='admin',
        catalog='hive',
        schema='default'
    )
    
    cursor = conn.cursor()
    
    # Create external table pointing to S3
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_events (
            event_id VARCHAR,
            customer_id BIGINT,
            event_type VARCHAR,
            event_date DATE
        )
        WITH (
            external_location = 's3://datamesh-datalake-votrenom/events/',
            format = 'PARQUET'
        )
    """)
    
    # Query S3 data
    cursor.execute("SELECT * FROM customer_events LIMIT 10")
    return cursor.fetchall()

# ============================================
# Example Usage
# ============================================

if __name__ == "__main__":
    print("🌐 Connecting to AWS...")
    
    # Test Sales RDS
    print("\n📊 Querying Sales RDS...")
    sales_conn = connect_sales_rds()
    cursor = sales_conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    print(f"Sales customers: {cursor.fetchone()[0]}")
    
    # Test Federated Query
    print("\n🔗 Federated query (Sales + Marketing on AWS)...")
    results = query_via_trino()
    for row in results:
        print(row)
    
    # Test S3 upload
    print("\n📦 Uploading to S3...")
    upload_to_s3('/home/jovyan/data/dataset.csv', 'datasets/dataset.csv')
    
    print("\n✅ AWS Hybrid Architecture Working!")
```

---

### Étape 3: Load Sample Data to AWS

**Créer:** `setup/aws/load_data_to_rds.py`

```python
#!/usr/bin/env python3
"""
Load sample data to AWS RDS PostgreSQL
"""

import psycopg2
import os

# Configuration
SALES_RDS_ENDPOINT = os.getenv('SALES_RDS_ENDPOINT', 'sales.xxxxx.rds.amazonaws.com')
MARKETING_RDS_ENDPOINT = os.getenv('MARKETING_RDS_ENDPOINT', 'marketing.xxxxx.rds.amazonaws.com')
DB_PASSWORD = os.getenv('RDS_PASSWORD', 'YourSecurePassword123!')

def load_sales_data():
    """Load sales data to RDS"""
    conn = psycopg2.connect(
        host=SALES_RDS_ENDPOINT,
        port=5432,
        database='sales_db',
        user='admin',
        password=DB_PASSWORD
    )
    
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert sample data
    cursor.execute("""
        INSERT INTO customers (customer_name, email, phone) VALUES
        ('Alice Johnson', 'alice@example.com', '555-1001'),
        ('Bob Smith', 'bob@example.com', '555-1002'),
        ('Carol White', 'carol@example.com', '555-1003')
    """)
    
    conn.commit()
    print("✅ Sales data loaded to RDS")

def load_marketing_data():
    """Load marketing data to RDS"""
    conn = psycopg2.connect(
        host=MARKETING_RDS_ENDPOINT,
        port=5432,
        database='marketing_db',
        user='admin',
        password=DB_PASSWORD
    )
    
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            campaign_id SERIAL PRIMARY KEY,
            campaign_name VARCHAR(100),
            budget DECIMAL(10,2),
            start_date DATE,
            end_date DATE
        )
    """)
    
    # Insert sample data
    cursor.execute("""
        INSERT INTO campaigns (campaign_name, budget, start_date, end_date) VALUES
        ('Spring Sale 2024', 50000.00, '2024-03-01', '2024-03-31'),
        ('Black Friday', 100000.00, '2024-11-25', '2024-11-30')
    """)
    
    conn.commit()
    print("✅ Marketing data loaded to RDS")

if __name__ == "__main__":
    print("📤 Loading data to AWS RDS...")
    load_sales_data()
    load_marketing_data()
    print("✅ All data loaded!")
```

---

## 💡 Avantages de l'Architecture Hybride

### ✅ Pour Votre Projet Académique:

1. **Professional Look**
   - Architecture cloud-native réelle
   - AWS sur le CV
   - Démo impressive pour jurys/recruteurs

2. **Cost-Efficient**
   - Local: Gratuit (déjà votre machine)
   - AWS: Seulement 195 USD pour 3 mois
   - 5 USD de marge

3. **Scalability Demo**
   - Montrer comment scaler avec le cloud
   - RDS = production-ready databases
   - S3 = unlimited storage

4. **Real-World Skills**
   - IAM authentication
   - RDS management
   - S3 integration
   - CloudWatch monitoring

5. **RBAC Gratuit**
   - IAM users = RBAC natif AWS
   - Policies pour limiter accès
   - Audit logs automatiques

---

## 📊 Monitoring avec CloudWatch

```python
# Dashboard automatique
import boto3

cloudwatch = boto3.client('cloudwatch')

# Créer alarme si coût > 180 USD
cloudwatch.put_metric_alarm(
    AlarmName='DataMeesh-Budget-Alert',
    MetricName='EstimatedCharges',
    Namespace='AWS/Billing',
    Statistic='Maximum',
    Period=86400,
    EvaluationPeriods=1,
    Threshold=180.0,
    ComparisonOperator='GreaterThanThreshold',
    AlarmActions=['arn:aws:sns:us-east-1:xxx:billing-alerts']
)
```

---

## 🎓 Points Forts pour Présentation Académique

### Slide 1: Architecture
```
"Architecture Hybride Moderne:
 • Local K8s pour development velocity
 • AWS Cloud pour production scalability
 • Best of both worlds"
```

### Slide 2: Technologies
```
"Technologies Enterprise:
 • AWS RDS (managed databases)
 • S3 (data lake)
 • IAM (authentication)
 • Trino (federated queries)
 • JupyterHub (data science)"
```

### Slide 3: Cost Optimization
```
"Budget-Conscious Design:
 • Total: 195 USD / 3 mois
 • RDS: 90 USD (2 databases)
 • S3: 15 USD (50GB)
 • Remaining: 90 USD flexible"
```

---

## 🚀 Script de Déploiement Complet

**Créer:** `setup/aws/deploy_aws_hybrid.py`

```python
#!/usr/bin/env python3
"""
Deploy DataMeesh AWS Hybrid Architecture
"""

import boto3
import time
import os
from getpass import getpass

def deploy_rds():
    """Deploy RDS PostgreSQL instances"""
    rds = boto3.client('rds', region_name='us-east-1')
    
    password = getpass("Enter RDS master password: ")
    
    print("🚀 Creating Sales RDS...")
    rds.create_db_instance(
        DBInstanceIdentifier='datamesh-sales',
        DBInstanceClass='db.t3.micro',
        Engine='postgres',
        MasterUsername='admin',
        MasterUserPassword=password,
        AllocatedStorage=20,
        PubliclyAccessible=True,
        BackupRetentionPeriod=7,
        Tags=[{'Key': 'Project', 'Value': 'DataMeesh'}]
    )
    
    print("🚀 Creating Marketing RDS...")
    rds.create_db_instance(
        DBInstanceIdentifier='datamesh-marketing',
        DBInstanceClass='db.t3.micro',
        Engine='postgres',
        MasterUsername='admin',
        MasterUserPassword=password,
        AllocatedStorage=20,
        PubliclyAccessible=True,
        BackupRetentionPeriod=7,
        Tags=[{'Key': 'Project', 'Value': 'DataMeesh'}]
    )
    
    print("⏳ Waiting for RDS instances... (5-10 minutes)")
    
    return password

def deploy_s3():
    """Deploy S3 bucket"""
    s3 = boto3.client('s3', region_name='us-east-1')
    
    bucket_name = f"datamesh-datalake-{os.getenv('USER', 'user')}"
    
    print(f"🚀 Creating S3 bucket: {bucket_name}")
    s3.create_bucket(Bucket=bucket_name)
    
    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    
    return bucket_name

def main():
    print("\n" + "="*70)
    print("☁️  DataMeesh - AWS Hybrid Deployment")
    print("="*70 + "\n")
    
    # Deploy
    password = deploy_rds()
    bucket = deploy_s3()
    
    print("\n" + "="*70)
    print("✅ AWS Resources Created!")
    print("="*70 + "\n")
    
    print("📝 Save these credentials:")
    print(f"   RDS Password: {password}")
    print(f"   S3 Bucket: {bucket}")
    print("\n⏳ Wait 10 minutes for RDS to be ready, then run:")
    print("   python setup/aws/load_data_to_rds.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
```

---

## 🎯 Résumé: Votre Configuration Idéale

### Local (Votre Machine):
- JupyterHub
- Trino
- Grafana
- Development

### AWS (200 USD):
- 2x RDS PostgreSQL (Sales + Marketing)
- S3 Data Lake
- IAM (RBAC gratuit!)
- CloudWatch

### Durée:
- **3 mois complets** avec ce budget

### Compétences Démontrées:
- ✅ Data Mesh architecture
- ✅ Hybrid cloud
- ✅ AWS expertise
- ✅ Cost optimization
- ✅ Production-ready setup

---

**Voulez-vous que je crée les scripts de déploiement AWS?** 🚀

