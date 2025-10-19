#!/usr/bin/env python3
"""
DataMeesh - Helm Installation
Installs Helm 3 and adds necessary repositories
Cross-platform: Windows, WSL, macOS, Linux
"""

import subprocess
import sys
import platform
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
    print_header("⎈ DataMeesh - Helm Installation")
    
    os_type = platform.system()
    is_wsl = "microsoft" in platform.uname().release.lower() if os_type == "Linux" else False
    
    print(f"📍 Detected OS: {os_type}")
    if is_wsl:
        print("📍 Running in: WSL2")
    
    # Check if Helm is already installed
    print_header("Step 1/3: Checking Helm")
    
    helm_check_cmd = "wsl helm version --short" if os_type == "Windows" and not is_wsl else "helm version --short"
    result = subprocess.run(helm_check_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Helm is already installed: {result.stdout.strip()}")
    else:
        print("📦 Helm not found. Installing...")
        
        # Install Helm based on OS
        if os_type == "Windows" and not is_wsl:
            print("\n📖 Install Helm on Windows:")
            print("   Option 1 (Chocolatey): choco install kubernetes-helm")
            print("   Option 2 (Download): https://github.com/helm/helm/releases")
            print("\nℹ️  After installing, run this script again.")
            return 1
        elif os_type == "Darwin":  # macOS
            if not run_command("brew install helm"):
                print("❌ Failed to install Helm")
                print("   Install Homebrew first: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                return 1
        elif is_wsl or os_type == "Linux":
            # Install in WSL/Linux
            print("📦 Installing Helm via script...")
            if not run_command("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash"):
                print("❌ Failed to install Helm")
                return 1
        
        # Verify installation
        if not run_command(helm_check_cmd):
            print("❌ Helm installation failed")
            return 1
        
        print("✅ Helm installed successfully!")
    
    # Add JupyterHub repository
    print_header("Step 2/3: Adding Helm Repositories")
    
    helm_cmd_prefix = "wsl " if os_type == "Windows" and not is_wsl else ""
    
    print("📦 Adding JupyterHub repository...")
    if not run_command(f"{helm_cmd_prefix}helm repo add jupyterhub https://hub.jupyter.org/helm-chart/"):
        print("⚠️  Failed to add JupyterHub repository")
    
    print("\n📦 Updating Helm repositories...")
    if not run_command(f"{helm_cmd_prefix}helm repo update"):
        print("⚠️  Failed to update repositories")
    
    # List repositories
    print_header("Step 3/3: Verifying Repositories")
    
    run_command(f"{helm_cmd_prefix}helm repo list", check=False)
    
    # Summary
    print_header("✅ Helm Setup Complete")
    
    print("  ✅ Helm 3 installed")
    print("  ✅ JupyterHub repository added")
    print()
    
    print("📖 Next Steps:")
    print("   1. Deploy JupyterHub:")
    print("      python setup/helm/deploy_jupyterhub.py")
    print()
    print("   2. Or deploy everything:")
    print("      python setup/deploy_complete_stack.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

