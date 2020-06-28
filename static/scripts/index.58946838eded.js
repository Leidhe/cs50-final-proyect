document.addEventListener('DOMContentLoaded', () => {
    //Make enter key submit

    let channel = document.querySelector("#input-search-navbar");
    channel.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector("#search-navbar").click();
        }
    });

    // By default, search-navbar button is disabled
    document.querySelector('#search-navbar').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#input-search-navbar').onkeyup = () => {
        if (document.querySelector('#input-search-navbar').value.length > 0)
            document.querySelector('#search-navbar').disabled = false;
        else
            document.querySelector('#search-navbar').disabled = true;
    };

    $('#sub-menu').on('change', function () {
        var url = $(this).val(); // get selected value
        if (url) { // require a URL
            window.location = url; // redirect
        }
        return false;
    });

});

function toggle(button) {

    var classbutton = $(button).val();
    var span = $(button).find("span")
    var x = document.getElementById(classbutton);
    if (x.style.display === "none") {
        x.style.display = "block";
        $(span).addClass("fa-rotate-90")

    } else {
        x.style.display = "none";
        $(span).removeClass();
        $(span).addClass("fa fa-chevron-right")
    }
}
