const button = document.querySelector('#toggleBtn');

button.addEventListener('click', handleButtonClick);

const handleButtonClick = () => {
  let data = {};
  if (button.innerHTML === "ON") {
    button.innerHTML = "OFF";
    data = { state: 0 };
  } else {
    button.innerHTML = "ON";
    data = { state: 1 };
  }

  fetch('/btn', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
};

// button.addEventListener('click', handleButtonClick);

// const button = document.getElementById('toggleBtn');

// button.addEventListener('click', () => {
//     let buttonValue == button.value;

//     console.log("got here")
//     var data = { 
    
//         if (buttonValue.innerHTML === "ON") {
//                 button.innerHTML = "OFF";
//         "btnvalue": 1,
                
//     };
        
//     fetch('/btn', {
//         method: 'POST',
//         body: JSON.stringify(data),
//         headers: { 'Content-Type': 'application/json' }
//     })
//     .then(response => {
//         if (response.ok){
//             console.log(response.status);
//             console.log("Request succeeded");
//             return response.json();
//         }
        
//         else{
        
//             console.log("error sending data");
//         }
//     })
//     .then(data => {
//         if (data.success === true){
//             console.log("succ");
//             window.location.replace('/on');
//         }
        
//         else{
                        
//             console.log(data);
//             console.log("i won't redirect");
//         }
//     })
//     .catch(error => console.error(error));
// });



// let button1 = document.querySelector('#on');
// let button2 = document.querySelector('#off');
// // Get the button element
// const button = document.querySelector('#toggleBtn');

// // Function to handle button click
// const handleButtonClick = () => {
//   let data = {};
//   if (button.innerHTML === "ON") {
//     button.innerHTML = "OFF";
//     "state" : 0;

// };
//   } else {
//     button.innerHTML = "ON";
//     data = { state: 1 };
//   }

//   // Send data to server
//   fetch('/btn', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(data)
//   })
//     .then(res => res.json())
//     .then(data => console.log(data))
//     .catch(error => console.error(error));
// };

// // Attach click event to button
// button.addEventListener('click', handleButtonClick);

// let button = document.getElementById("toggle-button");

// button.addEventListener("click", function() {

//   let status = button.innerHTML === "ON" ? "OFF" : "ON";
//   button.innerHTML = status;
  
//   let data = button.innerHTML === "ON" ? 1 : 0;
  
//   fetch("/your-server-endpoint", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({ status: data })
//   })
//   .then(response => {
//     console.log("Success:", response);
//   })
//   .catch(error => {
//     console.error("Error:", error);
//   });
// });

// var toggleBtn = document.getElementById("toggleBtn");
// var toggle = false;

// toggleBtn.addEventListener("click", function() {
//   toggle = !toggle;
//   toggleBtn.innerHTML = toggle ? "ON" : "OFF";
// });

// // // const button = document.getElementById('on');
// // // const button2 = document.getElementById('off');


// // let button1 = document.querySelector('#on');
// // let button2 = document.querySelector('#off');

// // button1.addEventListener('click', () => {
// //     console.log("got here")
// //     var data = { 
    
// //         "btnvalue": 1,
                
// //     };
        
// //     fetch('/btn', {
// //         method: 'POST',
// //         body: JSON.stringify(data),
// //         headers: { 'Content-Type': 'application/json' }
// //     })
// //     .then(response => {
// //         if (response.ok){
// //             console.log(response.status);
// //             console.log("Request succeeded");
// //             return response.json();
// //         }
        
// //         else{
        
// //             console.log("error sending data");
// //         }
// //     })
// //     .then(data => {
// //         if (data.success === true){
// //             console.log("succ");
// //             window.location.replace('/on');
// //         }
        
// //         else{
                        
// //             console.log(data);
// //             console.log("i won't redirect");
// //         }
// //     })
// //     .catch(error => console.error(error));

// // });

// // button2.addEventListener('click', () => {
// //     console.log("here");

// //     var data = { 
    
// //         "btnvalue": 0,
                
// //     };
        
// //     fetch('/btn', {
// //         method: 'POST',
// //         body: JSON.stringify(data),
// //         headers: { 'Content-Type': 'application/json' }
// //     })
// //     .then(response => {
// //         if (response.ok){
// //             console.log(response.status);
// //             console.log("Request succeeded");
// //             return response.json();
// //         }
        
// //         else{
        
// //             console.log("error sending data");
// //         }
// //     })
// //     .then(data => {
// //         if (data.success === true){
// //             console.log("succ");
// //             window.location.replace('/');
// //         }
        
// //         else{
                        
// //             console.log(data);
// //             console.log("i won't redirect");
// //         }
// //     })
// //     .catch(error => console.error(error));
// // });

