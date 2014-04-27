//Globals
var kp=new THREE.Vector2(-1.0,0.0);
var zip;

//Record 2D Images Function
function record_2d_images()
{
	//Create New Zip File
	zip=new JSZip();

	//Download North Pole Images
	universe.marker.visible=false;
	fallback_locations_index=0;
	kp.x=10;
	setTimeout(render_2d_images,1000);
}

//Render 2D Images
function render_2d_images()
{
	//Shoot Kp 0-9
	if(kp.x<10)
	{
		//Render Scene
		renderer.render();

		//Render Scene
		var data=renderer.domElement.toDataURL();

		//Add File to Zip
		zip.file(fallback_locations[fallback_locations_index].name+" "+
			kp.x+".png",data.substr(data.indexOf(',')+1),{base64:true});

		//Increase Kp
		kp.x=kp.x+1;

		//Increase Location Index
		if(kp.x>=10)
			fallback_locations_index=fallback_locations_index+1;

		//Give Some Time to Download
		setTimeout(render_2d_images,1000);
	}

	//Change Location
	else if(fallback_locations_index<fallback_locations.length)
	{
		var ele=fallback_locations[fallback_locations_index];
		view_latitude=view_latitude_to=ele.latitude;
		view_longitude=view_longitude_to=ele.longitude;
		zoom=ele.zoom;
		kp.x=0;
		setTimeout(render_2d_images,1000);
	}

	//Download Zip
	else
	{
		window.open(window.URL.createObjectURL(zip.generate({type:"blob"})));
		universe.marker.visible=true;
	}
}
