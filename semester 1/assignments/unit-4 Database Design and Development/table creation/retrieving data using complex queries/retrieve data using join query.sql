SELECT g.Name AS GuestName, r.RoomID, r.Type AS RoomType
FROM Guest g
JOIN Reservation res ON g.GuestID = res.GuestID
JOIN Room r ON res.RoomID = r.RoomID;
