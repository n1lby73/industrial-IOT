const button = document.querySelector('#toggleBtn');
const rotateImage = document.getElementById("rotate");

const handleButtonClick = () => {
  let data = {};
  if (button.innerHTML === "ON") {

    button.innerHTML = "OFF";
    data = { state: 1 };
    rotateImage.classList.toggle("rotate");
    document.title = 'running'

  } 
  
  else {

    button.innerHTML = "ON";
    data = { state: 0 };
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

button.addEventListener('click', handleButtonClick);
