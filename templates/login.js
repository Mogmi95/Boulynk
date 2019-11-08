
$(document).ready(function(){

    var socket = io();
    console.log("joinning")
    socket.emit('join');
    socket.on("join_ack", function(msg){
        console.log('login_ack', msg)
    })
})