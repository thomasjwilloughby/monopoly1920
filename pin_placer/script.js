function preload() {
	img = loadImage('./board.png');
}

function setup() {
	canvas_elem = document.getElementById("canvas");
	canvas_elem.addEventListener("contextmenu", e => e.preventDefault());
	createCanvas(800, 800, P2D, canvas_elem);
	frameRate(75);

	zoom = 1.0;
	view_x = 0;
	view_y = 0;

	imageMode(CENTER);
}

function screenToWorld(pos) {
	let screen_x = pos.x;
	let screen_y = pos.y;

	let world_x = (screen_x - width/2 - view_x*zoom) / 8 / zoom;
	let world_y = (screen_y - width/2 - view_y*zoom) / 8 / zoom;
	return createVector(world_x, world_y);
}

function clamp_view() {
	let scale_size = 400 + 400/zoom;
	let off = 50;

	if (view_x < (-scale_size+off)) {
		view_x = (-scale_size)+off;
	} else if (view_x > scale_size-off) {
		view_x = scale_size-off;
	}
	if (view_y < -scale_size+off) {
		view_y = -scale_size+off;
	} else if (view_y > scale_size-off) {
		view_y = scale_size-off;
	}
}

function draw() {
	clear();
	translate(width/2, height/2);

	clamp_view();

	translate(view_x * zoom, view_y * zoom);
	scale(zoom, zoom);
	image(img, 0, 0);

	smooth();
	scale(img.width/100, img.height/100);

	let m_pos= screenToWorld({x: mouseX, y: mouseY});
	let mx = m_pos.x;
	let my = m_pos.y;
	// console.log(mx, my);
	strokeWeight(0.25/zoom);
	circle(mx, my, 5/zoom);

}

function mouseWheel(event) {
	if (event.delta > 0) {
		zoom *= 0.5;
	} else {
		zoom *= 2;
	}
	if (zoom < 1) {
		zoom = 1;
	}
	console.log(zoom);
}

function mouseDragged(event) {
	// console.log(event);
	if (event.buttons == 2) {
		// console.log("Right Click");
		delta_x = event.movementX / zoom;
		delta_y = event.movementY / zoom;
		view_x += delta_x;
		view_y += delta_y;
		console.log(view_x, view_y);
	}
}

function keyPressed(event) {
	if (event.key === "r" && event.type === "keydown") {
		zoom = 1;
		view_x = 0;
		view_y = 0;
	}
}
