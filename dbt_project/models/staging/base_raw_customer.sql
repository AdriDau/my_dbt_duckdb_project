

select 
  customer_id,
  --customer_unique_id,
  customer_zip_code_prefix,
  customer_city,
  customer_state,   
from {{ source('raw', 'customer') }} c
-- Just two duplciate customer_id, each with one empty field : 
where customer_unique_id is not null and customer_city is not null

-- To keep one line per customer_id (fresher if we get a date, not actually then whatever) if any prob:
-- qualify row_number() over (partition by customer_id) = 1 