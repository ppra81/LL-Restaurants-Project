-- GetMaxQuantity: Find the order with the highest quantity
DELIMITER //
CREATE PROCEDURE GetMaxQuantity()
BEGIN
    SELECT OrderID, Quantity
    FROM Orders
    WHERE Quantity = (SELECT MAX(Quantity) FROM Orders);
END //
DELIMITER ;

-- ManageBooking: Check if a table is available on a given date
DELIMITER //
CREATE PROCEDURE ManageBooking(IN booking_date DATE, IN table_number INT)
BEGIN
    SELECT BookingID, CustomerID, BookingDate, TableNumber, NumberOfGuests
    FROM Bookings
    WHERE BookingDate = booking_date AND TableNumber = table_number;
END //
DELIMITER ;

-- AddBooking: Add a new booking
DELIMITER //
CREATE PROCEDURE AddBooking(IN customer_id VARCHAR(20), IN booking_date DATE, IN table_number INT, IN number_of_guests INT)
BEGIN
    INSERT INTO Bookings (CustomerID, BookingDate, TableNumber, NumberOfGuests)
    VALUES (customer_id, booking_date, table_number, number_of_guests);
    SELECT 'Booking added successfully' AS Message;
END //
DELIMITER ;

-- UpdateBooking: Update an existing booking
DELIMITER //
CREATE PROCEDURE UpdateBooking(IN booking_id INT, IN booking_date DATE, IN table_number INT, IN number_of_guests INT)
BEGIN
    UPDATE Bookings
    SET BookingDate = booking_date, TableNumber = table_number, NumberOfGuests = number_of_guests
    WHERE BookingID = booking_id;
    SELECT 'Booking updated successfully' AS Message;
END //
DELIMITER ;

-- CancelBooking: Delete a booking
DELIMITER //
CREATE PROCEDURE CancelBooking(IN booking_id INT)
BEGIN
    DELETE FROM Bookings
    WHERE BookingID = booking_id;
    SELECT 'Booking cancelled successfully' AS Message;
END //
DELIMITER ;