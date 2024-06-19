1) Initialize Database:

    Endpoint: GET /api/initialize/
    Description: Fetches data from the third-party API and seeds the database.
    Steps: Open Postman and create a new GET request to http://127.0.0.1:8000/api/initialize/. Click "Send" and check the response.

2) List Transactions with Search and Pagination:

    Endpoint: GET /api/transactions/
    Description: Lists transactions with optional search and pagination.
    Steps: Open Postman and create a new GET request to http://127.0.0.1:8000/api/transactions/. Add query parameters like month, search, page, and page_size as needed. Click "Send" and check the response.
3) Statistics:

    Endpoint: GET /api/statistics/
    Description: Returns statistics for the selected month.
    Steps: Open Postman and create a new GET request to http://127.0.0.1:8000/api/statistics/. Add a query parameter month (e.g., January). Click "Send" and check the response.
4) Bar Chart Data:

    Endpoint: GET /api/bar-chart/
    Description: Returns bar chart data for the selected month.
    Steps: Open Postman and create a new GET request to http://127.0.0.1:8000/api/bar-chart/. Add a query parameter month (e.g., January). Click "Send" and check the response.
5) Pie Chart Data:

    Endpoint: GET /api/pie-chart/
    Description: Returns pie chart data for the selected month.
    Steps: Open Postman and create a new GET request to http://127.0.0.1:8000/api/pie-chart/. Add a query parameter month (e.g., January). Click "Send" and check the response.
6) Combined Data:

    Endpoint: GET /api/combined-data/
    Description: Returns combined data from statistics, bar chart, and pie chart endpoints.
    Steps: Open Postman and create a new GET request to http://127.0.0.1:8000/api/combined-data/. Add a query parameter month (e.g., January). Click "Send" and check the response.