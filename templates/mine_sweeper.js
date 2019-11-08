

var back_end = "http://192.168.43.185:5000"
// var back_end = "http://127.0.0.1:5000"
var cell_size = 25

var BOMB_VALUE = -1


$(document).ready(function () {

    function updateGrid(grid) {
        var content = "";
        console.log(grid)
        grid_size = grid.size

        grid.forEach(function (sub, x) {
            content += `<div style="padding:0;margin:0;width:${grid_size * cell_size}px;height:${cell_size}px">`
            sub.forEach(function (v, y) {
                // col = (y + x) % 2 ? "white" : "black";
                content += `<div style="padding:0;margin:0;width:${cell_size}px;height:${cell_size}px;background-color: white;display: inline-block" class="mine-sweeper-grid" x="${x}" y="${y}">${v}</div>`
            })
            content += '</div>'
        })

        $("#game_board").html(content)


        $(".mine-sweeper-grid").on("click", function (e) {
            var payload = { x: parseInt($(this).attr("x")), y: parseInt($(this).attr("y")) }
            $.postJSON(`${back_end}/minesweeper/pos`, JSON.stringify(payload), function (data, s) {
                if (s) {
                    updateGrid(data)
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
                updateGrid(data)
            } else {
                console.log("/minesweeper/init failed")
            }
        })
    });

});