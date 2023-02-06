const button = document.querySelector('#toggleBtn');

const handleButtonClick = () => {
  let data = {};
  if (button.innerHTML === "ON") {

    button.innerHTML = "OFF";
    data = { state: 1 };
    document.title = 'running'

  } 
  
  else {

    button.innerHTML = "ON";
    data = { state: 0 };
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
