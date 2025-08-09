CREATE TABLE GuestContacts (
    GuestID VARCHAR(10),
    ContactNo VARCHAR(15),
    PRIMARY KEY (GuestID, ContactNo),
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID)
);
