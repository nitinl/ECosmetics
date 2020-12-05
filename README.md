# ECosmetics REST API

###  Set up the project as below
     1. Checkout the project from Git Repo
     2. Import the project into IDE 
     3. Install Virtual environment
        py -m pip install virtualenv
     4. Create virtual environment
        python -m venv c:\path\to\myenv
     5. Activate the virtual environment create at step 3
        .\myenv\Scripts\activate
     6. Install all the requirements available "requirements.txt" in the virtual environment (available in root of the project)
        pip install -r requirements.txt
     7. Run '\_\_init\_\_.py' - Initialize database and creates all the necessary models
     8. Run ECosmetics.py for running the main app i.e. ECosmetics API
     
 ### Endpoints

|HTTP Method|  URL                                | Description                                        |
|-----------|-------------------------------------|----------------------------------------------------|
|  POST     |   /signup                           |API to allow the user to signup                     |
|  POST     |   /login                            |API to get the access token which allows user for accessing all the functionalities in ECosmetics|
|  GET      |   /getdatafromexternalapi           |API to read the data from external API i.e MakeupAPI|
|  GET      |   /product/<int:product_id>         |API to fetch the product based on product_id        |
|  GET      |   /searchproduct                    |API to search for product based on brand,product_category,product_type,price_greater_than,price_less_than,rating_greater_than,rating_less_than,product_tags|
|  GET      |   /getallbrands                     |API to get all available Brands                     |                 
|  GET      |   /getallcategories                 |API to get all available Product Categories         |
|  GET      |   /getallcolors                     |API to get all available Product Colors             |
|  GET      |   /getallproducttypes               |API to get all available Product Types              |
|  GET      |   /getallproducttags                |API to get all available Product Tags               |
|  POST     |   /addproduct                       |API to add the product. Accepts JSON as input                             |
|  PUT      |   /updateproduct/<int:product_id>   |API to update a product based on product_id. Updates all fields passed as JSON|
|  PATCH    |   /updateproduct/<int:product_id>   |API to update a product based on product_id. Updates required fields passed as JSON|
|  DELETE   |   /delproduct/<int:product_id>      |API to delete a product based on product_id         |
