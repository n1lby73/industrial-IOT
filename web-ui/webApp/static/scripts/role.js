var role;

socket.on("connect", function() {
  console.log("immediately after connect socket");
  socket.emit("role");
  console.log("role inside socket");
});

console.log("role outside socket");


socket.on('storeRole', function(msg){

    console.log("role outside store role");

  role = msg.role;
   
  if(role === "user"){

    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.querySelector('#toggleBtn').style.display = "none";
    document.querySelector('#users').style.display = "none";

  }

  else if(role === "admin"){

    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.querySelector('#toggleBtn').style.display = "inline-block";
    document.querySelector('#users').style.display = "none";

  }

  else{

    console.log(role);
    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.querySelector('#toggleBtn').style.display = "inline-block";
    document.querySelector('#users').style.display = "inline-block";

  }

  // document.getElementById('loading-screen').style.display = 'none';
  // document.getElementById('content').style.display = 'block';

});

console.log(role);
