# Barebones Shopping Store
## By Viraj Bangari

## Features

## API Endpoints
Note: all API endpoints will return a 500 error code on schema error.

**Endpoint**
`/api/producer`

**Method**
`POST`

**Content Schema**
```
{"username": string, "password": string} with code 200
```

**Return Value**
`Producer`

**Explanation**
Creates a new producer and returns the schema for it.

-------

**Endpoint**
`/api/producer`

**Method**
`GET`

**Params**
`None`

**Return Value**
```
[Array of Producer] with code 200
```

**Explanation**
Returns all producers

-------

**Endpoint**
`/api/producer/<int:producer_id>`

**Method**
`GET`

**Params**
`None`

**Return Value**
```
Producer with code 200 if id found
{} with code 404 if id not found
```

**Explanation**
Returns a producer with the matching id. 

-------

**Endpoint**
`/api/products`

**Method**
`GET`

**Params**
`min-inventory-count: int`

**Return Value**
```
[Array of products] with code 200
```

**Explanation**
Returns all products whose inventory count is greater than the specified parameter. If no parameter is included, all products are returned.

-------

**Endpoint**
`/api/products`

**Method**
`POST`

**Content Schema**
```
{
    "producer_id": int,  // Id of the producer who creates this product.
    "title": string,
    "cost": decimal,
    "inventory_count": int
}
```

**Return Value**
```
Product with code 200
```

**Explanation**
Creates a new product with the associated producer id.

-------

**Endpoint**
`/api/products/<int:product_id>`

**Method**
`PUT`

**Content Schema**
```
{
    "title": string,  // optional
    "cost": decimal,  // optional 
    "inventory_count": int // optional
}
```

**Return Value**
```
Product with code 200 if id found
{} with code 404 if id not found
```

**Explanation**
Overwrites the attributes of a product with the specified attributes in the content.

------

**Endpoint**
`/api/products/<int:product_id>`

**Method**
`DELETE`

**Return Value**
```
Product with code 200 if id not found
{} with code 404 if id not found
```

**Explanation**
`Deletes a product with matching id`

------

**Endpoint**
`/api/shopping_cart`

**Method**
`POST`

**Return Value**
```
ShoppingCart with code 200
```

**Explanation**
`Creates a new shopping cart.`

## API Model Schema
**Producer**
```
{
    "id": int, // id of producer
    "username": string, // username of prodcuer
    "products": [Array of Product] // products created by producer
}
```

**Product**
```
{
    "id": int, // id of product
    "producer_id": int, // id of parent producer
    "title": string, // name of product
    "price": decimal, // price of product, must be greater than or equal to 0.1
    "inventory_count": int // number of available prodcuts, must be greater than or equal to 0
}
```

**Shopping Cart**
```
{
    "id": int, // id of shopping cart
    "cached_price": decimal, // cached price of all the products in the shopping cart.
                             // In the case where a producer changes the price of a product,
                             // the cached price will not update unless explicitly told to
                             // via the API or when a purchase is made.
    "shopping_cart_entries": [Array of ShoppingCartEntry]
}
```

**ShoppingCartEntry**
```
{
    "id": int, // id of shopping cart entry
    "shopping_cart_id": int, // parent shopping cart
    "quantity": int, // quantity of product request, must be greater than 0
    "product_id": int, // id of corresponding product
    "product": self.product.as_dict()
    "shopping_cart_entries": [Array of ShoppingCartEntry]
}

```


## Souce Code Explanation
```
barebones/model.py - The database models - Producer, Product, ShoppingCart, ShoppingCartEntry
barebones/api.py - Handling of API endpoints and updating model
barebones/app.py - Global Flask object creation
barebones/init.py - DB initialization code
barebones/run.py - Server running code
test/test_api.py - Integration tests with API calls
```

## How to Run
Required: Python 3.6+, SQLite3, Pip3

In the root folder, run the folowing to install the required python modules:
```
pip install -r requirements.txt
```

To initialize the database file, run:
```
python barebones/init.py
```
This only needs to be run once. By default, the `.db` file is stored in the `barebones` directory.

To run the server, run:
```
python barebones.run
```
