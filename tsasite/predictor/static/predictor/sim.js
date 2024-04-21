document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  const lanes = [];
  const laneWidth = 20;
  const laneSpacing = 30;

  const dotRadius = 5;
  const moveSpeed = 7;
  const totalDots = 100;

  let numLanes = 0;
  let simRunning = false;
  let dotsPerLane;
})


document.getElementById('addLane').addEventListener('click', () => {
  if (numLanes < 10) {
    const x = numLanes * (laneWidth + laneSpacing) + 50;
    lanes.push({x, dotsProcessed: 0});
    numLanes++;
    dotsPerLane();
    drawLane(x);
  }
});

document.getElementById('removeLane').addEventListener('click', () => {
  if (numLanes > 0) {
    numLanes--;
    lanes.pop();
    dotsPerLane();
    ctx.clearRect(0,0, canvas.width, canvas.height);
    lanes.forEach(lane => drawLane(lane.x));
  }
});

document.getElementById('toggleSim').addEventListener('click', () => {
  if (!simRunning) {
    this.textContext = "Stop Simulation";
    simRunning = true;
    startSimulation();
  } else {
    this.textContext = "Start Simulation";
    simRunning = false;
    stopSimulation();
  }
});

function drawLane(x) {
  ctx.beginPath();
  ctx.moveTo(x, 20);
  ctx.lineTo(x, 180);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x + laneWidth, 20);
  ctx.moveTo(x + laneWidth, 180);
  ctx.stroke();
}

function dotsPerLane() {
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
    drawDot(dot.x, dot.y);
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
  dot.y -= moveSpeed;
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
