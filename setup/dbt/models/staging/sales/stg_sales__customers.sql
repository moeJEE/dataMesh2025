{{
    config(
        materialized='view',
        tags=['sales', 'staging']
    )
}}

-- ============================================================================
-- Staging: Sales Customers
-- Clean and standardize customer data
-- ============================================================================

with source as (
    select * from {{ source('sales', 'customers') }}
),

renamed as (
    select
        -- Primary key
        customer_id,
        
        -- Attributes
        customer_name,
        lower(trim(email)) as email,
        phone,
        upper(trim(country)) as country,
        industry,
        company_size,
        
        -- Timestamps
        created_at,
        updated_at,
        
        -- Metadata
        current_timestamp as _dbt_loaded_at
        
    from source
)

select * from renamed

