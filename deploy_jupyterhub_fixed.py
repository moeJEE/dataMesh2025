#!/usr/bin/env python3
"""
Deploy JupyterHub with Fixed Configuration
Deploys JupyterHub with correct proxy API configuration
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
    print("  🚀 DEPLOYING JUPYTERHUB WITH FIXED CONFIGURATION")
    print("="*70)
    
    # 1. Delete existing deployment if it exists
    print("\n📦 Step 1/4: Cleaning up existing deployment...")
    run_command("kubectl delete namespace jupyterhub", check=False)
    time.sleep(10)
    
    # 2. Create namespace
    print("\n📦 Step 2/4: Creating namespace...")
    run_command("kubectl create namespace jupyterhub")
    
    # 3. Deploy with fixed configuration
    print("\n📦 Step 3/4: Deploying JupyterHub with fixed config...")
    
    deploy_cmd = """helm upgrade --install jupyterhub jupyterhub/jupyterhub \
        --namespace jupyterhub \
        --version=3.0.0 \
        --values setup/helm/jupyterhub-values.yaml \
        --timeout=600s"""
    
    if not run_command(deploy_cmd):
        print("❌ Failed to deploy JupyterHub")
        return 1
    
    # 4. Wait and verify
    print("\n⏳ Step 4/4: Waiting for deployment to complete...")
    time.sleep(30)
    
    print("\n🔍 Pod Status:")
    run_command("kubectl get pods -n jupyterhub", check=False)
    
    print("\n🌐 Service Status:")
    run_command("kubectl get services -n jupyterhub", check=False)
    
    print("\n📋 Hub Logs (last 10 lines):")
    run_command("kubectl logs -n jupyterhub deployment/hub --tail=10", check=False)
    
    print("\n📋 Proxy Logs (last 10 lines):")
    run_command("kubectl logs -n jupyterhub deployment/proxy --tail=10", check=False)
    
    print("\n✅ JupyterHub Deployment Complete!")
    print("\n🌐 Access JupyterHub:")
    print("   URL: http://localhost:30080")
    print("   Username: admin")
    print("   Password: datamesh2024")
    
    print("\n🔍 Check if configuration is correct:")
    print("   Look for 'api_url: http://proxy-api:8001' in hub logs")
    print("   Look for 'Proxy API at http://*:8001/api/routes' in proxy logs")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
