{{
    config(
        materialized='view',
        tags=['sales', 'staging']
    )
}}

-- ============================================================================
-- Staging: Sales Orders
-- Clean and enrich order data
-- ============================================================================

with source as (
    select * from {{ source('sales', 'orders') }}
),

renamed as (
    select
        -- Primary key
        order_id,
        
        -- Foreign keys
        customer_id,
        
        -- Order details
        order_date,
        total_amount,
        status,
        payment_method,
        
        -- Timestamps
        created_at,
        updated_at,
        
        -- Derived fields
        extract(year from order_date) as order_year,
        extract(month from order_date) as order_month,
        extract(quarter from order_date) as order_quarter,
        to_char(order_date, 'YYYY-MM') as order_year_month,
        
        -- Metadata
        current_timestamp as _dbt_loaded_at
        
    from source
)

select * from renamed

