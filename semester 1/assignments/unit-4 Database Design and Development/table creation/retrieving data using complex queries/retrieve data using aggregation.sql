SELECT GuestID, COUNT(*) AS TotalComplaints
FROM Complaints
GROUP BY GuestID;
