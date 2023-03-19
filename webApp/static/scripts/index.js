const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate");
var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change


socket.emit("current_status")


// const socket = io.connect('http://localhost:5000'); 

const handleButtonClick = () => {

  let data = {};

  if (button.innerHTML === "ON") {

    button.innerHTML = "OFF";

    data = { 
      
      state: 1,
      pin : 5

    };

    rotateImage.classList.toggle("rotate");
    document.title = 'running'

    socket.emit('update', data);

  } 
  
  else {

    button.innerHTML = "ON";
    data = {

      state: 0,
      pin : 5
      
    };

    rotateImage.classList.remove("rotate");
    document.title = 'halted'

    socket.emit('update', data)

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

function handleOnLoad(value){

  if(value === 1){

    button.innerHTML = "OFF";
    rotateImage.classList.toggle("rotate");
    document.title = 'running';

  }

  else{
    console.log("else");
  }

};

socket.on('message', function(msg){

  var value = JSON.parse(msg.success);
  console.log(value);

  handleOnLoad(value);
  
  console.log("valuefcmxgfdx ngfgf");
});



button.addEventListener('click', handleButtonClick);