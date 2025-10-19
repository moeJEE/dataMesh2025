# 🚀 DataMeesh - Deployment Guide

**Complete deployment guide from zero to running platform**

---

## ⚡ Quick Start (5 minutes)

```bash
# 1. Verify prerequisites
python setup/verify_prerequisites.py

# 2. Deploy everything
python setup/deploy_complete_stack.py

# 3. Access JupyterHub
# Open: http://localhost:30080
# Login: admin / datamesh2024
```

**Done!** Your Data Mesh platform is ready.

---

## 📋 Prerequisites

### Required

- ✅ **Docker Desktop** with Kubernetes enabled
- ✅ **Python 3.8+**
- ✅ **kubectl** CLI
- ✅ **8-10GB RAM** available

### Installation

#### Windows
```powershell
# Install Chocolatey first, then:
choco install docker-desktop
choco install python
choco install kubernetes-cli
```

#### macOS
```bash
brew install docker
brew install python3
brew install kubectl
```

#### WSL2/Linux
```bash
# Install Docker Desktop for Windows (includes Kubernetes)
# Or install Docker + kubectl:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install kubectl
```

---

## 🎯 Deployment Options

### Option 1: Complete Stack (Recommended)

Deploy everything in one command:

```bash
python setup/deploy_complete_stack.py
```

**Deploys:**
- ✅ Core domains (Sales + Marketing)
- ✅ JupyterHub (notebooks)
- ✅ Trino (federated queries)
- ✅ Grafana (dashboards)
- ✅ Sample data

**Time:** 10-15 minutes

---

### Option 2: Step-by-Step

Deploy components individually:

```bash
# 1. Core Kubernetes resources
python setup/kubernetes/deploy_k8s.py

# 2. Helm + JupyterHub
python setup/helm/install_helm.py
python setup/helm/deploy_jupyterhub.py

# 3. Trino stack
python setup/trino/deploy_trino.py

# 4. Grafana
python setup/grafana/deploy_grafana.py

# 5. Sample data
python setup/data/load_sample_data.py
```

---

### Option 3: Minimal (Core Only)

Deploy only core domains:

```bash
python setup/kubernetes/deploy_k8s.py
python setup/data/load_sample_data.py
```

---

## 🌐 Access Points

After deployment:

| Service | URL | Credentials |
|---------|-----|-------------|
| **JupyterHub** | http://localhost:30080 | admin / datamesh2024 |
| **Trino Web UI** | http://localhost:30808 | - |
| **Minio Console** | http://localhost:30901 | minioadmin / minioadmin |
| **Grafana** | http://localhost:30030 | admin / datamesh2024 |
| **DBT Docs** | http://localhost:30082 | - |

---

## 📊 Verify Deployment

Check all pods are running:

```bash
kubectl get pods --all-namespaces
```

Expected output:
```
NAMESPACE           NAME                                READY   STATUS
sales-domain        sales-postgres-0                    1/1     Running
sales-domain        sales-api-xxxxx                     1/1     Running
marketing-domain    marketing-postgres-0                1/1     Running
marketing-domain    marketing-api-xxxxx                 1/1     Running
data-platform       trino-coordinator-xxxxx             1/1     Running
data-platform       trino-worker-xxxxx                  1/1     Running
data-platform       minio-xxxxx                         1/1     Running
jupyterhub          hub-xxxxx                           1/1     Running
jupyterhub          proxy-xxxxx                         1/1     Running
monitoring          grafana-xxxxx                       1/1     Running
```

---

## 🔧 Troubleshooting

### Pods in "Pending" state

**Cause:** Insufficient memory

**Solution:**
```bash
# Increase Docker Desktop RAM:
# Docker Desktop → Settings → Resources → Memory → 10GB+

# Then restart deployment
python setup/cleanup.py
python setup/deploy_complete_stack.py
```

### Pods in "CrashLoopBackOff"

**Cause:** Configuration error or resource limits

**Solution:**
```bash
# Check logs
kubectl logs <pod-name> -n <namespace>

# Check pod details
kubectl describe pod <pod-name> -n <namespace>

# Restart pod
kubectl delete pod <pod-name> -n <namespace>
```

### "Cannot connect to cluster"

**Cause:** Kubernetes not enabled in Docker Desktop

**Solution:**
1. Open Docker Desktop
2. Settings → Kubernetes
3. Enable "Enable Kubernetes"
4. Wait for Kubernetes to start (green indicator)
5. Retry deployment

### Deployment takes too long

**Cause:** Slow image downloads

**Solution:**
- Check internet connection
- Wait for images to download (first time is slower)
- Images are cached for future deployments

---

## 🧹 Cleanup

### Remove everything:

```bash
python setup/cleanup.py
```

### Deep Docker cleanup:

```bash
python setup/cleanup_docker_cache.py
```

---

## 🔄 Redeploy

To redeploy after cleanup:

```bash
# 1. Verify system
python setup/verify_prerequisites.py

# 2. Deploy
python setup/deploy_complete_stack.py
```

---

## 📖 Next Steps

After deployment:

1. **Explore JupyterHub**
   - Open http://localhost:30080
   - Create a new Python notebook
   - Run example queries (see `examples/jupyter_notebook_example.py`)

2. **Query with Trino**
   - See `examples/trino_queries.sql` for query examples
   - Access Trino UI at http://localhost:30808

3. **Create Dashboards**
   - Open Grafana at http://localhost:30030
   - Create visualizations from Sales/Marketing data

4. **Setup DBT**
   - Run: `python setup/dbt/setup_dbt.py`
   - Build models, run tests, generate docs

---

## 📚 Additional Resources

- **Complete Platform Guide**: `docs/guides/COMPLETE_GUIDE.md`
- **Architecture Details**: `docs/architecture/`
- **Example Queries**: `examples/trino_queries.sql`
- **Setup Details**: `setup/README.md`

---

**Deploy once, analyze everywhere!** 🚀

