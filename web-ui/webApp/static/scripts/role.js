var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change

var role;

document.getElementById('loading-screen').style.display = 'block';


socket.emit("role")

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