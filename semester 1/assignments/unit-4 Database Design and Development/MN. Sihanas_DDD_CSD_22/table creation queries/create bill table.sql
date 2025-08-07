CREATE TABLE Bill (
    BillID VARCHAR(10) PRIMARY KEY,
    ServiceID VARCHAR(10),
    ReservationID VARCHAR(10),
    TotalAmount DECIMAL(10, 2),
    DeductedAmount DECIMAL(10, 2),
    FinalAmount DECIMAL(10, 2),
    FOREIGN KEY (ServiceID) REFERENCES AdditionalServices(ServiceID),
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
