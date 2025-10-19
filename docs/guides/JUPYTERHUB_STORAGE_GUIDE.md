# 📦 JupyterHub Storage Guide

**Where are data scientist files stored in DataMeesh?**

---

## 🎯 Quick Answer

Files uploaded by data scientists in JupyterHub are stored in:

```
📂 Kubernetes Persistent Volumes (PVC)
   ↓
💾 Docker Desktop's internal storage
   ↓
🖥️ Your local machine: C:\ProgramData\DockerDesktop\vm-data\
```

Each user gets **5GB of persistent storage** that survives pod restarts!

---

## 🏗️ Storage Architecture

```
┌─────────────────────────────────────────────────────┐
│          DATA SCIENTIST (JupyterHub User)           │
│  Uploads: notebooks, CSV, models, datasets          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  JupyterHub Pod      │
          │  User: admin         │
          │  /home/jovyan/       │ ← Working directory
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ PersistentVolumeClaim│
          │ claim-admin          │
          │ Size: 5Gi            │
          │ Class: datamesh-storage
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Kubernetes PV       │
          │  /var/lib/docker/... │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Docker Desktop VM   │
          │  C:\ProgramData\...  │
          └──────────────────────┘
```

---

## 📁 Storage Configuration

### From `jupyterhub-values.yaml`

```yaml
singleuser:
  storage:
    type: dynamic              # Automatic PVC creation
    capacity: 5Gi             # 5GB per user
    dynamic:
      storageClass: datamesh-storage  # StorageClass name
```

### What This Means:

1. **Per-User Volumes**: Each JupyterHub user gets their own 5GB volume
2. **Dynamic Creation**: PVC is created automatically when user logs in
3. **Persistent**: Files survive pod restarts and recreations
4. **Isolated**: Users cannot access each other's files

---

## 🔍 Verify Storage

### Check PVCs (Persistent Volume Claims)

```bash
# List all JupyterHub PVCs
kubectl get pvc -n jupyterhub

# Expected output:
# NAME                 STATUS   VOLUME       CAPACITY   STORAGECLASS
# claim-admin          Bound    pvc-xxxxx    5Gi        datamesh-storage
# claim-datascientist  Bound    pvc-yyyyy    5Gi        datamesh-storage
```

### Check Persistent Volumes

```bash
# List all PVs
kubectl get pv

# Shows the actual volumes backing the claims
```

### Check Storage Usage

```bash
# From JupyterHub terminal
df -h /home/jovyan

# Shows used/available space
```

---

## 📂 User Directory Structure

When you log into JupyterHub, your files are in:

```
/home/jovyan/                    ← Your persistent directory
├── .local/                      ← pip install --user packages
├── dbt_projects/                ← DBT projects
│   └── datamesh/
├── notebooks/                   ← Your Jupyter notebooks
├── data/                        ← Uploaded datasets
│   ├── sales_data.csv
│   └── customer_list.xlsx
├── scripts/                     ← Python scripts
└── models/                      ← ML models
```

**Everything in `/home/jovyan/` is persistent!**

---

## 📤 Uploading Files

### Method 1: JupyterHub Web UI

1. Open JupyterHub: http://localhost:30080
2. Login with any username / `datamesh2024`
3. Click **Upload** button (top right)
4. Select files from your computer
5. Files appear in `/home/jovyan/`

### Method 2: Terminal (from JupyterHub)

```bash
# In JupyterHub terminal
cd /home/jovyan/data
wget https://example.com/dataset.csv

# Or use curl
curl -O https://example.com/dataset.csv
```

### Method 3: kubectl cp (from your machine)

```bash
# Get user pod name
kubectl get pods -n jupyterhub | grep jupyter-admin

# Copy file from your machine to JupyterHub
kubectl cp myfile.csv jupyterhub/jupyter-admin:/home/jovyan/data/myfile.csv

# Copy file from JupyterHub to your machine
kubectl cp jupyterhub/jupyter-admin:/home/jovyan/data/results.csv ./results.csv
```

### Method 4: Git Clone

```bash
# In JupyterHub terminal
cd /home/jovyan
git clone https://github.com/yourrepo/your-project.git
```

---

## 💾 Uploading to Data Lake (Minio)

For large datasets, upload to **Minio** (data lake) instead of JupyterHub:

### Python Script (from JupyterHub)

```python
import boto3
from botocore.client import Config

# Configure Minio client
s3 = boto3.client(
    's3',
    endpoint_url='http://minio.data-platform.svc.cluster.local:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    config=Config(signature_version='s3v4')
)

# Create bucket
s3.create_bucket(Bucket='datalake')

# Upload file
s3.upload_file(
    '/home/jovyan/data/big_dataset.csv',
    'datalake',
    'datasets/big_dataset.csv'
)

print("✅ File uploaded to Minio data lake!")
```

### Using mc (Minio Client)

```bash
# In JupyterHub terminal
pip install minio

# Configure mc
mc alias set myminio http://minio.data-platform.svc.cluster.local:9000 minioadmin minioadmin

# Upload file
mc cp /home/jovyan/data/dataset.csv myminio/datalake/datasets/

# List files
mc ls myminio/datalake/datasets/
```

---

## 🔄 Data Persistence

### What Persists:

✅ **User files** in `/home/jovyan/`  
✅ **Notebooks** (.ipynb files)  
✅ **Datasets** (CSV, Excel, JSON, etc.)  
✅ **Installed packages** (`pip install --user`)  
✅ **Git repositories**  
✅ **DBT projects**

### What Doesn't Persist:

❌ **Running kernel state** (variables in memory)  
❌ **Temporary files** in `/tmp/`  
❌ **System-wide packages** (install with `--user` flag)  
❌ **Environment variables** (unless in `~/.bashrc`)

---

## 🔒 Data Security

### Per-User Isolation

```bash
# User "admin" CANNOT access user "datascientist" files
# Each PVC is bound to one user only
```

### Backup PVCs

```bash
# Create backup of user's data
kubectl exec -n jupyterhub jupyter-admin -- tar czf /tmp/backup.tar.gz /home/jovyan

# Copy backup to your machine
kubectl cp jupyterhub/jupyter-admin:/tmp/backup.tar.gz ./backup_admin_$(date +%Y%m%d).tar.gz
```

---

## 📊 Storage Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| **Per-User Storage** | 5Gi | PVC capacity |
| **Total Users** | ~10 | At 5Gi each = 50Gi total |
| **Max File Size** | 5Gi | Limited by PVC size |
| **Upload Speed** | ~50MB/s | Network dependent |

---

## 🐛 Troubleshooting

### Issue: "No space left on device"

**Cause**: User has used all 5GB

**Solution 1 - Clean up files:**
```bash
# In JupyterHub terminal
du -sh /home/jovyan/*  # Find large directories

# Delete old files
rm -rf /home/jovyan/data/old_datasets/
```

**Solution 2 - Increase PVC size:**
```bash
# Edit PVC
kubectl edit pvc claim-admin -n jupyterhub

# Change:
spec:
  resources:
    requests:
      storage: 10Gi  # Increase from 5Gi to 10Gi
```

### Issue: "Files disappeared after pod restart"

**Cause**: Files were saved outside `/home/jovyan/`

**Solution**: Always save files in `/home/jovyan/`
```bash
# Wrong (not persistent):
/tmp/myfile.csv

# Correct (persistent):
/home/jovyan/data/myfile.csv
```

### Issue: "Cannot access PVC"

**Check PVC status:**
```bash
kubectl get pvc -n jupyterhub
kubectl describe pvc claim-admin -n jupyterhub
```

---

## 🚀 Advanced: Shared Storage

If you want **shared storage** between users:

### Option 1: Minio (Data Lake)

All users can read/write to Minio:
```python
# Upload to shared location
s3.upload_file('mydata.csv', 'datalake', 'shared/mydata.csv')

# Other users can download
s3.download_file('datalake', 'shared/mydata.csv', '/home/jovyan/data/mydata.csv')
```

### Option 2: Shared PVC (Advanced)

Create a shared PVC accessible by all users:

```yaml
# shared-storage.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jupyterhub-shared
  namespace: jupyterhub
spec:
  accessModes:
    - ReadWriteMany  # Multiple pods can mount
  storageClassName: datamesh-storage
  resources:
    requests:
      storage: 20Gi

---
# Mount in all user pods
# Update jupyterhub-values.yaml:
singleuser:
  storage:
    extraVolumes:
      - name: shared-storage
        persistentVolumeClaim:
          claimName: jupyterhub-shared
    extraVolumeMounts:
      - name: shared-storage
        mountPath: /home/jovyan/shared
```

---

## 📚 Common Workflows

### 1. Upload Dataset, Query with Trino

```python
# 1. Upload CSV to JupyterHub
# (via Web UI or kubectl cp)

# 2. Load into Pandas
import pandas as pd
df = pd.read_csv('/home/jovyan/data/sales_new.csv')

# 3. Save to PostgreSQL
from sqlalchemy import create_engine
engine = create_engine('postgresql://sales_user:SuperSecurePass123!@sales-postgres.sales-domain.svc.cluster.local:5432/sales_db')
df.to_sql('sales_new', engine, if_exists='replace', index=False)

# 4. Query with Trino
from trino.dbapi import connect
conn = connect(host='trino-coordinator.data-platform.svc.cluster.local', port=8080, user='admin')
cursor = conn.cursor()
cursor.execute("SELECT * FROM sales.public.sales_new LIMIT 10")
print(cursor.fetchall())
```

### 2. Upload to Minio, Query with Hive

```python
# 1. Upload large dataset to Minio
s3.upload_file('/home/jovyan/data/big_data.csv', 'datalake', 'raw/big_data.csv')

# 2. Create Hive external table
cursor.execute("""
CREATE TABLE hive.default.big_data (
    id BIGINT,
    value VARCHAR,
    timestamp VARCHAR
)
WITH (
    external_location = 's3a://datalake/raw/',
    format = 'CSV'
)
""")

# 3. Query via Trino
cursor.execute("SELECT COUNT(*) FROM hive.default.big_data")
print(cursor.fetchall())
```

---

## 🎯 Best Practices

✅ **Save files in `/home/jovyan/`** for persistence  
✅ **Use Minio for datasets > 500MB**  
✅ **Use Git for code versioning**  
✅ **Regular backups** with `kubectl cp`  
✅ **Clean up old files** to save space  
✅ **Use compression** for large files (`.tar.gz`, `.parquet`)  
✅ **Document datasets** with README files

---

## 📖 Summary

| Storage Type | Use Case | Capacity | Persistence |
|-------------|----------|----------|-------------|
| **JupyterHub PVC** | Notebooks, scripts, small datasets | 5Gi/user | ✅ Yes |
| **Minio (Data Lake)** | Large datasets, shared files | 10Gi+ | ✅ Yes |
| **Sales PostgreSQL** | Structured sales data | 5Gi | ✅ Yes |
| **Marketing PostgreSQL** | Structured marketing data | 3Gi | ✅ Yes |
| **Hive Metastore** | Data lake metadata | 2Gi | ✅ Yes |

---

**Your files are safe and persistent! 🔒**

Upload, analyze, and never worry about losing your work. 🚀

```bash
# Check your storage usage anytime
df -h /home/jovyan
```

