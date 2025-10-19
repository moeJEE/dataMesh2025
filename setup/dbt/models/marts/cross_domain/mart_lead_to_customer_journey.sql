{{
    config(
        materialized='table',
        tags=['cross_domain', 'marts', 'analytics']
    )
}}

-- ============================================================================
-- Cross-Domain Mart: Lead to Customer Journey
-- Track the full customer journey from marketing lead to sales customer
-- ============================================================================

with marketing_leads as (
    select
        lead_id,
        lower(trim(email)) as email,
        first_name || ' ' || last_name as full_name,
        company,
        lead_source,
        lead_stage,
        lead_score,
        created_at as lead_created_at,
        updated_at as lead_updated_at
    from {{ source('marketing', 'leads') }}
),

sales_customers as (
    select * from {{ ref('stg_sales__customers') }}
),

sales_orders as (
    select * from {{ ref('stg_sales__orders') }}
),

-- Match leads to customers by email
lead_customer_match as (
    select
        l.lead_id,
        l.email,
        l.full_name as lead_name,
        l.company as lead_company,
        l.lead_source,
        l.lead_stage,
        l.lead_score,
        l.lead_created_at,
        
        c.customer_id,
        c.customer_name,
        c.country,
        c.industry,
        c.created_at as customer_created_at,
        
        -- Journey metrics
        case
            when c.customer_id is not null then true
            else false
        end as is_converted,
        
        case
            when c.customer_id is not null 
            then extract(day from c.created_at - l.lead_created_at)
            else null
        end as days_to_conversion,
        
        -- Metadata
        current_timestamp as _dbt_loaded_at
        
    from marketing_leads l
    left join sales_customers c on l.email = c.email
),

-- Add order data for converted customers
enriched_journey as (
    select
        lc.*,
        
        -- Order metrics (only for converted customers)
        count(o.order_id) as total_orders,
        coalesce(sum(o.total_amount), 0) as total_revenue,
        coalesce(avg(o.total_amount), 0) as average_order_value,
        min(o.order_date) as first_order_date,
        max(o.order_date) as last_order_date,
        
        -- Customer value classification
        case
            when coalesce(sum(o.total_amount), 0) = 0 then 'Not Yet Purchased'
            when sum(o.total_amount) >= {{ var('high_value_threshold') }} then 'High Value Customer'
            when sum(o.total_amount) >= {{ var('min_order_value') }} then 'Medium Value Customer'
            else 'Low Value Customer'
        end as customer_value_segment
        
    from lead_customer_match lc
    left join sales_orders o on lc.customer_id = o.customer_id
    group by
        lc.lead_id, lc.email, lc.lead_name, lc.lead_company,
        lc.lead_source, lc.lead_stage, lc.lead_score, lc.lead_created_at,
        lc.customer_id, lc.customer_name, lc.country, lc.industry,
        lc.customer_created_at, lc.is_converted, lc.days_to_conversion,
        lc._dbt_loaded_at
)

select * from enriched_journey

