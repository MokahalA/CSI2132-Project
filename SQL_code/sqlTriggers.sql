/* Trigger 1 */
CREATE TRIGGER updateRoomsAvailable AFTER INSERT ON Bookings 
BEGIN 
  UPDATE Rooms SET status = 'Booked' WHERE roomID = NEW.roomID; 
END; 


/* Trigger 2*/
CREATE TRIGGER updateBookedRooms AFTER DELETE ON Bookings 
BEGIN 
  UPDATE Rooms SET status = 'Available' WHERE roomID = OLD.roomID; 
END; 