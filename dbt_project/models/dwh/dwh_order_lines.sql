
select 
    i.item_id as id,
    -- Heder
    o.order_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date, 
    -- Lines
    c.customer_id,
    c.customer_zip_code_prefix,
    c.customer_city,
    c.customer_state,
    -- Items
    i.order_item_id,
    i.seller_id,
    i.shipping_limit_date,
    i.price,
    i.freight_value, 

    -- Products
    p.product_id,
    p.product_category_name,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
from {{ref("base_raw_items")}} i 
inner join {{ref("base_raw_orders")}} o 
    using (order_id)
inner join {{ref("base_raw_customer")}} c
    using (customer_id)
inner join {{ref("base_raw_products")}} p
    using (product_id)