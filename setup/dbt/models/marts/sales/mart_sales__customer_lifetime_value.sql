{{
    config(
        materialized='incremental',
        unique_key='customer_id',
        on_schema_change='fail',
        tags=['sales', 'marts', 'kpi']
    )
}}

-- ============================================================================
-- Mart: Customer Lifetime Value
-- Calculate key customer metrics
-- ============================================================================

with customers as (
    select * from {{ ref('stg_sales__customers') }}
),

orders as (
    select * from {{ ref('stg_sales__orders') }}
),

customer_metrics as (
    select
        c.customer_id,
        c.customer_name,
        c.email,
        c.country,
        c.industry,
        c.company_size,
        c.created_at as customer_since,
        
        -- Order metrics
        count(o.order_id) as total_orders,
        coalesce(sum(o.total_amount), 0) as lifetime_value,
        coalesce(avg(o.total_amount), 0) as average_order_value,
        min(o.order_date) as first_order_date,
        max(o.order_date) as last_order_date,
        
        -- Customer segmentation
        case
            when coalesce(sum(o.total_amount), 0) >= {{ var('high_value_threshold') }} then 'High Value'
            when coalesce(sum(o.total_amount), 0) >= {{ var('min_order_value') }} then 'Medium Value'
            when coalesce(sum(o.total_amount), 0) > 0 then 'Low Value'
            else 'No Orders'
        end as customer_segment,
        
        -- Recency
        case
            when max(o.order_date) >= current_date - interval '30 days' then 'Active'
            when max(o.order_date) >= current_date - interval '90 days' then 'At Risk'
            when max(o.order_date) is not null then 'Churned'
            else 'Never Ordered'
        end as customer_status,
        
        -- Metadata
        current_timestamp as _dbt_updated_at
        
    from customers c
    left join orders o on c.customer_id = o.customer_id
    
    {% if is_incremental() %}
        where o.updated_at > (select max(_dbt_updated_at) from {{ this }})
           or o.updated_at is null
    {% endif %}
    
    group by 1, 2, 3, 4, 5, 6, 7
)

select * from customer_metrics

