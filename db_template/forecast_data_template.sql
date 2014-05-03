drop table if exists now;
drop table if exists h1;
drop table if exists d3;
drop table if exists d28;
drop table if exists cr;
drop table if exists carrington_event_lookup;

create table now
(
	id integer auto_increment not null,
	predicted_time datetime not null,
	download_time datetime not null,
	kp float not null,
	primary key (id)
);

create table h1
(
	id integer auto_increment not null,
	predicted_time datetime not null,
	download_time datetime not null,
	kp float not null,
	primary key (id)

);

create table d3
(
	id integer auto_increment not null,
	predicted_time datetime not null,
	download_time datetime not null,
	kp float not null,
	primary key (id)

);

create table d28
(
	id integer auto_increment not null,
	predicted_time datetime not null,
	download_time datetime not null,
	kp float not null,
	primary key (id)

);

create table cr
(
	rotation_index integer not null,
	year integer not null,
	month integer not null,
	day float not null,
	primary key (rotation_index)
);

create table Carrington_event_lookup
(
	id integer auto_increment not null,
	predicted_date datetime not null,
	fixed_date datetime not null,
	carrington_rotation integer not null,
	kp_index float not null,
	forecast_type enum('now', 'h1', 'd3', 'd28')
);
