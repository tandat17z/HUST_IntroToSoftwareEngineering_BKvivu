const hiddenElement = document.querySelector(".subnav");
const hiddenElement_login = document.querySelector(".login");

let check = false;
tab_login.addEventListener("mouseover", () => {
  check = !check;
  if( check){
    hiddenElement_login.style.display = "block";
  }
  else{
    hiddenElement_login.style.display = "none";
  }
  // hiddenElement_login.addEventListener("mouseover", () => {
  //   hiddenElement_login.style.display = "block";
  // });
});

// tab_login.addEventListener("mouseout", () => {
//   hiddenElement_login.style.display = "none";
// });

// hiddenElement_login.addEventListener("mouseout", () => {
//     hiddenElement_login.style.display = "none";
//   });


// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


function checkPassword() {
  // Kiểm tra điều kiện và thiết lập thuộc tính disabled
  var input1 = document.getElementById('inputPswRegister');
  var input2 = document.getElementById('inputRepsw');
  // Thay bằng điều kiện thực tế từ server hoặc nơi khác
  if (input1.value.length >= 8 && input2.value.length == input1.value.length) {
      console.log('Ấn được nhé');
      document.getElementById('btnRegister').disabled = false;
  }
  else{
      console.log('Button disabled true.');
      document.getElementById('btnRegister').disabled = true;
  }
}