window.onload = function() {
  // Fade-in elements animation
  const fadeInElements = document.querySelectorAll('.fade-in');
  fadeInElements.forEach(function(element) {
      setTimeout(function() {
          element.classList.add('active');
      }, 200);
  });

  // Slide-in animation for footer text
  anime({
      targets: 'footer p', // targeting the paragraph in the footer
      translateX: ['-100%', 0], // this moves the footer text from 300px to its left to its original position
      duration: 1000,
      easing: 'easeOutExpo'
  });
  anime({
    targets: 'nav.navbar .logo-link img',
    translateX: ['-700%', 0],  // Further starting position
    duration: 4000,  // 2 seconds for animation
    easing: 'easeOutExpo'
  });
};
