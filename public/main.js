const canvas = document.getElementById('drawing-board');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth * 0.8;
canvas.height = window.innerHeight * 0.7;

// WebSocket connection
const ws = new WebSocket(`ws://${window.location.hostname}:8765`);

ws.onopen = () => {
    console.log('Connected to the WebSocket server');
};

ws.onmessage = (event) => {
    // The message from the server is a string, so we need to parse it back into an object
    const data = JSON.parse(event.data);
    drawCircle(data.x, data.y, data.color, data.radius);
};

function drawCircle(x, y, color, radius) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2, false);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const color = getRandomColor();
    const radius = 20; // Circle radius

    // Draw the circle locally
    drawCircle(x, y, color, radius);

    // Send the circle data to the server
    const data = { x, y, color, radius };
    ws.send(JSON.stringify(data));
});
