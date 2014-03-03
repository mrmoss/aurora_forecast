drop table if exists now;
drop table if exists d1;
drop table if exists d3;
drop table if exists d28;

create table now
(
	predicted_time datetime not null,
	download_time datetime not null,
	kp int not null,
	primary key (predicted_time)
);

create table d1
(
	predicted_time datetime not null,
	download_time datetime not null,
	kp int not null,
	primary key (predicted_time)
);

create table d3
(
	predicted_time datetime not null,
	download_time datetime not null,
	kp int not null,
	primary key (predicted_time)
);

create table d28
(
	predicted_time date not null,
	download_time date not null,
	kp int not null,
	primary key (predicted_time)
);
