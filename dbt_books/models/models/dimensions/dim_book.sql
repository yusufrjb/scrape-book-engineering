SELECT
    book_id,
    product_name,
    product_url
FROM {{ ref('stg_books') }}