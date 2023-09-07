
var $ = jQuery.noConflict();

$(document).ready(function(){
    setInterval(function() {
        var alertDiv = document.querySelector(".alert");
        if (alertDiv) {
          alertDiv.remove();
        }
    }, 5000);
})