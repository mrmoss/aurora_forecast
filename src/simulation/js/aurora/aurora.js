//Site Globals
var width= 300;
var height= 300;
var earth_radius=0.5;
var use_fallback=false;

//Three.js Globals
var renderer;
var scene;
var camera;
var universe;

//Simulation Globals
var view_latitude=0;
var view_longitude=0;
var view_latitude_to=0;
var view_longitude_to=0;
var view_latitude_down=0;
var view_longitude_down=0;
var zoom=2;
var zoom_min=0.7;
var zoom_max=3;
var zoom_down=zoom;
var scale_down=0;
var show_stars=false;
var show_sun=false;

//Setup Function (Happens Once)
function aurora_setup()
{
	//Get Forecast
	if(parent.forecast)
		forecast=parent.forecast;

	//Update Forecast
	setInterval(update_kp,1000);

	//Set Resize Callback
	if(parent.window)
		parent.window.addEventListener('resize',resize_function);

	//Detect WebGL
	if(!Detector.webgl)
	{
		use_fallback=true;
		//Detector.addGetWebGLMessage();
	}

	//Use WebGL
	if(!use_fallback)
	{
		//Get Canvas Div
		var canvas=document.getElementById("canvas");
		canvas.innerHTML="";

		//Enable Mobile Zooming
		Hammer(canvas).on
		(
			"pinch",
			function(e)
			{
				if(e.gesture.eventType==Hammer.EVENT_START)
				{
					zoom_down=zoom;
					scale_down=e.gesture.scale;
				}

				zoom=zoom_down+(scale_down-e.gesture.scale)*0.5;
				e.preventDefault();
			}
		);

		//Setup Input Callbacks
		mouse_scroll_init("canvas");
		canvas.addEventListener('mouseout',mouse_leave_window_callback,false);
		canvas.addEventListener('mousedown',mouse_down_callback,false);
		canvas.addEventListener('mouseup',mouse_up_callback,false);
		canvas.addEventListener('mousemove',mouse_move_callback,false);
		canvas.addEventListener('mouseover',mouse_over_callback,false);
		canvas.addEventListener('touchleave',touch_leave_window_callback,false);
		canvas.addEventListener('touchstart',touch_down_callback,false);
		canvas.addEventListener('touchend',touch_up_callback,false);
		canvas.addEventListener('touchmove',touch_move_callback,false);
		canvas.addEventListener('touchenter',touch_over_callback,false);

		//Create Renderer
		renderer=new THREE.WebGLRenderer({preserveDrawingBuffer:true});
		canvas.appendChild(renderer.domElement);

		//Create Scene
		scene=new THREE.Scene();

		//Create Camera
		camera=new THREE.PerspectiveCamera(45,width/height,0.01,1000);
		camera.position.x=0;
		camera.position.y=0;
		camera.position.z=5;

		//Create Universe
		universe=create_universe(scene,earth_radius,32);

		//Setup Locations
		setup_locations();

		//Go to Default Location
		if(locations.length>0)
		{
			view_latitude_to=locations[0].latitude;
			view_longitude_to=locations[0].longitude;
		}

		//Start Rendering
		aurora_render();
	}

	//Use Fallback
	else
	{
		//Setup Locations
		setup_locations();

		//Render Fallback
		aurora_render_fallback();
	}

	//Resize Simulation
	resize_function();
}

//Render Function (Happens Every Frame Update)
function aurora_render()
{
	//Limit Number of Touches
	if(touches>1&&mouse_down)
		mouse_down=false;

	//Limit Zoom
	if(zoom>zoom_max)
		zoom=zoom_max;
	if(zoom<zoom_min)
		zoom=zoom_min;

	//Limit Latitude
	if(view_latitude>=90)
		view_latitude=89.99;
	if(view_latitude<=-90)
		view_latitude=-89.99;
	if(view_latitude_to>=90)
		view_latitude_to=89.99;
	if(view_latitude_to<-90)
		view_latitude_to=-90;

	//Auto Move Location (P Controller)
	var move_speed=0.1;
	view_latitude+=(view_latitude_to-view_latitude)*move_speed;
	view_longitude+=(view_longitude_to-view_longitude)*move_speed;

	//Update Camera
	var look_at_x=Math.sin((90-view_latitude)/180*Math.PI)*Math.cos(Math.PI/2+
		(270-view_longitude)/180*Math.PI)*zoom;
	var look_at_y=Math.cos((90-view_latitude)/180*Math.PI)*zoom;
	var look_at_z=Math.sin((90-view_latitude)/180*Math.PI)*Math.sin(Math.PI/2+
		(270-view_longitude)/180*Math.PI)*zoom;
	camera.position.x=look_at_x;
	camera.position.y=look_at_y;
	camera.position.z=look_at_z;
	camera.lookAt(universe.planet.position);

	//Update Marker
	var marker_radius=earth_radius+universe.marker.radius/2.0;
	universe.marker.position.x=
		Math.sin((90-universe.marker.latitude)/180*Math.PI)*Math.cos(Math.PI/2+
		(270-universe.marker.longitude)/180*Math.PI)*marker_radius;
	universe.marker.position.y=
		Math.cos((90-universe.marker.latitude)/180*Math.PI)*marker_radius;
	universe.marker.position.z=
		Math.sin((90-universe.marker.latitude)/180*Math.PI)*Math.sin(Math.PI/2+
		(270-universe.marker.longitude)/180*Math.PI)*marker_radius;

	//Update North Pole Aurora
	universe.aurora_north.rotation.x=universe.planet.rotation.x-1.5;
	universe.aurora_north.rotation.y=universe.planet.rotation.y+0.04;
	universe.aurora_north.rotation.z=universe.planet.rotation.z+0.49

	//Update South Pole Aurora
	universe.aurora_south.rotation.x=universe.planet.rotation.x+1.8805985402277465;
	universe.aurora_south.rotation.y=universe.planet.rotation.y-0.11217274015818644;
	universe.aurora_south.rotation.z=universe.planet.rotation.z+2.8051980031399686;

	//Update Sun
	if(show_sun)
	{
		//Get Time
		var time_obj=get_time();
		var time_now=time_obj.hour*60*60+time_obj.minute*60+time_obj.second;
		var time_max=24*60*60;


		//Set Sun Position
		var sun_offset=60;
		universe.sun.longitude=sun_offset+time_now/time_max*360-180;
		universe.sun.latitude=0;

		//Limit Sun Position
		while(universe.sun.longitude>180)
			universe.sun.longitude-=360;
		while(universe.sun.longitude<-180)
			universe.sun.longitude+=360;

		//Set Sun Light
		var sun_radius=10;
		var sun_x=Math.sin((90-universe.sun.latitude)/180*Math.PI)*Math.cos(Math.PI/2+
			(270-universe.sun.longitude)/180*Math.PI)*sun_radius;
		var sun_y=Math.cos((90-universe.sun.latitude)/180*Math.PI)*sun_radius;
		var sun_z=Math.sin((90-universe.sun.latitude)/180*Math.PI)*Math.sin(Math.PI/2+
			(270-universe.sun.longitude)/180*Math.PI)*sun_radius;
		universe.sun.position.set(sun_x,sun_y,sun_z);
	}

	//Limit Kp
	if(kp.x>=0&&kp.x<=9)
	{
		view_kp(true);
		universe.aurora_north.visible=true;
		universe.aurora_south.visible=true;
	}
	else
	{
		view_kp(false);
		universe.aurora_north.visible=false;
		universe.aurora_south.visible=false;
	}

	//Render
	requestAnimationFrame(aurora_render);
	renderer.render(scene,camera);
}

//Render Fallback Function
function aurora_render_fallback()
{
	//Get Cavas Div
	var canvas=document.getElementById("canvas");

	//Limit Kp
	if(kp.x>9)
		kp.x=9;
	if(kp.x<0)
		kp.x=0;

	//View Kp
	view_kp(true);

	//Get Location Select
	var location_select=document.getElementById("locations");

	canvas.innerHTML="<img src='"+root+"images/fallback/"+
		location_select.options[location_select.selectedIndex].value+" "+
		Math.round(kp.x)+".png' width='100%' height='100%'/>";
}

//View Kp Function (Updates text in source file)
function view_kp(show)
{
	if(show)
	{
		var date=new Date();
		document.getElementById("view_date").textContent="Forecast for "+date.toDateString();
		document.getElementById("view_kp").textContent="Kp "+kp.x;
	}
}

//Create Universe Function (Creates Earth Scene)
function create_universe(scene,radius,segments)
{
	//Create Star Background
	var ret={};

	if(show_stars)
	{
		ret.stars=new THREE.Mesh
		(
			new THREE.SphereGeometry(90,segments,segments+1),
			new THREE.MeshBasicMaterial
			({
				map:  THREE.ImageUtils.loadTexture(root+"images/simulation/galaxy_starfield.png"),
				side: THREE.BackSide
			})
		);

		scene.add(ret.stars);
	}

	//Create Planet Earth
	ret.planet=new THREE.Mesh
	(
		new THREE.SphereGeometry(radius,segments,segments+1),
		new THREE.MeshPhongMaterial
		({
			map:         THREE.ImageUtils.loadTexture(root+"images/simulation/2_no_clouds_4k.png"),
			//bumpMap:     THREE.ImageUtils.loadTexture(root+"images/simulation/elev_bump_4k.png"),
			//bumpScale:   0.005,
			specularMap: THREE.ImageUtils.loadTexture(root+"images/simulation/water_4k.png"),
			specular:    new THREE.Color('grey')
		})
	);

	scene.add(ret.planet);

	//Create Marker
	var marker_radius=0.005;
	ret.marker=new THREE.Mesh
	(
		new THREE.SphereGeometry(marker_radius,segments,segments+1),
		new THREE.ShaderMaterial
		({
			vertexShader: document.getElementById('marker_vertex_shader').textContent,
			fragmentShader: document.getElementById('marker_fragment_shader').textContent
		})
	);

	ret.marker.radius=marker_radius;
	ret.marker.latitude=0;
	ret.marker.longitude=0;
	scene.add(ret.marker);

	//Create Northern Auroral Oval
	ret.aurora_north=new THREE.Mesh
	(
		new THREE.SphereGeometry
			(
				radius+0.003,segments,segments+1,
				0,Math.PI,0,Math.PI
			),
		new THREE.ShaderMaterial
		({
			transparent: true,
			uniforms:
			{
				kp:{type:"v2",value:kp}
			},
			vertexShader: document.getElementById('aurora_vertex_shader').textContent,
			fragmentShader: document.getElementById('aurora_fragment_shader').textContent
		})
	);

	ret.aurora_north.visible=false;
	scene.add(ret.aurora_north);

	//Create Southern Auroral Oval
	ret.aurora_south=new THREE.Mesh
	(
		new THREE.SphereGeometry
		(
			radius+0.003,segments,segments+1,
			0,Math.PI,0,Math.PI
		),
		new THREE.ShaderMaterial
		({
			transparent: true,
			uniforms:
			{
				kp:{type:"v2",value:kp}
			},
			vertexShader: document.getElementById('aurora_vertex_shader').textContent,
			fragmentShader: document.getElementById('aurora_fragment_shader').textContent
		})
	);

	ret.aurora_south.visible=false;
	scene.add(ret.aurora_south);

	//Create Ambient Light
	ret.ambient_light=new THREE.AmbientLight(0x444444);
	scene.add(ret.ambient_light);

	//Create Sun Light
	if(show_sun)
	{
		ret.sun=new THREE.DirectionalLight(0xffffff,1.5);
		ret.sun.position.set(0,0,0);
		ret.sun.latitude=0;
		ret.sun.longitude=0;
		scene.add(ret.sun);
	}

	//Create Ambient Light
	else
	{
		ret.light=new THREE.AmbientLight(0xaaaaaa,2);
		scene.add(ret.light);
	}

	//Return Scene
	return ret;
}
