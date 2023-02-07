const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate");

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

  } 
  
  else {

    button.innerHTML = "ON";
    data = {

      state: 0,
      pin : 5
      
    };

    rotateImage.classList.remove("rotate");
    document.title = 'halted'

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

function synchronize(){

  fetch('/query', {

    method: 'POST',
    headers: {'Content-Type': 'application/json'}

  })

  .then(response => {

    if (response.ok){

        return response.json();

    }

    else{

        console.log("error sending data");
    }
  })

  .then(data => {

    if (data.success == 1){

      button.innerHTML = "OFF";

      rotateImage.classList.toggle("rotate");
      document.title = 'running'
    }

    else {

      button.innerHTML = "ON";
    
      rotateImage.classList.remove("rotate");
      document.title = 'halted'
    
    }

  })

    .catch(error => console.error(error));

}

button.addEventListener('click', handleButtonClick);