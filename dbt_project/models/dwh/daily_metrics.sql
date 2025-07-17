
{{ config(
    materialized='view',
    post_hook="""
        COPY (
            SELECT * FROM {{ this }}
        ) TO '{{ env_var('EXPORT_PATH', '../') }}/{{ this.name }}.parquet' (FORMAT PARQUET)
    """
) }}



-- Instead of metrics per date & customer => metrics per date
-- There is only one order per customer per day max

with start_end_date as (
    select 
        min( DATE(order_purchase_timestamp)) AS start_date,
        max( DATE(order_purchase_timestamp)) AS end_date,
    from {{ref("dwh_order_lines")}}
)

,calendar as (
    SELECT start_date + (x || ' days')::interval AS order_purchase_date
    FROM start_end_date, range(0, DATE_DIFF('day', start_date, end_date) + 1) AS t(x)
)

,daily_orders as (
    select 
        DATE(order_purchase_timestamp) as order_purchase_date,
        count(distinct order_id) as nb_orders,
        sum(price + freight_value)  as total_amount,
    from {{ref("dwh_order_lines")}}
    GROUP BY order_purchase_date
)

select 
    c.order_purchase_date,
    IFNULL(d.nb_orders, 0) as nb_orders,
    IFNULL(d.total_amount, 0) as total_amount,
    IFNULL(d.total_amount / d.nb_orders, 0) as avg_order_amount,
from calendar c
left join daily_orders d
    using(order_purchase_date)
order by order_purchase_date