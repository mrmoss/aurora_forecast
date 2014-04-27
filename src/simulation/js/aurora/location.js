//Setup Locations Function
function setup_locations()
{
	//Update Location Options
	update_location_options();

	//Update Live Location
	set_location();

	//Get Current Location
	if(!use_fallback)
		navigator.geolocation.getCurrentPosition(get_current_location);
}

//Get Current Location Callback
function get_current_location(location)
{
	//Get Current Location
	var current_location={name:"My Location",latitude:location.coords.latitude,
		longitude:location.coords.longitude};

	//Insert Into Locations Array
	locations.splice(0,0,current_location);

	//Update Location Options
	update_location_options();

	//Get Location Select
	var location_select=document.getElementById("locations");

	//Auto Set Location
	if(location_select.length>0)
	{
		location_select.selectedIndex=0;
		set_location();
	}
}

//Create Locations
var locations=new Array();
locations.push({name:"Fairbanks, AK",latitude:64.8436,longitude:-147.7231});
locations.push({name:"Adelaide",latitude:-34.9333300,longitude:138.6});

//2D Fallback Locations
var fallback_locations=new Array();
var fallback_locations_index=0;
fallback_locations.push({name:"Alaska",latitude:64.8436,longitude:-147.7231,zoom:0.84});
fallback_locations.push({name:"United States",latitude:37.28,longitude:-100.61,zoom:1.06});
fallback_locations.push({name:"Europe",latitude:50.41,longitude:10.03,zoom:1.06});
fallback_locations.push({name:"North Polar",latitude:65.41,longitude:-66.975,zoom:1.42});
fallback_locations.push({name:"South Polar",latitude:-83.02,longitude:108.81,zoom:1.3});

//Update Location Options Function
function update_location_options()
{
	//Get Location Select
	var location_select=document.getElementById("locations");

	//Clear Out Old Options
	location_select.options.length=0;

	//Add Locations
	if(!use_fallback)
	{
		for(var ii=0;ii<locations.length;++ii)
			location_select.options[ii]=new Option(locations[ii].name);
	}
	else
	{
		for(var ii=0;ii<fallback_locations.length;++ii)
			location_select.options[ii]=new Option(fallback_locations[ii].name);

	}
}

//Set Location
function set_location()
{
	//Get Location Select
	var location_select=document.getElementById("locations");

	//Simulation
	if(!use_fallback)
	{
		//Set "To" Location
		view_latitude_to=locations[location_select.selectedIndex].latitude;
		view_longitude_to=locations[location_select.selectedIndex].longitude;

		//Limit Longitude Wrap Around
		while(view_longitude>180)
			view_longitude-=360;
		while(view_longitude<-180)
			view_longitude+=360;

		//Set Marker Location
		universe.marker.latitude=view_latitude_to;
		universe.marker.longitude=view_longitude_to;
	}

	//2D Fallback
	else
	{
		aurora_render_fallback();
	}
}
