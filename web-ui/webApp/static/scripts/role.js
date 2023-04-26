// var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change
// var socket = io.connect('https://' + window.location.hostname+ ':' + location.port);
// var socket = io('http://192.168.0.145:5000/', {
//     cors: {
//         origin: '*',
//         methods: ['GET', 'POST']
//     }
// });
var socket= io.connect('https://industrialiot.onrender.com/', {
  cors: {
      origin: '*',
      methods: ['GET', 'POST']
  }
})

var role;

document.getElementById('loading-screen').style.display = 'block';
// console.dir(io)

// socket.emit("role")

socket.on("connect", function() {
  socket.emit("role");
});

socket.on('storeRole', function(msg){

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