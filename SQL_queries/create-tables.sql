CREATE TABLE HotelChain(
	chainName varchar(50),
	centralOfficeAddress(100),
	numHotels int,
	email varchar(50),
	phoneNumber varchar(15),
	PRIMARY KEY(chainName)
);

CREATE TABLE Hotels(
	locationName varchar(50),
	starRating int,
	numRooms int,
	street varchar(50),
	city varchar(50),
	province varchar(20),
	zip varchar(10),
	email varchar(50),
	phoneNumber varchar(15),
	managerSSN int,
	chainName varchar(50),
	PRIMARY KEY(locationName),
	FOREIGN KEY (chainName) REFERENCES HotelChain(chainName)
);

CREATE TABLE Customer(
	SSN int,
	first_name varchar(50),
	last_name varchar(50),
	street varchar(50),
	city varchar(50),
	province varchar(20),
	zip varchar(10),
	dateRegistered DATE,
	locationName varchar(50),
	PRIMARY KEY(SSN),
	FOREIGN KEY (locationName) REFERENCES Hotels(locationName)
);


CREATE TABLE Employee(
	SSN int,
	first_name varchar(50),
	last_name varchar(50),
	street varchar(50),
	city varchar(50),
	province varchar(20),
	zip varchar(10),
	positions varchar(50),
	PRIMARY KEY(SSN)
);