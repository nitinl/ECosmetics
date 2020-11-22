# ECosmetic REST API

### Run '\_\_init\_\_.py' - Initialize database and creates all the necessary models
    
### Endpoints

|HTTP Method|  URL                                      | Description                                        |
|-----------|-------------------------------------------|----------------------------------------------------|
|  GET      |   /getdatafromexternalapi                 |API to read the data from external API i.e MakeupAPI|
|  GET      |   /product/<int:product_id>               |API to fetch the product based on product_id        |
|  GET      |   /searchproduct                          |API to search for product based on brand,product_category,product_type,price_greater_than,price_less_than,rating_greater_than,rating_less_than,product_tags|
|  GET      |   /getallbrands                           |API to get all available Brands                     |                 
|  GET      |   /getallcategories                       |API to get all available Product Categories         |
|  GET      |   /getallcolors                           |API to get all available Product Colors             |
|  GET      |   /getallproducttypes                     |API to get all available Product Types              |
|  GET      |   /getallproducttags                      |API to get all available Product Tags               |
|  POST     |   /addproduct                             |API to add the product                              |
|  PUT      |   /updateproduct/<int:product_id>         |API to update a product based on product_id. Updates all fields|
|  PATCH    |   /updateproduct/<int:product_id>         |API to update a product based on product_id. Updates required fields|
|  DELETE   |   /delproduct/<int:product_id>            |API to delete a product based on product_id         |
