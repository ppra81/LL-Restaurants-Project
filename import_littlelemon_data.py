import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import logging
import os

# Configure logging
log_file = 'data_import.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database configuration
config = {
    'user': 'your_username',  # Replace with your MySQL username
    'password': 'your_password',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'LittleLemon',
    'buffered': True
}

def validate_date(date_value, field_name, index):
    """Validate and convert date value to date object."""
    try:
        if pd.isna(date_value):
            return None
        if isinstance(date_value, pd.Timestamp):
            return date_value.date()
        if isinstance(date_value, str):
            return datetime.strptime(date_value, '%d-%m-%Y').date()
        logger.error(f"Invalid {field_name} type at index {index}: {type(date_value)}")
        return None
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid {field_name} at index {index}: {date_value} - {e}")
        return None

def main():
    connection = None
    cursor = None
    try:
        # Connect to database
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            logger.info("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)

            # Read and preprocess CSV
            logger.info("Loading LittleLemon_data.csv")
            df = pd.read_csv('LittleLemon_data.csv')
            logger.info(f"Loaded dataset with {len(df)} rows")

            # Print column names
            logger.info(f"CSV Columns: {df.columns.tolist()}")

            # Remove duplicate Order IDs (keep first occurrence)
            initial_rows = len(df)
            df = df.drop_duplicates(subset=['Order ID'], keep='first')
            logger.info(f"Removed {initial_rows - len(df)} duplicate Order ID rows. Remaining rows: {len(df)}")

            # Check for remaining duplicates
            duplicate_counts = df['Order ID'].value_counts()
            if (duplicate_counts > 1).any():
                logger.warning(f"Found {len(duplicate_counts[duplicate_counts > 1])} duplicate Order IDs")
                logger.warning(f"Sample duplicates:\n{duplicate_counts[duplicate_counts > 1].head().to_string()}")
            logger.info(f"Total unique Order IDs: {df['Order ID'].nunique()}")

            # Fix illogical dates by swapping
            df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
            df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], format='%d-%m-%Y', errors='coerce')
            mask = df['Delivery Date'] < df['Order Date']
            swapped_rows = mask.sum()
            df.loc[mask, ['Order Date', 'Delivery Date']] = df.loc[mask, ['Delivery Date', 'Order Date']].values
            logger.info(f"Swapped Order Date and Delivery Date for {swapped_rows} rows with illogical dates")

            # Replace NaN with None
            df = df.where(pd.notnull(df), None)

            # Initialize counters
            inserted_rows = {'Customers': 0, 'Cuisines': 0, 'Courses': 0, 'Starters': 0, 
                            'Desserts': 0, 'Drinks': 0, 'Sides': 0, 'Orders': 0}
            skipped_rows = 0

            # Truncate Orders table to ensure clean import
            logger.info("Truncating Orders table")
            cursor.execute("TRUNCATE TABLE Orders")
            connection.commit()

            # Insert Customers
            customers_df = df[['Customer ID', 'Customer Name', 'City', 'Country', 'Postal Code', 'Country Code']].drop_duplicates()
            for index, row in customers_df.iterrows():
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO Customers (CustomerID, Name, City, Country, PostalCode, CountryCode)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (row['Customer ID'], row['Customer Name'], row['City'], row['Country'], row['Postal Code'], row['Country Code']))
                    if cursor.rowcount > 0:
                        inserted_rows['Customers'] += 1
                except Error as e:
                    logger.error(f"Error inserting customer at index {index}: {e}")
                    logger.debug(f"Customer data: {row.to_dict()}")

            # Insert Cuisines
            unique_cuisines = df['Cuisine Name'].unique()
            for cuisine in unique_cuisines:
                if cuisine is not None:
                    try:
                        cursor.execute("INSERT IGNORE INTO Cuisines (CuisineName) VALUES (%s)", (cuisine,))
                        if cursor.rowcount > 0:
                            inserted_rows['Cuisines'] += 1
                    except Error as e:
                        logger.error(f"Error inserting cuisine {cuisine}: {e}")

            # Insert Courses
            unique_courses = df[['Course Name', 'Cuisine Name']].drop_duplicates()
            for index, row in unique_courses.iterrows():
                if row['Course Name'] is not None and row['Cuisine Name'] is not None:
                    try:
                        cursor.execute("SELECT CuisineID FROM Cuisines WHERE CuisineName = %s", (row['Cuisine Name'],))
                        cuisine_id = cursor.fetchone()
                        if cuisine_id:
                            cursor.execute("INSERT IGNORE INTO Courses (CourseName, CuisineID) VALUES (%s, %s)", 
                                          (row['Course Name'], cuisine_id[0]))
                            if cursor.rowcount > 0:
                                inserted_rows['Courses'] += 1
                        else:
                            logger.warning(f"Cuisine {row['Cuisine Name']} not found for course {row['Course Name']} at index {index}")
                    except Error as e:
                        logger.error(f"Error inserting course at index {index}: {e}")
                        logger.debug(f"Course data: {row.to_dict()}")

            # Insert Starters
            unique_starters = df['Starter Name'].unique()
            for starter in unique_starters:
                if starter is not None:
                    try:
                        cursor.execute("INSERT IGNORE INTO Starters (StarterName) VALUES (%s)", (starter,))
                        if cursor.rowcount > 0:
                            inserted_rows['Starters'] += 1
                    except Error as e:
                        logger.error(f"Error inserting starter {starter}: {e}")

            # Insert Desserts
            unique_desserts = df['Desert Name'].unique()
            for dessert in unique_desserts:
                if dessert is not None:
                    try:
                        cursor.execute("INSERT IGNORE INTO Desserts (DessertName) VALUES (%s)", (dessert,))
                        if cursor.rowcount > 0:
                            inserted_rows['Desserts'] += 1
                    except Error as e:
                        logger.error(f"Error inserting dessert {dessert}: {e}")

            # Insert Drinks
            unique_drinks = df['Drink'].unique()
            for drink in unique_drinks:
                if drink is not None:
                    try:
                        cursor.execute("INSERT IGNORE INTO Drinks (DrinkName) VALUES (%s)", (drink,))
                        if cursor.rowcount > 0:
                            inserted_rows['Drinks'] += 1
                    except Error as e:
                        logger.error(f"Error inserting drink {drink}: {e}")

            # Insert Sides
            unique_sides = df['Sides'].unique()
            for side in unique_sides:
                if side is not None:
                    try:
                        cursor.execute("INSERT IGNORE INTO Sides (SideName) VALUES (%s)", (side,))
                        if cursor.rowcount > 0:
                            inserted_rows['Sides'] += 1
                    except Error as e:
                        logger.error(f"Error inserting side {side}: {e}")

            # Insert Orders
            for index, row in df.iterrows():
                try:
                    # Validate and convert dates
                    order_date = validate_date(row['Order Date'], 'Order Date', index)
                    delivery_date = validate_date(row['Delivery Date'], 'Delivery Date', index)

                    # Skip if dates are invalid
                    if order_date is None or delivery_date is None:
                        logger.warning(f"Skipping row at index {index} due to invalid dates")
                        skipped_rows += 1
                        continue

                    # Fetch IDs for menu items
                    course_id = None
                    if row['Course Name']:
                        cursor.execute("SELECT CourseID FROM Courses WHERE CourseName = %s", (row['Course Name'],))
                        result = cursor.fetchone()
                        course_id = result[0] if result else None
                        cursor.fetchall()
                        if not course_id:
                            logger.warning(f"Course {row['Course Name']} not found at index {index}")

                    starter_id = None
                    if row['Starter Name']:
                        cursor.execute("SELECT StarterID FROM Starters WHERE StarterName = %s", (row['Starter Name'],))
                        result = cursor.fetchone()
                        starter_id = result[0] if result else None
                        cursor.fetchall()
                        if not starter_id:
                            logger.warning(f"Starter {row['Starter Name']} not found at index {index}")

                    dessert_id = None
                    if row['Desert Name']:
                        cursor.execute("SELECT DessertID FROM Desserts WHERE DessertName = %s", (row['Desert Name'],))
                        result = cursor.fetchone()
                        dessert_id = result[0] if result else None
                        cursor.fetchall()
                        if not dessert_id:
                            logger.warning(f"Dessert {row['Desert Name']} not found at index {index}")

                    drink_id = None
                    if row['Drink']:
                        cursor.execute("SELECT DrinkID FROM Drinks WHERE DrinkName = %s", (row['Drink'],))
                        result = cursor.fetchone()
                        drink_id = result[0] if result else None
                        cursor.fetchall()
                        if not drink_id:
                            logger.warning(f"Drink {row['Drink']} not found at index {index}")

                    side_id = None
                    if row['Sides']:
                        cursor.execute("SELECT SideID FROM Sides WHERE SideName = %s", (row['Sides'],))
                        result = cursor.fetchone()
                        side_id = result[0] if result else None
                        cursor.fetchall()
                        if not side_id:
                            logger.warning(f"Side {row['Sides']} not found at index {index}")

                    # Insert order
                    cursor.execute("""
                        INSERT INTO Orders (OrderID, OrderDate, DeliveryDate, CustomerID, CourseID, StarterID, DessertID, DrinkID, SideID, Quantity, Cost, Sales, Discount, DeliveryCost)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        row['Order ID'], order_date, delivery_date, row['Customer ID'], course_id, starter_id, dessert_id, 
                        drink_id, side_id, row['Quantity'], row[' Cost'], row['Sales'], row['Discount'], row['Delivery Cost']
                    ))
                    if cursor.rowcount > 0:
                        inserted_rows['Orders'] += 1

                except Error as e:
                    logger.error(f"Error inserting order at index {index}: {e}")
                    logger.debug(f"Order data: {row.to_dict()}")
                    skipped_rows += 1

            # Commit changes
            connection.commit()
            logger.info("Data imported successfully")
            logger.info(f"Inserted rows: {inserted_rows}")
            logger.info(f"Swapped {swapped_rows} rows due to illogical dates")
            logger.info(f"Skipped {skipped_rows} rows due to invalid data")

            # Verify inserted orders
            cursor.execute("SELECT COUNT(*) FROM Orders")
            order_count = cursor.fetchone()[0]
            logger.info(f"Total orders in database: {order_count}")

    except Error as e:
        logger.error(f"Database error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection closed")

if __name__ == "__main__":
    main()