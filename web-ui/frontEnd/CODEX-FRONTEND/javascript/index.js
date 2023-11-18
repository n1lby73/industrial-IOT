const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate-image");
const offlineMsg = document.getElementById("online");

// const socket = io('http://127.0.0.1:5000'); 
// const socket = io.connect( {cookie: false}, 'https://industrialiot.onrender.com');
// const socket = io.connect('https://industrialiot.onrender.com');
// const socket = io('industrialiot.onrender.com');
// const socket = io('https://industrialiot.onrender.com');
var socket = io.connect();

socket.on('connect', () => {

    socket.emit("current_status")
    // socket.emit("espstatus")
    console.log('WebSocket connection opened');
  console.log('Successfully connected to Socket.IO server.');
});

var onlineStatus;

offlineMsg.style.display = "none";

const handleButtonClick = () => {

  // offlineMsg.classList.remove("online");
  let data = {};
  
  if (button.innerHTML === "Turn ON") {

    button.innerHTML = "Turn OFF";

    data = { 
      
      state: 1,
      pin : 5
    };

    rotateImage.classList.toggle("rotate");
    
    document.title = 'Running'
    socket.emit('update', data);

  } 
  
  else {

    button.innerHTML = "Turn ON";

    data = {
      state: 0,
      pin : 5
      
    };

    rotateImage.classList.remove("rotate");
    document.title = 'Halted'
    socket.emit('update', data)

  }
};

function handleOnLoad(value){

  if (value === "1"){

    button.innerHTML = "Turn OFF";

    document.title = 'Running';

  }

  else{

    button.innerHTML = "Turn ON";
    rotateImage.classList.toggle("rotate");
    document.title = 'Halted';
    console.log("else");
  }

};

socket.on('currentUpdate', function(msg){

  var value = msg.success;
  onlineStatus = msg.value;
  console.log("socket io message");
  console.log(value);
  console.log(onlineStatus);
  handleOnLoad(value);
  
});

socket.on('localUpdate', function(msg){

  var update = JSON.parse(msg.update);
  
  console.log(update);

  handleOnLoad(update, 1);
  
  console.log("syncupdate");
});

// socket.on('espOnlineState', function(msg){

//   onlineStatus = msg.value;

//   if (onlineStatus === 0){

//     offlineMsg.style.display = "inline";
//     document.title = 'Offline';

//   }

//   else{

//     offlineMsg.style.display = "none";
    
//   }
// })

button.addEventListener('click', handleButtonClick);