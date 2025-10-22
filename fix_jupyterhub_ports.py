#!/usr/bin/env python3
"""
Fix JupyterHub Port Configuration
Fixes the port mismatch issue (8000/8081 vs 80/8080)
"""

import subprocess
import sys
import time

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

def main():
    print("\n" + "="*70)
    print("  🔧 FIXING JUPYTERHUB PORT CONFIGURATION")
    print("="*70)
    
    # 1. Delete existing JupyterHub deployment
    print("\n📦 Step 1/4: Removing existing JupyterHub...")
    run_command("kubectl delete namespace jupyterhub", check=False)
    
    # Wait for namespace to be deleted
    print("⏳ Waiting for namespace to be deleted...")
    time.sleep(10)
    
    # 2. Recreate namespace
    print("\n📦 Step 2/4: Creating fresh namespace...")
    run_command("kubectl create namespace jupyterhub")
    
    # 3. Deploy with fixed configuration
    print("\n📦 Step 3/4: Deploying JupyterHub with correct ports...")
    
    # Use the fixed values file
    deploy_cmd = """helm upgrade --install jupyterhub jupyterhub/jupyterhub \
        --namespace jupyterhub \
        --version=3.0.0 \
        --values setup/helm/jupyterhub-values.yaml \
        --timeout=600s"""
    
    if not run_command(deploy_cmd):
        print("❌ Failed to deploy JupyterHub")
        return 1
    
    # 4. Wait and verify
    print("\n⏳ Step 4/4: Waiting for JupyterHub to be ready...")
    time.sleep(30)
    
    # Check pod status
    print("\n📊 Pod Status:")
    run_command("kubectl get pods -n jupyterhub", check=False)
    
    # Check services
    print("\n🌐 Service Status:")
    run_command("kubectl get services -n jupyterhub", check=False)
    
    print("\n✅ JupyterHub Port Fix Complete!")
    print("\n🌐 Access JupyterHub:")
    print("   URL: http://localhost:30080")
    print("   Username: admin")
    print("   Password: datamesh2024")
    
    print("\n🔍 Check logs if issues persist:")
    print("   kubectl logs -n jupyterhub deployment/hub")
    print("   kubectl logs -n jupyterhub deployment/proxy")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
