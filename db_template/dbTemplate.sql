DROP TABLE 28_forecast;
DROP TABLE 3_forecast;
DROP TABLE 1_forecast;
DROP TABLE nowCast;

CREATE TABLE 28_forecast(
	date_forecasted DATE NOT NULL,
	when_was_it_forecasted DATE NOT NULL,
	kp_value int NOT NULL,
	PRIMARY KEY (when_was_it_forecasted)	
);

CREATE TABLE 3_forecast(
	date_forecasted DATETIME NOT NULL,
	when_was_it_forecasted DATETIME NOT NULL,
	kp_value int NOT NULL,
	PRIMARY KEY (when_was_it_forecasted)
);

CREATE TABLE 1_forecast(
	date_forecasted DATETIME NOT NULL,
	when_was_it_forecasted DATETIME NOT NULL,
	kp_value int NOT NULL,
	PRIMARY KEY (when_was_it_forecasted)
);

CREATE TABLE nowCast(
	date_forecasted DATETIME NOT NULL,
	when_was_it_forecasted DATETIME NOT NULL,
	kp_value int NOT NULL,
	PRIMARY KEY (when_was_it_forecasted)
);