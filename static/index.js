let message_input = $('#message');
let message_button = $('#send');
let message_container = $('.chat_container')
message_container.scrollTop(1000000);
let login = $('#login')
let title = $('title');
let chat = [];
let time = new Date().getTime()

$.get('/load_messages').done(function (data){chat = JSON.parse(data);})

function send_message(oihqefb){
    if(message_input.val().length > 0 && Date().getTime() - time > 500){
        time = new Date().getTime()
        $.post('/add_message', {'text':message_input.val()});}
}

function add_message(logi, text){
    $(`<div class="message"><a href="">${logi}</a><p>${text}</p></div>`).appendTo(message_container);
    message_container.scrollTop(1000000);
}

function get_last_message() {
    $.get('/load_message').done(function (data){
        let text = JSON.parse(data);
        add_message(text[0], text[1]);
        chat.push(text);})
}

function check_messages(){
    $.post('/check_message', {'login':chat[chat.length - 1][0], 'message':chat[chat.length - 1][1]}).done(function(data){
        if(data == 'yes'){get_last_message();}})
}
setInterval('check_messages()', 1000);
message_button.click(send_message);
message_input.keypress(function (event){
    if(event.which == 13){send_message()};
})