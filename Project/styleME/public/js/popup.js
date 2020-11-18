// When the user clicks on div, open the popup
function popup() {
    var popup = document.getElementsByClassName("popup");
    for (var i = 0; i < popup.length; i++) {
        popup[i].classList.toggle('show')
    }
}