# DataMeesh - Sample Data Model & Analytics Guide

## 📊 Overview

This Data Mesh platform contains **realistic sample data** for two domains:
- **Sales Domain**: Customer orders, products, revenue
- **Marketing Domain**: Campaigns, leads, website traffic

---

## 🏢 Sales Domain

### Database Schema

```
customers (15 records)
├── customer_id (PK)
├── customer_name
├── email
├── phone
├── country (USA, UK, Germany, France, Australia, Canada)
├── industry (Technology, Finance, Healthcare, Retail, etc.)
├── company_size (Enterprise, Mid-Market, Small)
└── created_at / updated_at

products (10 records)
├── product_id (PK)
├── product_name
├── category (Software, Infrastructure)
├── price (range: $8K - $50K)
├── cost
└── description

orders (20 records - Last 6 months)
├── order_id (PK)
├── customer_id (FK)
├── order_date
├── order_status (Completed, Processing, Pending)
├── total_amount (Total: ~$1.2M)
├── payment_method
├── sales_rep
└── region (North America, Europe, Asia Pacific)

order_items
├── item_id (PK)
├── order_id (FK)
├── product_id (FK)
├── quantity
├── unit_price
├── discount_percent
└── line_total
```

###Pre-built Analytics Views

**1. sales_summary**
```sql
SELECT * FROM sales_summary;
-- Monthly aggregated sales metrics
-- Columns: month, order_count, total_revenue, avg_order_value, unique_customers
```

**2. customer_lifetime_value**
```sql
SELECT * FROM customer_lifetime_value;
-- Customer ranking by total value
-- Columns: customer_id, customer_name, country, industry, total_orders, lifetime_value, avg_order_value, last_order_date
```

**3. product_performance**
```sql
SELECT * FROM product_performance;
-- Product sales rankings
-- Columns: product_id, product_name, category, times_sold, total_quantity, total_revenue, avg_discount
```

---

## 📈 Marketing Domain

### Database Schema

```
campaigns (8 records)
├── campaign_id (PK)
├── campaign_name
├── campaign_type (Product Launch, Webinar, Lead Gen, PPC, etc.)
├── channel (LinkedIn, Google Ads, Email, etc.)
├── start_date / end_date
├── budget (Total: $505K)
├── spent
├── status (Active, Completed)
└── target_audience

leads (15 records)
├── lead_id (PK)
├── first_name / last_name
├── email
├── company
├── job_title (CTO, CIO, VP, etc.)
├── country
├── lead_source (Website, LinkedIn, Email, etc.)
├── lead_score (0-100)
├── status (New, Nurturing, Qualified, Converted)
├── campaign_id (FK)
└── created_at / converted_at

campaign_metrics
├── metric_id (PK)
├── campaign_id (FK)
├── metric_date
├── impressions
├── clicks
├── conversions
├── cost_per_click
└── conversion_rate

website_traffic
├── traffic_id (PK)
├── visit_date
├── page_url
├── source (Organic, Paid Search, Social Media, Email)
├── visitors
├── page_views
├── bounce_rate
└── avg_time_on_page
```

### Pre-built Analytics Views

**1. campaign_performance**
```sql
SELECT * FROM campaign_performance;
-- Campaign ROI and effectiveness
-- Columns: campaign_id, campaign_name, channel, budget, spent, remaining_budget, budget_utilization_pct, total_leads, converted_leads, conversion_rate
```

**2. lead_funnel**
```sql
SELECT * FROM lead_funnel;
-- Lead stage distribution
-- Columns: status, lead_count, avg_lead_score, campaigns_contributing
```

---

## 🔗 Cross-Domain Analytics (Data Mesh Magic!)

### 1. **Lead-to-Customer Journey**
Track which marketing leads became paying customers:

```python
# In JupyterHub
import psycopg2
import pandas as pd

# Connect to both domains
sales_conn = psycopg2.connect(
    host="sales-postgres.sales-domain.svc.cluster.local",
    database="sales_db",
    user="sales_user",
    password="SuperSecurePass123!"
)

marketing_conn = psycopg2.connect(
    host="marketing-postgres.marketing-domain.svc.cluster.local",
    database="marketing_db",
    user="marketing_user",
    password="SuperSecurePass123!"
)

# Get marketing leads
leads_df = pd.read_sql("""
    SELECT lead_id, email, company, lead_source, campaign_id, created_at, status
    FROM leads
    WHERE status = 'Converted'
""", marketing_conn)

# Get sales customers
customers_df = pd.read_sql("""
    SELECT customer_id, customer_name, email, created_at
    FROM customers
""", sales_conn)

# Join by email to track journey
journey_df = leads_df.merge(
    customers_df, 
    left_on='email', 
    right_on='email', 
    how='inner'
)

print(f"Leads that became customers: {len(journey_df)}")
print(journey_df[['company', 'lead_source', 'created_at_x', 'created_at_y']])
```

### 2. **Campaign ROI Analysis**
Calculate return on marketing investment:

```python
# Get campaign spending
campaigns_df = pd.read_sql("SELECT * FROM campaign_performance", marketing_conn)

# Get revenue from converted leads
revenue_query = """
SELECT 
    l.campaign_id,
    c.campaign_name,
    SUM(o.total_amount) as attributed_revenue,
    COUNT(DISTINCT o.order_id) as orders
FROM leads l
JOIN customers cust ON l.email = cust.email
JOIN orders o ON cust.customer_id = o.customer_id
JOIN campaigns c ON l.campaign_id = c.campaign_id
WHERE l.status = 'Converted'
GROUP BY l.campaign_id, c.campaign_name
"""
# Note: This requires cross-domain join - perfect for JupyterHub!

# Calculate ROI
roi_df = campaigns_df.merge(revenue_df, on='campaign_id')
roi_df['roi'] = (roi_df['attributed_revenue'] - roi_df['spent']) / roi_df['spent'] * 100
roi_df.sort_values('roi', ascending=False)
```

### 3. **Customer Acquisition Cost (CAC)**
```python
total_marketing_spend = campaigns_df['spent'].sum()
new_customers = customers_df[customers_df['created_at'] > '2024-06-01'].shape[0]

cac = total_marketing_spend / new_customers
print(f"Customer Acquisition Cost: ${cac:,.2f}")
```

### 4. **Channel Effectiveness**
Which marketing channels drive the most revenue?

```python
channel_analysis = pd.read_sql("""
    SELECT 
        c.channel,
        COUNT(DISTINCT l.lead_id) as total_leads,
        COUNT(DISTINCT CASE WHEN l.status = 'Converted' THEN l.lead_id END) as converted_leads,
        SUM(c.spent) as total_spent
    FROM campaigns c
    LEFT JOIN leads l ON c.campaign_id = l.campaign_id
    GROUP BY c.channel
""", marketing_conn)

# Add revenue data from sales domain
# ... join with sales data ...

channel_analysis['revenue_per_dollar'] = channel_analysis['total_revenue'] / channel_analysis['total_spent']
```

### 5. **Product-Campaign Correlation**
Which campaigns sell which products?

```python
# Complex cross-domain analysis
correlation_query = """
-- This demonstrates data mesh federated queries
-- Each domain owns its data, JupyterHub federates the analysis
"""
```

---

## 💡 Sample Analytics Scenarios

### Scenario 1: Sales Performance Dashboard
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Monthly revenue trend
monthly_sales = pd.read_sql("SELECT * FROM sales_summary ORDER BY month", sales_conn)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales['month'], monthly_sales['total_revenue']/1000, marker='o')
plt.title('Monthly Revenue Trend (Last 6 Months)')
plt.xlabel('Month')
plt.ylabel('Revenue ($K)')
plt.grid(True)
plt.tight_layout()
plt.show()
```

### Scenario 2: Customer Segmentation
```python
from sklearn.cluster import KMeans

# Get customer features
clv_df = pd.read_sql("SELECT * FROM customer_lifetime_value", sales_conn)

# Prepare features for clustering
features = clv_df[['total_orders', 'lifetime_value', 'avg_order_value']].fillna(0)

# K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clv_df['segment'] = kmeans.fit_predict(features)

# Visualize segments
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    clv_df['total_orders'], 
    clv_df['lifetime_value'],
    c=clv_df['segment'],
    cmap='viridis',
    s=100,
    alpha=0.6
)
plt.xlabel('Total Orders')
plt.ylabel('Lifetime Value ($)')
plt.title('Customer Segments')
plt.colorbar(scatter, label='Segment')
plt.tight_layout()
plt.show()
```

### Scenario 3: Lead Scoring Model
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Get lead features
leads_full = pd.read_sql("SELECT * FROM leads", marketing_conn)

# Create target variable (converted = 1, not converted = 0)
leads_full['converted'] = (leads_full['status'] == 'Converted').astype(int)

# Feature engineering
features = pd.get_dummies(leads_full[['lead_score', 'lead_source', 'country']], drop_first=True)
target = leads_full['converted']

# Train model
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Feature importance
importance_df = pd.DataFrame({
    'feature': features.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("Top features predicting conversion:")
print(importance_df.head(10))
```

### Scenario 4: Time Series Forecasting
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Get historical revenue
monthly_sales = pd.read_sql("""
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(total_amount) as revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
    ORDER BY month
""", sales_conn)

# Forecast next 3 months
model = ExponentialSmoothing(
    monthly_sales['revenue'],
    seasonal_periods=3,
    trend='add',
    seasonal='add'
)
fit = model.fit()
forecast = fit.forecast(steps=3)

print("Revenue forecast for next 3 months:")
print(forecast)
```

---

## 🎯 Data Quality & Governance

### Data Quality Checks

```python
# Example data quality checks
def check_data_quality(conn, domain):
    checks = []
    
    # Check for null values
    null_check = pd.read_sql("""
        SELECT 
            column_name,
            COUNT(*) FILTER (WHERE column_value IS NULL) as null_count
        FROM information_schema.columns
        -- ... actual query ...
    """, conn)
    
    # Check for duplicates
    # Check for referential integrity
    # Check for data freshness
    # Check for outliers
    
    return checks

quality_report = check_data_quality(sales_conn, 'sales')
```

### Metadata Catalog

Each domain should maintain metadata:

```python
metadata = {
    "domain": "sales",
    "owner": "sales-team@company.com",
    "description": "Customer orders and revenue data",
    "update_frequency": "real-time",
    "data_classification": "confidential",
    "tables": {
        "customers": {
            "description": "Customer master data",
            "row_count": 15,
            "last_updated": "2024-10-18",
            "quality_score": 98.5
        },
        "orders": {
            "description": "Sales orders",
            "row_count": 20,
            "last_updated": "2024-10-18",
            "quality_score": 100.0
        }
    }
}
```

---

## 🚀 Getting Started

### 1. Deploy Data Mesh
```bash
python setup/deploy_cluster.py
python setup/addons/install_helm.py
python setup/addons/deploy_jupyterhub.py
```

### 2. Load Sample Data
```bash
python setup/addons/setup_sample_data.py
```

### 3. Access JupyterHub
Open: http://localhost:30080
- Username: `admin`
- Password: `datamesh2024`

### 4. Create Your First Notebook
```python
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to sales domain
sales_conn = psycopg2.connect(
    host="sales-postgres.sales-domain.svc.cluster.local",
    database="sales_db",
    user="sales_user",
    password="SuperSecurePass123!"
)

# Your first query
df = pd.read_sql("SELECT * FROM customer_lifetime_value LIMIT 10", sales_conn)
print(df)
```

---

## 📈 Advanced Use Cases

1. **Churn Prediction**: Predict which customers are likely to stop buying
2. **Next Best Action**: Recommend best marketing action for each lead
3. **Price Optimization**: Find optimal pricing for each product
4. **Attribution Modeling**: Multi-touch attribution across campaigns
5. **Cohort Analysis**: Track customer cohorts over time
6. **A/B Testing**: Compare campaign variations
7. **Real-time Dashboards**: Live metrics using Grafana
8. **Anomaly Detection**: Flag unusual patterns in sales or traffic

---

## 🤝 Data Mesh Principles in Action

✅ **Domain Ownership**: Sales team owns customer/order data, Marketing owns campaign/lead data  
✅ **Data as a Product**: Each domain exposes clean, documented APIs  
✅ **Self-Service**: Data scientists access data via JupyterHub without IT help  
✅ **Federated Governance**: Standardized schemas, quality checks, metadata  
✅ **Distributed Architecture**: Each domain has its own database and API  
✅ **Interoperability**: Standard PostgreSQL + REST APIs for integration  

---

## 📝 Notes

- All data is **sample/fictional** for demonstration purposes
- Passwords are for demo only - use proper secrets management in production
- Extend the data model as needed for your use cases
- Add more domains (Finance, Operations, etc.) following the same pattern

---

**Made with ❤️ for Data Engineering Excellence**

