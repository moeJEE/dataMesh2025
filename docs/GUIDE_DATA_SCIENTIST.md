# 📊 **GUIDE DATA SCIENTIST: CSV → Trino → Grafana**

## 🎯 **WORKFLOW COMPLET**

### **1️⃣ IMPORTER UN CSV DANS MINIO**

#### **Accès à MinIO:**
- **URL:** http://localhost:30901/browser/datalake
- **Login:** `minioadmin` / `minioadmin`

#### **Étapes d'import:**
1. **Ouvrir MinIO Console**
2. **Créer un bucket** (ex: `raw-data`)
3. **Uploader votre CSV** dans le bucket
4. **Noter le chemin** (ex: `s3://raw-data/mon_fichier.csv`)

---

### **2️⃣ RÉCUPÉRER LES DONNÉES AVEC TRINO**

#### **Option A: Dans JupyterHub (Recommandé)**
```python
# Dans JupyterHub (http://localhost:30080)
from trino.dbapi import connect
import pandas as pd

# Connexion Trino
conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin'
)

# Requête pour lire le CSV depuis MinIO
query = """
SELECT * FROM hive.raw_data.mon_fichier_csv
LIMIT 10
"""

# Exécuter et convertir en DataFrame
df = pd.read_sql(query, conn)
print(df.head())
```

#### **Option B: Via Trino UI**
- **URL:** http://localhost:30808
- **Requête:**
```sql
SELECT * FROM hive.raw_data.mon_fichier_csv
LIMIT 10;
```

---

### **3️⃣ CRÉER UN TABLEAU DE BORD GRAFANA**

#### **Accès à Grafana:**
- **URL:** http://localhost:30030
- **Login:** `admin` / `datamesh2024`

#### **Configuration de la source de données:**
1. **Aller dans:** Configuration → Data Sources
2. **Ajouter:** Trino
3. **URL:** `http://trino-coordinator.data-platform.svc.cluster.local:8080`
4. **User:** `admin`
5. **Test & Save**

#### **Création du dashboard:**
1. **Créer un nouveau dashboard**
2. **Ajouter un panel**
3. **Sélectionner Trino comme source**
4. **Écrire votre requête:**
```sql
SELECT 
    column1,
    column2,
    COUNT(*) as count
FROM hive.raw_data.mon_fichier_csv
GROUP BY column1, column2
ORDER BY count DESC
```

---

## 🔧 **EXEMPLE PRATIQUE COMPLET**

### **Étape 1: Créer des données d'exemple**

Dans JupyterHub, créez un notebook avec :

```python
import pandas as pd

# Créer des données d'exemple
data = {
    'date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'sales': [1200, 25, 75, 300, 1200],
    'region': ['North', 'South', 'East', 'West', 'North'],
    'customer_id': [1, 2, 3, 4, 5]
}

df = pd.DataFrame(data)
df.to_csv('sales_data.csv', index=False)
print(df)
```

### **Étape 2: Upload vers MinIO**

1. **Ouvrir:** http://localhost:30901/browser/datalake
2. **Login:** `minioadmin` / `minioadmin`
3. **Créer bucket:** `raw-data`
4. **Uploader:** `sales_data.csv`

### **Étape 3: Requêtes Trino**

Dans JupyterHub :

```python
from trino.dbapi import connect
import pandas as pd

# Connexion Trino
conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin'
)

# Requête pour lire le CSV
query = """
SELECT * FROM hive.raw_data.sales_data_csv
LIMIT 10
"""

df = pd.read_sql(query, conn)
print(df.head())
```

### **Étape 4: Dashboard Grafana**

1. **Ouvrir:** http://localhost:30030
2. **Login:** `admin` / `datamesh2024`
3. **Configuration → Data Sources → Add Trino**
4. **URL:** `http://trino-coordinator.data-platform.svc.cluster.local:8080`
5. **User:** `admin`
6. **Test & Save**

#### **Requêtes pour dashboard:**

**Ventes par région:**
```sql
SELECT region, SUM(sales) as total_sales
FROM hive.raw_data.sales_data_csv
GROUP BY region
ORDER BY total_sales DESC
```

**Ventes par produit:**
```sql
SELECT product, COUNT(*) as count, AVG(sales) as avg_sales
FROM hive.raw_data.sales_data_csv
GROUP BY product
ORDER BY count DESC
```

**Évolution des ventes:**
```sql
SELECT date, SUM(sales) as daily_sales
FROM hive.raw_data.sales_data_csv
GROUP BY date
ORDER BY date
```

---

## 🌐 **ACCÈS AUX SERVICES**

| Service | URL | Login |
|---------|-----|-------|
| **MinIO** | http://localhost:30901 | minioadmin / minioadmin |
| **Trino UI** | http://localhost:30808 | - |
| **Grafana** | http://localhost:30030 | admin / datamesh2024 |
| **JupyterHub** | http://localhost:30080 | admin / datamesh2024 |

---

## 💡 **CONSEILS PRATIQUES**

### **Pour les CSV:**
- **Format:** CSV avec en-têtes
- **Encodage:** UTF-8
- **Séparateur:** Virgule (,)
- **Taille:** Pas de limite (MinIO gère le Big Data)

### **Pour Trino:**
- **Schéma:** `hive.raw_data` pour les CSV
- **Tables:** Nom du fichier sans extension
- **Requêtes:** SQL standard

### **Pour Grafana:**
- **Refresh:** 5s, 1m, 5m selon vos besoins
- **Variables:** Utilisez les variables pour la flexibilité
- **Alertes:** Configurez des alertes sur les métriques importantes

---

## 🚀 **PROCHAINES ÉTAPES**

1. **Explorer les données** avec Trino
2. **Créer des vues** pour simplifier les requêtes
3. **Développer des modèles** avec DBT
4. **Automatiser** les dashboards
5. **Mettre en place** des alertes

**Votre Data Mesh est prêt pour l'analyse de données ! 🎉📊**
