

// var back_end = "http://192.168.43.185:5000"
var back_end = "http://127.0.0.1:5000"
var cell_size = 25

var BOMB_VALUE = -1


$(document).ready(function () {

    function updateGrid(grid, is_init = false) {
        console.log(grid)
        grid_size = grid.size
        var content = ""
        grid.forEach(function (sub, x) {
            content += `<div class="mine_row">`
            sub.forEach(function (v, y) {
                // col = (y + x) % 2 ? "white" : "black";
                value = v
                if (v <= 0) {
                    value = " ";
                }
                oddness = (x+y) %2 == 0 ? "odd" : "even"
                content += `<div class="mine mine_${v} ${oddness}" x="${x}" y="${y}">${value}</div>`
            })
            content += '</div>'
        })
        if (is_init) {
            content = `<div class='mine_field'>${content}</div>`
        }

        $("#game_board").html(content)


        $(".mine").on("click", function (e) {
            var payload = { x: parseInt($(this).attr("x")), y: parseInt($(this).attr("y")) }
            console.log(payload)
            $.postJSON(`${back_end}/minesweeper/pos`, JSON.stringify(payload), function (data, s) {
                if (s) {
                    console.log(data["status"])
                    updateGrid(data["grid"])
                }
            })
        })
    }

    $("#GO").on("click", function (e) {

        // Send size
        var grid_size = parseInt($('#size').val());
        var nb_bomb = parseInt($('#nb_bomb').val());
        var payload = {
            "nb_bomb": nb_bomb, "grid_size": grid_size
        }

        $.postJSON(`${back_end}/minesweeper/init`, JSON.stringify(payload), function (data, success) {
            if (success) {
                console.log(data["status"])
                updateGrid(data["grid"], data["status"] == "Start")
            } else {
                console.log("/minesweeper/init failed")
            }
        })
    });

});