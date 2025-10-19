# 🔐 RBAC & Access Control Guide

**Implémenter des utilisateurs avec permissions limitées par domaine**

---

## 🎯 Objectif

Créer 3 utilisateurs avec des accès différents:

1. **admin** → Accès complet (tous les domaines)
2. **sales_analyst** → Accès UNIQUEMENT Sales
3. **marketing_analyst** → Accès UNIQUEMENT Marketing

---

## 📊 Architecture Actuelle vs Cible

### ❌ Architecture Actuelle (Demo)

```yaml
# setup/helm/jupyterhub-values.yaml
hub:
  config:
    DummyAuthenticator:
      password: "datamesh2024"  # Même mot de passe pour tous
```

**Problème:** N'importe quel username peut se connecter et accéder à TOUT.

### ✅ Architecture Cible (Production)

```
┌──────────────────────────────────────────────┐
│  ADMIN (admin)                               │
│  ✅ Créer/gérer utilisateurs                 │
│  ✅ Accès Sales + Marketing + Hive           │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  SALES ANALYST (sales_analyst)               │
│  ✅ Accès Sales PostgreSQL                   │
│  ❌ Pas accès Marketing                      │
│  ❌ Pas accès Hive                           │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  MARKETING ANALYST (marketing_analyst)       │
│  ❌ Pas accès Sales                          │
│  ✅ Accès Marketing PostgreSQL               │
│  ❌ Pas accès Hive                           │
└──────────────────────────────────────────────┘
```

---

## 🔧 Implémentation

### Étape 1: Changer l'Authentification JupyterHub

Remplacer `DummyAuthenticator` par `NativeAuthenticator` (permet de créer des users).

**Créer:** `config/jupyterhub-rbac-values.yaml`

```yaml
# JupyterHub avec authentification native
proxy:
  service:
    type: NodePort
    nodePorts:
      http: 30080
  secretToken: "GENERATE_NEW_SECRET_TOKEN"

hub:
  config:
    JupyterHub:
      authenticator_class: nativeauthenticator.NativeAuthenticator
      admin_access: true
      admin_users:
        - admin
    
    NativeAuthenticator:
      enable_signup: false  # Seul admin peut créer des users
      ask_email_on_signup: false
      minimum_password_length: 8
      allowed_failed_logins: 3
      seconds_before_next_try: 600
  
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "250m"

singleuser:
  image:
    name: jupyterhub-dbt
    tag: "latest"
    pullPolicy: Never
  
  cpu:
    limit: 0.5
    guarantee: 0.05
  memory:
    limit: "512M"
    guarantee: "256M"
  
  storage:
    type: dynamic
    capacity: 5Gi
    dynamic:
      storageClass: datamesh-storage
  
  # Variables d'environnement par utilisateur
  profileList:
    - display_name: "Sales Analyst"
      description: "Accès aux données Sales uniquement"
      slug: sales
      default: false
      kubespawner_override:
        extra_labels:
          domain: sales
        environment:
          ALLOWED_CATALOGS: "sales"
          TRINO_USER: "sales_analyst"
    
    - display_name: "Marketing Analyst"
      description: "Accès aux données Marketing uniquement"
      slug: marketing
      default: false
      kubespawner_override:
        extra_labels:
          domain: marketing
        environment:
          ALLOWED_CATALOGS: "marketing"
          TRINO_USER: "marketing_analyst"
    
    - display_name: "Data Engineer (Full Access)"
      description: "Accès à tous les domaines"
      slug: admin
      default: true
      kubespawner_override:
        extra_labels:
          domain: all
        environment:
          ALLOWED_CATALOGS: "sales,marketing,hive"
          TRINO_USER: "admin"

cull:
  enabled: true
  timeout: 3600
  every: 600

rbac:
  create: true

debug:
  enabled: false
```

---

### Étape 2: Configurer Trino avec Authentification

**Créer:** `config/trino-rbac.yaml`

```yaml
# Trino avec contrôle d'accès par utilisateur
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-access-control
  namespace: data-platform
data:
  # Règles d'accès par catalogue
  rules.json: |
    {
      "catalogs": [
        {
          "user": "admin",
          "catalog": "(sales|marketing|hive)",
          "allow": "all"
        },
        {
          "user": "sales_analyst",
          "catalog": "sales",
          "allow": "all"
        },
        {
          "user": "sales_analyst",
          "catalog": "(marketing|hive)",
          "allow": "none"
        },
        {
          "user": "marketing_analyst",
          "catalog": "marketing",
          "allow": "all"
        },
        {
          "user": "marketing_analyst",
          "catalog": "(sales|hive)",
          "allow": "none"
        }
      ]
    }
  
  # Fichier de configuration access control
  access-control.properties: |
    access-control.name=file
    security.config-file=/etc/trino/access-control/rules.json

---
# Mise à jour du ConfigMap Trino Coordinator
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-coordinator-config
  namespace: data-platform
data:
  config.properties: |
    coordinator=true
    node-scheduler.include-coordinator=false
    http-server.http.port=8080
    discovery.uri=http://trino-coordinator:8080
    http-server.authentication.type=PASSWORD
    
  password-authenticator.properties: |
    password-authenticator.name=file
    file.password-file=/etc/trino/password.db
    
  # Hash des mots de passe (bcrypt)
  password.db: |
    admin:$2y$10$YourBcryptHashHere
    sales_analyst:$2y$10$YourBcryptHashHere
    marketing_analyst:$2y$10$YourBcryptHashHere
```

---

### Étape 3: Script de Déploiement RBAC

**Créer:** `setup/rbac/deploy_rbac.py`

```python
#!/usr/bin/env python3
"""
Deploy DataMeesh with RBAC (Role-Based Access Control)
Creates 3 users: admin, sales_analyst, marketing_analyst
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

def run_command(cmd, check=True):
    """Execute shell command"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def generate_bcrypt_hash(password):
    """Generate bcrypt hash for password"""
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    except ImportError:
        print("❌ bcrypt not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "bcrypt"])
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def main():
    print("\n" + "="*70)
    print("🔐 DataMeesh - RBAC Deployment")
    print("="*70 + "\n")
    
    # Get passwords
    print("📝 Creating 3 users with passwords:\n")
    
    admin_pass = getpass.getpass("Password for 'admin': ")
    sales_pass = getpass.getpass("Password for 'sales_analyst': ")
    marketing_pass = getpass.getpass("Password for 'marketing_analyst': ")
    
    # Generate bcrypt hashes
    print("\n🔒 Generating password hashes...")
    admin_hash = generate_bcrypt_hash(admin_pass)
    sales_hash = generate_bcrypt_hash(sales_pass)
    marketing_hash = generate_bcrypt_hash(marketing_pass)
    
    # Create Trino password file
    password_db = f"""admin:{admin_hash}
sales_analyst:{sales_hash}
marketing_analyst:{marketing_hash}"""
    
    # Update Trino ConfigMap
    print("📝 Creating Trino access control...")
    
    trino_rbac_yaml = f"""
apiVersion: v1
kind: ConfigMap
metadata:
  name: trino-passwords
  namespace: data-platform
data:
  password.db: |
{chr(10).join('    ' + line for line in password_db.split(chr(10)))}
"""
    
    # Write to file
    rbac_file = Path("config/trino-rbac-passwords.yaml")
    rbac_file.write_text(trino_rbac_yaml)
    
    print(f"✅ Created: {rbac_file}")
    
    # Deploy
    print("\n📦 Deploying RBAC configuration...")
    
    # Apply Trino RBAC
    run_command("kubectl apply -f config/trino-rbac.yaml")
    run_command("kubectl apply -f config/trino-rbac-passwords.yaml")
    
    # Redeploy JupyterHub with RBAC
    print("📦 Redeploying JupyterHub with authentication...")
    run_command("helm upgrade jupyterhub jupyterhub/jupyterhub "
               "--namespace jupyterhub "
               "--values config/jupyterhub-rbac-values.yaml "
               "--version=3.0.0")
    
    # Restart Trino
    print("🔄 Restarting Trino pods...")
    run_command("kubectl rollout restart deployment/trino-coordinator -n data-platform")
    run_command("kubectl rollout restart deployment/trino-worker -n data-platform")
    
    print("\n" + "="*70)
    print("✅ RBAC Deployment Complete!")
    print("="*70 + "\n")
    
    print("🔑 User Credentials:")
    print("─" * 70)
    print(f"  👑 Admin:")
    print(f"     Username: admin")
    print(f"     Password: {admin_pass}")
    print(f"     Access: Sales + Marketing + Hive")
    print()
    print(f"  📊 Sales Analyst:")
    print(f"     Username: sales_analyst")
    print(f"     Password: {sales_pass}")
    print(f"     Access: Sales ONLY")
    print()
    print(f"  📈 Marketing Analyst:")
    print(f"     Username: marketing_analyst")
    print(f"     Password: {marketing_pass}")
    print(f"     Access: Marketing ONLY")
    print("─" * 70)
    
    print("\n🌐 Access JupyterHub: http://localhost:30080\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

### Étape 4: Créer les Utilisateurs (Admin)

Une fois déployé, l'admin peut créer des users via l'interface:

1. Se connecter comme **admin** à http://localhost:30080
2. Aller dans **Control Panel** → **Admin**
3. Cliquer **Add Users**
4. Ajouter `sales_analyst` et `marketing_analyst`
5. Assigner les mots de passe

---

## 🧪 Test du Contrôle d'Accès

### Test 1: Admin (Accès Complet)

```python
# Login: admin / [votre_mot_de_passe]

from trino.dbapi import connect

conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='admin',
    http_scheme='https',
    auth=trino.auth.BasicAuthentication('admin', 'admin_password')
)

cursor = conn.cursor()

# ✅ Accès Sales
cursor.execute("SELECT * FROM sales.public.customers LIMIT 5")
print(cursor.fetchall())

# ✅ Accès Marketing
cursor.execute("SELECT * FROM marketing.public.campaigns LIMIT 5")
print(cursor.fetchall())

# ✅ Accès Hive
cursor.execute("SHOW SCHEMAS FROM hive")
print(cursor.fetchall())
```

### Test 2: Sales Analyst (Sales Seulement)

```python
# Login: sales_analyst / [votre_mot_de_passe]

conn = connect(
    host='trino-coordinator.data-platform.svc.cluster.local',
    port=8080,
    user='sales_analyst',
    http_scheme='https',
    auth=trino.auth.BasicAuthentication('sales_analyst', 'sales_password')
)

cursor = conn.cursor()

# ✅ Accès Sales
cursor.execute("SELECT * FROM sales.public.customers LIMIT 5")
print(cursor.fetchall())  # Fonctionne!

# ❌ Accès Marketing REFUSÉ
cursor.execute("SELECT * FROM marketing.public.campaigns LIMIT 5")
# Erreur: Access Denied: Cannot access catalog marketing
```

### Test 3: Marketing Analyst (Marketing Seulement)

```python
# Login: marketing_analyst / [votre_mot_de_passe]

# ✅ Accès Marketing
cursor.execute("SELECT * FROM marketing.public.campaigns LIMIT 5")
# Fonctionne!

# ❌ Accès Sales REFUSÉ
cursor.execute("SELECT * FROM sales.public.customers LIMIT 5")
# Erreur: Access Denied: Cannot access catalog sales
```

---

## 🚀 Déploiement Complet

### Option 1: Déployer avec RBAC depuis le début

```bash
# 1. Créer les fichiers de configuration
#    (jupyterhub-rbac-values.yaml, trino-rbac.yaml)

# 2. Exécuter le script RBAC
python setup/rbac/deploy_rbac.py

# 3. Tester les accès
```

### Option 2: Migrer depuis la configuration actuelle

```bash
# 1. Sauvegarder la config actuelle
kubectl get configmap -n data-platform -o yaml > backup_config.yaml

# 2. Appliquer RBAC
python setup/rbac/deploy_rbac.py

# 3. Vérifier
kubectl get pods --all-namespaces
```

---

## 📊 Tableau Récapitulatif

| Utilisateur | Username | Accès Sales | Accès Marketing | Accès Hive | Admin JupyterHub |
|-------------|----------|-------------|-----------------|------------|------------------|
| **Admin** | admin | ✅ | ✅ | ✅ | ✅ |
| **Sales Analyst** | sales_analyst | ✅ | ❌ | ❌ | ❌ |
| **Marketing Analyst** | marketing_analyst | ❌ | ✅ | ❌ | ❌ |

---

## 🔐 Sécurité Avancée

### Ajouter JWT Authentication

```yaml
# Pour production
http-server.authentication.type=JWT
http-server.authentication.jwt.key-file=/etc/trino/jwt.key
```

### Ajouter LDAP/Active Directory

```yaml
# Intégration avec AD d'entreprise
password-authenticator.name=ldap
ldap.url=ldap://ldap.example.com:389
ldap.user-bind-pattern=uid=${USER},ou=users,dc=example,dc=com
```

### Audit Logging

```yaml
# Tracer toutes les requêtes par utilisateur
event-listener.name=audit
audit.enabled=true
audit.log-path=/var/log/trino/audit.log
```

---

## 🎯 Résumé

**Configuration Actuelle (Demo):**
- ❌ Aucune authentification réelle
- ❌ Tous accèdent à tout
- ✅ Facile pour apprendre

**Configuration RBAC (Production):**
- ✅ Authentification par mot de passe
- ✅ Contrôle d'accès par domaine
- ✅ Admin peut gérer les users
- ✅ Audit et sécurité

**Pour implémenter:**
1. Créer `config/jupyterhub-rbac-values.yaml`
2. Créer `config/trino-rbac.yaml`
3. Créer `setup/rbac/deploy_rbac.py`
4. Exécuter `python setup/rbac/deploy_rbac.py`

---

**Voulez-vous que je crée ces fichiers pour vous?** 🚀

