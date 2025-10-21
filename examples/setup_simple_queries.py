#!/usr/bin/env python3
"""
Script pour configurer des requêtes simples avec les données existantes
"""

import subprocess

def run_command(cmd, check=True):
    """Exécute une commande et retourne le résultat"""
    print(f"🔨 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Erreur: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    return True

def test_existing_data():
    """Teste les données existantes dans PostgreSQL"""
    print("🧪 Test des données existantes...")
    
    # Test des données Sales
    print("\n📊 Données Sales (PostgreSQL):")
    cmd = "kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"SELECT * FROM sales.public.customers LIMIT 3\""
    run_command(cmd, check=False)
    
    # Test des données Marketing
    print("\n📢 Données Marketing (PostgreSQL):")
    cmd = "kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"SELECT * FROM marketing.public.campaigns LIMIT 3\""
    run_command(cmd, check=False)
    
    # Test des données DBT transformées
    print("\n🔄 Données DBT transformées:")
    cmd = "kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"SELECT * FROM hive.analytics_analytics_analytics.sales_customers LIMIT 3\""
    run_command(cmd, check=False)

def create_sample_queries():
    """Crée des exemples de requêtes pour JupyterHub"""
    print("\n📋 Exemples de requêtes pour JupyterHub:")
    
    queries = {
        "Données Sales brutes": """
SELECT 
    c.customer_name,
    c.email,
    c.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue
FROM sales.public.customers c
LEFT JOIN sales.public.orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email, c.country
ORDER BY total_revenue DESC
LIMIT 10
""",
        
        "Données Marketing brutes": """
SELECT 
    campaign_name,
    channel,
    status,
    budget,
    start_date,
    end_date
FROM marketing.public.campaigns
WHERE status = 'Active'
ORDER BY budget DESC
""",
        
        "Données DBT transformées": """
SELECT 
    customer_name,
    country,
    industry,
    company_size
FROM hive.analytics_analytics_analytics.sales_customers
WHERE country = 'USA'
ORDER BY customer_name
LIMIT 10
""",
        
        "Analyse des ventes": """
SELECT 
    c.country,
    c.industry,
    COUNT(o.order_id) as orders,
    SUM(o.total_amount) as revenue,
    AVG(o.total_amount) as avg_order_value
FROM sales.public.customers c
LEFT JOIN sales.public.orders o ON c.customer_id = o.customer_id
GROUP BY c.country, c.industry
HAVING COUNT(o.order_id) > 0
ORDER BY revenue DESC
"""
    }
    
    for title, query in queries.items():
        print(f"\n🔍 {title}:")
        print("```sql")
        print(query.strip())
        print("```")

def main():
    """Fonction principale"""
    print("🚀 CONFIGURATION DES REQUÊTES SIMPLES")
    print("=" * 50)
    
    # Tester les données existantes
    test_existing_data()
    
    # Créer des exemples de requêtes
    create_sample_queries()
    
    print("\n✅ CONFIGURATION TERMINÉE!")
    print("=" * 50)
    print("🌐 Utilisez ces requêtes dans JupyterHub:")
    print("   from trino.dbapi import connect")
    print("   import pandas as pd")
    print("   ")
    print("   conn = connect(")
    print("       host='trino-coordinator.data-platform.svc.cluster.local',")
    print("       port=8080,")
    print("       user='admin'")
    print("   )")
    print("   ")
    print("   df = pd.read_sql(query, conn)")
    print("   print(df)")
    
    print("\n📊 Données disponibles:")
    print("   ✅ sales.public.customers - Clients")
    print("   ✅ sales.public.orders - Commandes")
    print("   ✅ marketing.public.campaigns - Campagnes")
    print("   ✅ hive.analytics_analytics_analytics.* - Données DBT")

if __name__ == "__main__":
    main()
