//Globals
var touches=0;

//Touch Leave Window Callback
function touch_leave_window_callback(event)
{
	event=event?event:window.event;

	var from=event.relatedTarget||event.toElement;

	if(!from||from.nodeName=="HTML")
		mouse_down=false;
}

//Touch Down Callback
function touch_down_callback(event)
{
	touches=event.touches.length;

	var canvas=document.getElementById("canvas");

	if(event.target!=canvas)
	{
		mouse_down=true;

		view_latitude_down=view_latitude;
		view_longitude_down=view_longitude;

		mouse_down_x=event.changedTouches[0].pageX-canvas.offsetLeft;
		mouse_down_y=event.changedTouches[0].pageY-canvas.offsetTop;

		event.preventDefault();
	}
}

//Touch Up Callback
function touch_up_callback(event)
{
	mouse_down=false;
}

//Touch Move Callback
function touch_move_callback(event)
{
	touches=event.touches.length;

	var canvas=document.getElementById("canvas");

	if(mouse_down)
	{
		var mouse_x=event.changedTouches[0].pageX-canvas.offsetLeft;
		var mouse_y=event.changedTouches[0].pageY-canvas.offsetTop;

		view_latitude_to=view_latitude_down+mouse_y-mouse_down_y;
		view_longitude_to=view_longitude_down+mouse_down_x-mouse_x;

		event.preventDefault();
	}
}

//Touch Over Callback
function touch_over_callback(event)
{
	touches=event.touches.length;

	if(event.target==canvas)
		mouse_down=false;
}
