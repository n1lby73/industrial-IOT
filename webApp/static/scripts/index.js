// const button = document.getElementById('on');
// const button2 = document.getElementById('off');


let button1 = document.querySelector('#on');
let button2 = document.querySelector('#off');

// button1.addEventListener('click', function() {
//   console.log('Button 1 clicked');
// });

// button2.addEventListener('click', function() {
//   console.log('Button 2 clicked');
// });

button1.addEventListener('click', () => {

    var data = { 
    
        "btnvalue": 1,
                
    };
        
    fetch('/btn', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (response.ok){
            console.log(response.status);
            console.log("Request succeeded");
            return response.json();
        }
        
        else{
        
            console.log("error sending data");
        }
    })
    .then(data => {
        if (data.success === true){
            console.log("succ");
            window.location.replace('/on');
        }
        
        else{
                        
            console.log(data);
            console.log("i won't redirect");
        }
    })
    .catch(error => console.error(error));

});

button2.addEventListener('click', () => {
    alert("go off");
//     var data = { 
    
//         "btnvalue": 0,
                
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
//             window.location.replace('/');
//         }
        
//         else{
                        
//             console.log(data);
//             console.log("i won't redirect");
//         }
//     })
//     .catch(error => console.error(error));

});