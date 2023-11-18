const usersLink = document.getElementById("users");
const userModal = document.getElementById("user-modal");
const closeModal = document.querySelector(".close");
const searchInput = document.getElementById("user-search");
const rows = document.querySelectorAll("tbody tr");

// Get the confirmation modal
var confirmModal = document.getElementById("confirmModal");

// Get the cancel and save buttons
var cancelBtn = confirmModal.querySelector(".cancel-button");
var saveBtn = confirmModal.querySelector(".save-button");

// Get all the messages in the dropdown
var messages = document.querySelectorAll(".message");

// When a message is clicked
messages.forEach(function(message) {
  message.addEventListener("click", function(event) {
    event.preventDefault();

    // Show the confirmation modal
    confirmModal.style.display = "block";
  });
});

// When the cancel button is clicked
cancelBtn.addEventListener("click", function() {
  // Hide the confirmation modal
  confirmModal.style.display = "none";
});

// When the save button is clicked
saveBtn.addEventListener("click", function() {
  // Do something here (e.g. submit a form)

  // Hide the confirmation modal
  confirmModal.style.display = "none";
});

// When the user clicks on the close button of the modals
var closeButtons = document.querySelectorAll(".close");
closeButtons.forEach(function(button) {
  button.addEventListener("click", function() {
    // Hide the modal
    var modal = button.parentElement.parentElement;
    modal.style.display = "none";
  });
});

window.addEventListener("click", function(event) {
    if (event.target == confirmModal) {
      confirmModal.style.display = "none";
    }
  });

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