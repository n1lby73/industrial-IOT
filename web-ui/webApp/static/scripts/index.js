const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate-image");
const offlineMsg = document.getElementById("online");

// var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change
// var socket = io('http://192.168.0.145:5000/', {
//     cors: {
//         origin: '*',
//         methods: ['GET', 'POST']
//     }
// });
var socket = io.connect('http://' + window.location.hostname + ':' + location.port);
var onlineStatus;

offlineMsg.style.display = "none";

// socket.emit("current_status")
// socket.emit("espstatus")


socket.on("connect", function() {
  // socket.emit("role");
  socket.emit("current_status")
  socket.emit("espstatus")

});

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

socket.on('message', function(msg){

  var value = JSON.parse(msg.success);
  // onlineStatus = JSON.parse(msg.value);
  onlineStatus = msg.value;

  handleOnLoad(value, onlineStatus);
  
});

socket.on('localUpdate', function(msg){

  var update = JSON.parse(msg.update);
  
  console.log(update);

  handleOnLoad(update, 1);
  
  console.log("syncupdate");
});

socket.on('espOnlineState', function(msg){

  // console.log(msg.value);
  // onlineStatus = JSON.parse(msg.value);
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