drop view if exists VW_RoomCapacity;

/* SQL View 1 creation code */

CREATE VIEW VW_RoomCapacity AS 
SELECT 
    Hotels.locationName, 
    Rooms.roomID,
    Rooms.roomCapacity
FROM Hotels 
JOIN Rooms ON Hotels.hotelID = Rooms.hotelID;