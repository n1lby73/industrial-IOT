const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate");
const offlineMsg = document.getElementById("online");
var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change
var onlineStatus;

socket.emit("current_status")


// const socket = io.connect('http://localhost:5000'); 

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

    offlineMsg.classList.toggle("online");
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

    offlineMsg.classList.toggle("online");
    document.title = 'Offline';

  }
};

socket.on('message', function(msg){

  var value = JSON.parse(msg.success);
  onlineStatus = JSON.parse(msg.value);
  console.log(onlineStatus)
  console.log("here we are");
  handleOnLoad(value, onlineStatus);
  
});

socket.on('localUpdate', function(msg){

  var update = JSON.parse(msg.update);
  
  console.log(update);

  handleOnLoad(update, 1);
  
  console.log("syncupdate");
});

socket.on('espOnlineState', function(msg){
  onlineStatus = JSON.parse(msg.value);
  console.log("under is the value");
  console.log(onlineStatus);
})
button.addEventListener('click', handleButtonClick);