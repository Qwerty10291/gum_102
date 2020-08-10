let message_input = $('#message');
let message_button = $('#send');
let message_container = $('.chat_container')
let title = $('title');
let chat = [];

function send_message(){
    $.post('/add_message', {'text':message_input.val()});
}

function add_message(login, text){
    $()
}

function get_last_message() {
    $.get('/load_message').done(function (data){
        let text = JSON.parse(data);
        chat.push(text);
    })
}

message_button.click(add_message);