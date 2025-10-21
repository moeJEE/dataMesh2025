#!/usr/bin/env python3
"""
Script pour mettre à jour la documentation DBT et la déployer sur nginx
"""

import subprocess
import sys
import os

def run_command(cmd, check=True):
    """Exécute une commande et retourne le résultat"""
    print(f"🔨 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Erreur: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    return True

def print_header(title):
    """Affiche un en-tête"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def main():
    print_header("🔄 Mise à jour de la documentation DBT")
    
    # 1. Générer la documentation dans JupyterHub
    print("\n📚 Génération de la documentation DBT...")
    generate_cmd = """kubectl exec -n jupyterhub jupyter-admin -- bash -c "cd /home/jovyan/dbt_project && dbt docs generate --profiles-dir /home/jovyan/.dbt" """
    
    if not run_command(generate_cmd):
        print("❌ Échec de la génération de la documentation")
        return False
    
    print("✅ Documentation générée avec succès")
    
    # 2. Copier les fichiers vers nginx
    print("\n📦 Déploiement de la documentation sur nginx...")
    
    # Obtenir le nom du pod nginx
    get_pod_cmd = "kubectl get pods -n dbt-docs -o jsonpath='{.items[0].metadata.name}'"
    result = subprocess.run(get_pod_cmd, shell=True, capture_output=True, text=True)
    pod_name = result.stdout.strip()
    
    if not pod_name:
        print("❌ Impossible de trouver le pod nginx")
        return False
    
    print(f"📦 Pod nginx trouvé: {pod_name}")
    
    # Copier index.html
    print("📄 Copie de index.html...")
    run_command(f"kubectl exec -n jupyterhub jupyter-admin -- cat /home/jovyan/dbt_project/target/index.html > temp_index.html")
    run_command(f"kubectl cp temp_index.html dbt-docs/{pod_name}:/usr/share/nginx/html/index.html")
    
    # Copier catalog.json
    print("📄 Copie de catalog.json...")
    run_command(f"kubectl exec -n jupyterhub jupyter-admin -- cat /home/jovyan/dbt_project/target/catalog.json > temp_catalog.json")
    run_command(f"kubectl cp temp_catalog.json dbt-docs/{pod_name}:/usr/share/nginx/html/catalog.json")
    
    # Copier manifest.json
    print("📄 Copie de manifest.json...")
    run_command(f"kubectl exec -n jupyterhub jupyter-admin -- cat /home/jovyan/dbt_project/target/manifest.json > temp_manifest.json")
    run_command(f"kubectl cp temp_manifest.json dbt-docs/{pod_name}:/usr/share/nginx/html/manifest.json")
    
    # 3. Nettoyer les fichiers temporaires
    print("\n🧹 Nettoyage des fichiers temporaires...")
    run_command("Remove-Item temp_*.html, temp_*.json -Force -ErrorAction SilentlyContinue")
    
    # 4. Vérifier le déploiement
    print("\n✅ Vérification du déploiement...")
    verify_cmd = f"kubectl exec -n dbt-docs {pod_name} -- ls -la /usr/share/nginx/html/"
    run_command(verify_cmd)
    
    print_header("🎉 Documentation DBT mise à jour avec succès!")
    print("\n🌐 Accès à la documentation:")
    print("   📚 DBT Docs: http://localhost:30082")
    print("\n💡 Pour mettre à jour après des changements:")
    print("   python setup/dbt/update_dbt_docs.py")

if __name__ == "__main__":
    main()
