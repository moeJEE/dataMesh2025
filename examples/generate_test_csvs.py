#!/usr/bin/env python3
"""
Générateur de CSV de test pour le Data Mesh
Génère différents types de données pour tester le workflow complet
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sales_data():
    """Génère des données de ventes réalistes"""
    print("📊 Génération des données de ventes...")
    
    # Paramètres
    n_records = 1000
    start_date = datetime(2024, 1, 1)
    
    # Données de base
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'Tablet', 'Phone']
    regions = ['North', 'South', 'East', 'West', 'Central']
    sales_reps = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown']
    categories = ['Electronics', 'Accessories', 'Computing', 'Mobile']
    
    # Génération des données
    data = []
    for i in range(n_records):
        product = random.choice(products)
        region = random.choice(regions)
        sales_rep = random.choice(sales_reps)
        category = random.choice(categories)
        
        # Prix basé sur le produit
        base_prices = {
            'Laptop': (800, 2000), 'Mouse': (10, 50), 'Keyboard': (20, 100),
            'Monitor': (150, 500), 'Headphones': (30, 200), 'Webcam': (40, 150),
            'Tablet': (200, 800), 'Phone': (300, 1200)
        }
        min_price, max_price = base_prices[product]
        unit_price = round(random.uniform(min_price, max_price), 2)
        
        # Quantité et remise
        quantity = random.randint(1, 5)
        discount = round(random.uniform(0, 0.2), 2)  # 0-20% de remise
        total_amount = round(unit_price * quantity * (1 - discount), 2)
        
        # Date aléatoire
        random_days = random.randint(0, 365)
        order_date = start_date + timedelta(days=random_days)
        
        # Statut basé sur la date
        if order_date > datetime.now() - timedelta(days=30):
            status = random.choice(['Pending', 'Processing', 'Shipped'])
        else:
            status = random.choice(['Completed', 'Cancelled'])
        
        data.append({
            'order_id': f'ORD-{i+1:06d}',
            'customer_id': random.randint(1, 200),
            'product_name': product,
            'category': category,
            'region': region,
            'sales_rep': sales_rep,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'unit_price': unit_price,
            'quantity': quantity,
            'discount': discount,
            'total_amount': total_amount,
            'status': status,
            'payment_method': random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash'])
        })
    
    df = pd.DataFrame(data)
    df.to_csv('examples/sales_data.csv', index=False)
    print(f"✅ sales_data.csv généré: {len(df)} enregistrements")
    return df

def generate_customer_data():
    """Génère des données clients"""
    print("👥 Génération des données clients...")
    
    # Noms et prénoms
    first_names = ['Alice', 'Bob', 'Carol', 'David', 'Eva', 'Frank', 'Grace', 'Henry', 
                   'Ivy', 'Jack', 'Kate', 'Liam', 'Mia', 'Noah', 'Olivia', 'Paul',
                   'Quinn', 'Rachel', 'Sam', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xavier', 'Yara', 'Zoe']
    
    last_names = ['Johnson', 'Smith', 'Davis', 'Wilson', 'Brown', 'Jones', 'Garcia', 'Miller',
                  'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin',
                  'Jackson', 'Thompson', 'White', 'Lopez', 'Lee', 'Gonzalez', 'Harris', 'Clark']
    
    companies = ['TechCorp', 'DataSoft', 'CloudSys', 'InfoTech', 'Digital Solutions', 'ByteWorks',
                 'CodeCraft', 'DataFlow', 'TechNova', 'CloudBase', 'InfoStream', 'DataCore']
    
    industries = ['Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing', 'Retail',
                  'Consulting', 'Media', 'Government', 'Non-profit']
    
    countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands',
                 'Australia', 'Japan', 'Brazil', 'Mexico', 'India', 'China', 'South Korea']
    
    data = []
    for i in range(200):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        company = random.choice(companies)
        industry = random.choice(industries)
        country = random.choice(countries)
        
        # Email basé sur le nom
        email = f"{first_name.lower()}.{last_name.lower()}@{company.lower().replace(' ', '')}.com"
        
        # Téléphone
        phone = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        # Taille d'entreprise
        company_size = random.choice(['Small (1-50)', 'Medium (51-200)', 'Large (201-1000)', 'Enterprise (1000+)'])
        
        # Date de création
        created_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        
        data.append({
            'customer_id': i + 1,
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}",
            'email': email,
            'phone': phone,
            'company': company,
            'industry': industry,
            'country': country,
            'company_size': company_size,
            'created_date': created_date.strftime('%Y-%m-%d'),
            'is_active': random.choice([True, True, True, False])  # 75% actifs
        })
    
    df = pd.DataFrame(data)
    df.to_csv('examples/customers_data.csv', index=False)
    print(f"✅ customers_data.csv généré: {len(df)} enregistrements")
    return df

def generate_marketing_campaigns():
    """Génère des données de campagnes marketing"""
    print("📢 Génération des données de campagnes marketing...")
    
    campaign_names = [
        'Spring Product Launch', 'Summer Social Media Blitz', 'Q4 Enterprise Outreach',
        'Black Friday Sale', 'Cyber Monday Special', 'Holiday Shopping Spree',
        'New Year Promotion', 'Valentine\'s Day Offer', 'Back to School Campaign',
        'Tech Innovation Showcase', 'Customer Retention Program', 'Brand Awareness Drive'
    ]
    
    channels = ['Email', 'Social Media', 'Webinar', 'Google Ads', 'Facebook Ads', 'LinkedIn', 'Direct Mail']
    statuses = ['Active', 'Completed', 'Paused', 'Draft']
    
    data = []
    for i in range(50):
        campaign_name = random.choice(campaign_names)
        channel = random.choice(channels)
        status = random.choice(statuses)
        
        # Budget basé sur le canal
        budget_ranges = {
            'Email': (1000, 5000), 'Social Media': (2000, 8000), 'Webinar': (500, 2000),
            'Google Ads': (3000, 15000), 'Facebook Ads': (2000, 10000), 'LinkedIn': (1000, 5000),
            'Direct Mail': (500, 3000)
        }
        min_budget, max_budget = budget_ranges[channel]
        budget = round(random.uniform(min_budget, max_budget), 2)
        
        # Dates
        start_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 200))
        duration_days = random.randint(7, 90)
        end_date = start_date + timedelta(days=duration_days)
        
        # Métriques (si la campagne est terminée)
        if status == 'Completed':
            impressions = random.randint(10000, 100000)
            clicks = random.randint(100, 5000)
            conversions = random.randint(10, 500)
            ctr = round(clicks / impressions * 100, 2)
            conversion_rate = round(conversions / clicks * 100, 2)
            cost_per_click = round(budget / clicks, 2)
        else:
            impressions = random.randint(1000, 50000)
            clicks = random.randint(50, 2500)
            conversions = random.randint(5, 250)
            ctr = round(clicks / impressions * 100, 2)
            conversion_rate = round(conversions / clicks * 100, 2)
            cost_per_click = round(budget / clicks, 2)
        
        data.append({
            'campaign_id': f'CAMP-{i+1:03d}',
            'campaign_name': campaign_name,
            'channel': channel,
            'status': status,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'budget': budget,
            'impressions': impressions,
            'clicks': clicks,
            'conversions': conversions,
            'ctr': ctr,
            'conversion_rate': conversion_rate,
            'cost_per_click': cost_per_click,
            'roi': round(random.uniform(1.5, 4.0), 2)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('examples/marketing_campaigns.csv', index=False)
    print(f"✅ marketing_campaigns.csv généré: {len(df)} enregistrements")
    return df

def generate_website_traffic():
    """Génère des données de trafic web"""
    print("🌐 Génération des données de trafic web...")
    
    pages = ['/home', '/products', '/about', '/contact', '/blog', '/pricing', '/features', '/support']
    sources = ['Google', 'Facebook', 'LinkedIn', 'Twitter', 'Direct', 'Email', 'Referral']
    devices = ['Desktop', 'Mobile', 'Tablet']
    countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands']
    
    data = []
    for i in range(5000):
        page = random.choice(pages)
        source = random.choice(sources)
        device = random.choice(devices)
        country = random.choice(countries)
        
        # Date et heure
        date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        timestamp = date.replace(hour=hour, minute=minute)
        
        # Durée de session basée sur la page
        session_durations = {
            '/home': (30, 300), '/products': (60, 600), '/about': (30, 180),
            '/contact': (45, 300), '/blog': (120, 900), '/pricing': (90, 600),
            '/features': (60, 480), '/support': (180, 1200)
        }
        min_duration, max_duration = session_durations[page]
        session_duration = random.randint(min_duration, max_duration)
        
        # Bounce rate basé sur la source
        bounce_rates = {
            'Google': 0.4, 'Facebook': 0.3, 'LinkedIn': 0.2, 'Twitter': 0.35,
            'Direct': 0.25, 'Email': 0.15, 'Referral': 0.3
        }
        is_bounce = random.random() < bounce_rates[source]
        
        data.append({
            'session_id': f'SESS-{i+1:06d}',
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'page': page,
            'source': source,
            'device': device,
            'country': country,
            'session_duration': session_duration,
            'is_bounce': is_bounce,
            'page_views': random.randint(1, 10) if not is_bounce else 1
        })
    
    df = pd.DataFrame(data)
    df.to_csv('examples/website_traffic.csv', index=False)
    print(f"✅ website_traffic.csv généré: {len(df)} enregistrements")
    return df

def generate_financial_data():
    """Génère des données financières"""
    print("💰 Génération des données financières...")
    
    accounts = ['Sales Revenue', 'Marketing Expenses', 'R&D Costs', 'Administrative', 'Operations']
    categories = ['Revenue', 'Expense', 'Asset', 'Liability', 'Equity']
    
    data = []
    for i in range(365):  # Une année de données
        date = datetime(2024, 1, 1) + timedelta(days=i)
        
        for account in accounts:
            # Montant basé sur le type de compte
            if 'Revenue' in account:
                amount = round(random.uniform(50000, 200000), 2)
            elif 'Expense' in account or 'Cost' in account:
                amount = round(random.uniform(10000, 80000), 2)
            else:
                amount = round(random.uniform(1000, 50000), 2)
            
            # Variation saisonnière
            if date.month in [11, 12]:  # Q4 - plus d'activité
                amount *= 1.3
            elif date.month in [6, 7, 8]:  # Été - moins d'activité
                amount *= 0.8
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'account': account,
                'category': random.choice(categories),
                'amount': amount,
                'currency': 'USD',
                'department': random.choice(['Sales', 'Marketing', 'R&D', 'Admin', 'Operations'])
            })
    
    df = pd.DataFrame(data)
    df.to_csv('examples/financial_data.csv', index=False)
    print(f"✅ financial_data.csv généré: {len(df)} enregistrements")
    return df

def main():
    """Génère tous les CSV de test"""
    print("🚀 GÉNÉRATION DES CSV DE TEST POUR DATA MESH")
    print("=" * 60)
    
    # Créer le dossier examples s'il n'existe pas
    os.makedirs('examples', exist_ok=True)
    
    # Générer tous les datasets
    sales_df = generate_sales_data()
    customers_df = generate_customer_data()
    campaigns_df = generate_marketing_campaigns()
    traffic_df = generate_website_traffic()
    financial_df = generate_financial_data()
    
    print("\n🎉 GÉNÉRATION TERMINÉE!")
    print("=" * 60)
    print("📁 Fichiers générés dans le dossier 'examples/':")
    print("   📊 sales_data.csv - Données de ventes (1000 enregistrements)")
    print("   👥 customers_data.csv - Données clients (200 enregistrements)")
    print("   📢 marketing_campaigns.csv - Campagnes marketing (50 enregistrements)")
    print("   🌐 website_traffic.csv - Trafic web (5000 enregistrements)")
    print("   💰 financial_data.csv - Données financières (1825 enregistrements)")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Uploadez ces CSV dans MinIO (http://localhost:30901)")
    print("   2. Créez des buckets: raw-data, marketing-data, web-data, financial-data")
    print("   3. Testez les requêtes Trino dans JupyterHub")
    print("   4. Créez des dashboards Grafana")
    
    print("\n🌐 ACCÈS AUX SERVICES:")
    print("   📦 MinIO: http://localhost:30901 (minioadmin/minioadmin)")
    print("   📓 JupyterHub: http://localhost:30080 (admin/datamesh2024)")
    print("   🔮 Trino UI: http://localhost:30808")
    print("   📊 Grafana: http://localhost:30030 (admin/datamesh2024)")

if __name__ == "__main__":
    main()
