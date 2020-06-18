document.addEventListener('DOMContentLoaded', () => {
    //Make enter key submit

    let msg = document.querySelector("#input-search");
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector("#main-search").click();
        }
    });

    let channel = document.querySelector("#input-search-navbar");
    channel.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector("#search-navbar").click();
        }
    });

    // By default, main-search button is disabled
    document.querySelector('#main-search').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#input-search').onkeyup = () => {
        if (document.querySelector('#input-search').value.length > 0)
            document.querySelector('#main-search').disabled = false;
        else
            document.querySelector('#send_message').disabled = true;
    };

    // By default, search-navbar button is disabled
    document.querySelector('#search-navbar').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#input-search-navbar').onkeyup = () => {
        if (document.querySelector('#input-search-navbar').value.length > 0)
            document.querySelector('#search-navbar').disabled = false;
        else
            document.querySelector('#search-navbar').disabled = true;
    };
});
