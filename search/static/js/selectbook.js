
var $ = jQuery.noConflict();

$(document).ready(function () {
    $(document).on("click", "input[type=checkbox]", function (params) {
        // params.preventDefault()
        console.log(this.checked, this.dataset.bookId);
        $.ajax({
            url: "/book/shop/add/",
            type: "POST",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            data: {
                "bookId": parseInt(this.dataset.bookId),
                "checkStatus": this.checked
            },
            success: function (res, status) {
                console.log(res['status']);
                if (res['status']) {
                    var message = '<div class="alert alert-success" role="alert">' + res["message"] + '</div>'
                } else {
                    var message = '<div class="alert alert-danger" role="alert">' + res["message"] + '</div>'
                }
                document.querySelector(".messages").innerHTML = message
            },
            error: function (res) {
                console.error(res.status);
            },
        });
    })

    // Function to get the CSRF token from the cookie
    function getCSRFToken() {
        var csrfToken = null;
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                csrfToken = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
        return csrfToken;
    }
})