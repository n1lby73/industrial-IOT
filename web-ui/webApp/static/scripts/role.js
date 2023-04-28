// const socket = new WebSocket('ws://127.0.0.1:5000');


var role;

document.getElementById('loading-screen').style.display = 'block';

socket.addEventListener('connect', (event) => {

    socket.emit("role");
    console.log("role inside socket");

});

// socket.on("connect", function() {
//   console.log("immediately after connect socket");
//   socket.emit("role");
//   console.log("role inside socket");
// });

console.log("role outside socket");

// socket.addEventListener('storeRole', (msg) => {

//     console.log("role outside store role");

//     role = msg.role;
   
//     if(role === "user"){

//         document.querySelector('#toggleBtn').style.display = "none";
//         document.querySelector('#users').style.display = "none";

//     }

//     else if(role === "admin"){

//         document.querySelector('#toggleBtn').style.display = "inline-block";
//         document.querySelector('#users').style.display = "none";

//     }

//     else{

//         document.querySelector('#toggleBtn').style.display = "inline-block";
//         document.querySelector('#users').style.display = "inline-block";

//     }

//     document.getElementById('loading-screen').style.display = 'none';
//     document.getElementById('content').style.display = 'block';

// });

socket.on('storeRole', function(msg){

    console.log("role outside store role");

  role = msg.role;
   
  if(role === "user"){

    document.querySelector('#toggleBtn').style.display = "none";
    document.querySelector('#users').style.display = "none";

  }

  else if(role === "admin"){

    document.querySelector('#toggleBtn').style.display = "inline-block";
    document.querySelector('#users').style.display = "none";

  }

  else{

    document.querySelector('#toggleBtn').style.display = "inline-block";
    document.querySelector('#users').style.display = "inline-block";

  }

  document.getElementById('loading-screen').style.display = 'none';
  document.getElementById('content').style.display = 'block';

});