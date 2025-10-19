#!/usr/bin/env python3
"""
DataMeesh - Sample Data Loader
Loads realistic sample data into Sales and Marketing databases
"""

import subprocess
import sys
import time

def run_command(cmd, check=True):
    """Run command"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        if result.stderr:
            print(f"   Error: {result.stderr}")
        return False
    return True

def print_header(text):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")

def execute_sql(namespace, pod_name, database, user, sql_commands):
    """Execute SQL commands in PostgreSQL pod"""
    print(f"📊 Executing SQL in {database}...")
    
    # Create temp SQL file
    sql_file = f"/tmp/datamesh_{database}.sql"
    with open(sql_file, "w") as f:
        f.write(sql_commands)
    
    # Copy SQL file to pod
    copy_cmd = f"kubectl cp {sql_file} {namespace}/{pod_name}:{sql_file}"
    if not run_command(copy_cmd):
        return False
    
    # Execute SQL
    exec_cmd = f"kubectl exec -n {namespace} {pod_name} -- psql -U {user} -d {database} -f {sql_file}"
    if not run_command(exec_cmd):
        return False
    
    print(f"✅ Data loaded into {database}")
    return True

def main():
    print_header("📦 DataMeesh - Sample Data Loader")
    
    # 1. Check prerequisites
    print_header("Step 1/3: Checking Prerequisites")
    
    if not run_command("kubectl cluster-info"):
        print("❌ Cannot connect to Kubernetes cluster")
        return 1
    
    # Check if databases are running
    print("🔍 Checking database pods...")
    
    result = subprocess.run(
        "kubectl get pods -n sales-domain -l app=sales-postgres --no-headers",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print("❌ Sales PostgreSQL not found. Deploy it first:")
        print("   python setup/kubernetes/deploy_k8s.py")
        return 1
    
    sales_pod = result.stdout.strip().split()[0]
    print(f"✅ Found Sales pod: {sales_pod}")
    
    result = subprocess.run(
        "kubectl get pods -n marketing-domain -l app=marketing-postgres --no-headers",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print("❌ Marketing PostgreSQL not found. Deploy it first:")
        print("   python setup/kubernetes/deploy_k8s.py")
        return 1
    
    marketing_pod = result.stdout.strip().split()[0]
    print(f"✅ Found Marketing pod: {marketing_pod}")
    
    # 2. Load Sales data
    print_header("Step 2/3: Loading Sales Domain Data")
    
    sales_sql = """
-- Sales Domain Sample Data

-- Customers
INSERT INTO customers (customer_name, email, phone, country, industry, company_size, created_at, updated_at) VALUES
('Acme Corporation', 'contact@acme.com', '+1-555-0101', 'USA', 'Technology', 'Enterprise', NOW(), NOW()),
('Global Tech Solutions', 'info@globaltech.com', '+44-20-7946-0958', 'UK', 'Technology', 'Large', NOW(), NOW()),
('Smart Systems GmbH', 'sales@smartsystems.de', '+49-30-12345678', 'Germany', 'Manufacturing', 'Medium', NOW(), NOW()),
('DataDrive Inc', 'hello@datadrive.com', '+1-555-0202', 'USA', 'Analytics', 'Medium', NOW(), NOW()),
('Digital Dynamics', 'contact@digitaldynamics.com.au', '+61-2-9876-5432', 'Australia', 'Technology', 'Large', NOW(), NOW()),
('Alpha Retailers', 'support@alpharetail.com', '+1-555-0303', 'USA', 'Retail', 'Large', NOW(), NOW()),
('Beta Logistics', 'info@betalogistics.co.uk', '+44-20-7946-0959', 'UK', 'Logistics', 'Medium', NOW(), NOW()),
('Gamma Healthcare', 'contact@gammahc.com', '+1-555-0404', 'USA', 'Healthcare', 'Enterprise', NOW(), NOW()),
('Delta Finance', 'hello@deltafinance.com', '+1-555-0505', 'USA', 'Finance', 'Large', NOW(), NOW()),
('Epsilon Energy', 'info@epsilonenergy.de', '+49-30-87654321', 'Germany', 'Energy', 'Enterprise', NOW(), NOW()),
('Future Finance', 'contact@futurefinance.com', '+1-555-0606', 'USA', 'Finance', 'Medium', NOW(), NOW()),
('Zeta Consulting', 'hello@zetaconsulting.com', '+1-555-0707', 'USA', 'Consulting', 'Small', NOW(), NOW()),
('Eta Education', 'info@etaedu.com', '+44-20-7946-0960', 'UK', 'Education', 'Medium', NOW(), NOW()),
('Theta Transport', 'contact@thetatransport.com', '+1-555-0808', 'USA', 'Logistics', 'Small', NOW(), NOW()),
('Iota Insurance', 'hello@iotainsurance.com', '+1-555-0909', 'USA', 'Insurance', 'Large', NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

-- Products
INSERT INTO products (product_name, category, price, stock_quantity, description, created_at) VALUES
('Enterprise Analytics Platform', 'Software', 49999.99, 100, 'Complete analytics solution', NOW()),
('Data Integration Suite', 'Software', 29999.99, 150, 'ETL and data integration tools', NOW()),
('Cloud Storage Pro', 'Service', 999.99, 1000, 'Unlimited cloud storage', NOW()),
('Business Intelligence Dashboard', 'Software', 19999.99, 200, 'Interactive BI dashboards', NOW()),
('Machine Learning Toolkit', 'Software', 39999.99, 75, 'ML model development platform', NOW()),
('API Management Gateway', 'Software', 24999.99, 100, 'Secure API management', NOW()),
('Real-time Monitoring System', 'Software', 34999.99, 80, 'System monitoring and alerts', NOW()),
('Data Visualization Pro', 'Software', 14999.99, 150, 'Advanced data visualization', NOW()),
('Security Compliance Suite', 'Software', 44999.99, 60, 'Complete security solution', NOW()),
('Customer Analytics Platform', 'Software', 54999.99, 50, '360-degree customer view', NOW())
ON CONFLICT (product_name) DO NOTHING;

-- Orders
INSERT INTO orders (customer_id, order_date, order_status, total_amount, payment_method, sales_rep, region, created_at)
SELECT 
    c.customer_id,
    NOW() - (random() * interval '90 days'),
    CASE WHEN random() < 0.8 THEN 'Completed' ELSE 'Pending' END,
    (random() * 80000 + 20000)::numeric(10,2),
    CASE WHEN random() < 0.5 THEN 'Credit Card' ELSE 'Wire Transfer' END,
    'Sales Rep ' || (floor(random() * 5) + 1)::text,
    CASE 
        WHEN c.country = 'USA' THEN 'North America'
        WHEN c.country IN ('UK', 'Germany') THEN 'Europe'
        ELSE 'APAC'
    END,
    NOW()
FROM customers c
ORDER BY random()
LIMIT 20
ON CONFLICT DO NOTHING;

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
SELECT 
    o.order_id,
    p.product_id,
    floor(random() * 3 + 1)::int,
    p.price,
    p.price * floor(random() * 3 + 1)::int
FROM orders o
CROSS JOIN LATERAL (
    SELECT product_id, price 
    FROM products 
    ORDER BY random() 
    LIMIT 2
) p
ON CONFLICT DO NOTHING;
"""
    
    if not execute_sql("sales-domain", sales_pod, "sales_db", "sales_user", sales_sql):
        print("❌ Failed to load Sales data")
        return 1
    
    # 3. Load Marketing data
    print_header("Step 3/3: Loading Marketing Domain Data")
    
    marketing_sql = """
-- Marketing Domain Sample Data

-- Campaigns
INSERT INTO campaigns (campaign_name, channel, budget, start_date, end_date, status, target_audience, created_at) VALUES
('Spring Product Launch', 'Email', 50000.00, NOW() - interval '60 days', NOW() + interval '30 days', 'Active', 'Enterprise', NOW()),
('Summer Social Media Blitz', 'Social Media', 75000.00, NOW() - interval '45 days', NOW() + interval '45 days', 'Active', 'SMB', NOW()),
('Q4 Enterprise Outreach', 'Webinar', 100000.00, NOW() - interval '30 days', NOW() + interval '60 days', 'Active', 'Enterprise', NOW()),
('Partner Network Drive', 'Partner', 60000.00, NOW() - interval '90 days', NOW() - interval '10 days', 'Completed', 'Partners', NOW()),
('Content Marketing Initiative', 'Content', 40000.00, NOW() - interval '75 days', NOW() + interval '15 days', 'Active', 'All', NOW()),
('Trade Show Season', 'Event', 150000.00, NOW() - interval '20 days', NOW() + interval '70 days', 'Active', 'Enterprise', NOW()),
('Email Nurture Campaign', 'Email', 30000.00, NOW() - interval '50 days', NOW() + interval '40 days', 'Active', 'Leads', NOW()),
('Retargeting Campaign', 'Display', 45000.00, NOW() - interval '15 days', NOW() + interval '75 days', 'Active', 'Website Visitors', NOW())
ON CONFLICT DO NOTHING;

-- Leads
INSERT INTO leads (first_name, last_name, email, phone, company, job_title, lead_source, lead_stage, campaign_id, created_at)
SELECT 
    'FirstName' || gs,
    'LastName' || gs,
    'lead' || gs || '@company' || (gs % 10) || '.com',
    '+1-555-' || lpad(gs::text, 4, '0'),
    'Company ' || (gs % 10),
    CASE (gs % 5)
        WHEN 0 THEN 'CEO'
        WHEN 1 THEN 'CTO'
        WHEN 2 THEN 'VP Engineering'
        WHEN 3 THEN 'Director of Analytics'
        ELSE 'Data Scientist'
    END,
    CASE (gs % 4)
        WHEN 0 THEN 'Website'
        WHEN 1 THEN 'Referral'
        WHEN 2 THEN 'Campaign'
        ELSE 'Partner'
    END,
    CASE (gs % 3)
        WHEN 0 THEN 'New'
        WHEN 1 THEN 'Qualified'
        ELSE 'Contacted'
    END,
    (SELECT campaign_id FROM campaigns ORDER BY random() LIMIT 1),
    NOW() - (random() * interval '90 days')
FROM generate_series(1, 15) gs
ON CONFLICT (email) DO NOTHING;

-- Campaign Metrics
INSERT INTO campaign_metrics (campaign_id, metric_date, impressions, clicks, conversions, cost, created_at)
SELECT 
    c.campaign_id,
    NOW() - (random() * interval '60 days'),
    floor(random() * 10000 + 5000)::int,
    floor(random() * 500 + 100)::int,
    floor(random() * 50 + 10)::int,
    (random() * 5000 + 1000)::numeric(10,2),
    NOW()
FROM campaigns c
ORDER BY random()
LIMIT 8
ON CONFLICT DO NOTHING;

-- Website Traffic
INSERT INTO website_traffic (traffic_date, page_url, page_views, unique_visitors, bounce_rate, avg_time_on_page, referral_source, created_at)
SELECT 
    NOW() - (random() * interval '90 days'),
    '/page' || (floor(random() * 10) + 1)::text,
    floor(random() * 1000 + 100)::int,
    floor(random() * 500 + 50)::int,
    (random() * 50 + 20)::numeric(5,2),
    floor(random() * 300 + 30)::int,
    CASE (floor(random() * 4)::int)
        WHEN 0 THEN 'Google'
        WHEN 1 THEN 'LinkedIn'
        WHEN 2 THEN 'Direct'
        ELSE 'Twitter'
    END,
    NOW()
FROM generate_series(1, 50) gs
ON CONFLICT DO NOTHING;
"""
    
    if not execute_sql("marketing-domain", marketing_pod, "marketing_db", "marketing_user", marketing_sql):
        print("❌ Failed to load Marketing data")
        return 1
    
    # Summary
    print_header("✅ Sample Data Loading Complete")
    
    print("📊 Data Loaded:")
    print("  Sales Domain:")
    print("    • 15 Customers")
    print("    • 10 Products")
    print("    • 20 Orders")
    print("    • 40+ Order Items")
    print()
    print("  Marketing Domain:")
    print("    • 8 Campaigns")
    print("    • 15 Leads")
    print("    • 8 Campaign Metrics")
    print("    • 50 Website Traffic Records")
    print()
    
    print("📖 Next Steps:")
    print("   1. Query data via Trino:")
    print("      python setup/trino/deploy_trino.py")
    print()
    print("   2. Analyze in JupyterHub:")
    print("      http://localhost:30080")
    print()
    print("   3. Create dashboards in Grafana:")
    print("      http://localhost:30030")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

