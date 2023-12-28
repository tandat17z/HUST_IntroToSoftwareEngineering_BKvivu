const community = document.getElementById("community");
const hiddenElement = document.querySelector(".subnav");

// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

let check_com = true;
community.addEventListener("mouseover", () => {
  check_com = !check_com;
  if(check_com)
    hiddenElement.style.display = "block";
  else
    hiddenElement.style.display = "none";
});

// community.addEventListener("mouseout", () => {
//   hiddenElement.style.display = "none";
// });
// hiddenElement.addEventListener("mouseout", () => {
//   hiddenElement.style.display = "none";
// });