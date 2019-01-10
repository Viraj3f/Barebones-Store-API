# Barebones Shopping Store
## By Viraj Bangari

## Features

## API Endpoints
**Endpoint**
`/api/producer`

**Method**
`POST`

**Content Schema**
`{"username": string, "password": string}`

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
`[Array of Producer]`

**Explanation**
Returns all producers

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
    "price": decimal, // price of product
    "inventory_count": int // number of available prodcuts
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
    "quantity": int, // quantity of product request
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
