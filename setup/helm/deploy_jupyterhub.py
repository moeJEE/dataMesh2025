#!/usr/bin/env python3
"""
DataMeesh - JupyterHub Deployment
Deploys JupyterHub with custom DBT image using Helm
"""

import subprocess
import sys
import os
import time
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
    print_header("📓 DataMeesh - JupyterHub Deployment")
    
    # Detect OS
    os_type = platform.system()
    is_wsl = "microsoft" in platform.uname().release.lower() if os_type == "Linux" else False
    helm_cmd_prefix = "wsl " if os_type == "Windows" and not is_wsl else ""
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # 1. Check prerequisites
    print_header("Step 1/5: Checking Prerequisites")
    
    if not run_command(f"{helm_cmd_prefix}helm version --short"):
        print("❌ Helm not found. Install it first:")
        print("   python setup/helm/install_helm.py")
        return 1
    
    if not run_command("kubectl cluster-info"):
        print("❌ Cannot connect to Kubernetes cluster")
        return 1
    
    # 2. Build custom Docker image
    print_header("Step 2/5: Building Custom JupyterHub Image")
    
    dockerfile_path = os.path.join(project_root, "setup", "docker", "Dockerfile.jupyterhub-dbt")
    
    if not os.path.exists(dockerfile_path):
        print(f"⚠️  Dockerfile not found at {dockerfile_path}")
        print("   Using default JupyterHub image instead")
        image_name = "jupyter/datascience-notebook:latest"
    else:
        print(f"🐳 Building Docker image from {dockerfile_path}")
        
        # Build image
        build_cmd = f"docker build -f {dockerfile_path} -t jupyterhub-dbt:latest {os.path.dirname(dockerfile_path)}"
        if not run_command(build_cmd):
            print("⚠️  Failed to build custom image, using default")
            image_name = "jupyter/datascience-notebook:latest"
        else:
            print("✅ Custom image built successfully")
            image_name = "jupyterhub-dbt:latest"
    
    # 3. Create namespace
    print_header("Step 3/5: Creating Namespace")
    
    run_command("kubectl create namespace jupyterhub", check=False)
    
    # 4. Generate Helm values
    print_header("Step 4/5: Generating Helm Values")
    
    # Generate secret token
    import secrets
    token = secrets.token_hex(32)
    
    values_content = f"""# JupyterHub Helm Values - DataMeesh
proxy:
  secretToken: "{token}"

hub:
  config:
    JupyterHub:
      admin_users:
        - admin
    DummyAuthenticator:
      password: "datamesh2024"
    Authenticator:
      admin_users:
        - admin
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "250m"

singleuser:
  image:
    name: {image_name.split(":")[0]}
    tag: {image_name.split(":")[1] if ":" in image_name else "latest"}
    pullPolicy: {"Never" if "jupyterhub-dbt" in image_name else "IfNotPresent"}
  cpu:
    limit: 0.5
    guarantee: 0.1
  memory:
    limit: "1G"
    guarantee: "512M"
  storage:
    capacity: "2Gi"

scheduling:
  userScheduler:
    enabled: false

cull:
  enabled: true
  timeout: 3600
  every: 600

rbac:
  create: true

debug:
  enabled: false
"""
    
    values_file = os.path.join(project_root, "setup", "helm", "jupyterhub-values.yaml")
    with open(values_file, "w") as f:
        f.write(values_content)
    
    print(f"✅ Helm values file created: {values_file}")
    
    # 5. Deploy JupyterHub
    print_header("Step 5/5: Deploying JupyterHub")
    
    print("📦 Installing JupyterHub via Helm...")
    print("   This may take 2-3 minutes...")
    
    deploy_cmd = f"{helm_cmd_prefix}helm upgrade --install jupyterhub jupyterhub/jupyterhub --namespace jupyterhub --version=3.0.0 --values {values_file} --timeout=600s"
    
    if not run_command(deploy_cmd):
        print("❌ Failed to deploy JupyterHub")
        return 1
    
    print("\n⏳ Waiting for JupyterHub to be ready...")
    time.sleep(30)
    
    # Check pod status
    print("\n📊 Pod Status:")
    run_command("kubectl get pods -n jupyterhub", check=False)
    
    # Summary
    print_header("✅ JupyterHub Deployment Complete")
    
    print("📦 Deployed Components:")
    print("  ✅ JupyterHub Hub")
    print("  ✅ JupyterHub Proxy")
    print(f"  ✅ Custom Image: {image_name}")
    print()
    
    print("🌐 Access JupyterHub:")
    print("   URL: http://localhost:30080")
    print("   Username: admin")
    print("   Password: datamesh2024")
    print()
    
    print("📖 Next Steps:")
    print("   1. Access JupyterHub and start a notebook")
    print()
    print("   2. Setup DBT:")
    print("      python setup/dbt/setup_dbt.py")
    print()
    print("   3. Load sample data:")
    print("      python setup/data/load_sample_data.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

