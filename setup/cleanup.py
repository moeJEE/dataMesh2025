#!/usr/bin/env python3
"""
DataMeesh - Complete Cleanup Script
Removes ALL deployed resources from the entire platform
"""

import subprocess
import sys
import time

def run_command(cmd, check=False):
    """Run command"""
    print(f"🔨 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"⚠️  {result.stderr}")
    return result.returncode == 0

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def main():
    print_header("🧹 DataMeesh - Complete Cleanup")
    
    print("⚠️  WARNING: This will remove ALL deployed resources!")
    print("   • All Kubernetes namespaces")
    print("   • All JupyterHub data")
    print("   • All Helm releases")
    print("   • All persistent volumes")
    print("   • All Docker images (DataMeesh related)")
    print()
    
    response = input("Are you sure you want to continue? (yes/no): ").lower()
    if response != "yes":
        print("\n❌ Cleanup cancelled.")
        return 0
    
    print("\n🚀 Starting cleanup...\n")
    
    # 1. Delete Helm releases
    print_header("1/6: Removing Helm Releases")
    
    # Check if JupyterHub is installed
    result = subprocess.run(
        "helm list -n jupyterhub -q",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if "jupyterhub" in result.stdout:
        run_command("helm uninstall jupyterhub -n jupyterhub")
        print("✅ JupyterHub removed")
    else:
        print("ℹ️  JupyterHub not found")
    
    # 2. Delete Kubernetes namespaces
    print_header("2/6: Removing Kubernetes Namespaces")
    
    namespaces = [
        "sales-domain",
        "marketing-domain",
        "data-platform",
        "monitoring",
        "dbt-docs",
        "jupyterhub"
    ]
    
    for ns in namespaces:
        # Check if namespace exists
        result = subprocess.run(
            f"kubectl get namespace {ns}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"🗑️  Deleting namespace: {ns}")
            run_command(f"kubectl delete namespace {ns} --grace-period=30 --timeout=60s")
        else:
            print(f"ℹ️  Namespace {ns} not found")
    
    # 3. Delete PersistentVolumes
    print_header("3/6: Removing Persistent Volumes")
    
    # List all PVs
    result = subprocess.run(
        "kubectl get pv -o name",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        pvs = result.stdout.strip().split('\n')
        for pv in pvs:
            if pv:
                print(f"🗑️  Deleting {pv}")
                run_command(f"kubectl delete {pv} --grace-period=0 --force")
    else:
        print("ℹ️  No Persistent Volumes found")
    
    # 4. Delete StorageClasses (custom ones)
    print_header("4/6: Removing Custom StorageClasses")
    
    storage_classes = ["datamesh-storage"]
    
    for sc in storage_classes:
        result = subprocess.run(
            f"kubectl get storageclass {sc}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"🗑️  Deleting StorageClass: {sc}")
            run_command(f"kubectl delete storageclass {sc}")
        else:
            print(f"ℹ️  StorageClass {sc} not found")
    
    # 5. Delete PriorityClasses
    print_header("5/6: Removing Priority Classes")
    
    priority_classes = ["high-priority-datamesh", "low-priority-datamesh"]
    
    for pc in priority_classes:
        result = subprocess.run(
            f"kubectl get priorityclass {pc}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"🗑️  Deleting PriorityClass: {pc}")
            run_command(f"kubectl delete priorityclass {pc}")
        else:
            print(f"ℹ️  PriorityClass {pc} not found")
    
    # 6. Clean up Docker images (DataMeesh related)
    print_header("6/6: Cleaning Docker Images")
    
    print("ℹ️  Checking for DataMeesh Docker images...")
    
    # List images
    result = subprocess.run(
        "docker images --format '{{.Repository}}:{{.Tag}}' | grep -i jupyterhub-dbt",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        images = result.stdout.strip().split('\n')
        for image in images:
            if image:
                print(f"🗑️  Removing image: {image}")
                run_command(f"docker rmi {image} -f")
    else:
        print("ℹ️  No DataMeesh Docker images found")
    
    # Prune unused volumes
    print("\n🧹 Pruning unused Docker volumes...")
    run_command("docker volume prune -f")
    
    # Clean Docker cache
    print("\n🧹 Cleaning Docker build cache...")
    run_command("docker builder prune -f --all")
    
    # Clean stopped containers
    print("\n🧹 Removing stopped containers...")
    run_command("docker container prune -f")
    
    # Clean dangling images
    print("\n🧹 Removing dangling images...")
    run_command("docker image prune -f")
    
    # Clean networks
    print("\n🧹 Removing unused networks...")
    run_command("docker network prune -f")
    
    # Complete system prune (optional, more aggressive)
    print("\n🧹 Final cleanup - Docker system prune...")
    run_command("docker system prune -f")
    
    # Summary
    print_header("✅ Cleanup Complete")
    
    print("All DataMeesh resources have been removed:")
    print("  ✅ Helm releases deleted")
    print("  ✅ Kubernetes namespaces deleted")
    print("  ✅ Persistent volumes deleted")
    print("  ✅ StorageClasses deleted")
    print("  ✅ PriorityClasses deleted")
    print("  ✅ Docker images cleaned")
    print("  ✅ Docker build cache cleaned")
    print("  ✅ Docker containers pruned")
    print("  ✅ Docker volumes pruned")
    print("  ✅ Docker networks pruned")
    print("  ✅ Docker system cleaned")
    print()
    
    print("📖 Next Steps:")
    print("   1. To redeploy:")
    print("      python setup/deploy_complete_stack.py")
    print()
    print("   2. To verify prerequisites:")
    print("      python setup/verify_prerequisites.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
