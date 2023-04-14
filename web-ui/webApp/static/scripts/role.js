var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change

var reloadFlag = true;
var priviledges;
var role;



socket.emit("role")

socket.on('storeRole', function(msg){

  role = msg.role;
  console.log(msg.role);
  console.log("from web socket");
  localStorage.setItem('role', role);
   

});



if(localStorage.getItem('role')){

  console.log("no data yet");
  document.getElementById('loading-screen').style.display = 'block';
  
  
}

if (!localStorage.getItem('role')){

  console.log("Got Here again");

}


// else{
//   priviledges = localStorage.getItem('role');
//   console.log("Got Here again")

//   if (priviledges === "user"){
      
//     console.log("users");
//     document.querySelector('#toggleBtn').style.display = "none";
//     document.querySelector('#users').style.display = "none";

//     document.getElementById('loading-screen').style.display = 'none';
//     document.getElementById('content').style.display = 'block';
    
//   }
  
//   else if (priviledges === "admin"){
//     console.log("admin");
//     document.querySelector('#toggleBtn').style.display = "inline-block";
//     document.querySelector('#users').style.display = "none";
//     console.log("here");

//     document.getElementById('loading-screen').style.display = 'none';
//     document.getElementById('content').style.display = 'block';
  
//   }
  
//   else{
//      console.log("owner");
//     document.querySelector('#toggleBtn').style.display = "inline-block";
//     document.querySelector('#users').style.display = "inline-block";
    
//     document.getElementById('loading-screen').style.display = 'none';
//     document.getElementById('content').style.display = 'block';
//   }

// }

// // if (!reloadFlag){

// //   localStorage.setItem('reload', "true");
// //   location.reload();

// // }

// const delRole = () => {

//   localStorage.clear();

// };

// document.querySelector('#logout').addEventListener('click', delRole);


// priviledges = localStorage.getItem('role');

// // Show the loading screen
// document.getElementById('loading-screen').style.display = 'block';

// const interval = setInterval(function() {
//   if (role) {
//     // Hide the loading screen and show the content element
//     document.getElementById('loading-screen').style.display = 'none';
//     document.getElementById('content').style.display = 'block';
//     // clearInterval(interval);
//   }
// });

// const priviledgeInterval = setInterval(function() {

//   if (priviledges) {

//     localStorage.setItem('priviledges', "true");
    
//   }
// });

// if (localStorage.getItem('priviledges') === "true"){

//   if (priviledges === "user"){
      
//     console.log("users");
//     document.querySelector('#toggleBtn').style.display = "none";
//     document.querySelector('#users').style.display = "none";
    
//   }
  
//   else if (priviledges === "admin"){
//     console.log("admin");
//     document.querySelector('#toggleBtn').style.display = "inline-block";
//     document.querySelector('#users').style.display = "none";
//     console.log("here");
  
//   }
  
//   else{
//      console.log("owner");
//     document.querySelector('#toggleBtn').style.display = "inline-block";
//     document.querySelector('#users').style.display = "inline-block";
  
//   }

// }

// if (!reloadFlag){

//   localStorage.setItem('reload', "true");
//   location.reload();

// }

// const delRole = () => {

//   localStorage.clear();

// };

// document.querySelector('#logout').addEventListener('click', delRole);