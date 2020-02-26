function fadeIn(element, speed) {
  if (element.style.opacity != 1) {
    var speed = speed || 30;
    var num = 0;
    var st = setInterval(function() {
      num++;
      element.style.opacity = num / 10;
      if (num >= 10) {
        clearInterval(st);
      }
    }, speed);
  }
}

function Load() {
  document.getElementById("loading").removeAttribute("hidden");
  fadeIn(loading, 20)
  // $("#loading").fadeIn(500);
  // $("#loading").show();
}