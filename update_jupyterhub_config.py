#!/usr/bin/env python3
"""
Update JupyterHub Configuration
Updates JupyterHub to use modern ConfigurableHTTPProxy configuration
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
    print("  🔧 UPDATING JUPYTERHUB CONFIGURATION")
    print("="*70)
    
    # 1. Update the deployment with modern config
    print("\n📦 Step 1/3: Updating JupyterHub with modern configuration...")
    
    update_cmd = """helm upgrade jupyterhub jupyterhub/jupyterhub \
        --namespace jupyterhub \
        --version=3.0.0 \
        --values setup/helm/jupyterhub-values.yaml \
        --timeout=600s"""
    
    if not run_command(update_cmd):
        print("❌ Failed to update JupyterHub")
        return 1
    
    # 2. Wait for update to complete
    print("\n⏳ Step 2/3: Waiting for update to complete...")
    time.sleep(30)
    
    # 3. Check status
    print("\n📊 Step 3/3: Checking deployment status...")
    
    print("\n🔍 Pod Status:")
    run_command("kubectl get pods -n jupyterhub", check=False)
    
    print("\n🌐 Service Status:")
    run_command("kubectl get services -n jupyterhub", check=False)
    
    print("\n📋 Hub Logs (last 10 lines):")
    run_command("kubectl logs -n jupyterhub deployment/hub --tail=10", check=False)
    
    print("\n📋 Proxy Logs (last 10 lines):")
    run_command("kubectl logs -n jupyterhub deployment/proxy --tail=10", check=False)
    
    print("\n✅ JupyterHub Configuration Updated!")
    print("\n🌐 Access JupyterHub:")
    print("   URL: http://localhost:30080")
    print("   Username: admin")
    print("   Password: datamesh2024")
    
    print("\n🔍 If still having issues, check:")
    print("   kubectl logs -n jupyterhub deployment/hub -f")
    print("   kubectl logs -n jupyterhub deployment/proxy -f")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
