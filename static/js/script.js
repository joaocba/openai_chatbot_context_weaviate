
// Chat messages append
function getCompletion() {
    let userText = $("#userMessage").val();
    let userHtml = '<div class="row justify-content-start my-4"><div class="col-10 d-flex justify-content-start"><img src="static\\img\\002-man.png" class="me-3" alt="" width="50" height="58"><div class="alert alert-secondary" role="alert">' + userText + '</div></div></div>';
    $("#userMessage").val("");
    $("#messagebox").append(userHtml);

    // Scroll to bottom after message input
    var messageBox = document.getElementById("messagebox");
    messageBox.scrollTop = messageBox.scrollHeight;

    $.get("/get", { msg: userText }).done(function (data) {
        var assistantHTML = '<div class="row justify-content-end my-4"><div class="col-10 d-flex justify-content-end"><div class="alert alert-primary" role="alert">' + data + '</div><img src="static\\img\\001-assistant.png" class="ms-3" alt="" width="50" height="58"></div></div>';
        $("#messagebox").append(assistantHTML);

        // Scroll to the bottom of the messagebox after a short delay
        setTimeout(function () {
            var messageBox2 = document.getElementById("messagebox");
            messageBox2.scrollTop = messageBox2.scrollHeight;
        }, 100);
    });
}
$("#userMessage").keypress(function (e) {
    // allows message to be sent with enter key
    if (e.which == 13) {
        getCompletion();
    }
});
// allows message to be sent by clicking the Send button
$("#sendButton").click(function () {
    getCompletion();
});