#!/usr/bin/env python3
"""
Script simple pour mettre à jour la documentation DBT depuis JupyterHub
"""

import subprocess
import sys

def run_command(cmd):
    """Exécute une commande et affiche le résultat"""
    print(f"🔨 {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("🔄 Mise à jour de la documentation DBT...")
    
    # 1. Générer la documentation
    print("\n📚 Génération de la documentation...")
    if not run_command('kubectl exec -n jupyterhub jupyter-admin -- bash -c "cd /home/jovyan/dbt_project && dbt docs generate --profiles-dir /home/jovyan/.dbt"'):
        print("❌ Erreur lors de la génération")
        return
    
    # 2. Obtenir le nom du pod nginx
    print("\n🔍 Recherche du pod nginx...")
    result = subprocess.run('kubectl get pods -n dbt-docs -o jsonpath="{.items[0].metadata.name}"', shell=True, capture_output=True, text=True)
    nginx_pod = result.stdout.strip()
    
    if not nginx_pod:
        print("❌ Pod nginx non trouvé")
        return
    
    print(f"✅ Pod nginx trouvé: {nginx_pod}")
    
    # 3. Copier les fichiers
    print("\n📦 Copie des fichiers...")
    
    # Créer les fichiers temporaires
    run_command("kubectl exec -n jupyterhub jupyter-admin -- cat /home/jovyan/dbt_project/target/index.html > temp_index.html")
    run_command("kubectl exec -n jupyterhub jupyter-admin -- cat /home/jovyan/dbt_project/target/catalog.json > temp_catalog.json")
    run_command("kubectl exec -n jupyterhub jupyter-admin -- cat /home/jovyan/dbt_project/target/manifest.json > temp_manifest.json")
    
    # Copier vers nginx
    run_command(f"kubectl cp temp_index.html dbt-docs/{nginx_pod}:/usr/share/nginx/html/index.html")
    run_command(f"kubectl cp temp_catalog.json dbt-docs/{nginx_pod}:/usr/share/nginx/html/catalog.json")
    run_command(f"kubectl cp temp_manifest.json dbt-docs/{nginx_pod}:/usr/share/nginx/html/manifest.json")
    
    # Nettoyer
    run_command("del temp_*.html temp_*.json 2>nul")
    
    print("\n✅ Documentation mise à jour!")
    print("🌐 Accès: http://localhost:30082")

if __name__ == "__main__":
    main()
