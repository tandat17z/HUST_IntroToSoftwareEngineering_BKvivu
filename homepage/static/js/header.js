const community = document.getElementById("community");
const tab_login = document.getElementById("tab_login");
const hiddenElement = document.querySelector(".subnav");
const hiddenElement_login = document.querySelector(".login");

community.addEventListener("mouseover", () => {
  hiddenElement.style.display = "block";
  hiddenElement.addEventListener("mouseover", () => {
    hiddenElement.style.display = "block";
  });
});

community.addEventListener("mouseout", () => {
  hiddenElement.style.display = "none";
});
hiddenElement.addEventListener("mouseout", () => {
  hiddenElement.style.display = "none";
});

tab_login.addEventListener("mouseover", () => {
  hiddenElement_login.style.display = "block";
  hiddenElement_login.addEventListener("mouseover", () => {
    hiddenElement_login.style.display = "block";
  });
});

tab_login.addEventListener("mouseout", () => {
  hiddenElement_login.style.display = "none";
});
hiddenElement_login.addEventListener("mouseout", () => {
    hiddenElement_login.style.display = "none";
  });


// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

