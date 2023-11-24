let title = document.getElementById("site-nav");

originalHeaderFontSize = parseFloat(window.getComputedStyle(title).fontSize);
headerFontUnit = window.getComputedStyle(title).fontSize.match(/(px|em|pt)/)[1];

function resizeEverything() {
  let scrollPosition = window.pageYOffset;
  let rescaleFactor = Math.max(1 - scrollPosition * 0.0005, 0.55);

  title.style.fontSize = (originalHeaderFontSize * rescaleFactor) + headerFontUnit;
}

window.onscroll = resizeEverything;
