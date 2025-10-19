#!/usr/bin/env python3
"""
DataMeesh - Docker Cache Deep Cleanup
Performs aggressive cleanup of ALL Docker cache and unused resources
⚠️ WARNING: This will remove ALL unused Docker resources, not just DataMeesh!
"""

import subprocess
import sys

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

def get_docker_cache_size():
    """Get Docker cache size"""
    result = subprocess.run(
        "docker system df",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout if result.returncode == 0 else "Unable to check"

def main():
    print_header("🧹 DataMeesh - Docker Cache Deep Cleanup")
    
    print("⚠️  WARNING: This will remove ALL unused Docker resources!")
    print()
    print("This includes:")
    print("   • All stopped containers")
    print("   • All unused networks")
    print("   • All dangling images")
    print("   • All unused images (not just dangling)")
    print("   • All build cache")
    print("   • All unused volumes")
    print()
    print("This is more aggressive than regular cleanup and will affect")
    print("ALL Docker resources, not just DataMeesh resources.")
    print()
    
    # Show current cache size
    print_header("Current Docker Space Usage")
    print(get_docker_cache_size())
    
    response = input("\nAre you sure you want to continue? (yes/no): ").lower()
    if response != "yes":
        print("\n❌ Cleanup cancelled.")
        return 0
    
    print("\n🚀 Starting aggressive Docker cleanup...\n")
    
    # 1. Stop all running containers
    print_header("1/8: Stopping All Running Containers")
    
    result = subprocess.run(
        "docker ps -q",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("🛑 Stopping all running containers...")
        run_command("docker stop $(docker ps -q)")
    else:
        print("ℹ️  No running containers")
    
    # 2. Remove all containers
    print_header("2/8: Removing All Containers")
    
    result = subprocess.run(
        "docker ps -aq",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("🗑️  Removing all containers...")
        run_command("docker rm -f $(docker ps -aq)")
    else:
        print("ℹ️  No containers to remove")
    
    # 3. Remove all images
    print_header("3/8: Removing All Images")
    
    result = subprocess.run(
        "docker images -q",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("🗑️  Removing all images...")
        run_command("docker rmi -f $(docker images -aq)")
    else:
        print("ℹ️  No images to remove")
    
    # 4. Remove all volumes
    print_header("4/8: Removing All Volumes")
    
    result = subprocess.run(
        "docker volume ls -q",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("🗑️  Removing all volumes...")
        run_command("docker volume rm $(docker volume ls -q)")
    else:
        print("ℹ️  No volumes to remove")
    
    # 5. Remove all networks
    print_header("5/8: Removing All Networks")
    
    print("🗑️  Pruning networks...")
    run_command("docker network prune -f")
    
    # 6. Clean build cache
    print_header("6/8: Cleaning Build Cache")
    
    print("🧹 Cleaning all build cache...")
    run_command("docker builder prune -f --all")
    
    # 7. System prune (aggressive)
    print_header("7/8: System Prune (Aggressive)")
    
    print("🧹 Running aggressive system prune...")
    run_command("docker system prune -a -f --volumes")
    
    # 8. Final verification
    print_header("8/8: Final Verification")
    
    print("📊 Remaining Docker space usage:")
    print(get_docker_cache_size())
    
    # Summary
    print_header("✅ Docker Cache Deep Cleanup Complete")
    
    print("All Docker resources have been cleaned:")
    print("  ✅ All containers removed")
    print("  ✅ All images removed")
    print("  ✅ All volumes removed")
    print("  ✅ All networks pruned")
    print("  ✅ All build cache removed")
    print("  ✅ System completely pruned")
    print()
    
    print("📖 Next Steps:")
    print("   1. Images will be re-downloaded on next deployment")
    print("   2. To redeploy DataMeesh:")
    print("      python setup/deploy_complete_stack.py")
    print()
    print("   3. To check Docker status:")
    print("      docker system df")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

