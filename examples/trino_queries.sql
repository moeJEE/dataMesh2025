-- ============================================================================
-- TRINO FEDERATED QUERIES - DataMeesh Platform
-- ============================================================================
-- Use these queries in JupyterHub or Trino CLI
-- Connection: trino-coordinator.data-platform.svc.cluster.local:8080
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. BASIC QUERIES - Single Domain
-- ----------------------------------------------------------------------------

-- Sales: Top 10 Customers by Revenue
SELECT 
    customer_name,
    email,
    country,
    industry,
    SUM(total_amount) as lifetime_value,
    COUNT(DISTINCT order_id) as total_orders
FROM sales.public.customers c
JOIN sales.public.orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3, 4
ORDER BY lifetime_value DESC
LIMIT 10;

-- Marketing: Campaign Performance
SELECT 
    campaign_name,
    channel,
    budget,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    SUM(conversions) as total_conversions,
    ROUND(SUM(clicks) * 100.0 / NULLIF(SUM(impressions), 0), 2) as ctr_percent,
    ROUND(SUM(conversions) * 100.0 / NULLIF(SUM(clicks), 0), 2) as conversion_rate
FROM marketing.public.campaigns c
JOIN marketing.public.campaign_metrics m ON c.campaign_id = m.campaign_id
GROUP BY 1, 2, 3
ORDER BY total_conversions DESC;

-- ----------------------------------------------------------------------------
-- 2. CROSS-DOMAIN QUERIES - The Power of Data Mesh!
-- ----------------------------------------------------------------------------

-- Lead-to-Customer Journey Analysis
SELECT 
    l.lead_source,
    COUNT(DISTINCT l.lead_id) as total_leads,
    COUNT(DISTINCT c.customer_id) as converted_customers,
    ROUND(COUNT(DISTINCT c.customer_id) * 100.0 / COUNT(DISTINCT l.lead_id), 2) as conversion_rate_percent,
    SUM(o.total_amount) as total_revenue,
    ROUND(SUM(o.total_amount) / NULLIF(COUNT(DISTINCT c.customer_id), 0), 2) as avg_revenue_per_customer
FROM marketing.public.leads l
LEFT JOIN sales.public.customers c ON LOWER(TRIM(l.email)) = LOWER(TRIM(c.email))
LEFT JOIN sales.public.orders o ON c.customer_id = o.customer_id
GROUP BY l.lead_source
ORDER BY total_revenue DESC NULLS LAST;

-- Campaign ROI with Sales Attribution
SELECT 
    c.campaign_name,
    c.channel,
    c.budget,
    COUNT(DISTINCT l.lead_id) as leads_generated,
    COUNT(DISTINCT cust.customer_id) as customers_acquired,
    SUM(o.total_amount) as attributed_revenue,
    ROUND((SUM(o.total_amount) - c.budget) / NULLIF(c.budget, 0) * 100, 2) as roi_percent
FROM marketing.public.campaigns c
LEFT JOIN marketing.public.leads l ON c.campaign_id = l.campaign_id
LEFT JOIN sales.public.customers cust ON LOWER(TRIM(l.email)) = LOWER(TRIM(cust.email))
LEFT JOIN sales.public.orders o ON cust.customer_id = o.customer_id
GROUP BY 1, 2, 3
ORDER BY attributed_revenue DESC NULLS LAST;

-- ----------------------------------------------------------------------------
-- 3. ADVANCED ANALYTICS
-- ----------------------------------------------------------------------------

-- Customer Segmentation with Marketing Attribution
WITH customer_segments AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.country,
        c.industry,
        SUM(o.total_amount) as lifetime_value,
        COUNT(o.order_id) as order_count,
        CASE 
            WHEN SUM(o.total_amount) >= 100000 THEN 'High Value'
            WHEN SUM(o.total_amount) >= 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END as segment
    FROM sales.public.customers c
    LEFT JOIN sales.public.orders o ON c.customer_id = o.customer_id
    GROUP BY 1, 2, 3, 4
),
lead_attribution AS (
    SELECT 
        c.customer_id,
        l.lead_source,
        l.campaign_id
    FROM sales.public.customers c
    JOIN marketing.public.leads l ON LOWER(TRIM(c.email)) = LOWER(TRIM(l.email))
)
SELECT 
    cs.segment,
    cs.country,
    la.lead_source,
    COUNT(DISTINCT cs.customer_id) as customer_count,
    ROUND(AVG(cs.lifetime_value), 2) as avg_lifetime_value,
    ROUND(AVG(cs.order_count), 2) as avg_orders
FROM customer_segments cs
LEFT JOIN lead_attribution la ON cs.customer_id = la.customer_id
GROUP BY 1, 2, 3
ORDER BY cs.segment, customer_count DESC;

-- Product Performance by Customer Segment
SELECT 
    p.product_name,
    p.category,
    CASE 
        WHEN SUM(o.total_amount) >= 100000 THEN 'High Value'
        WHEN SUM(o.total_amount) >= 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment,
    COUNT(DISTINCT c.customer_id) as unique_customers,
    SUM(oi.quantity) as units_sold,
    SUM(oi.subtotal) as total_revenue
FROM sales.public.products p
JOIN sales.public.order_items oi ON p.product_id = oi.product_id
JOIN sales.public.orders o ON oi.order_id = o.order_id
JOIN sales.public.customers c ON o.customer_id = c.customer_id
GROUP BY 1, 2, 3
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- 4. TIME-BASED ANALYSIS
-- ----------------------------------------------------------------------------

-- Monthly Sales Trends with Marketing Spend
SELECT 
    DATE_TRUNC('month', o.order_date) as month,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.total_amount) as revenue,
    COUNT(DISTINCT o.customer_id) as active_customers,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT o.order_id), 2) as avg_order_value
FROM sales.public.orders o
GROUP BY 1
ORDER BY month DESC;

-- Lead Velocity Rate (LVR) - Growth Metric
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(lead_id) as leads_created,
    LAG(COUNT(lead_id)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as previous_month_leads,
    ROUND(
        (COUNT(lead_id) - LAG(COUNT(lead_id)) OVER (ORDER BY DATE_TRUNC('month', created_at))) 
        * 100.0 / NULLIF(LAG(COUNT(lead_id)) OVER (ORDER BY DATE_TRUNC('month', created_at)), 0), 
        2
    ) as growth_rate_percent
FROM marketing.public.leads
GROUP BY 1
ORDER BY month DESC;

-- ----------------------------------------------------------------------------
-- 5. DATA QUALITY CHECKS
-- ----------------------------------------------------------------------------

-- Check for orphaned records
SELECT 
    'Orders without customers' as issue,
    COUNT(*) as count
FROM sales.public.orders o
LEFT JOIN sales.public.customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL

UNION ALL

SELECT 
    'Leads with invalid emails' as issue,
    COUNT(*) as count
FROM marketing.public.leads
WHERE email NOT LIKE '%@%.%'

UNION ALL

SELECT 
    'Orders with zero amount' as issue,
    COUNT(*) as count
FROM sales.public.orders
WHERE total_amount <= 0;

-- ----------------------------------------------------------------------------
-- 6. COHORT ANALYSIS
-- ----------------------------------------------------------------------------

-- Customer Cohort Analysis by Lead Source
WITH first_order AS (
    SELECT 
        customer_id,
        MIN(order_date) as first_order_date,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM sales.public.orders
    GROUP BY customer_id
),
customer_cohorts AS (
    SELECT 
        fo.cohort_month,
        la.lead_source,
        COUNT(DISTINCT fo.customer_id) as cohort_size,
        SUM(o.total_amount) as total_revenue
    FROM first_order fo
    JOIN sales.public.orders o ON fo.customer_id = o.customer_id
    LEFT JOIN (
        SELECT c.customer_id, l.lead_source
        FROM sales.public.customers c
        JOIN marketing.public.leads l ON LOWER(TRIM(c.email)) = LOWER(TRIM(l.email))
    ) la ON fo.customer_id = la.customer_id
    WHERE o.order_date <= fo.first_order_date + INTERVAL '90' DAY
    GROUP BY 1, 2
)
SELECT 
    cohort_month,
    lead_source,
    cohort_size,
    total_revenue,
    ROUND(total_revenue / cohort_size, 2) as revenue_per_customer_90days
FROM customer_cohorts
ORDER BY cohort_month DESC, total_revenue DESC;

-- ============================================================================
-- HOW TO USE IN JUPYTERHUB
-- ============================================================================
-- 
-- from trino.dbapi import connect
-- 
-- conn = connect(
--     host='trino-coordinator.data-platform.svc.cluster.local',
--     port=8080,
--     user='admin'
-- )
-- 
-- cursor = conn.cursor()
-- cursor.execute("SELECT * FROM sales.public.customers LIMIT 10")
-- rows = cursor.fetchall()
-- 
-- # Or with pandas
-- import pandas as pd
-- df = pd.read_sql(query, conn)
-- 
-- ============================================================================

