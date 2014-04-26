//Window Resize Function
function resize_function(event)
{
	var size=document.body.clientWidth;

	if(!use_fallback)
		renderer.setSize(size,size);
	else
		document.getElementById("canvas").width=document.getElementById("canvas").height=size;

	if(parent.document.getElementById("simulation"))
		parent.document.getElementById("simulation").height=String(size);
}
