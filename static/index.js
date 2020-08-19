let message_input = $('#message');
let message_button = $('#send');
let message_container = $('.chat_container')
message_container.scrollTop(1000000);
let login = $('#login')
let title = $('title');
let chat = [];
let doc = document.querySelectorAll('.reader-view__wrap img').style.width = '1000px';

$.get('/load_messages').done(function (data){chat = JSON.parse(data);console.log(chat);})

function send_message(oihqefb){
    if(message_input.val().length > 0){
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
    console.log(chat[chat.length - 1][0], chat[chat.length - 1][1])
    $.post('/check_message', {'login':chat[chat.length - 1][0], 'message':chat[chat.length - 1][1]}).done(function(data){
        if(data == 'yes'){get_last_message();}})
}
setInterval('check_messages()', 1000);
message_button.click(send_message);