drop table if exists now;
drop table if exists h1;
drop table if exists d3;
drop table if exists d28;

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
