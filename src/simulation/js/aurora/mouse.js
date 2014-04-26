//Globals
var mouse_down=false;
var mouse_down_x=0.0;
var mouse_down_y=0.0;

//Mouse Leave Window Callback
function mouse_leave_window_callback(event)
{
	event=event?event:window.event;

	var from=event.relatedTarget||event.toElement;

	if(!from||from.nodeName=="HTML")
		mouse_down=false;
}

//Mouse Wheel Initialize Function
function mouse_scroll_init(div)
{
	var elem=document.getElementById(div);

	if(elem.addEventListener)
	{
		elem.addEventListener("mousewheel",mouse_wheel_callback,false);
		elem.addEventListener("DOMMouseScroll",mouse_wheel_callback,false);
	}
	else
	{
		if(elem.attachEvent)
			elem.attachEvent("onmousewheel",MouseScroll);
	}
}

//Mouse Wheel Callback
function mouse_wheel_callback(event)
{
	var roll=0;

	if('wheelDelta' in event)
		roll=event.wheelDelta;
	else
		roll=-40*event.detail;

	var canvas=document.getElementById("canvas");

	if(event.target!=canvas||mouse_down)
	{
		zoom+=roll*0.001;
		event.preventDefault();
	}
}

//Mouse Down Callback
function mouse_down_callback(event)
{
	var canvas=document.getElementById("canvas");

	if(event.target!=canvas)
	{
		mouse_down=true;
		view_latitude_down=view_latitude;
		view_longitude_down=view_longitude;
		mouse_down_x=event.pageX-canvas.offsetLeft;
		mouse_down_y=event.pageY-canvas.offsetTop;
	}
}

//Mouse Up Callback
function mouse_up_callback(event)
{
	mouse_down=false;
}

//Mouse Move Callback
function mouse_move_callback(event)
{
	var canvas=document.getElementById("canvas");

	if(mouse_down)
	{
		var mouse_x=event.pageX-canvas.offsetLeft;
		var mouse_y=event.pageY-canvas.offsetTop;

		view_latitude_to=view_latitude_down+mouse_y-mouse_down_y;
		view_longitude_to=view_longitude_down+mouse_down_x-mouse_x;
	}
}

//Mouse Over Callback
function mouse_over_callback(event)
{
	if(event.target==canvas)
		mouse_down=false;
}
