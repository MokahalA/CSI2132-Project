/* Index 1 */
CREATE INDEX i_hotelID ON Rooms(hotelID); 
 
/* Index 2 */
CREATE INDEX i_employeeInfo ON Employee(SSN); 
 
/* Index 3 */
CREATE INDEX i_capacity ON Rooms(hotelID, roomCapacity); 