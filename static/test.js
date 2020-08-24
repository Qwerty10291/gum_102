let message_input = $('#message');
let message_button = $('#send');
let message_container = $('.chat_container')
message_container.scrollTop(1000000);
let login = $('#login')
let time = new Date().getTime()

web = new WebSocket('ws://127.0.0.1:6789');
web.onmessage = function (event){
    data = JSON.parse(event.data);
    add_message(data['login'], data['text']);
}

function add_message(logi, text){
    $(`<div class="message"><a href="">${logi}</a><p>${text}</p></div>`).appendTo(message_container);
    message_container.scrollTop(1000000);
}

function send_message(){
    let time_now = new Date().getTime()
    if(time_now - time > 500 && message_input.val().length > 0){
        time = new Date().getTime();
        let data = JSON.stringify({login: login.text(), text: message_input.val()});
        web.send(data);
    }
}
message_button.click(send_message);
message_input.keypress(function (event){
    if(event.which == 13){message_input.val(message_input.val().replace('\n', ''));
        send_message();};
})