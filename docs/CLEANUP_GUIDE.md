# 🧹 DataMeesh - Cleanup Guide

**Complete guide to cleaning up resources and Docker cache**

---

## 📋 Two Cleanup Options

### ✅ Option 1: Standard Cleanup (Recommended)

**Script**: `setup/cleanup.py`

**Removes:**
- ✅ All DataMeesh Kubernetes resources
- ✅ DataMeesh Docker images
- ✅ Docker build cache
- ✅ Unused Docker containers
- ✅ Unused Docker volumes
- ✅ Unused Docker networks

**Usage:**
```bash
python setup/cleanup.py
```

**Time:** 2-3 minutes

---

### ⚠️ Option 2: Deep Docker Cache Cleanup (Advanced)

**Script**: `setup/cleanup_docker_cache.py`

**Removes:**
- ❌ ALL Docker containers
- ❌ ALL Docker images
- ❌ ALL Docker volumes
- ❌ ALL Docker networks
- ❌ ALL Docker build cache

**Usage:**
```bash
python setup/cleanup_docker_cache.py
```

⚠️ **WARNING:** Removes ALL Docker resources, not just DataMeesh!

**Time:** 5-10 minutes

---

## 🔍 Comparison

| Aspect | Standard | Deep Cache |
|--------|----------|------------|
| Scope | DataMeesh only | ALL Docker |
| Docker images | DataMeesh only | ALL |
| Containers | Unused only | ALL |
| Risk | Low | Medium |

---

## 📊 Check Cache Size

```bash
docker system df
```

---

## 🔄 Typical Workflows

### Redeploy DataMeesh

```bash
python setup/cleanup.py
python setup/deploy_complete_stack.py
```

### Free up Docker space

```bash
# Try standard first
python setup/cleanup.py

# If still full, use deep cleanup
python setup/cleanup_docker_cache.py
```

---

## ✅ Verify Cleanup

```bash
# Check Kubernetes
kubectl get all --all-namespaces

# Check Docker
docker system df
docker images
docker ps -a
```

---

**Choose the right cleanup for your needs!** 🧹

