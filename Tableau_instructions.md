     # Tableau Visualizations for Little Lemon Project

     This document outlines how to create Tableau visualizations using the `LittleLemon` database.

     ## Connect to Database
     1. Open Tableau Desktop or Tableau Public.
     2. Under **Connect**, select **MySQL**.
     3. Enter:
        - Server: `localhost`
        - Port: `3306`
        - Database: `LittleLemon`
        - Username: Your MySQL username
        - Password: Your MySQL password
     4. Drag tables to the canvas: `Orders`, `Customers`, `Courses`, `Cuisines`.
     5. Verify joins (e.g., `Orders.CustomerID = Customers.CustomerID`).

     ## Visualizations
     ### 1. Total Sales by Country (Bar Chart)
     - SQL Query:
       ```sql
       SELECT c.Country, SUM(o.Sales) as TotalSales
       FROM Orders o
       JOIN Customers c ON o.CustomerID = c.CustomerID
       GROUP BY c.Country
       ORDER BY TotalSales DESC;
       ```
     - Steps:
       1. Create a new worksheet named `Total Sales by Country`.
       2. Drag `Country` (Customers) to **Rows**, `Sales` (Orders) to **Columns**.
       3. Set `Sales` to `Sum`.
       4. Select **Bar** in the Marks card.
       5. Sort `Country` by `Sum of Sales` (descending).
       6. Format: Add labels, set title to `Total Sales by Country`, use currency format for `Sales`.

     ### 2. Popular Courses (Pie Chart)
     - SQL Query:
       ```sql
       SELECT co.CourseName, COUNT(*) as OrderCount
       FROM Orders o
       JOIN Courses co ON o.CourseID = co.CourseID
       GROUP BY co.CourseName
       ORDER BY OrderCount DESC;
       ```
     - Steps:
       1. Create a new worksheet named `Popular Courses`.
       2. Drag `CourseName` (Courses) to **Rows**, `OrderID` (Orders) to **Text**.
       3. Set `OrderID` to `Count (Distinct)`.
       4. Select **Pie** in the Marks card.
       5. Drag `CNTD(OrderID)` to **Angle**, `CourseName` to **Color**.
       6. Sort `CourseName` by `CNTD(OrderID)` (descending).
       7. Format: Add labels, set title to `Popular Courses`.

     ### 3. Sales Over Time (Line Chart)
     - SQL Query:
       ```sql
       SELECT DATE_FORMAT(OrderDate, '%Y-%m') as Month, SUM(Sales) as TotalSales
       FROM Orders
       GROUP BY Month
       ORDER BY Month;
       ```
     - Steps:
       1. Create a new worksheet named `Sales Over Time`.
       2. Drag `OrderDate` (Orders) to **Columns**, set to `Month` (e.g., `January 2020`).
       3. Drag `Sales` (Orders) to **Rows**, set to `Sum`.
       4. Select **Line** in the Marks card.
       5. Format: Set title to `Sales Over Time`, use currency format for `Sales`.

     ## Create Dashboard
     1. Create a new dashboard named `Little Lemon Sales Dashboard`.
     2. Drag `Total Sales by Country`, `Popular Courses`, and `Sales Over Time` to the canvas.
     3. Arrange charts (e.g., bar chart left, pie and line charts right).
     4. Add interactivity: Use `Total Sales by Country` as a filter (click chart, select **Use as Filter**).
     5. Add a title: `Little Lemon Sales Dashboard`.
     6. Save as `LittleLemon_Dashboard.twb` or `LittleLemon_Dashboard.twbx`.

     ## Notes
     - Ensure ~1,000 orders are in the database (post-import).
     - Verify no illogical dates (`DeliveryDate < OrderDate`).
     - Check `data_import.log` for import issues.
     ```
