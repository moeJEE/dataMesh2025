#!/usr/bin/env python3
"""
Script pour configurer les schémas Hive et créer les tables pour les CSV
"""

import subprocess
import time

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

def create_hive_schemas():
    """Crée les schémas Hive nécessaires"""
    print("📁 Création des schémas Hive...")
    
    schemas = ['raw_data', 'marketing_data', 'web_data', 'financial_data']
    
    for schema in schemas:
        print(f"   Création du schéma: {schema}")
        cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"CREATE SCHEMA IF NOT EXISTS hive.{schema}\""
        run_command(cmd, check=False)

def create_hive_tables():
    """Crée les tables Hive pour les CSV"""
    print("\n📊 Création des tables Hive...")
    
    # Table sales_data
    print("   Création de la table sales_data...")
    sales_table = """
    CREATE TABLE IF NOT EXISTS hive.raw_data.sales_data_csv (
        order_id VARCHAR,
        customer_id BIGINT,
        product_name VARCHAR,
        category VARCHAR,
        region VARCHAR,
        sales_rep VARCHAR,
        order_date VARCHAR,
        unit_price DOUBLE,
        quantity BIGINT,
        discount DOUBLE,
        total_amount DOUBLE,
        status VARCHAR,
        payment_method VARCHAR
    )
    WITH (
        external_location = 's3a://raw-data/sales_data.csv',
        format = 'CSV',
        skip_header_line_count = 1
    )
    """
    
    cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"{sales_table}\""
    run_command(cmd, check=False)
    
    # Table customers_data
    print("   Création de la table customers_data...")
    customers_table = """
    CREATE TABLE IF NOT EXISTS hive.raw_data.customers_data_csv (
        customer_id BIGINT,
        first_name VARCHAR,
        last_name VARCHAR,
        full_name VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        company VARCHAR,
        industry VARCHAR,
        country VARCHAR,
        company_size VARCHAR,
        created_date VARCHAR,
        is_active BOOLEAN
    )
    WITH (
        external_location = 's3a://raw-data/customers_data.csv',
        format = 'CSV',
        skip_header_line_count = 1
    )
    """
    
    cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"{customers_table}\""
    run_command(cmd, check=False)
    
    # Table marketing_campaigns
    print("   Création de la table marketing_campaigns...")
    marketing_table = """
    CREATE TABLE IF NOT EXISTS hive.marketing_data.marketing_campaigns_csv (
        campaign_id VARCHAR,
        campaign_name VARCHAR,
        channel VARCHAR,
        status VARCHAR,
        start_date VARCHAR,
        end_date VARCHAR,
        budget DOUBLE,
        impressions BIGINT,
        clicks BIGINT,
        conversions BIGINT,
        ctr DOUBLE,
        conversion_rate DOUBLE,
        cost_per_click DOUBLE,
        roi DOUBLE
    )
    WITH (
        external_location = 's3a://marketing-data/marketing_campaigns.csv',
        format = 'CSV',
        skip_header_line_count = 1
    )
    """
    
    cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"{marketing_table}\""
    run_command(cmd, check=False)
    
    # Table website_traffic
    print("   Création de la table website_traffic...")
    traffic_table = """
    CREATE TABLE IF NOT EXISTS hive.web_data.website_traffic_csv (
        session_id VARCHAR,
        timestamp VARCHAR,
        page VARCHAR,
        source VARCHAR,
        device VARCHAR,
        country VARCHAR,
        session_duration BIGINT,
        is_bounce BOOLEAN,
        page_views BIGINT
    )
    WITH (
        external_location = 's3a://web-data/website_traffic.csv',
        format = 'CSV',
        skip_header_line_count = 1
    )
    """
    
    cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"{traffic_table}\""
    run_command(cmd, check=False)
    
    # Table financial_data
    print("   Création de la table financial_data...")
    financial_table = """
    CREATE TABLE IF NOT EXISTS hive.financial_data.financial_data_csv (
        date VARCHAR,
        account VARCHAR,
        category VARCHAR,
        amount DOUBLE,
        currency VARCHAR,
        department VARCHAR
    )
    WITH (
        external_location = 's3a://financial-data/financial_data.csv',
        format = 'CSV',
        skip_header_line_count = 1
    )
    """
    
    cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"{financial_table}\""
    run_command(cmd, check=False)

def test_tables():
    """Teste l'accès aux tables créées"""
    print("\n🧪 Test des tables créées...")
    
    test_queries = [
        ("Vérification des schémas", "SHOW SCHEMAS FROM hive"),
        ("Tables dans raw_data", "SHOW TABLES FROM hive.raw_data"),
        ("Tables dans marketing_data", "SHOW TABLES FROM hive.marketing_data"),
        ("Test sales_data", "SELECT COUNT(*) FROM hive.raw_data.sales_data_csv"),
        ("Test customers_data", "SELECT COUNT(*) FROM hive.raw_data.customers_data_csv")
    ]
    
    for description, query in test_queries:
        print(f"\n   {description}:")
        cmd = f"kubectl exec -n data-platform deployment/trino-coordinator -- trino --execute \"{query}\""
        run_command(cmd, check=False)

def main():
    """Fonction principale"""
    print("🚀 CONFIGURATION DES SCHÉMAS HIVE")
    print("=" * 50)
    
    # Créer les schémas
    create_hive_schemas()
    
    # Attendre un peu
    print("\n⏳ Attente de la propagation des schémas...")
    time.sleep(5)
    
    # Créer les tables
    create_hive_tables()
    
    # Attendre un peu
    print("\n⏳ Attente de la création des tables...")
    time.sleep(10)
    
    # Tester les tables
    test_tables()
    
    print("\n✅ CONFIGURATION TERMINÉE!")
    print("=" * 50)
    print("🌐 Vous pouvez maintenant utiliser les requêtes Trino:")
    print("   SELECT * FROM hive.raw_data.sales_data_csv LIMIT 5;")
    print("   SELECT * FROM hive.raw_data.customers_data_csv LIMIT 5;")
    print("   SELECT * FROM hive.marketing_data.marketing_campaigns_csv LIMIT 5;")
    
    print("\n📋 Schémas créés:")
    print("   📊 hive.raw_data - Données de ventes et clients")
    print("   📢 hive.marketing_data - Campagnes marketing")
    print("   🌐 hive.web_data - Trafic web")
    print("   💰 hive.financial_data - Données financières")

if __name__ == "__main__":
    main()
