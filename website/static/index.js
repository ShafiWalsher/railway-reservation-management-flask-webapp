

//Login form function
function onThemeChange() {
    let cssStyleSheet = document.getElementById("mainStyle");
    let path = (cssStyleSheet.href).substring((cssStyleSheet.href).length-9, (cssStyleSheet.href).length);
    if(path === "style.css") {
        cssStyleSheet.href = "assets/css/style_dark.css";
        document.getElementById("header_logo").src = "assets/img/logo_dark.png";
        document.getElementById("theme_icon").className = "fas fa-sun";
    } else {
        cssStyleSheet.href = "assets/css/style.css";
        document.getElementById("header_logo").src = "assets/img/logo.png";
        document.getElementById("theme_icon").className = "fas fa-moon";
    }
}