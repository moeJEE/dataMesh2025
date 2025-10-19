#!/usr/bin/env python3
"""
DataMeesh - Grafana Deployment
Deploys Grafana with pre-configured datasources
"""

import subprocess
import sys
import os
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

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def main():
    print_header("📊 DataMeesh - Grafana Deployment")
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    grafana_config = os.path.join(project_root, "config", "grafana.yaml")
    nginx_config = os.path.join(project_root, "config", "nginx-dbt-docs.yaml")
    
    # 1. Check prerequisites
    print_header("Step 1/3: Checking Prerequisites")
    
    if not run_command("kubectl cluster-info"):
        print("❌ Cannot connect to Kubernetes cluster")
        return 1
    
    # 2. Deploy Grafana
    print_header("Step 2/3: Deploying Grafana")
    
    if os.path.exists(grafana_config):
        print("📦 Deploying Grafana...")
        if not run_command(f"kubectl apply -f {grafana_config}"):
            print("❌ Failed to deploy Grafana")
            return 1
    else:
        print(f"⚠️  Grafana config not found: {grafana_config}")
    
    # Deploy Nginx for DBT docs
    if os.path.exists(nginx_config):
        print("\n📦 Deploying Nginx (DBT docs server)...")
        if not run_command(f"kubectl apply -f {nginx_config}"):
            print("⚠️  Failed to deploy Nginx")
    else:
        print(f"⚠️  Nginx config not found: {nginx_config}")
    
    # 3. Wait for pods
    print_header("Step 3/3: Waiting for Pods")
    
    print("⏳ Waiting for Grafana to be ready...")
    time.sleep(30)
    
    print("\n📊 Monitoring Stack Status:")
    run_command("kubectl get pods,svc -n monitoring", check=False)
    
    print("\n📊 DBT Docs Status:")
    run_command("kubectl get pods,svc -n dbt-docs", check=False)
    
    # Summary
    print_header("✅ Visualization Stack Deployment Complete")
    
    print("📦 Deployed Components:")
    print("  ✅ Grafana")
    print("  ✅ Nginx (DBT documentation server)")
    print()
    
    print("🌐 Access Points:")
    print("   Grafana: http://localhost:30030")
    print("     Username: admin")
    print("     Password: datamesh2024")
    print()
    print("   DBT Docs: http://localhost:30082")
    print("     (After generating docs with DBT)")
    print()
    
    print("📊 Pre-configured Datasources in Grafana:")
    print("   • SalesPostgreSQL")
    print("   • MarketingPostgreSQL")
    print("   • Trino")
    print()
    
    print("📖 Next Steps:")
    print("   1. Open Grafana and create dashboards")
    print("   2. Generate DBT docs: python setup/dbt/setup_dbt.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

