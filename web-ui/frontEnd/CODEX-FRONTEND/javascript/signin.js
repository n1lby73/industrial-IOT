
async function submitForm() {
    const email = document.forms["loginForm"]["email"].value;
    const password = document.forms["loginForm"]["password"].value;

    const formData = {
        email: email,
        password: password
    };

   try{
    const response = await fetch('https://industrialiot.onrender.com/api/loginapi', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(formData)
    });

    if(!response.ok){
        throw new Error('Login Failed')
    }
    // return response.text();
    console.log('Login Success');
 
    location.assign('/index');

   }
   catch (error){
    console.error(error);
   showErrorMessage(error);
   return false;
   }
}


function showErrorMessage(error){
    errorMsg.innerText = error;
    console.log(errorMsg);
    errorMsg.style.display = 'block';
}

























// fetch('https://industrialiot.onrender.com/api/loginapi', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
 
//     },
//     body: JSON.stringify(formData)
// })
// .then(
//     response => {
//         if(!response.ok) {
//           throw new Error('Network response was not ok'); 
//         }
//         return response.text();}
// )
// .then()
// .catch();

// return false;