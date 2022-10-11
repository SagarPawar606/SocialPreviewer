// Toggle between different preview styles i.e. Custom, facebook, twitter style preview

var divs = ["custom", "facebook", "twitter"];
var btns = ["custom-btn", "facebook-btn", "twitter-btn"];
var visibleId = null;
function display_preview(id) {
  if (visibleId !== id) {
    visibleId = id;
  }
  hide();
}
function hide() {
  var div, i, id;
  for (i = 0; i < divs.length; i++) {
    id = divs[i];
    btn = btns[i];
    div = document.getElementById(id);
    if (visibleId === id) {
      div.style.display = "block";
      document.getElementById(btn).style.background = '#3a67ec';

    } else {
      div.style.display = "none";
      document.getElementById(btn).style.background = 'transparent';
    }
  }
}  