const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate-image");
const offlineMsg = document.getElementById("online");

// const socket = io('http://127.0.0.1:5000');
// const socket = io('https://industrialiot.onrender.com');

const socket = io('http://127.0.0.1:5000');

socket.on('connect', () => {

    socket.emit("current_status")
    socket.emit("espstatus")
    console.log('WebSocket connection opened');
  console.log('Successfully connected to Socket.IO server.');
});

// Handle connection errors
socket.on('connect_error', (error) => {
  console.log(`Failed to connect to ${socket.io.uri}. Error: ${error}.`);

  try {
    socket.disconnect(); // Disconnect from the first URL
    socket.io.uri = 'http://second-url.com'; // Set the new URL
    socket.connect(); // Attempt to connect to the new URL
    socket.emit("current_status")
    socket.emit("espstatus")
    console.log('WebSocket connection opened');
  } catch (e) {
    console.log(`Failed to connect to ${socket.io.uri}. Error: ${e}.`);
  }
});

// Use the socket object to send and receive data with the server


var onlineStatus;

offlineMsg.style.display = "none";


// socket.addEventListener('connect', (event) => {

//     socket.emit("current_status")
//     socket.emit("espstatus")
//     console.log('WebSocket connection opened');
    
// });

// socket.on("connect", function() {

//     socket.emit("current_status")
//     socket.emit("espstatus")
//     console.log('WebSocket connection opened');

// });

const handleButtonClick = () => {

  if (onlineStatus === 1){

    offlineMsg.classList.remove("online");

    let data = {};

    if (button.innerHTML === "ON") {

      button.innerHTML = "OFF";

      data = { 
        
        state: 1,
        pin : 5

      };

      rotateImage.classList.toggle("rotate");
      console.log("tuygjyfg kxqkJG CB UF GCJGuy g BCHJ")
      document.title = 'Running'

      socket.emit('update', data);

    } 
    
    else {

      button.innerHTML = "ON";
      data = {

        state: 0,
        pin : 5
        
      };

      rotateImage.classList.remove("rotate");
      document.title = 'Halted'

      socket.emit('update', data)

    }
  }
  
  else{

    offlineMsg.style.display = "inline";
    document.title = 'Offline';

    }
};

function handleOnLoad(value, onlineStatus){
  if (onlineStatus === 1){

    offlineMsg.classList.remove("online");

    if (value === 1){

      button.innerHTML = "OFF";
      rotateImage.classList.toggle("rotate");
      document.title = 'Running';

    }

    else{

      button.innerHTML = "ON";
      rotateImage.classList.remove("rotate");
      document.title = 'Halted';
      console.log("else");
    }
  }

  else{

    offlineMsg.style.display = "inline";
    document.title = 'Offline';

  }
};

// socket.addEventListener('message', (msg) => {

//     var value = JSON.parse(msg.success);

//     onlineStatus = msg.value;

//     handleOnLoad(value, onlineStatus);
//     console.log(`Received message: ${msg.success}`);

// });

socket.on('message', function(msg){

  var value = JSON.parse(msg.success);

  onlineStatus = msg.value;

  handleOnLoad(value, onlineStatus);
  
});

// socket.addEventListener('localUpdate', (msg) => {

//     var update = JSON.parse(msg.update);
  
//     console.log(update);

//     handleOnLoad(update, 1);
    
//     console.log("syncupdate");

//     console.log(`Received message: ${msg.update}`);
// });


socket.on('localUpdate', function(msg){

  var update = JSON.parse(msg.update);
  
  console.log(update);

  handleOnLoad(update, 1);
  
  console.log("syncupdate");
});

// socket.addEventListener('message', (msg) => {

//     onlineStatus = msg.value;

//     if (onlineStatus === 0){
  
//       offlineMsg.style.display = "inline";
//       document.title = 'Offline';
  
//     }
  
//     else{
  
//       offlineMsg.style.display = "none";
      
//     }
//     console.log(`Received message: ${mg.value}`);
//   });

socket.on('espOnlineState', function(msg){

  onlineStatus = msg.value;

  if (onlineStatus === 0){

    offlineMsg.style.display = "inline";
    document.title = 'Offline';

  }

  else{

    offlineMsg.style.display = "none";
    
  }
})

button.addEventListener('click', handleButtonClick);