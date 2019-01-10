# Barebones Shopping Store
### By Viraj Bangari

A barebones shopping API that supports multiple producers, products and shopping carts.

## Table of Contents

[Features](#features)

[API Endpoints](#api-endpoints)

[API Model Schema](#api-model-schema)

[Souce Code Explanation](#source-code-explanation)

[How to run](#how-to-run)

## Features
<a name="features"/>

* Statless RESTful API.
* ORM that can be used with any production grade RDMS. (default: SQLite)
* Supports producers, who can create an account and start creating products.
* Producers can update the price, quantity and title of their products.
* Producers can delete their prodicuts.
* Allows for GETing all products, filtering by their quantity.
* Allows the creation and deletion of shopping carts, which can contain multiple products and can have the total price cached.
* Shopping carts do not require an account and are secured using API tokens.
* Concurrency-safe when checking out a shopping cart.
* Integration tested

## API Endpoints
<a name="api-endpoints"/>
Note: all API endpoints will return a 500 error code on schema error.

**Endpoint**
`/api/producer`

**Method**
`POST`

**Content Schema**
```
{"username": string, "password": string}
```

**Return Value**
`Producer with code 200`

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

**params**
`min-inventory-count: int`

**Return Value**
```
[Array of products] with code 200
```

**Explanation**
Returns all products whose inventory count is greater than the specified parameter. If no parameter is included, it is as if min-inventory-count is set to 1.

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
`/api/products/<int:product_id> `

**Method**
`DELETE`

**Return Value**
```
Code 200 if id found
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

------

**Endpoint**
`/api/shopping_cart/<int:shopping_cart_id>`

**Method**
`GET`

**params**
`use-cache: int // 0 is false, anything else or unspecified is true.`

**Return Value**
```
ShoppingCart with code 200
```

**Explanation**
```
Returns the shopping cart with the cached price. If use-cache is set to False, then the total price is recomputed by traversing through the list of products. This will only be an issue if a producer changes the price of a product while it is in a shopping cart.
```

------

**Endpoint**
`/api/shopping_cart/<int:shopping_cart_id>`

**Method**
`DELETE`

**Return Value**
```
Message with code 200
```

**Explanation**
```
Code 200 if id found
{} with code 404 if id not found
```

## API Model Schema
<a name="api-model-schema"/>

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
<a name="source-code-explanation"/>

```
barebones/model.py - The database models - Producer, Product, ShoppingCart, ShoppingCartEntry
barebones/api.py - Handling of API endpoints and updating model
barebones/app.py - Global Flask object creation
barebones/init.py - DB initialization code
barebones/run.py - Server running code
test/test\_api.py - Integration tests with API calls
```

## How to Run

<a name="how-to-run"/>
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
