let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
}

function showSlidess() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlidess, 5000); // Change image every 2 seconds
}

//top dich vu --------------------------------------------------
// openCity(event, 'London')
function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the link that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

// Phan comment
const next = document.querySelector('#comment .next')
const prev = document.querySelector('#comment .prev')
const comment = document.querySelector('.post-list')
const commentItem = document.querySelectorAll('.post-list .item')

var translateY = 0
var count = commentItem.length

next.addEventListener('click', function (event) {
event.preventDefault()
if( count == 1){
    translateY += 600*(commentItem.length - 1)
    comment.style.transform = `translateY(${translateY}px`
    count = commentItem.length
}
else{
    translateY += -600
    comment.style.transform = `translateY(${translateY}px`
    count --
}
})

prev.addEventListener('click', function (event) {
    event.preventDefault()
    if( count == commentItem.length){
        translateY += -600*(commentItem.length - 1)
        comment.style.transform = `translateY(${translateY}px`
        count = 1
    }
    else{
        translateY += 600
        comment.style.transform = `translateY(${translateY}px`
        count ++
    }
})