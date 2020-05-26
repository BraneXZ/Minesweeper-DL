$(document).ready(function () {
    var $container = $('#main-container');
    var agent_game_status = 0;

    $('#new-game-button').on('click', function() {
        newGame();
    });
    
    $('#agent-button').on('click', async function() {
        newGame();
        while (agent_game_status === 0){
            await sleep(500);
            playAgent();
            console.log(`Current game status: ${agent_game_status}`);
        }
        agent_game_status = 0;
    });


    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function updateBoard(board){
        $container.html('');
        $container.css('grid-template-columns', 'repeat(' + board.board[0].length + ', auto)');
        board.board.forEach(function(row, i){
            row.forEach(function (val, j) {
                var src = `"/static/minesweeper_img/${val}.png"`;
                $container.append(`<img id="${i}x${j}" class="unclicked" src=${src} alt="field" width="40" height="40">`);
            });
        });
        $container.css('visibility','visible');
    }

    function playAgent(){
        $.ajax({
            type: 'GET',
            async: false,
            url: '/playAgent',
            data:{
                "agent": $('#agent').val()
            },
            success: function(data){
                updateBoard(data)
                agent_game_status = data.status;
                console.log(`Agent select row: ${data.select_row}\nAgent select col: ${data.select_col}`)
            },
            error: function(){
                alert("Error playing agent");
            }
        });
    }

    function newGame(){
        $.ajax({
            type: 'GET',
            url: '/newBoard',
            async: false,
            data: {
                "row": $('#row').val(),
                "col": $('#col').val(),
                "mine": $('#mine').val()
            },
            success: function(data){
                updateBoard(data)
            },
            error: function(){
                alert('Error loading new game')
            }
        });

    }

    $container.on('click', '.unclicked', function() {
        var str = $(this).attr('id');
        var clickedXY = str.split('x');
        console.log(`${clickedXY[0]} - ${clickedXY[1]} was clicked. Str: ${str}`);

        $.ajax({
            type: 'GET',
            url: '/applyMove',
            data: {
                "row": clickedXY[0],
                "col": clickedXY[1]
            },
            success: function(data){
                console.log(`Game status: ${data.status}`);
                updateBoard(data);
                if (data.status === 1){
                    alert("You win!");
                }
                else if (data.status === -1){
                    alert("You lost nerd!");
                }


            },
            error: function(){
                alert('Error applying move');
            }
        });
    });
});