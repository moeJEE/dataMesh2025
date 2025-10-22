#!/usr/bin/env python3
"""
Force Restart JupyterHub Components
Restarts JupyterHub to apply new port configuration
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
    print("  🔄 FORCE RESTARTING JUPYTERHUB COMPONENTS")
    print("="*70)
    
    # 1. Restart the proxy deployment
    print("\n📦 Step 1/4: Restarting proxy deployment...")
    run_command("kubectl rollout restart deployment/proxy -n jupyterhub")
    
    # 2. Restart the hub deployment
    print("\n📦 Step 2/4: Restarting hub deployment...")
    run_command("kubectl rollout restart deployment/hub -n jupyterhub")
    
    # 3. Wait for restarts to complete
    print("\n⏳ Step 3/4: Waiting for restarts to complete...")
    print("   This may take 2-3 minutes...")
    
    # Wait for proxy to be ready
    print("   Waiting for proxy...")
    run_command("kubectl rollout status deployment/proxy -n jupyterhub --timeout=300s")
    
    # Wait for hub to be ready
    print("   Waiting for hub...")
    run_command("kubectl rollout status deployment/hub -n jupyterhub --timeout=300s")
    
    # 4. Check status
    print("\n📊 Step 4/4: Checking deployment status...")
    
    print("\n🔍 Pod Status:")
    run_command("kubectl get pods -n jupyterhub", check=False)
    
    print("\n🌐 Service Status:")
    run_command("kubectl get services -n jupyterhub", check=False)
    
    print("\n📋 Hub Logs (last 15 lines):")
    run_command("kubectl logs -n jupyterhub deployment/hub --tail=15", check=False)
    
    print("\n📋 Proxy Logs (last 15 lines):")
    run_command("kubectl logs -n jupyterhub deployment/proxy --tail=15", check=False)
    
    print("\n✅ JupyterHub Restart Complete!")
    print("\n🌐 Access JupyterHub:")
    print("   URL: http://localhost:30080")
    print("   Username: admin")
    print("   Password: datamesh2024")
    
    print("\n🔍 Check if ports are now correct:")
    print("   Look for 'Proxying http://*:80 to http://hub:8080' in proxy logs")
    print("   Look for 'Running JupyterHub at http://0.0.0.0:8080' in hub logs")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
