"""
DataMeesh Platform - JupyterHub Example Notebook
================================================

This script demonstrates how to:
1. Connect to Trino
2. Query federated data
3. Perform analysis
4. Create visualizations

Run this in JupyterHub: http://localhost:30080
"""

# ============================================================================
# 1. SETUP & IMPORTS
# ============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from trino.dbapi import connect

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 2. CONNECT TO TRINO
# ============================================================================

def get_trino_connection():
    """Create connection to Trino coordinator"""
    return connect(
        host='trino-coordinator.data-platform.svc.cluster.local',
        port=8080,
        user='admin',
        catalog='sales',
        schema='public'
    )

conn = get_trino_connection()
print("✅ Connected to Trino")

# ============================================================================
# 3. LOAD DATA
# ============================================================================

# Sales Data
query_sales = """
SELECT 
    c.customer_id,
    c.customer_name,
    c.country,
    c.industry,
    c.company_size,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as lifetime_value
FROM sales.public.customers c
LEFT JOIN sales.public.orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3, 4, 5
"""

df_sales = pd.read_sql(query_sales, conn)
print(f"✅ Loaded {len(df_sales)} customers")
print(df_sales.head())

# Marketing Data
query_marketing = """
SELECT 
    l.lead_id,
    l.lead_source,
    l.lead_stage,
    c.campaign_name,
    c.channel
FROM marketing.public.leads l
LEFT JOIN marketing.public.campaigns c ON l.campaign_id = c.campaign_id
"""

df_marketing = pd.read_sql(query_marketing, conn)
print(f"✅ Loaded {len(df_marketing)} leads")

# ============================================================================
# 4. DATA ANALYSIS
# ============================================================================

print("\n" + "="*60)
print("📊 DATA ANALYSIS")
print("="*60)

# Customer Value Distribution
print("\n1. Customer Lifetime Value Distribution:")
print(df_sales['lifetime_value'].describe())

# Revenue by Country
print("\n2. Revenue by Country:")
revenue_by_country = df_sales.groupby('country')['lifetime_value'].sum().sort_values(ascending=False)
print(revenue_by_country)

# Customer Segmentation
df_sales['segment'] = pd.cut(
    df_sales['lifetime_value'], 
    bins=[0, 10000, 50000, float('inf')],
    labels=['Low Value', 'Medium Value', 'High Value']
)

print("\n3. Customer Segments:")
print(df_sales['segment'].value_counts())

# Lead Source Performance
print("\n4. Lead Sources:")
print(df_marketing['lead_source'].value_counts())

# ============================================================================
# 5. CROSS-DOMAIN ANALYSIS
# ============================================================================

query_joined = """
SELECT 
    l.lead_source,
    COUNT(DISTINCT l.lead_id) as total_leads,
    COUNT(DISTINCT c.customer_id) as converted_customers,
    SUM(o.total_amount) as total_revenue
FROM marketing.public.leads l
LEFT JOIN sales.public.customers c ON LOWER(l.email) = LOWER(c.email)
LEFT JOIN sales.public.orders o ON c.customer_id = o.customer_id
GROUP BY 1
ORDER BY total_revenue DESC NULLS LAST
"""

df_attribution = pd.read_sql(query_joined, conn)

# Calculate conversion rate
df_attribution['conversion_rate'] = (
    df_attribution['converted_customers'] / df_attribution['total_leads'] * 100
).round(2)

print("\n" + "="*60)
print("🔗 CROSS-DOMAIN ANALYSIS: Lead Attribution")
print("="*60)
print(df_attribution)

# ============================================================================
# 6. VISUALIZATIONS
# ============================================================================

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('DataMeesh Platform - Analytics Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Revenue by Country
ax1 = axes[0, 0]
revenue_by_country.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title('Revenue by Country', fontsize=14, fontweight='bold')
ax1.set_xlabel('Country')
ax1.set_ylabel('Revenue ($)')
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Customer Segments
ax2 = axes[0, 1]
df_sales['segment'].value_counts().plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90)
ax2.set_title('Customer Segments', fontsize=14, fontweight='bold')
ax2.set_ylabel('')

# Plot 3: Lead Sources
ax3 = axes[1, 0]
df_marketing['lead_source'].value_counts().plot(kind='barh', ax=ax3, color='lightcoral')
ax3.set_title('Leads by Source', fontsize=14, fontweight='bold')
ax3.set_xlabel('Count')
ax3.set_ylabel('Lead Source')

# Plot 4: Lead Attribution - Conversion vs Revenue
ax4 = axes[1, 1]
scatter = ax4.scatter(
    df_attribution['conversion_rate'], 
    df_attribution['total_revenue'],
    s=df_attribution['total_leads'] * 10,
    alpha=0.6,
    c=range(len(df_attribution)),
    cmap='viridis'
)
for idx, row in df_attribution.iterrows():
    ax4.annotate(
        row['lead_source'], 
        (row['conversion_rate'], row['total_revenue']),
        fontsize=9
    )
ax4.set_title('Lead Source: Conversion Rate vs Revenue', fontsize=14, fontweight='bold')
ax4.set_xlabel('Conversion Rate (%)')
ax4.set_ylabel('Total Revenue ($)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('datamesh_dashboard.png', dpi=300, bbox_inches='tight')
print("\n✅ Dashboard saved as 'datamesh_dashboard.png'")
plt.show()

# ============================================================================
# 7. EXPORT RESULTS
# ============================================================================

# Export to CSV
df_sales.to_csv('sales_analysis.csv', index=False)
df_attribution.to_csv('lead_attribution.csv', index=False)
print("\n✅ Results exported to CSV files")

# ============================================================================
# 8. SUMMARY REPORT
# ============================================================================

print("\n" + "="*60)
print("📋 SUMMARY REPORT")
print("="*60)

print(f"""
Total Customers: {len(df_sales):,}
Total Revenue: ${df_sales['lifetime_value'].sum():,.2f}
Average Customer Value: ${df_sales['lifetime_value'].mean():,.2f}

Top 3 Countries by Revenue:
{revenue_by_country.head(3).to_string()}

Customer Segments:
{df_sales['segment'].value_counts().to_string()}

Lead Conversion Summary:
Total Leads: {df_attribution['total_leads'].sum():,}
Converted Customers: {df_attribution['converted_customers'].sum():,}
Overall Conversion Rate: {(df_attribution['converted_customers'].sum() / df_attribution['total_leads'].sum() * 100):.2f}%
""")

conn.close()
print("\n✅ Analysis complete!")

