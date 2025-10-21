#!/usr/bin/env python3
"""
Exemple complet de workflow Data Scientist
CSV → MinIO → Trino → Grafana
"""

import pandas as pd
from trino.dbapi import connect
import requests
import json

def step1_upload_csv_to_minio():
    """
    Étape 1: Uploader un CSV vers MinIO
    """
    print("📤 ÉTAPE 1: Upload CSV vers MinIO")
    print("=" * 50)
    
    # Créer des données d'exemple
    data = {
        'date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop'],
        'sales': [1200, 25, 75, 300, 1200],
        'region': ['North', 'South', 'East', 'West', 'North'],
        'customer_id': [1, 2, 3, 4, 5]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('sales_data.csv', index=False)
    
    print("✅ Fichier CSV créé: sales_data.csv")
    print("📋 Données:")
    print(df)
    print("\n💡 Maintenant:")
    print("   1. Allez sur http://localhost:30901/browser/datalake")
    print("   2. Login: minioadmin / minioadmin")
    print("   3. Créez un bucket 'raw-data'")
    print("   4. Uploadez sales_data.csv")
    print("   5. Notez le chemin: s3://raw-data/sales_data.csv")

def step2_query_with_trino():
    """
    Étape 2: Récupérer les données avec Trino
    """
    print("\n🔍 ÉTAPE 2: Récupérer les données avec Trino")
    print("=" * 50)
    
    try:
        # Connexion Trino
        conn = connect(
            host='trino-coordinator.data-platform.svc.cluster.local',
            port=8080,
            user='admin'
        )
        
        print("✅ Connexion Trino établie")
        
        # Requête pour lister les tables disponibles
        cursor = conn.cursor()
        cursor.execute("SHOW SCHEMAS FROM hive")
        schemas = cursor.fetchall()
        print(f"📁 Schémas disponibles: {[s[0] for s in schemas]}")
        
        # Requête pour lire le CSV (si uploadé)
        try:
            query = """
            SELECT * FROM hive.raw_data.sales_data_csv
            LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            print("📊 Données du CSV:")
            for row in results:
                print(f"   {row}")
                
        except Exception as e:
            print(f"⚠️  CSV pas encore uploadé: {e}")
            print("   Uploadez d'abord le CSV dans MinIO")
        
        # Requête sur les données existantes
        print("\n📊 Données existantes (Sales):")
        cursor.execute("SELECT * FROM sales.public.customers LIMIT 3")
        customers = cursor.fetchall()
        for row in customers:
            print(f"   {row}")
            
    except Exception as e:
        print(f"❌ Erreur Trino: {e}")

def step3_grafana_dashboard():
    """
    Étape 3: Configuration Grafana
    """
    print("\n📊 ÉTAPE 3: Configuration Grafana")
    print("=" * 50)
    
    print("🌐 Accès Grafana: http://localhost:30030")
    print("🔑 Login: admin / datamesh2024")
    
    print("\n📋 Configuration de la source de données:")
    print("   1. Aller dans Configuration → Data Sources")
    print("   2. Ajouter Trino")
    print("   3. URL: http://trino-coordinator.data-platform.svc.cluster.local:8080")
    print("   4. User: admin")
    print("   5. Test & Save")
    
    print("\n📊 Requêtes pour dashboard:")
    print("   -- Ventes par région:")
    print("   SELECT region, SUM(sales) as total_sales")
    print("   FROM hive.raw_data.sales_data_csv")
    print("   GROUP BY region")
    print("   ORDER BY total_sales DESC")
    
    print("\n   -- Ventes par produit:")
    print("   SELECT product, COUNT(*) as count, AVG(sales) as avg_sales")
    print("   FROM hive.raw_data.sales_data_csv")
    print("   GROUP BY product")
    print("   ORDER BY count DESC")

def main():
    """
    Workflow complet Data Scientist
    """
    print("🚀 WORKFLOW DATA SCIENTIST COMPLET")
    print("=" * 60)
    
    # Étape 1: Créer et uploader CSV
    step1_upload_csv_to_minio()
    
    # Étape 2: Requêtes Trino
    step2_query_with_trino()
    
    # Étape 3: Configuration Grafana
    step3_grafana_dashboard()
    
    print("\n🎉 WORKFLOW TERMINÉ!")
    print("=" * 60)
    print("📋 Récapitulatif:")
    print("   ✅ CSV créé et prêt pour upload")
    print("   ✅ Connexion Trino testée")
    print("   ✅ Instructions Grafana fournies")
    print("\n🌐 Accès aux services:")
    print("   📦 MinIO: http://localhost:30901")
    print("   🔮 Trino UI: http://localhost:30808")
    print("   📊 Grafana: http://localhost:30030")
    print("   📓 JupyterHub: http://localhost:30080")

if __name__ == "__main__":
    main()
