#!/usr/bin/env python3
"""
DataMeesh - DataHub Deployment
Deploys DataHub metadata catalog with Docker Compose
⚠️ Requires 10-12GB RAM (2-3GB additional)
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, check=True):
    """Run command"""
    print(f"\n🔨 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr)
    if check and result.returncode != 0:
        return False
    return True

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def main():
    print_header("🗂️ DataMeesh - DataHub Deployment")
    
    # Detect OS
    os_type = platform.system()
    is_wsl = "microsoft" in platform.uname().release.lower() if os_type == "Linux" else False
    
    # Check RAM
    print("⚠️  IMPORTANT: DataHub Requirements")
    print()
    print("DataHub requires:")
    print("  • 2-3GB additional RAM")
    print("  • Total system RAM: 10-12GB recommended")
    print()
    print("DataHub components:")
    print("  • datahub-gms (Metadata Service)")
    print("  • datahub-frontend (Web UI)")
    print("  • MySQL (Metadata storage)")
    print("  • Elasticsearch (Search & Graph)")
    print("  • Kafka (Event streaming)")
    print("  • Schema Registry")
    print("  • Zookeeper")
    print()
    
    response = input("Continue with DataHub deployment? (yes/no): ").lower()
    if response != "yes":
        print("\n❌ DataHub deployment cancelled.")
        return 0
    
    # 1. Check prerequisites
    print_header("Step 1/4: Checking Prerequisites")
    
    # Check if acryl-datahub is installed
    result = subprocess.run(
        "pip show acryl-datahub",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("📦 Installing acryl-datahub...")
        if not run_command("pip install --upgrade acryl-datahub"):
            print("❌ Failed to install acryl-datahub")
            return 1
    else:
        print("✅ acryl-datahub already installed")
    
    # 2. Start DataHub
    print_header("Step 2/4: Starting DataHub")
    
    print("🚀 Starting DataHub quickstart...")
    print("   This will take 2-3 minutes...")
    print()
    
    # Prepare command based on OS
    if os_type == "Windows" and not is_wsl:
        datahub_cmd = "wsl bash -c 'export PATH=$PATH:~/.local/bin && datahub docker quickstart'"
    else:
        datahub_cmd = "datahub docker quickstart"
    
    print(f"Running: {datahub_cmd}")
    print()
    
    result = subprocess.run(datahub_cmd, shell=True)
    
    if result.returncode != 0:
        print("\n⚠️  DataHub quickstart failed.")
        print()
        print("Troubleshooting:")
        print("  1. Ensure Docker Desktop has 10-12GB RAM")
        print("  2. Check Docker is running: docker ps")
        print("  3. Try manually:")
        if os_type == "Windows":
            print("     wsl datahub docker quickstart")
        else:
            print("     datahub docker quickstart")
        print()
        return 1
    
    # 3. Create ingestion recipes
    print_header("Step 3/4: Creating Ingestion Recipes")
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    recipes_dir = os.path.join(project_root, "recipes")
    
    # Ensure recipes directory exists
    os.makedirs(recipes_dir, exist_ok=True)
    
    # Trino ingestion recipe
    trino_recipe_path = os.path.join(recipes_dir, "datahub_trino_recipe.yml")
    if not os.path.exists(trino_recipe_path):
        trino_recipe = """source:
  type: trino
  config:
    host_port: "localhost:30808"
    database: sales
    username: ""
    
sink:
  type: datahub-rest
  config:
    server: "http://localhost:8080"
"""
        with open(trino_recipe_path, "w") as f:
            f.write(trino_recipe)
        print(f"✅ Created {trino_recipe_path}")
    else:
        print(f"ℹ️  Recipe already exists: {trino_recipe_path}")
    
    # DBT ingestion recipe
    dbt_recipe_path = os.path.join(recipes_dir, "datahub_dbt_recipe.yml")
    if not os.path.exists(dbt_recipe_path):
        dbt_recipe = """source:
  type: dbt
  config:
    manifest_path: "./dbt_target/manifest.json"
    catalog_path: "./dbt_target/catalog.json"
    target_platform: "postgres"
    
sink:
  type: datahub-rest
  config:
    server: "http://localhost:8080"
"""
        with open(dbt_recipe_path, "w") as f:
            f.write(dbt_recipe)
        print(f"✅ Created {dbt_recipe_path}")
    else:
        print(f"ℹ️  Recipe already exists: {dbt_recipe_path}")
    
    # 4. Summary
    print_header("Step 4/4: Verification")
    
    print("⏳ Waiting for DataHub to be ready...")
    print("   (This may take 2-3 minutes)")
    print()
    
    import time
    time.sleep(60)
    
    # Check if DataHub is accessible
    result = subprocess.run(
        "curl -s http://localhost:9002 > /dev/null",
        shell=True,
        capture_output=True
    )
    
    if result.returncode == 0:
        print("✅ DataHub is accessible!")
    else:
        print("⚠️  DataHub may still be starting...")
        print("   Wait 1-2 more minutes and check http://localhost:9002")
    
    # Summary
    print_header("✅ DataHub Deployment Complete")
    
    print("🌐 Access DataHub:")
    print("   URL:      http://localhost:9002")
    print("   Username: datahub")
    print("   Password: datahub")
    print()
    
    print("🔄 Ingest Metadata:")
    print()
    print("   1. Ingest from Trino (Sales + Marketing):")
    if os_type == "Windows":
        print("      wsl datahub ingest -c recipes/datahub_trino_recipe.yml")
    else:
        print("      datahub ingest -c recipes/datahub_trino_recipe.yml")
    print()
    
    print("   2. Ingest from DBT (transformations + lineage):")
    print("      First, copy DBT artifacts from JupyterHub:")
    print("      kubectl cp jupyterhub/<pod-name>:/home/jovyan/dbt_projects/datamesh/target ./dbt_target")
    print()
    print("      Then ingest:")
    if os_type == "Windows":
        print("      wsl datahub ingest -c recipes/datahub_dbt_recipe.yml")
    else:
        print("      datahub ingest -c recipes/datahub_dbt_recipe.yml")
    print()
    
    print("📚 What you'll see in DataHub:")
    print("   • All tables from Sales & Marketing domains")
    print("   • DBT models and transformations")
    print("   • Data lineage graphs")
    print("   • Column-level metadata")
    print("   • Documentation")
    print()
    
    print("🔧 Management Commands:")
    print("   Stop DataHub:")
    if os_type == "Windows":
        print("     wsl datahub docker quickstart --stop")
    else:
        print("     datahub docker quickstart --stop")
    print()
    print("   View logs:")
    print("     docker-compose -f ~/.datahub/quickstart/docker-compose.yml logs")
    print()
    print("   Clean up:")
    if os_type == "Windows":
        print("     wsl datahub docker nuke")
    else:
        print("     datahub docker nuke")
    print()
    
    print("📖 Documentation:")
    print("   See docs/guides/DATAHUB_GUIDE.md for detailed usage")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

