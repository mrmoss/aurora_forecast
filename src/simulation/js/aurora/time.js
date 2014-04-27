//Get Time Function (Gives UTC by default.)
function get_time(offset)
{
	var date=new Date();

	if(offset)
		date.setHours(date.getHours()+offset);

	var ret={};
	ret.second=date.getUTCSeconds();
	ret.minute=date.getUTCMinutes();
	ret.hour=date.getUTCHours();
	ret.day=date.getUTCDate();
	ret.month=date.getMonth()+1;
	ret.year=date.getFullYear();

	return ret;
}

//Translates a JSON Date Object into a Javascript Date Object
function json_to_date(json)
{
	var date=new Date(parseInt(json.year),parseInt(json.month),parseInt(json.day),
		parseInt(json.hour),parseInt(json.minute),0,0);

	return date;
}
