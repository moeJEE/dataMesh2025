# 🗂️ DataHub - Metadata Catalog

**DataHub deployment for metadata management and data lineage**

---

## ⚠️ Requirements

### RAM Requirements

DataHub requires **additional 2-3GB RAM**:
- Base platform: 6GB
- DataHub: 2-3GB
- **Total needed: 10-12GB RAM**

### Prerequisites

- ✅ Docker Desktop with 10-12GB RAM
- ✅ Python 3.8+
- ✅ DataMeesh platform already deployed

---

## 🚀 Deployment

### Deploy DataHub

```bash
python setup/datahub/deploy_datahub.py
```

This will:
1. Install `acryl-datahub` package
2. Start DataHub with Docker Compose
3. Create ingestion recipes

**Time:** 5-10 minutes

---

## 🌐 Access

**URL:** http://localhost:9002

**Credentials:**
- Username: `datahub`
- Password: `datahub`

---

## 🔄 Ingest Metadata

### 1. Ingest from Trino

This catalogs all Sales and Marketing tables:

```bash
# Windows
wsl datahub ingest -c recipes/datahub_trino_recipe.yml

# macOS/Linux
datahub ingest -c recipes/datahub_trino_recipe.yml
```

**What gets ingested:**
- ✅ sales.public.customers
- ✅ sales.public.orders
- ✅ sales.public.products
- ✅ marketing.public.campaigns
- ✅ marketing.public.leads

---

### 2. Ingest from DBT

This adds DBT models and lineage:

**Step 1:** Copy DBT artifacts from JupyterHub

```bash
# Find JupyterHub pod
kubectl get pods -n jupyterhub -l component=singleuser-server

# Copy artifacts
kubectl cp jupyterhub/<pod-name>:/home/jovyan/dbt_projects/datamesh/target ./dbt_target
```

**Step 2:** Update recipe path

Edit `recipes/datahub_dbt_recipe.yml`:
```yaml
manifest_path: "./dbt_target/manifest.json"
catalog_path: "./dbt_target/catalog.json"
```

**Step 3:** Ingest

```bash
# Windows
wsl datahub ingest -c recipes/datahub_dbt_recipe.yml

# macOS/Linux
datahub ingest -c recipes/datahub_dbt_recipe.yml
```

**What gets ingested:**
- ✅ DBT models
- ✅ Data lineage
- ✅ Tests
- ✅ Documentation

---

## 📊 Features

### Data Discovery

- Search all datasets
- Browse by platform
- Filter by tags

### Data Lineage

- Visualize data flow
- Understand dependencies
- Impact analysis

### Metadata Management

- Add documentation
- Tag datasets
- Set ownership
- Track usage

---

## 🔧 Management

### Stop DataHub

```bash
# Windows
wsl datahub docker quickstart --stop

# macOS/Linux
datahub docker quickstart --stop
```

### Restart DataHub

```bash
# Windows
wsl datahub docker quickstart

# macOS/Linux
datahub docker quickstart
```

### View Logs

```bash
docker-compose -f ~/.datahub/quickstart/docker-compose.yml logs
```

### Clean Up DataHub

```bash
# Windows
wsl datahub docker nuke

# macOS/Linux
datahub docker nuke
```

---

## 🔧 Troubleshooting

### DataHub not starting

**Cause:** Insufficient RAM

**Solution:**
1. Check Docker Desktop settings
2. Increase RAM to 10-12GB
3. Restart Docker Desktop
4. Redeploy DataHub

### Port 9002 already in use

**Cause:** Another service using the port

**Solution:**
```bash
# Find process
netstat -ano | findstr :9002  # Windows
lsof -i :9002                  # macOS/Linux

# Stop conflicting service or use different port
```

### Ingestion fails

**Cause:** Connection issues

**Solution:**
1. Ensure DataHub is running: `docker ps | grep datahub`
2. Check Trino is accessible: `curl http://localhost:30808`
3. Verify recipe configuration

---

## 📚 Documentation

For detailed usage, see: `docs/guides/DATAHUB_GUIDE.md`

---

## 💡 Tips

1. **Schedule ingestion:** Set up cron jobs for daily metadata refresh
2. **Add documentation:** Document datasets in DataHub UI
3. **Set ownership:** Assign owners to datasets
4. **Tag datasets:** Use tags for better organization
5. **Monitor lineage:** Regularly check data lineage for issues

---

**DataHub is optional but powerful for metadata management!** 🗂️

