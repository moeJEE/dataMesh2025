#!/usr/bin/env python3
"""
DataMeesh - Kubernetes Core Deployment
Deploys core domains: Sales + Marketing with PostgreSQL and APIs
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
    if result.stderr and (result.returncode != 0 or check):
        print(result.stderr)
    if check and result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        return False
    return True

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def wait_for_pods(namespace, timeout=180):
    """Wait for all pods in namespace to be ready"""
    print(f"\n⏳ Waiting for pods in {namespace} to be ready (timeout: {timeout}s)...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = subprocess.run(
            f"kubectl get pods -n {namespace} --no-headers",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            all_ready = True
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    status = parts[2]
                    if status not in ['Running', 'Completed']:
                        all_ready = False
                        break
            
            if all_ready:
                print(f"✅ All pods in {namespace} are ready!")
                return True
        
        time.sleep(5)
    
    print(f"⚠️  Timeout waiting for pods in {namespace}")
    return False

def main():
    print_header("🚀 DataMeesh - Kubernetes Core Deployment")
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_file = os.path.join(project_root, "config", "datamesh.yaml")
    
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        return 1
    
    print(f"📁 Config file: {config_file}")
    print(f"📍 Project root: {project_root}")
    
    # 1. Check kubectl
    print_header("Step 1/4: Verifying kubectl")
    
    if not run_command("kubectl version --client"):
        print("❌ kubectl not found. Please install kubectl first.")
        return 1
    
    # Check cluster
    if not run_command("kubectl cluster-info"):
        print("❌ Cannot connect to Kubernetes cluster.")
        print("   Enable Kubernetes in Docker Desktop:")
        print("   Docker Desktop → Settings → Kubernetes → Enable")
        return 1
    
    # 2. Deploy core domains
    print_header("Step 2/4: Deploying Core Domains")
    
    print("📦 Deploying Sales and Marketing domains...")
    print("   • Sales Domain: PostgreSQL + APIs")
    print("   • Marketing Domain: PostgreSQL + APIs")
    print("   • Network Policies")
    print("   • Resource Quotas")
    print("   • Auto-scaling (HPA)")
    print()
    
    if not run_command(f"kubectl apply -f {config_file}"):
        print("❌ Failed to deploy core domains")
        return 1
    
    # 3. Wait for pods
    print_header("Step 3/4: Waiting for Pods")
    
    # Wait for Sales domain
    if not wait_for_pods("sales-domain", timeout=180):
        print("⚠️  Sales domain pods not ready yet")
        print("   Check status: kubectl get pods -n sales-domain")
    
    # Wait for Marketing domain
    if not wait_for_pods("marketing-domain", timeout=180):
        print("⚠️  Marketing domain pods not ready yet")
        print("   Check status: kubectl get pods -n marketing-domain")
    
    # 4. Verify deployment
    print_header("Step 4/4: Verifying Deployment")
    
    print("📊 Sales Domain:")
    run_command("kubectl get pods,svc -n sales-domain", check=False)
    
    print("\n📊 Marketing Domain:")
    run_command("kubectl get pods,svc -n marketing-domain", check=False)
    
    # Summary
    print_header("✅ Kubernetes Core Deployment Complete")
    
    print("📦 Deployed Components:")
    print("  ✅ Sales Domain")
    print("     • PostgreSQL (256MB)")
    print("     • Sales APIs (2 replicas)")
    print("     • Secrets & ConfigMaps")
    print("  ✅ Marketing Domain")
    print("     • PostgreSQL (128MB)")
    print("     • Marketing APIs (2 replicas)")
    print("     • Secrets & ConfigMaps")
    print("  ✅ Network Policies")
    print("  ✅ Resource Quotas")
    print("  ✅ Horizontal Pod Autoscalers")
    print()
    
    print("🌐 Access Points:")
    print("   Sales PostgreSQL:")
    print("     kubectl port-forward -n sales-domain svc/sales-postgres 5432:5432")
    print("   Marketing PostgreSQL:")
    print("     kubectl port-forward -n marketing-domain svc/marketing-postgres 5432:5432")
    print()
    
    print("📖 Next Steps:")
    print("   1. Load sample data:")
    print("      python setup/data/load_sample_data.py")
    print()
    print("   2. Deploy additional components:")
    print("      python setup/trino/deploy_trino.py")
    print("      python setup/helm/deploy_jupyterhub.py")
    print("      python setup/grafana/deploy_grafana.py")
    print()
    print("   3. Or deploy everything at once:")
    print("      python setup/deploy_complete_stack.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

