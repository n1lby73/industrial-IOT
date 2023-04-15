const usersLink = document.getElementById("users");
const userModal = document.getElementById("user-modal");
const closeModal = document.querySelector(".close");

usersLink.addEventListener("click", function() {
    event.preventDefault();
    userModal.style.display = "block";
    userModal.style.display = "flex";
});

closeModal.addEventListener("click", function() {
    userModal.style.display = "none";
});

window.addEventListener("click", function(event) {
    if (event.target === userModal) {
        userModal.style.display = "none";
    }
});