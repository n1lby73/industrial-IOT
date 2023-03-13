const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate");
var socket = io.connect('http://127.0.0.1:5000'); //url currently subject to change
var test;
// const socket = io.connect('http://localhost:5000'); 

// const handleButtonClick = () => {

//   let data = {};

//   if (button.innerHTML === "ON") {

//     button.innerHTML = "OFF";

//     data = { 
      
//       state: 1,
//       pin : 5

//     };

//     rotateImage.classList.toggle("rotate");
//     document.title = 'running'

//   } 
  
//   else {

//     button.innerHTML = "ON";
//     data = {

//       state: 0,
//       pin : 5
      
//     };

//     rotateImage.classList.remove("rotate");
//     document.title = 'halted'

//   }

//   fetch('/btn', {

//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify(data)

//   })

// };

const handleButtonClick = () => {

};

function synchronize(){

  fetch('/query', {

    method: 'POST',
    headers: {'Content-Type': 'application/json'}

  })

  .then(response => {

    if (response.ok){

        return response.json();

    }

    else{

        console.log("error sending data");
    }
  })

  .then(data => {

    if (data.success == 1){

      button.innerHTML = "OFF";

      rotateImage.classList.toggle("rotate");
      document.title = 'running'
    }

    else {

      button.innerHTML = "ON";
    
      rotateImage.classList.remove("rotate");
      document.title = 'halted'
    
    }

  })

    .catch(error => console.error(error));

}


socket.on('connect', function() {

  socket.send('I\'m connected!'); 

});

socket.on('message', function(msg){

  var value = msg.success;

  if (value == 1){

    button.innerHTML = "OFF";

    rotateImage.classList.toggle("rotate");
    document.title = 'running'
  }

  else {

    button.innerHTML = "ON";
  
    rotateImage.classList.remove("rotate");
    document.title = 'halted'
  
  }

  console.log(msg.success);
});

button.addEventListener('click', handleButtonClick);