# sales_proj
This web service serves as a basic store with 'customer', 'product' and 'cart' tables
It supports following API calls:

PUT /{secure_string}/sku -                                  adds product to the service
DELETE /{secure_string}/sku/{product_sku} -                 removes product from the service by product_sku

PUT /{secure_string}/customer -                             adds product to the service
DELETE /{secure_string}/customer/{customer_id} -            removes customer from the service by customer_id

GET /{secure_string}/cart -                                 returns all customer's carts
PUT /{secure_string}/cart -                                 adds a product to the customer's cart
DELETE /{secure_string}/cart/{customer_id}/{product_sku} -  removes a product from the customer's cart
                                                            by customer_id and product_sku
