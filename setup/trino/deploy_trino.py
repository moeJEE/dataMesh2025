#!/usr/bin/env python3
"""
DataMeesh - Trino Stack Deployment
Deploys Trino, Minio, and Hive Metastore for federated queries
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

def wait_for_pods(namespace, timeout=300):
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
        
        time.sleep(10)
    
    print(f"⚠️  Timeout waiting for pods in {namespace}")
    return False

def main():
    print_header("🔮 DataMeesh - Trino Stack Deployment")
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_file = os.path.join(project_root, "config", "minio-trino-hive.yaml")
    
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        return 1
    
    print(f"📁 Config file: {config_file}")
    
    # 1. Check prerequisites
    print_header("Step 1/3: Checking Prerequisites")
    
    if not run_command("kubectl cluster-info"):
        print("❌ Cannot connect to Kubernetes cluster")
        return 1
    
    # 2. Create namespace if not exists
    print_header("Step 2/4: Creating Namespace")
    
    # Check if namespace exists
    result = subprocess.run(
        "kubectl get namespace data-platform",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("📦 Creating namespace: data-platform")
        if not run_command("kubectl create namespace data-platform"):
            print("❌ Failed to create namespace")
            return 1
    else:
        print("✅ Namespace data-platform already exists")
    
    # 3. Deploy Trino stack
    print_header("Step 3/4: Deploying Trino Stack")
    
    print("📦 Deploying components:")
    print("   • Minio (S3-compatible storage)")
    print("   • Hive PostgreSQL")
    print("   • Hive Metastore")
    print("   • Trino Coordinator")
    print("   • Trino Worker")
    print()
    
    if not run_command(f"kubectl apply -f {config_file}"):
        print("❌ Failed to deploy Trino stack")
        return 1
    
    # 4. Wait for pods
    print_header("Step 4/4: Waiting for Pods")
    
    if not wait_for_pods("data-platform", timeout=300):
        print("⚠️  Some pods may not be ready yet")
        print("   Check status: kubectl get pods -n data-platform")
    
    # Show status
    print("\n📊 Trino Stack Status:")
    run_command("kubectl get pods,svc -n data-platform", check=False)
    
    # Summary
    print_header("✅ Trino Stack Deployment Complete")
    
    print("📦 Deployed Components:")
    print("  ✅ Minio (S3 storage)")
    print("  ✅ Hive PostgreSQL")
    print("  ✅ Hive Metastore")
    print("  ✅ Trino Coordinator (1.5GB)")
    print("  ✅ Trino Worker (1.5GB)")
    print()
    
    print("🌐 Access Points:")
    print("   Trino Web UI: http://localhost:30808")
    print("   Minio Console: http://localhost:30901")
    print("     Username: minioadmin")
    print("     Password: minioadmin")
    print()
    
    print("📊 Query Examples:")
    print("   # Connect via Trino CLI (in JupyterHub)")
    print("   trino --server http://trino-coordinator.data-platform.svc.cluster.local:8080")
    print()
    print("   # Query Sales data")
    print("   SELECT * FROM sales.public.customers LIMIT 10;")
    print()
    print("   # Query Marketing data")
    print("   SELECT * FROM marketing.public.campaigns LIMIT 10;")
    print()
    
    print("📖 Next Steps:")
    print("   1. Query data from JupyterHub or Trino Web UI")
    print("   2. Check examples/trino_queries.sql for more queries")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

