var btn = document.getElementById("theme");
var link = document.getElementById("theme-link");

btn.addEventListener("click", function () {
  ChangeTheme();
});

function ChangeTheme() {
  let lightTheme = "../static/css/light.css";
  let darkTheme = "../static/css/dark.css";

  var currTheme = link.getAttribute("href");
  var theme = "";

  if (currTheme == lightTheme) {
    currTheme = darkTheme;
    theme = "dark";
  } else {
    currTheme = lightTheme;
    theme = "light";
  }

  function Save(theme) {
    var Request = new XMLHttpRequest();
    Request.open("GET", "themes.php?theme=" + theme, true); //У вас путь может отличаться
    Request.send();
  }

  link.setAttribute("href", currTheme);

  Save(theme);
}
