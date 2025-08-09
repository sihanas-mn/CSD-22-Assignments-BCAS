SELECT * FROM Reservation
WHERE PaymentStatus IS NULL OR PaymentStatus = '';
