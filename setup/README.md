# 🔧 DataMeesh - Setup Directory

**Portable, cross-platform deployment scripts for the entire Data Mesh platform**

---

## 📂 Directory Structure

```
setup/
├── 📄 verify_prerequisites.py     # Verify all requirements
├── 📄 deploy_complete_stack.py    # Deploy everything (ONE COMMAND!)
├── 📄 cleanup.py                  # Remove all resources
├── 📄 cleanup_docker_cache.py     # Deep clean Docker cache
├── 📄 README.md                   # This file
│
├── ⚙️  kubernetes/                 # Kubernetes deployments
│   └── deploy_k8s.py              # Deploy core domains
│
├── ⎈  helm/                        # Helm charts
│   ├── install_helm.py            # Install Helm
│   ├── deploy_jupyterhub.py       # Deploy JupyterHub
│   └── jupyterhub-values.yaml     # Helm values
│
├── 🔮 trino/                       # Trino stack
│   └── deploy_trino.py            # Deploy Trino + Minio + Hive
│
├── 📊 grafana/                     # Grafana dashboards
│   └── deploy_grafana.py          # Deploy Grafana + Nginx
│
├── 🔧 dbt/                         # DBT project
│   ├── setup_dbt.py               # Setup DBT in JupyterHub
│   ├── dbt_project.yml            # DBT configuration
│   ├── profiles.yml               # Connection profiles
│   └── models/                    # DBT models
│       ├── staging/               # Staging models (views)
│       └── marts/                 # Mart models (tables)
│
├── 📦 data/                        # Sample data
│   └── load_sample_data.py        # Load test data
│
├── 🗂️  datahub/                    # DataHub (optional)
│   ├── deploy_datahub.py          # Deploy DataHub
│   └── README.md                  # DataHub guide
│
└── 🐳 docker/                      # Docker images
    └── Dockerfile.jupyterhub-dbt  # Custom JupyterHub image
```

---

## 🚀 Quick Start

### Option 1: Deploy Everything (Recommended)

```bash
# 1. Verify prerequisites
python setup/verify_prerequisites.py

# 2. Deploy the entire platform
python setup/deploy_complete_stack.py

# Done! Access at http://localhost:30080
```

### Option 2: Step-by-Step Deployment

```bash
# 1. Verify system
python setup/verify_prerequisites.py

# 2. Deploy core Kubernetes resources
python setup/kubernetes/deploy_k8s.py

# 3. Install Helm
python setup/helm/install_helm.py

# 4. Deploy JupyterHub
python setup/helm/deploy_jupyterhub.py

# 5. Deploy Trino stack
python setup/trino/deploy_trino.py

# 6. Deploy Grafana
python setup/grafana/deploy_grafana.py

# 7. Load sample data
python setup/data/load_sample_data.py

# 8. (Optional) Setup DBT
python setup/dbt/setup_dbt.py

# 9. (Optional) Deploy DataHub - Requires 10-12GB RAM
python setup/datahub/deploy_datahub.py
```

---

## 📋 Script Details

### 🔍 **verify_prerequisites.py**

Verifies all requirements:
- ✅ Python 3.8+
- ✅ Docker Desktop
- ✅ kubectl
- ✅ Kubernetes cluster
- ✅ Helm (optional, will install if missing)
- ✅ System resources (RAM, disk)
- ✅ Network connectivity

**Usage:**
```bash
python setup/verify_prerequisites.py
```

---

### 🚀 **deploy_complete_stack.py**

Deploys the entire platform in one command:

1. Core Kubernetes resources (Sales + Marketing)
2. Helm + JupyterHub
3. Trino + Minio + Hive
4. Grafana + Nginx
5. Sample data

**Usage:**
```bash
python setup/deploy_complete_stack.py
```

**Time:** ~10-15 minutes  
**Requirements:** 8-10GB RAM

---

### 🧹 **cleanup.py**

Removes ALL deployed DataMeesh resources:
- Helm releases (JupyterHub)
- Kubernetes namespaces
- Persistent volumes
- StorageClasses
- PriorityClasses
- Docker images (DataMeesh related)
- Docker build cache
- Docker containers
- Docker volumes
- Docker networks
- Docker system cache

**Usage:**
```bash
python setup/cleanup.py
```

⚠️ **Warning:** This removes all DataMeesh resources!

---

### 🧹 **cleanup_docker_cache.py** (Advanced)

**ULTRA-AGGRESSIVE** Docker cleanup - removes ALL Docker resources:
- ALL containers (even non-DataMeesh)
- ALL images (even non-DataMeesh)
- ALL volumes
- ALL networks
- ALL build cache

**Usage:**
```bash
python setup/cleanup_docker_cache.py
```

⚠️ **DANGER:** This removes ALL Docker resources, not just DataMeesh!  
Use only if you want to completely clean Docker.

---

### 🗂️ **datahub/deploy_datahub.py** (Optional)

**DataHub metadata catalog** - requires 10-12GB RAM:
- ALL containers (even non-DataMeesh)
- ALL images (even non-DataMeesh)
- ALL volumes
- Metadata catalog
- Data lineage visualization
- Dataset documentation

**Usage:**
```bash
python setup/datahub/deploy_datahub.py
```

⚠️ **Requirements:**
- Docker Desktop with 10-12GB RAM
- Base platform already deployed

**Access:** http://localhost:9002 (datahub / datahub)

---

## 🎯 By-Technology Scripts

### Kubernetes

**File:** `kubernetes/deploy_k8s.py`

Deploys core domains:
- Sales domain (PostgreSQL + APIs)
- Marketing domain (PostgreSQL + APIs)
- Secrets & ConfigMaps
- Network Policies
- Resource Quotas
- Auto-scaling (HPA)

---

### Helm & JupyterHub

**Files:**
- `helm/install_helm.py` - Install Helm
- `helm/deploy_jupyterhub.py` - Deploy JupyterHub
- `helm/jupyterhub-values.yaml` - Configuration

Features:
- Multi-user notebooks
- Custom DBT image
- Trino client
- Git integration
- Scheduler extension

---

### Trino Stack

**File:** `trino/deploy_trino.py`

Deploys:
- Trino Coordinator
- Trino Worker
- Minio (S3 storage)
- Hive PostgreSQL
- Hive Metastore

Enables:
- Federated SQL queries
- Cross-domain analytics
- Data lake access

---

### Grafana

**File:** `grafana/deploy_grafana.py`

Deploys:
- Grafana dashboards
- Nginx (DBT docs server)

Pre-configured datasources:
- Sales PostgreSQL
- Marketing PostgreSQL
- Trino

---

### DBT

**Files:**
- `dbt/setup_dbt.py` - Setup DBT in JupyterHub
- `dbt/dbt_project.yml` - Project configuration
- `dbt/profiles.yml` - Connection profiles
- `dbt/models/` - Data models

Models included:
- `stg_sales__customers` - Customer staging
- `stg_sales__orders` - Orders staging
- `mart_sales__customer_lifetime_value` - CLV with RFM

---

### Data

**File:** `data/load_sample_data.py`

Loads realistic sample data:
- Sales: 15 customers, 10 products, 20 orders
- Marketing: 8 campaigns, 15 leads, 50 traffic records

---

### Docker

**File:** `docker/Dockerfile.jupyterhub-dbt`

Custom JupyterHub image with:
- DBT (core, Trino, PostgreSQL)
- Trino CLI
- MinIO client
- Python packages (pandas, matplotlib, etc.)
- Git integration
- JupyterLab extensions

---

## 🔄 Workflow Examples

### Fresh Installation

```bash
# On a new machine
git clone <repo>
cd DataMeesh

# Verify system
python setup/verify_prerequisites.py

# Deploy everything
python setup/deploy_complete_stack.py

# Access JupyterHub
# Open http://localhost:30080
# Login: admin / datamesh2024
```

### Rebuilding

```bash
# Clean up
python setup/cleanup.py

# Redeploy
python setup/deploy_complete_stack.py
```

### Adding Just Trino

```bash
# If you only need Trino
python setup/trino/deploy_trino.py
```

---

## 🌐 Cross-Platform Support

All scripts work on:
- ✅ **Windows** (PowerShell)
- ✅ **WSL2** (Ubuntu/Debian)
- ✅ **macOS** (Homebrew)
- ✅ **Linux** (apt/yum)

**Detection is automatic!** Scripts adapt to your OS.

---

## 📖 Script Naming Convention

| Prefix | Purpose | Example |
|--------|---------|---------|
| `verify_` | Check requirements | `verify_prerequisites.py` |
| `install_` | Install tools | `install_helm.py` |
| `deploy_` | Deploy resources | `deploy_k8s.py` |
| `setup_` | Configure/setup | `setup_dbt.py` |
| `load_` | Load data | `load_sample_data.py` |
| `cleanup` | Remove resources | `cleanup.py` |

---

## 🎓 Best Practices

### Portability

✅ **DO:**
- Use Python for all scripts
- Detect OS automatically
- Use `kubectl` and platform-agnostic commands
- Handle errors gracefully

❌ **DON'T:**
- Use shell scripts (.sh, .bat)
- Hard-code paths
- Assume specific OS

### Error Handling

All scripts:
- ✅ Check prerequisites
- ✅ Provide clear error messages
- ✅ Suggest solutions
- ✅ Allow continuation after failures

### Documentation

Each script includes:
- ✅ Clear docstring
- ✅ Step-by-step output
- ✅ Next steps guidance
- ✅ Access points

---

## 🔧 Development

### Adding a New Component

1. Create directory: `setup/<component>/`
2. Add deployment script: `deploy_<component>.py`
3. Update `deploy_complete_stack.py` to include it
4. Document in this README

### Testing

```bash
# Test individual script
python setup/kubernetes/deploy_k8s.py

# Test full deployment
python setup/deploy_complete_stack.py

# Test cleanup
python setup/cleanup.py
```

---

## 📞 Troubleshooting

### Script fails with "kubectl not found"

```bash
# Install kubectl
python setup/verify_prerequisites.py
# Follow installation instructions
```

### Pods in "Pending" state

```bash
# Check resources
kubectl describe pod <pod-name> -n <namespace>

# Increase Docker Desktop RAM:
# Docker Desktop → Settings → Resources → Memory → 10GB+
```

### "Cannot connect to cluster"

```bash
# Enable Kubernetes in Docker Desktop:
# Docker Desktop → Settings → Kubernetes → Enable
```

---

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [Quick Start](../QUICK_START.md) - Fast deployment
- [Complete Guide](../docs/guides/COMPLETE_GUIDE.md) - Detailed guide
- [Architecture](../docs/architecture/) - Technical details

---

## ✅ Checklist for New Machine

- [ ] Install Docker Desktop
- [ ] Enable Kubernetes in Docker Desktop
- [ ] Install Python 3.8+
- [ ] Clone repository
- [ ] Run `python setup/verify_prerequisites.py`
- [ ] Run `python setup/deploy_complete_stack.py`
- [ ] Access http://localhost:30080

**Time to productive platform: ~20 minutes!**

---

**The setup directory is designed for maximum portability and ease of use. Deploy anywhere, anytime!** 🚀

