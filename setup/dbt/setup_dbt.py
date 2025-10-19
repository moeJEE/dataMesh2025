#!/usr/bin/env python3
"""
DataMeesh - DBT Setup
Sets up DBT project in JupyterHub with models and configurations
"""

import subprocess
import sys
import os

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
    print_header("🔧 DataMeesh - DBT Setup")
    
    print("This script will copy DBT models to your JupyterHub pod.")
    print()
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    dbt_source = os.path.join(script_dir, "models")
    
    # 1. Find JupyterHub pod
    print_header("Step 1/3: Finding JupyterHub Pod")
    
    result = subprocess.run(
        "kubectl get pods -n jupyterhub -l component=singleuser-server --no-headers",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print("❌ No active JupyterHub user pods found")
        print("   1. Open JupyterHub: http://localhost:30080")
        print("   2. Login and start a notebook")
        print("   3. Run this script again")
        return 1
    
    pod_name = result.stdout.strip().split()[0]
    print(f"✅ Found pod: {pod_name}")
    
    # 2. Create DBT project structure
    print_header("Step 2/3: Creating DBT Project")
    
    print("📁 Creating DBT directories...")
    run_command(f"kubectl exec -n jupyterhub {pod_name} -- mkdir -p ~/dbt_projects/datamesh/models")
    
    # 3. Copy DBT files
    print_header("Step 3/3: Copying DBT Files")
    
    if os.path.exists(dbt_source):
        print(f"📦 Copying DBT models from {dbt_source}")
        
        # Copy entire models directory
        copy_cmd = f"kubectl cp {dbt_source} jupyterhub/{pod_name}:/home/jovyan/dbt_projects/datamesh/"
        if not run_command(copy_cmd):
            print("⚠️  Failed to copy DBT models")
    else:
        print(f"⚠️  DBT models directory not found: {dbt_source}")
        print("   DBT project structure will be created manually")
    
    # Summary
    print_header("✅ DBT Setup Complete")
    
    print("📝 Next Steps in JupyterHub Terminal:")
    print()
    print("   1. Open a terminal in JupyterHub")
    print()
    print("   2. Navigate to DBT project:")
    print("      cd ~/dbt_projects/datamesh")
    print()
    print("   3. Initialize profiles.yml (if not exists):")
    print("      mkdir -p ~/.dbt")
    print("      cat > ~/.dbt/profiles.yml << 'EOF'")
    print("datamesh_dbt:")
    print("  target: prod")
    print("  outputs:")
    print("    prod:")
    print("      type: postgres")
    print("      host: sales-postgres.sales-domain.svc.cluster.local")
    print("      port: 5432")
    print("      user: sales_user")
    print("      password: SuperSecurePass123!")
    print("      database: sales_db")
    print("      schema: dbt_marts")
    print("      threads: 4")
    print("EOF")
    print()
    print("   4. Test connection:")
    print("      dbt debug")
    print()
    print("   5. Run DBT models:")
    print("      dbt run")
    print()
    print("   6. Run tests:")
    print("      dbt test")
    print()
    print("   7. Generate documentation:")
    print("      dbt docs generate")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

