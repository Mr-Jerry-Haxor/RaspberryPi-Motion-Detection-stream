// let videoElement;
// let video;
// let poseNet;
// let pose;
// let skeleton;

// async function setup() {
//   createCanvas(640, 480);
//   videoElement = document.getElementById("remotevideo");
//   const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//   videoElement.srcObject = stream;
//   videoElement.play();

//   poseNet = ml5.poseNet(videoElement, modelLoaded);
//   poseNet.on('pose', gotPoses);

// }

// function gotPoses(poses) {
//   //console.log(poses); 
//   if (poses.length > 0) {
//     pose = poses[0].pose;
//     skeleton = poses[0].skeleton;
//   }
// }


// function modelLoaded() {
//   console.log('poseNet ready');
// }

// function draw() {
//   image(videoElement, 0, 0);

//   if (pose) {
//     let eyeR = pose.rightEye;
//     let eyeL = pose.leftEye;
//     let d = dist(eyeR.x, eyeR.y, eyeL.x, eyeL.y);
//     fill(255, 0, 0);
//     ellipse(pose.nose.x, pose.nose.y, d);
//     fill(0, 0, 255);
//     ellipse(pose.rightWrist.x, pose.rightWrist.y, 32);
//     ellipse(pose.leftWrist.x, pose.leftWrist.y, 32);
    
//     for (let i = 0; i < pose.keypoints.length; i++) {
//       let x = pose.keypoints[i].position.x;
//       let y = pose.keypoints[i].position.y;
//       fill(0,255,0);
//       ellipse(x,y,16,16);
//     }
    
//     for (let i = 0; i < skeleton.length; i++) {
//       let a = skeleton[i][0];
//       let b = skeleton[i][1];
//       strokeWeight(2);
//       stroke(255);
//       line(a.position.x, a.position.y,b.position.x,b.position.y);      
//     }
//   }
// }
videoElement = document.getElementById("remotevideo");
const stream = await navigator.mediaDevices.getUserMedia({ video: true });
videoElement.srcObject = stream;
videoElement.play();

const video = document.getElementById('remotevideo');

async function setupCamera() {
    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
        resolve(video);
        };
    });
}

async function loadPoseNet() {
    const net = await posenet.load();
    return net;
}

async function detectPoseInRealTime(video, net) {
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

document.body.appendChild(canvas);

canvas.width = video.videoWidth;
canvas.height = video.videoHeight;

async function poseDetectionFrame() {
    const pose = await net.estimateSinglePose(video, {
    flipHorizontal: false
    });

    drawPose(pose, ctx);
    requestAnimationFrame(poseDetectionFrame);
}

poseDetectionFrame();
}

function drawPose(pose, ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    drawKeypoints(pose.keypoints, ctx);
    drawSkeleton(pose.keypoints, ctx);
}

function drawKeypoints(keypoints, ctx) {
    keypoints.forEach(keypoint => {
        if (keypoint.score > 0.5) {
        const { y, x } = keypoint.position;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = 'red';
        ctx.fill();
        }
    });
}

function drawSkeleton(keypoints, ctx) {
const adjacentKeyPoints = posenet.getAdjacentKeyPoints(keypoints, 0.5);

adjacentKeyPoints.forEach(keypoints => {
        const [from, to] = keypoints;
        ctx.beginPath();
        ctx.moveTo(from.position.x, from.position.y);
        ctx.lineTo(to.position.x, to.position.y);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

async function main() {
    const net = await loadPoseNet();
    await setupCamera();
    video.play();
    detectPoseInRealTime(video, net);
}

main();