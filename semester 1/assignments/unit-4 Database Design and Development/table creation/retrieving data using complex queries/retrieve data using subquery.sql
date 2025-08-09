SELECT Name
FROM Guest
WHERE GuestID IN (
    SELECT GuestID
    FROM Reservation res
    JOIN Room r ON res.RoomID = r.RoomID
    JOIN RoomDetail rd ON r.Type = rd.Type
    WHERE rd.Charge > 2000
);
