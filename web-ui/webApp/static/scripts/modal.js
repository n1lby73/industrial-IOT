const usersLink = document.getElementById("users");
const userModal = document.getElementById("user-modal");
const closeModal = document.querySelector(".close");
const searchInput = document.getElementById("user-search");
const rows = document.querySelectorAll("tbody tr");

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

searchInput.addEventListener("keyup", function(event) {
    const query = event.target.value.toLowerCase();

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();

        if (text.includes(query)) {
            row.style.display = "table-row";
        } else {
            row.style.display = "none";
        }
    });
});