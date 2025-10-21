#!/usr/bin/env python3
"""
Script à exécuter DANS JupyterHub pour mettre à jour la documentation
"""

import subprocess
import os

def run_command(cmd):
    """Exécute une commande et affiche le résultat"""
    print(f"🔨 {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("🔄 Mise à jour de la documentation DBT depuis JupyterHub...")
    
    # 1. Générer la documentation
    print("\n📚 Génération de la documentation...")
    if not run_command("dbt docs generate --profiles-dir /home/jovyan/.dbt"):
        print("❌ Erreur lors de la génération")
        return
    
    print("✅ Documentation générée!")
    print("\n💡 Pour déployer sur nginx, exécutez depuis votre machine:")
    print("   python setup/dbt/update_docs_simple.py")
    print("\n🌐 Ou accédez directement à la documentation locale:")
    print("   dbt docs serve --profiles-dir /home/jovyan/.dbt --port 8080")

if __name__ == "__main__":
    main()
