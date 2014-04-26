//Update Kp Function (Gets JSON object containing kp data.)
function update_kp()
{
	if(forecast=="now")
		update_nowcast();

	if(forecast=="h1")
		update_h1cast();
}

function update_nowcast()
{
	var time=get_time(-9);
	time.minute=Math.floor(time.minute/15)*15;

	var request_obj={};
	request_obj.forecast=forecast;
	request_obj.predicted_time={year:time.year,month:time.month,day:time.day,
		hour:time.hour,minute:time.minute};

	var url="http://aurora.cs.uaf.edu/cgi-bin/kp_cgi.py?r="+JSON.stringify(request_obj);

	var xmlhttp=new XMLHttpRequest();
	xmlhttp.open("GET",url,true);

	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4&&xmlhttp.status==200)
		{
			try
			{
				var obj=JSON.parse(xmlhttp.responseText);

				if(obj.values.length>0)
				{
					kp.x=parseInt(obj.values[obj.values.length-1].kp);

					if(use_fallback)
						aurora_render_fallback();
				}
			}
			catch(e)
			{}
		}
	}

	xmlhttp.send();
}

function update_h1cast()
{
	var time=get_time(-9);
	time.hour+=1;

	var request_obj={};
	request_obj.forecast=forecast;
	request_obj.predicted_time={year:time.year,month:time.month,day:time.day,
		hour:time.hour,minute:-1};

	var url="http://aurora.cs.uaf.edu/cgi-bin/kp_cgi.py?r="+JSON.stringify(request_obj);

	var xmlhttp=new XMLHttpRequest();
	xmlhttp.open("GET",url,true);

	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4&&xmlhttp.status==200)
		{
			try
			{
				var obj=JSON.parse(xmlhttp.responseText);

				if(obj.values.length>0)
				{
					kp.x=parseInt(obj.values[obj.values.length-1].kp);

					if(use_fallback)
						aurora_render_fallback();
				}
			}
			catch(e)
			{}
		}
	}

	xmlhttp.send();
}
