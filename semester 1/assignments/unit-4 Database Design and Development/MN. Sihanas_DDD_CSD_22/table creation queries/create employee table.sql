CREATE TABLE Employee (
    EmployeeID VARCHAR(10) PRIMARY KEY,
    RoomID VARCHAR(10),
    Name VARCHAR(50),
    Role VARCHAR(30),
    AssignedRoom VARCHAR(10),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);
