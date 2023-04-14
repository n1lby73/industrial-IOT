var socket = io.connect('http://127.0.0.1:5000/'); //url currently subject to change

var priviledges;
var role;


socket.emit("role")

socket.on('storeRole', function(msg){

  role = msg.role
  console.log(msg.role)
  console.log("got here")
  localStorage.setItem('role', role);

})

priviledges = localStorage.getItem('role');

// Show the loading screen
document.getElementById('loading-screen').style.display = 'block';

const interval = setInterval(function() {
  if (role) {
    // Hide the loading screen and show the content element
    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    // clearInterval(interval);
  }
});

if (priviledges === "user"){

  console.log("users");

  document.querySelector('#toggleBtn').style.display = "none";
  document.querySelector('#users').style.display = "none";
  
}

else if (priviledges === "admin"){

  console.log("admin");
  // document.querySelector('#toggleBtn').style.display = "inline";
  // document.querySelector('#users').style.display = "none";

}

else{

  console.log("owner")
  // document.querySelector('#toggleBtn').style.display = "inline";
  // document.querySelector('#users').style.display = "inline";

}

const delRole = () => {

  localStorage.clear();

};

document.querySelector('#logout').addEventListener('click', delRole);