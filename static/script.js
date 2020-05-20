$(document).ready(function () {
    var $container = $('#main-container');

    $('#new-game-button').on('click', function() {
        $container.css('visibility','hidden');
        $container.html('');
        newGame();
    });
    
    function newGame(){
        console.log($('#row').val());
        $.ajax({
            type: 'GET',
            url: '/newBoard',
            data: {
                "row": $('#row').val(),
                "col": $('#col').val(),
                "mine": $('#mine').val()
            },
            success: function(data){
                $container.css('grid-template-columns', 'repeat(' + data[0].length + ', auto)');
                data.forEach(function(row, i){
                    row.forEach(function (val, j) {
                        var src = `"/static/minesweeper_img/${val}.png"`;
                        $container.append(`<img id="${i}'x'${j}" class="unclicked" src=${src} alt="field" width="40" height="40">`);
                    });
                });
                $container.css('visibility','visible');
            },
            error: function(){
                alert('error loading new game')
            }
        });

    }
});