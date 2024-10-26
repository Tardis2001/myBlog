
document.addEventListener("DOMContentLoaded", function () {
  const elements = document.querySelectorAll(".reveal > *");
  const slowobserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("text--visible");
    }
      else{
        entry.target.classList.remove("text--visible")
    
      }
    });
  }, { threshold:0.1 });
  elements.forEach((el) => slowobserver.observe(el));

});

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  const backToTopBtn = document.getElementById("backToTopBtn");
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    backToTopBtn.classList.add("text--visible");
  } else {
    backToTopBtn.classList.remove("text--visible");
  }
}

function scrollToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}