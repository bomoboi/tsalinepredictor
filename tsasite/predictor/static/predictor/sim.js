const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const cw = canvas.width;
const ch = canvas.height;

const lanes = [];
const laneWidth = 20;
const laneSpacing = 30;

const dotRadius = 5;
const moveSpeed = 2;
const totalDots = 100;

const agents = JSON.parse(document.getElementById('agents').textContent);
const ap = JSON.parse(document.getElementById('ap').textContent);

const newFactor = (Math.random()) + 1;
const wt_handle = document.getElementById('waitTime');
const wt = ((agents * newFactor)+ 5).toFixed(2);

let numLanes = 0;
let simRunning = false;
let dotsPerLane = 0;


document.addEventListener('DOMContentLoaded', function() {
  wt_handle.innerText = parseFloat(wt);
});

document.getElementById('addLane').addEventListener('click', () => {
  if (numLanes < 5) {
    const x = numLanes * (laneWidth + laneSpacing) + 40;
    lanes.push({x, dotsProcessed: 0});
    numLanes++;
    currWt = parseFloat(wt_handle.innerText);
    newWt = ((((5-numLanes)/5) + 0.1) * currWt);
    wt_handle.innerText = newWt.toFixed(2);
    calcDotsPerLane();
    drawLane(x);
  }
});

document.getElementById('removeLane').addEventListener('click', () => {
  if (numLanes > 0) {
    numLanes--;
    lanes.pop();
    stopSimulation();
    calcDotsPerLane();
    ctx.clearRect(0,0, canvas.width, canvas.height);
    lanes.forEach(lane => drawLane(lane.x));
    startSimulation();
  }
});

document.getElementById('toggleSim').addEventListener('click', function() {
  if (!simRunning) {
    this.innerText = "Stop Simulation";
    simRunning = true;
    startSimulation();
  } else {
    this.innerText = "Start Simulation";
    simRunning = false;
    stopSimulation();
  }
});

function drawLane(x) {
  ctx.beginPath();
  ctx.moveTo(x, 20);
  ctx.lineTo(x, ch-20);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x + laneWidth, 20);
  ctx.lineTo(x + laneWidth, ch-20);
  ctx.stroke();
}

function calcDotsPerLane() {
  dotsPerLane = Math.ceil(totalDots / numLanes);
}

function startSimulation() {
  lanes.forEach((lane, index) => {
    processLane(lane, index);
  });
}

function stopSimulation() {
  simRunning = false;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  lanes.forEach(lane => {
    lane.dotsProcessed = 0;
    drawLane(lane.x);
  });
}

function processLane(lane, index) {
  if (lane.dotsProcessed < dotsPerLane) {
    const dot = { x: (lane.x + laneWidth/2), y: 180 };
    drawDot(dot.x, (dot.y));
    moveDot(dot, lane, index)
  }
}

function moveDot(dot, lane, index) {
  if (!simRunning || lane.dotsProcessed >= dotsPerLane) {
    return;
  }

  ctx.clearRect( (dot.x - dotRadius - 1),
                 (dot.y - dotRadius - 1),
                 (dotRadius * 2 + 2),
                 (dotRadius * 2 + 2));

  let rand_step = ((Math.random() * 2.5))
  console.log(rand_step)
  dot.y -= (moveSpeed + rand_step);
  if (dot.y <= 20) {
    lane.dotsProcessed++;
    processLane(lane, index);
  } else {
    drawDot(dot.x, dot.y);
    setTimeout(() => moveDot(dot, lane, index), 20);
  }
}

function drawDot(x, y) {
  ctx.fillStyle = 'blue';
  ctx.beginPath();
  ctx.arc(x, y, dotRadius, 0, Math.PI *2, true);
  ctx.fill();
}
