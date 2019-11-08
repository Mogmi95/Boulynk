
$(document).ready(function () {


    socket.on("test", function (data) {
        console.log(data)
    })
    socket.on("game_update", function (data) {
        $("#game_config").hide()
        $("#game_board").show()
        // console.log(JSON.parse(data), data)
        data = JSON.parse(data)
        for (var key in data) {
            updateGrid(key, data[key]["status"], data[key]["grid"])
        }
    })

    function updateGrid(id, status, grid) {
        grid_size = grid.size
        var content = ""
        grid.forEach(function (sub, x) {
            content += `<div class="mine_row">`
            sub.forEach(function (v, y) {
                value = v
                if (v <= 0) {
                    value = " ";
                }
                oddness = (x + y) % 2 == 0 ? "odd" : "even"
                content += `<div class="mine mine_${v} ${oddness}" x="${x}" y="${y}">${value}</div>`
            })
            content += '</div>'
        })
        content = `<div class='mine_field'>${content}</div>`
        content += "<div id=final_screen></div>"


        $(`#${id}`).html(content)
        if (status == 'win') {
            $(`#${id} #final_screen`).html("<img id='win_screen' src='https://img.pngio.com/you-win-png-99-images-in-collection-page-1-win-png-650_468.jpg' />")
            $("#game_config").show()
        } else if (status == 'lose') {
            console.log("loser");
            $(`#${id} #final_screen`).html("<img id='lose_screen' src='https://cdn.futura-sciences.com/buildsv6/images/wide1920/4/4/2/44209deae5_96298_bombe-hydrogene.jpg' />")
            $("#game_config").show()
        } else {
            // We add callbacks only if game has not ended.
            if (id != "user_board") {
                // We don't click on other user cells.
                return;
            }
            $(`#${id} .mine`).on("click", function (e) {
                var payload = { x: parseInt($(this).attr("x")), y: parseInt($(this).attr("y")) }

                socket.emit('grid_click', JSON.stringify(payload))
            })
        }
    }

    $("#GO").on("click", function (e) {

        // Send size
        var width = parseInt($('#width').val());
        var height = parseInt($('#height').val());
        var nb_bomb = parseInt($('#nb_bomb').val());
        var payload = {
            "nb_bomb": nb_bomb,
            "width": width,
            "height": height
        }

        $.postJSON(`${back_end}/minesweeper/init`, JSON.stringify(payload), function (data, success) {
            if (success) {
                $("#game_config").hide()
                $("#game_board").show()
                $("#user_ready").on("click", function () {
                    socket.emit("user_ready");
                })
            } else {
                console.log("/minesweeper/init failed")
            }
        })
    });

    $.getJSON(`${back_end}/minesweeper/get`, function(data, success) {
        if (success) {
            if (data.hasOwnProperty("no_grid")) {
                return;
            }

            $("#game_config").hide()
            $("#game_board").show()
            for (var key in data) {
                updateGrid(key, data[key]["status"], data[key]["grid"])
            }
        } else {
            console.log("/minesweeper/init failed")
        }
    })

});