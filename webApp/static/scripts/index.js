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

// const handleButtonClick = () => {
  
//   if (button.innerHTML === "ON") {
//     button.innerHTML = "OFF";

//     data = { 
//       state: 1
//       pin : 5
//     };

//     rotateImage.classList.toggle("rotate");
//     document.title = 'running'

//     const jsonString = JSON.stringify(data);
//     socket.send(jsonString);
//   };

//   else {

//     button.innerHTML = "ON";
//     data = {
    
//       state: 0,
//       pin : 5
       
//     };
   
//     rotateImage.classList.remove("rotate");
//     document.title = 'halted'
    
//   }

// };

// function synchronize(){

//   fetch('/query', {

//     method: 'POST',
//     headers: {'Content-Type': 'application/json'}

//   })

//   .then(response => {

//     if (response.ok){

//         return response.json();

//     }

//     else{

//         console.log("error sending data");
//     }
//   })

//   .then(data => {

//     if (data.success == 1){

//       button.innerHTML = "OFF";

//       rotateImage.classList.toggle("rotate");
//       document.title = 'running'
//     }

//     else {

//       button.innerHTML = "ON";
    
//       rotateImage.classList.remove("rotate");
//       document.title = 'halted'
    
//     }

//   })

//     .catch(error => console.error(error));

// }


// socket.on('connect', function() {

//   console.log('browser connected!');

// });

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
  onlineStatus = JSON.parse(msg.onlineStatus)

  console.log(value);

  handleOnLoad(value, onlineStatus);
  
  console.log("valuefcmxgfdx ngfgf");
});



button.addEventListener('click', handleButtonClick);