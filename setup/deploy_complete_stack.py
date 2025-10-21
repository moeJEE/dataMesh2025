#!/usr/bin/env python3
"""
DataMeesh - Complete Stack Deployment
Deploys the entire Data Mesh platform in one command
Cross-platform: Windows, WSL, macOS, Linux
"""

import subprocess
import sys
import os
import time

def run_script(script_path, description):
    """Run a Python script"""
    print(f"\n{'=' * 70}")
    print(f"  {description}")
    print(f"{'=' * 70}\n")
    
    result = subprocess.run([sys.executable, script_path], capture_output=False)
    
    if result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        return False
    
    print(f"\n✅ Completed: {description}")
    return True

def wait_for_jupyterhub():
    """Wait for JupyterHub to be ready"""
    print("\n⏳ Waiting for JupyterHub to be ready...")
    print("   This ensures DBT setup can find an active user pod.")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        result = subprocess.run(
            "kubectl get pods -n jupyterhub -l component=singleuser-server --no-headers",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("✅ JupyterHub user pod found!")
            return True
        
        print(f"   Attempt {attempt + 1}/{max_attempts} - waiting for user pod...")
        time.sleep(10)
    
    print("⚠️  No JupyterHub user pod found after 5 minutes")
    print("   DBT setup will prompt you to login to JupyterHub first")
    return False

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def main():
    print_header("🚀 DataMeesh - Complete Stack Deployment")
    
    print("""
This will deploy the entire Data Mesh platform:
  
  ✅ Core Kubernetes Resources (Sales + Marketing domains)
  ✅ Helm + JupyterHub (Multi-user notebooks)
  ✅ Trino Stack (Federated SQL queries)
  ✅ Grafana (Dashboards + visualization)
  ✅ Sample Data (Realistic test data)
  ✅ DBT Setup & Transformations (Data modeling)

⚠️  Note: DataHub NOT included (requires 10-12GB RAM)
    To deploy DataHub separately:
    python setup/datahub/deploy_datahub.py

Estimated time: 15-20 minutes
Required RAM: 8-10GB (or 10-12GB with DataHub)
    """)
    
    response = input("Continue with deployment? (yes/no): ").lower()
    if response != "yes":
        print("\n❌ Deployment cancelled.")
        return 0
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Start timer
    start_time = time.time()
    
    # Deployment steps
    steps = [
        (os.path.join(script_dir, "kubernetes", "deploy_k8s.py"), "1/7: Deploy Core Kubernetes Resources"),
        (os.path.join(script_dir, "helm", "install_helm.py"), "2/7: Install Helm"),
        (os.path.join(script_dir, "helm", "deploy_jupyterhub.py"), "3/7: Deploy JupyterHub"),
        (os.path.join(script_dir, "trino", "deploy_trino.py"), "4/7: Deploy Trino Stack"),
        (os.path.join(script_dir, "grafana", "deploy_grafana.py"), "5/7: Deploy Grafana"),
        (os.path.join(script_dir, "data", "load_sample_data.py"), "6/7: Load Sample Data"),
        (os.path.join(script_dir, "dbt", "setup_dbt_complete.py"), "7/7: Setup DBT & Run Transformations"),
    ]
    
    failed_steps = []
    
    for script_path, description in steps:
        if not os.path.exists(script_path):
            print(f"⚠️  Script not found: {script_path}")
            failed_steps.append(description)
            continue
        
        # Special handling for DBT setup - wait for JupyterHub
        if "setup_dbt_complete.py" in script_path:
            print("\n🔧 DBT Setup requires JupyterHub to be ready...")
            wait_for_jupyterhub()
        
        if not run_script(script_path, description):
            failed_steps.append(description)
            
            # Ask if user wants to continue
            print(f"\n⚠️  Step failed: {description}")
            response = input("Continue with remaining steps? (yes/no): ").lower()
            if response != "yes":
                print("\n❌ Deployment stopped.")
                break
    
    # End timer
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    # Final summary
    print_header("📊 Deployment Summary")
    
    if failed_steps:
        print("⚠️  Deployment completed with some failures:\n")
        for step in failed_steps:
            print(f"  ❌ {step}")
        print()
        print("✅ Successful steps:")
        for script_path, description in steps:
            if description not in failed_steps:
                print(f"  ✅ {description}")
    else:
        print("🎉 All components deployed successfully!")
    
    print(f"\n⏱️  Total time: {minutes}m {seconds}s")
    
    # Platform overview
    print_header("🌐 DataMeesh Platform - Access Points")
    
    print("""
┌─────────────────────────────────────────────────────────────┐
│                     YOUR DATA MESH PLATFORM                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📓 JupyterHub          http://localhost:30080              │
│     Login: admin / datamesh2024                             │
│     • Python notebooks                                      │
│     • Trino queries                                         │
│     • DBT transformations                                   │
│                                                             │
│  🔮 Trino Web UI        http://localhost:30808              │
│     • Query monitor                                         │
│     • Performance stats                                     │
│                                                             │
│  📦 Minio Console       http://localhost:30901              │
│     Login: minioadmin / minioadmin                          │
│     • S3 bucket management                                  │
│     • Data lake storage                                     │
│     • File upload/download                                  │
│                                                             │
│  📊 Grafana             http://localhost:30030              │
│     Login: admin / datamesh2024                             │
│     • Business dashboards                                   │
│     • Real-time metrics                                     │
│                                                             │
│  📚 DBT Docs            http://localhost:30082              │
│     • Data lineage                                          │
│     • Model documentation                                   │
│     • Ready-to-use transformations                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    """)
    
    print_header("📚 Quick Start Guide")
    
    print("""
1. Open JupyterHub (http://localhost:30080)
   - Username: admin
   - Password: datamesh2024

2. Start a new Python notebook

3. Query raw data with Trino:
   
   from trino.dbapi import connect
   
   conn = connect(
       host='trino-coordinator.data-platform.svc.cluster.local',
       port=8080,
       user='admin'
   )
   
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM sales.public.customers LIMIT 10")
   print(cursor.fetchall())

4. Query transformed data (DBT models):
   
   cursor.execute("SELECT * FROM hive.analytics_analytics.customer_campaign_analysis")
   print(cursor.fetchall())

5. Use pandas for analysis:
   
   import pandas as pd
   query = "SELECT * FROM hive.analytics_analytics.sales_customers"
   df = pd.read_sql(query, conn)
   df.head()

6. Upload files to MinIO Data Lake:
   - Open http://localhost:30901
   - Login: minioadmin / minioadmin
   - Create buckets and upload CSV/Parquet files
   - Access via Trino: SELECT * FROM hive.raw.your_table

7. Create dashboards in Grafana:
   - Open http://localhost:30030
   - Add visualizations
   - Query from Sales, Marketing, or Trino datasources

8. View DBT documentation:
   - Open http://localhost:30082
   - Browse data models and lineage

9. Deploy DataHub (optional - requires 10-12GB RAM):
   python setup/datahub/deploy_datahub.py
    """)
    
    print_header("📖 Documentation")
    
    print("""
For detailed guides:
  • Complete Guide: docs/guides/COMPLETE_GUIDE.md
  • Architecture: docs/architecture/
  • Example Queries: examples/trino_queries.sql
  • Example Notebook: examples/jupyter_notebook_example.py
    """)
    
    print_header("🔧 Management Commands")
    
    print("""
Check deployment status:
  kubectl get pods --all-namespaces

View logs:
  kubectl logs -n <namespace> <pod-name>

Clean up everything:
  python setup/cleanup.py

Redeploy:
  python setup/deploy_complete_stack.py
    """)
    
    if failed_steps:
        print_header("⚠️  Action Required")
        print("Some components failed to deploy. Please:")
        print("  1. Check the error messages above")
        print("  2. Fix any issues")
        print("  3. Re-run: python setup/deploy_complete_stack.py")
        print()
        return 1
    else:
        print_header("✅ You're All Set!")
        print("Your Data Mesh platform is ready to use. Happy analyzing! 🚀\n")
        return 0

if __name__ == "__main__":
    sys.exit(main())
