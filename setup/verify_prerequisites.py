#!/usr/bin/env python3
"""
DataMeesh - Complete Prerequisites Verification
Verifies all requirements for the entire platform
Cross-platform: Windows, WSL, macOS, Linux
"""

import subprocess
import sys
import os
import platform
import shutil

def run_command(cmd, check=False):
    """Run command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def check_item(name, success, details=""):
    """Print check result"""
    status = "✅" if success else "❌"
    print(f"{status} {name}")
    if details and not success:
        print(f"   └─ {details}")
    return success

def main():
    print_header("🔍 DataMeesh - Prerequisites Verification")
    
    checks_passed = []
    checks_failed = []
    
    # Detect OS
    os_type = platform.system()
    is_wsl = "microsoft" in platform.uname().release.lower() if os_type == "Linux" else False
    
    print(f"📍 Detected OS: {os_type}")
    if is_wsl:
        print(f"📍 Running in: WSL2\n")
    else:
        print()
    
    # 1. Check Python
    print_header("1/8: Python")
    success = sys.version_info >= (3, 8)
    if check_item(f"Python {sys.version.split()[0]}", success):
        checks_passed.append("Python 3.8+")
    else:
        checks_failed.append("Python 3.8+")
        print("   └─ Install Python 3.8 or higher")
    
    # 2. Check Docker
    print_header("2/8: Docker")
    docker_cmd = "wsl docker --version" if os_type == "Windows" and not is_wsl else "docker --version"
    success, output = run_command(docker_cmd)
    if check_item("Docker Engine", success, output if not success else ""):
        checks_passed.append("Docker")
        
        # Check Docker is running
        docker_ps_cmd = "wsl docker ps" if os_type == "Windows" and not is_wsl else "docker ps"
        success, _ = run_command(docker_ps_cmd)
        if check_item("Docker Running", success):
            checks_passed.append("Docker Running")
        else:
            checks_failed.append("Docker Running")
            print("   └─ Start Docker Desktop")
    else:
        checks_failed.append("Docker")
        print("   └─ Install Docker Desktop")
    
    # 3. Check kubectl
    print_header("3/8: kubectl")
    kubectl_cmd = "wsl kubectl version --client --short" if os_type == "Windows" and not is_wsl else "kubectl version --client --short"
    success, output = run_command(kubectl_cmd)
    if check_item("kubectl CLI", success, output if not success else ""):
        checks_passed.append("kubectl")
    else:
        checks_failed.append("kubectl")
        if os_type == "Windows":
            print("   └─ Install: choco install kubernetes-cli")
        elif os_type == "Darwin":
            print("   └─ Install: brew install kubectl")
        else:
            print("   └─ Install: sudo apt-get install kubectl")
    
    # 4. Check Kubernetes Cluster
    print_header("4/8: Kubernetes Cluster")
    
    # Check kubeconfig exists
    if is_wsl:
        home = os.path.expanduser("~")
        kubeconfig = os.path.join(home, ".kube", "config")
        if not os.path.exists(kubeconfig):
            print("⚠️  Kubeconfig not found in WSL")
            print("   └─ Syncing from Windows...")
            windows_user = os.environ.get("USER", "User")
            win_kubeconfig = f"/mnt/c/Users/{windows_user}/.kube/config"
            if os.path.exists(win_kubeconfig):
                os.makedirs(os.path.dirname(kubeconfig), exist_ok=True)
                shutil.copy(win_kubeconfig, kubeconfig)
                os.chmod(kubeconfig, 0o600)
                print("   └─ ✅ Kubeconfig synced")
    
    cluster_cmd = "wsl kubectl cluster-info" if os_type == "Windows" and not is_wsl else "kubectl cluster-info"
    success, output = run_command(cluster_cmd)
    if check_item("Kubernetes Cluster", success):
        checks_passed.append("K8s Cluster")
        
        # Check nodes
        nodes_cmd = "wsl kubectl get nodes" if os_type == "Windows" and not is_wsl else "kubectl get nodes"
        success, output = run_command(nodes_cmd)
        if check_item("Cluster Nodes Ready", success):
            checks_passed.append("K8s Nodes")
        else:
            checks_failed.append("K8s Nodes")
    else:
        checks_failed.append("K8s Cluster")
        print("   └─ Enable Kubernetes in Docker Desktop:")
        print("      Docker Desktop → Settings → Kubernetes → Enable")
    
    # 5. Check Helm
    print_header("5/8: Helm")
    helm_cmd = "wsl helm version --short" if os_type == "Windows" and not is_wsl else "helm version --short"
    success, output = run_command(helm_cmd)
    if check_item("Helm 3", success, output if not success else ""):
        checks_passed.append("Helm")
    else:
        checks_failed.append("Helm")
        print("   └─ Will be installed automatically")
    
    # 6. Check Available Resources
    print_header("6/8: System Resources")
    
    # Check Docker resources
    if os_type == "Windows" or is_wsl:
        docker_info_cmd = "wsl docker info --format '{{.MemTotal}}'" if os_type == "Windows" and not is_wsl else "docker info --format '{{.MemTotal}}'"
        success, output = run_command(docker_info_cmd)
        if success and output.strip():
            try:
                mem_bytes = int(output.strip())
                mem_gb = mem_bytes / (1024**3)
                if mem_gb >= 8:
                    check_item(f"Docker Memory: {mem_gb:.1f}GB", True)
                    checks_passed.append("Memory")
                else:
                    check_item(f"Docker Memory: {mem_gb:.1f}GB (Minimum 8GB recommended)", False)
                    checks_failed.append("Memory")
                    print("   └─ Increase in Docker Desktop → Settings → Resources")
            except:
                check_item("Docker Memory", False, "Cannot parse")
                checks_failed.append("Memory")
        else:
            check_item("Docker Memory", False, "Cannot check")
            checks_failed.append("Memory")
    else:
        check_item("System Memory", True, "Check manually")
        checks_passed.append("Memory")
    
    # 7. Check Disk Space
    print_header("7/8: Disk Space")
    if os_type == "Windows":
        disk_cmd = "wsl df -h / | tail -1" if not is_wsl else "df -h / | tail -1"
    else:
        disk_cmd = "df -h / | tail -1"
    
    success, output = run_command(disk_cmd)
    if success:
        check_item("Disk Space Available", True)
        checks_passed.append("Disk Space")
        print(f"   └─ {output.strip()}")
    else:
        check_item("Disk Space", False)
        checks_failed.append("Disk Space")
    
    # 8. Check Network
    print_header("8/8: Network Connectivity")
    
    # Check internet
    if os_type == "Windows" and not is_wsl:
        ping_cmd = "ping -n 1 8.8.8.8"
    else:
        ping_cmd = "ping -c 1 8.8.8.8"
    
    success, _ = run_command(ping_cmd)
    if check_item("Internet Connectivity", success):
        checks_passed.append("Network")
    else:
        checks_failed.append("Network")
    
    # Check Docker Hub access
    docker_pull_cmd = "wsl docker pull hello-world" if os_type == "Windows" and not is_wsl else "docker pull hello-world"
    success, _ = run_command(docker_pull_cmd)
    if check_item("Docker Hub Access", success):
        checks_passed.append("Docker Hub")
    else:
        checks_failed.append("Docker Hub")
        print("   └─ Check firewall/proxy settings")
    
    # Summary
    print_header("📋 Verification Summary")
    
    total = len(checks_passed) + len(checks_failed)
    
    print(f"✅ Passed: {len(checks_passed)}/{total}")
    for item in checks_passed:
        print(f"   • {item}")
    
    if checks_failed:
        print(f"\n❌ Failed: {len(checks_failed)}/{total}")
        for item in checks_failed:
            print(f"   • {item}")
        
        print(f"\n{'=' * 70}")
        print("⚠️  Some checks failed. Please fix the issues above.")
        print(f"{'=' * 70}\n")
        
        print("📖 Next Steps:")
        print("   1. Fix the failed checks")
        print("   2. Run this script again")
        print("   3. Once all checks pass, run: python setup/deploy_complete_stack.py\n")
        
        return 1
    else:
        print(f"\n{'=' * 70}")
        print("🎉 All checks passed! System is ready.")
        print(f"{'=' * 70}\n")
        
        print("📖 Next Steps:")
        print("   1. Deploy the platform:")
        print("      python setup/deploy_complete_stack.py")
        print()
        print("   2. Or deploy step by step:")
        print("      python setup/kubernetes/deploy_k8s.py")
        print("      python setup/helm/deploy_jupyterhub.py")
        print("      python setup/trino/deploy_trino.py")
        print("      python setup/grafana/deploy_grafana.py")
        print("      python setup/data/load_sample_data.py")
        print()
        
        return 0

if __name__ == "__main__":
    sys.exit(main())
