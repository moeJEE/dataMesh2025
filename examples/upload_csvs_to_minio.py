#!/usr/bin/env python3
"""
Script pour uploader automatiquement les CSV de test vers MinIO
"""

import subprocess
import os
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

def create_buckets():
    """Crée les buckets nécessaires dans MinIO"""
    print("📦 Création des buckets MinIO...")
    
    buckets = ['raw-data', 'marketing-data', 'web-data', 'financial-data', 'test-data']
    
    for bucket in buckets:
        print(f"   Création du bucket: {bucket}")
        # Créer le bucket en utilisant kubectl exec
        cmd = f"kubectl exec -n data-platform deployment/minio -- mkdir -p /data/{bucket}"
        run_command(cmd, check=False)

def upload_csvs():
    """Upload les CSV vers MinIO"""
    print("\n📤 Upload des CSV vers MinIO...")
    
    csv_files = [
        ('sales_data.csv', 'raw-data'),
        ('customers_data.csv', 'raw-data'),
        ('marketing_campaigns.csv', 'marketing-data'),
        ('website_traffic.csv', 'web-data'),
        ('financial_data.csv', 'financial-data')
    ]
    
    for csv_file, bucket in csv_files:
        if os.path.exists(f"examples/{csv_file}"):
            print(f"   Upload de {csv_file} vers {bucket}...")
            cmd = f"kubectl cp examples/{csv_file} data-platform/minio-0:/data/{bucket}/{csv_file}"
            if run_command(cmd, check=False):
                print(f"   ✅ {csv_file} uploadé avec succès")
            else:
                print(f"   ⚠️  Échec de l'upload de {csv_file}")
        else:
            print(f"   ❌ Fichier {csv_file} non trouvé")

def verify_upload():
    """Vérifie que les fichiers ont été uploadés"""
    print("\n🔍 Vérification de l'upload...")
    
    cmd = "kubectl exec -n data-platform deployment/minio -- find /data -name '*.csv' -type f"
    run_command(cmd, check=False)

def main():
    """Fonction principale"""
    print("🚀 UPLOAD DES CSV VERS MINIO")
    print("=" * 50)
    
    # Vérifier que les CSV existent
    csv_files = ['sales_data.csv', 'customers_data.csv', 'marketing_campaigns.csv', 
                 'website_traffic.csv', 'financial_data.csv']
    
    missing_files = []
    for csv_file in csv_files:
        if not os.path.exists(f"examples/{csv_file}"):
            missing_files.append(csv_file)
    
    if missing_files:
        print("❌ Fichiers CSV manquants:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Exécutez d'abord: python examples/generate_test_csvs.py")
        return
    
    # Créer les buckets
    create_buckets()
    
    # Upload les CSV
    upload_csvs()
    
    # Vérifier l'upload
    verify_upload()
    
    print("\n✅ UPLOAD TERMINÉ!")
    print("=" * 50)
    print("🌐 Vérifiez dans MinIO Console:")
    print("   http://localhost:30901/browser/datalake")
    print("   Login: minioadmin / minioadmin")
    
    print("\n📋 BUCKETS CRÉÉS:")
    print("   📊 raw-data/ - Données de ventes et clients")
    print("   📢 marketing-data/ - Campagnes marketing")
    print("   🌐 web-data/ - Trafic web")
    print("   💰 financial-data/ - Données financières")
    
    print("\n🔍 REQUÊTES TRINO POUR TESTER:")
    print("   SELECT * FROM hive.raw_data.sales_data_csv LIMIT 5;")
    print("   SELECT * FROM hive.raw_data.customers_data_csv LIMIT 5;")
    print("   SELECT * FROM hive.marketing_data.marketing_campaigns_csv LIMIT 5;")

if __name__ == "__main__":
    main()
