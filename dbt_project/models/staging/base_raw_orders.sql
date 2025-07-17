



select 
  order_id,
  customer_id,
  order_status,
  order_purchase_timestamp,
  order_approved_at,
  order_delivered_carrier_date,
  order_delivered_customer_date,
  order_estimated_delivery_date, 
from {{ source('raw', 'orders') }}
-- Filter some strange date values:
WHERE order_purchase_timestamp between TIMESTAMP '2000-01-01' and  current_localtimestamp()