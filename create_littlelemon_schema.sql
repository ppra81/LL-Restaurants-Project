-- Create database
CREATE DATABASE IF NOT EXISTS LittleLemon;
USE LittleLemon;

-- Customers table
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100),
    City VARCHAR(100),
    Country VARCHAR(100),
    PostalCode VARCHAR(20),
    CountryCode VARCHAR(10)
);

-- Cuisines table
CREATE TABLE IF NOT EXISTS Cuisines (
    CuisineID INT AUTO_INCREMENT PRIMARY KEY,
    CuisineName VARCHAR(50) UNIQUE
);

-- Courses table
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseName VARCHAR(100) UNIQUE,
    CuisineID INT,
    FOREIGN KEY (CuisineID) REFERENCES Cuisines(CuisineID)
);

-- Starters table
CREATE TABLE IF NOT EXISTS Starters (
    StarterID INT AUTO_INCREMENT PRIMARY KEY,
    StarterName VARCHAR(100) UNIQUE
);

-- Desserts table
CREATE TABLE IF NOT EXISTS Desserts (
    DessertID INT AUTO_INCREMENT PRIMARY KEY,
    DessertName VARCHAR(100) UNIQUE
);

-- Drinks table
CREATE TABLE IF NOT EXISTS Drinks (
    DrinkID INT AUTO_INCREMENT PRIMARY KEY,
    DrinkName VARCHAR(100) UNIQUE
);

-- Sides table
CREATE TABLE IF NOT EXISTS Sides (
    SideID INT AUTO_INCREMENT PRIMARY KEY,
    SideName VARCHAR(100) UNIQUE
);

-- Orders table
CREATE TABLE IF NOT EXISTS Orders (
    OrderID VARCHAR(20) PRIMARY KEY,
    OrderDate DATE,
    DeliveryDate DATE,
    CustomerID VARCHAR(20),
    CourseID INT,
    StarterID INT,
    DessertID INT,
    DrinkID INT,
    SideID INT,
    Quantity INT,
    Cost DECIMAL(10,2),
    Sales DECIMAL(10,2),
    Discount DECIMAL(10,2),
    DeliveryCost DECIMAL(10,2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (StarterID) REFERENCES Starters(StarterID),
    FOREIGN KEY (DessertID) REFERENCES Desserts(DessertID),
    FOREIGN KEY (DrinkID) REFERENCES Drinks(DrinkID),
    FOREIGN KEY (SideID) REFERENCES Sides(SideID)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS Bookings (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID VARCHAR(20),
    BookingDate DATE,
    TableNumber INT,
    NumberOfGuests INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);