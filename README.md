# E-commerce Admin App Backend
Welcome to the E-commerce Admin App Backend! This backend application provides the server-side functionality for an e-commerce admin panel. It is built using FastAPI and SQLAlchemy.

## Prerequisites
Before getting started, ensure that you have the following prerequisites installed on your machine:

- Python (3.7+ required)

## Setup
1. Clone the Repository: You can download the code or clone this repository to your local machine using the following command:
`gh repo clone Adan-Asim/E-commerce-Admin-App-Backend`

2. Create a Virtual Environment: To isolate project dependencies, create a virtual environment. Use the appropriate command based on your operating system:
- Windows: `python -m venv venv`
- macOS or Linux: `python3 -m venv venv`

3. Install Dependencies: Install the required dependencies for the project using pip. Run one of the following commands based on your system:
- Windows: `pip install fastapi uvicorn pydantic sqlalchemy`
- macOS:  `python3 -m pip install fastapi uvicorn pydantic sqlalchemy`

4. Run the Server: Start the server using uvicorn with the following command:
`uvicorn main:app --reload`

5. Access the Application: Open your web browser and navigate to http://127.0.0.1:8000/ to access the application. Alternatively, you can use any API client to send requests to the API endpoints.

6. Explore the API Documentation: Visit the Swagger UI documentation by going to http://127.0.0.1:8000/docs. Here, you can explore and test the available API endpoints interactively.

7. Come back to the terminal, and type the following command: `python script`, this will run a script, and will populate the database with bulk of demo data

## Usage
Here you will see the following six APIs:

<img width="1728" alt="image" src="https://github.com/Adan-Asim/E-commerce-Admin-App-Backend/assets/67644268/d11fae1f-fed3-4dec-b3a2-b5fe0f477cb3">

Each of them has its own purpose as follows:

### 1- Endpoint: `/sales/`
#### Purpose: retrieve, filter, and analyze sales data using date range, product, and category

Description: This endpoint retrieves sales data within a specified date range for a given product or category. It allows you to filter and view sales data based on criteria such as start and end dates, product name, and category name.

### 2- Endpoint: `/revenue/`
#### Purpose: analyze revenue on a daily, weekly, monthly, and annual basis and also compare revenue across different periods and categories.

Description: This endpoint provides revenue analysis based on sales data. You can specify the date range (start and end dates) and the interval (e.g., daily, weekly, monthly, annual) for revenue calculation. Additionally, you can filter revenue data by category.

### 3- Endpoint: `/inventory/`
#### Purpose: view current inventory status, including low stock alerts.

Description: This endpoint retrieves inventory status, including information about products with low stock levels. You can set a low stock threshold to filter products that are below a certain quantity.

### 4- Endpoint: `/inventory/update/`
#### Purpose: update inventory levels and stocks

Description: This endpoint allows you to update the inventory level of a specific product. You can provide the product name and the quantity to add to the inventory. If the product is not found, it returns a 404 error.

### 5- Endpoint: `/inventory/changes/`
#### Purpose: Track changes to inventory over time

Description: This endpoint retrieves a log of inventory changes within a specified date and time range for a given product. It provides information about changes such as quantity additions or subtractions.

### 6- Endpoint: `/products/`
#### Purpose: Register new product

Description: This endpoint allows you to register a new product in the system. You need to provide product details such as name, description, price, category name, initial stock level, and low stock alert threshold. It returns the created product if successful.

These API endpoints provide essential functionality for managing sales data, revenue analysis, inventory status, inventory updates, inventory change logs, and product registration within your e-commerce admin application. You can use the provided APIs to interact with and manage your e-commerce backend efficiently.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
