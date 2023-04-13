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

// if (role === undefined ){

//   // console.log("hdghncdghcgn ff");
//   // return <div>loading</div>;
//   var loadingDiv = document.createElement('div');
//   loadingDiv.textContent = 'Loading...';
//   document.body.appendChild(loadingDiv);
//   console.log("hdghncdghcgn ff");

// }
// if (priviledges !== "owner"){
//   console.log("what is happening")
//   console.log(localStorage.getItem('role'))
// }


// Show the loading screen
document.getElementById('loading-screen').style.display = 'block';

// Use setInterval to check if the variable is assigned
const interval = setInterval(function() {
  if (role) {
    // Hide the loading screen and show the content element
    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    clearInterval(interval);
  }
});