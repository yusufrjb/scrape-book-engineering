SELECT
    book_id,
    price,
    rating,
    stock_quantity,
    scraped_at
FROM {{ ref('stg_books') }}