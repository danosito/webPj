var btn = document.getElementById("theme");
var link = document.getElementById("theme-link");
link.setAttribute("href", "/static/css/" + document.cookie.replace("theme=", "") + ".css");

btn.addEventListener("click", function () {
ChangeTheme();
});

function ChangeTheme() {

var currTheme = document.cookie.replace("theme=", "");


if (currTheme == "light") {
  currTheme = "dark";
  document.cookie = "theme=dark; path=/; max-age=31560000";
} else {
  currTheme = "light";
  document.cookie = "theme=light; path=/;  max-age=31560000";
}

link.setAttribute("href", "/static/css/" + currTheme + ".css");
}