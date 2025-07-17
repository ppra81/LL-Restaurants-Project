# LL-Restaurants-Project
Database project for Little Lemon restaurant, including MySQL schema, Python data import script, stored procedures, and Tableau visualization instructions.

# LLRestaurant Database Project
This project implements a database solution for the Little Lemon restaurant, including a MySQL database schema, stored procedures, a Python script for data import, and instructions for Tableau visualizations. The project handles data quality issues such as duplicate `Order ID` values and illogical dates.

Project Structure

`create_littlelemon_schema.sql`: MySQL script to create the `LittleLemon` database and tables.\
`stored_procedures.sql`: MySQL stored procedures for order and booking management.\
`import_littlelemon_data.py`: Python script to import data from `LittleLemon_data.csv`, handling duplicates and illogical dates.\
`README.md`: Project documentation.\
`.gitignore`: Excludes sensitive files like `LittleLemon_data.csv` and logs.

Prerequisites

MySQL Server (version 8.0 or later)\
Python 3.8+ with packages: `mysql-connector-python`, `pandas`\
Tableau Desktop or Tableau Public (for visualizations)

Git
Setup Instructions

**Clone the Repository**:```bashgit clone https://github.com/your-username/LittleLemon-Project.git\cd LittleLemon-Project```

**Set Up MySQL Database**:


Start MySQL server.\
Run the schema script:```bashmysql -u your_username -p < create_littlelemon_schema.sql```\
Run the stored procedures script:```bashmysql -u your_username -p < stored_procedures.sql```


**Install Python Dependencies**:```bashpip install mysql-connector-python pandas```

**Update Database Credentials**:


Edit `import_littlelemon_data.py` to update the `config` dictionary with your MySQL username and password.\


**Run Data Import**:\


Place `LittleLemon_data.csv` (not included) in the project directory.\
Run the Python script:```bashpython import_littlelemon_data.py```
Check `data_import.log` for import details.

Data Import Details

The script processes `LittleLemon_data.csv` (~21,000 rows).\
Removes duplicate `Order ID` entries, keeping the first occurrence (~1,000 unique orders).\
Swaps `Order Date` and `Delivery Date` for rows where `Delivery Date` < `Order Date` (~446 rows).\
Logs errors and warnings to `data_import.log`.\

<img width="589" height="871" alt="Image" src="https://github.com/user-attachments/assets/1e6b8b01-18dd-4342-b946-d0deb12853b9" />

Stored Procedures\

`GetMaxQuantity`: Returns the order with the highest quantity.\
`ManageBooking`: Checks table availability.\
`AddBooking`, `UpdateBooking`, `CancelBooking`: Manage restaurant bookings.\

Tableau Visualizations\

**Connect to Database**:\


In Tableau, connect to MySQL using `LittleLemon` database credentials.\
Select tables: `Orders`, `Customers`, `Courses`, `Cuisines`.\


**Visualizations**:\


**Total Sales by Country**: Bar chart or map showing sales by country.\
**Popular Courses**: Pie chart showing order counts by course.\
**Sales Over Time**: Line chart showing monthly sales.\


**Dashboard**:\


Combine visualizations into a dashboard with interactive filters.\

ER Diagram\

Entities: `Customers`, `Cuisines`, `Courses`, `Starters`, `Desserts`, `Drinks`, `Sides`, `Orders`, `Bookings`.\
ER Diagram was generated using MySQL.\\

Usage\

Run SQL queries to verify data:```sqlSELECT COUNT(*) FROM Orders; -- Expect ~1,000SELECT OrderID, OrderDate, DeliveryDate FROM Orders WHERE DeliveryDate < OrderDate; -- Expect 0```\
Test stored procedures:```sqlCALL GetMaxQuantity();CALL AddBooking('53-236-6596', '2025-08-01', 5, 4);```\

Notes\

`LittleLemon_data.csv` is excluded due to sensitive data (customer information).\
The Python script handles data quality issues (duplicates, illogical dates).\
Check `data_import.log` for import errors or warnings.\

License\
MIT License
