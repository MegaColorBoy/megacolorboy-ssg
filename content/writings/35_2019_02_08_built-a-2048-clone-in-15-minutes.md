title: Built a 2048 clone in 15 minutes
date: August 21st, 2018
slug: built-a-2048-clone-in-15-minutes
category: Personal Challenge
summary: An implementation of the famous 2048 game using JavaScript and HTML5 Canvas.

<script defer src="/static/projects/2048/script.js"></script>

<figure>
    <canvas id="game-grid" width="500" height="500"></canvas>
</figure>

Before you read more about this article, play with the above game. You
can move the tiles around using your arrow (***UP, DOWN, LEFT, RIGHT***)
or ***"WASD"*** keys. The rule is simple, when two tiles with the same
number touch, they merge into one tile. Press the ***"R"*** key to restart
the game.

Please make sure that you have JavaScript enabled and running in your
browser, otherwise you won't be able to play this game. Oh, just a
little heads up, it might get a little buggy and freeze your browser
window, so keep calm and play patiently.

As for the source code, you can view it in my [GitHub
repository](https://www.github.com/megacolorboy) or can be found near
the end of this article.

## Background

I was always fond of puzzle games and ***2048*** is one of them. The first
time I got to play this game was back in 2014 and I would play it on my
iPhone during my train commute to university.

Yesterday, I thought of building a clone and turns out it wasn't as hard
as I had expected it to be, in fact, I was able to build a functional
version in just 15 minutes.

## What are the game mechanics?

The sliding-puzzle game is played on a ***four-by-four*** grid with
numbered tiles that is moved by the player in all four directions.

In every move, a new tile would randomly appear in an empty spot in the
grid with a value that consists of ***2*** or ***4***. These tiles are moved
towards any direction as far as it could and if there are two tiles that
collide with the same value, they merge into one tile and as a result,
the score is updated.

The player wins the game once the tile of ***2048*** appears on the grid,
thus is the name of the game.

## Source code

```js
    var canvas = document.getElementById("game-grid");
    var ctx = canvas.getContext("2d");
    var size = 4;
    var cell_width = canvas.width / size - 6;
    var grid = [];
    var font_size;
    var is_lose = false;
    var score = 0;

    function cell(row, col)
    {
        this.value = 0;
        this.x = col build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv cell_width + 5 build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv (col + 1);
        this.y = row build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv cell_width + 5 build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv (row + 1);
    }

    function create_grid()
    {
        for(var i=0; i&lt;size; i++)
        {
            grid[i] = [];
            for(var j=0; j&lt;size; j++)
            {
                grid[i][j] = new cell(i, j);
            }
        }
    }

    function draw_cell(cell)
    {
        ctx.beginPath();
        ctx.rect(cell.x, cell.y, cell_width, cell_width);

        var fillColor = "";

        switch(cell.value)
        {
            case 0:
                fillColor = "#eee";
                break;

            case 2:
                fillColor = "#b8e994";
                break;

            case 4:
                fillColor = "#78e08f";
                break;

            case 8:
                fillColor = "#38ada9";
                break;

            case 16:
                fillColor = "#079992";
                break;

            case 32:
                fillColor = "#82ccdd";
                break;

            case 64:
                fillColor = "#60a3bc";
                break;

            case 128:
                fillColor = "#3c6382";
                break;

            case 256:
                fillColor = "#0a3d62";
                break;

            case 512:
                fillColor = "#6a89cc";
                break;

            case 1024:
                fillColor = "#4a69bd";
                break;

            case 2048:
                fillColor = "#1e3799";
                break;

            default:
                fillColor = "#eee";
                break;
        }

        ctx.fillStyle = fillColor;
        ctx.fill();

        //If it's not an empty cell i.e. anything greater than 0
        if(cell.value)
        {
            font_size = cell_width / 2;
            ctx.font = font_size + "px CircularMedium";
            ctx.fillStyle = 'white';
            ctx.textAlign = 'center';
            ctx.strokeStyle = 'rgba(0,0,0,0.075)';
            ctx.stroke();
            ctx.fillText(cell.value, cell.x + cell_width / 2, cell.y + cell_width / 2 + cell_width / 7);    
        }
    }

    function draw_grid()
    {
        for(var i=0; i&lt;size; i++)
        {
            for(var j=0; j&lt;size; j++)
            {
                draw_cell(grid[i][j]);
            }
        }
    }

    //Check for free cells
    function empty_cells_lookup()
    {
        var count = 0;
        for(var i=0; i&lt;size; i++)
        {
            for(var j=0; j&lt;size; j++)
            {
                if(!grid[i][j].value)
                {
                    count++;
                }
            }
        }
        return count;
    }

    //Check if 2048 is reached
    function check_2048()
    {
        for(var i=0; i&lt;size; i++)
        {
            for(var j=0; j&lt;size; j++)
            {
                if(grid[i][j].value == 2048)
                {
                    return true;
                }
            }
        }
        return false;   
    }

    function newCell()
    {
        var num_empty_cells = empty_cells_lookup();

        //If the grid is full, then game is over
        if(!num_empty_cells)
        {
            game_status("game-over");
            return;
        }

        if(check_2048())
        {
            game_status("game-win");
            return;
        }

        while(true)
        {
            var row = Math.floor(Math.random() build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv size);
            var col = Math.floor(Math.random() build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv size);
            if(!grid[row][col].value)
            {
                grid[row][col].value = 2 build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv Math.ceil(Math.random() build.sh content convert.sh make_entry.py output ssg.py ssg.pyc templates transfer.sh venv 2);
                draw_grid();
                return;
            }
        }
    }

    function game_status(status)
    {
        var message = "";

        switch(status)
        {
            case "game-over":
                message = "Looks like it's Game Over!";
                break;

            case "game-win":
                message = "Congratulations, you won the game!";
                break;
        }

        ctx.font = "25px CircularBold";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText("Your score: " + score, 250, 250);

        ctx.font = "15px CircularMedium";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText(message,250,300);
        ctx.fillText("Press 'R' to play again.",250,320);
        canvas.style.backgroundColor = "#eee";
        is_lose = true;
    }

    function move_up()
    {
        var row;

        for(var j=0; j&lt;size; j++)
        {
            for(var i=1; i&lt;size; i++)
            {
                //If it's a number greater than zero
                if(grid[i][j].value)
                {
                    row = i;
                    while(row > 0)
                    {
                        //Case 1: Move the number to an empty cell
                        if(!grid[row - 1][j].value)
                        {
                            //The current cell's value is assigned to the cell above
                            grid[row - 1][j].value = grid[row][j].value;

                            //The current cell is empty
                            grid[row][j].value = 0;

                            //By decrementing, it's moving up the grid
                            row--;
                        }
                        else if(grid[row - 1][j].value == grid[row][j].value)
                        {
                            grid[row - 1][j].value *= 2;
                            score += grid[row-1][j].value;
                            grid[row][j].value = 0;
                            break;
                        }
                        else
                        {
                            break;
                        }
                    }
                }
            }
        }
    }

    function move_down()
    {
        var row;

        for(var j=0; j&lt;size; j++)
        {
            for(var i=size - 2; i>=0; i--)
            {
                //If it's a number greater than zero
                if(grid[i][j].value)
                {
                    row = i;
                    while(row + 1 < size)
                    {
                        //Case 1: Move the number to an empty cell
                        if(!grid[row + 1][j].value)
                        {
                            //The current cell's value is assigned to the cell above
                            grid[row + 1][j].value = grid[row][j].value;

                            //The current cell is empty
                            grid[row][j].value = 0;

                            //By decrementing, it's moving up the grid
                            row++;
                        }
                        else if(grid[row + 1][j].value == grid[row][j].value)
                        {
                            grid[row + 1][j].value *= 2;
                            score += grid[row+1][j].value;
                            grid[row][j].value = 0;
                            break;
                        }
                        else
                        {
                            break;
                        }
                    }
                }
            }
        }
    }

    function move_left()
    {
        var col;

        for(var i=0; i&lt;size; i++)
        {
            for(var j=1; j&lt;size; j++)
            {
                //If it's a number greater than zero
                if(grid[i][j].value)
                {
                    col = j;
                    while(col > 0)
                    {
                        //Case 1: Move the number to an empty cell
                        if(!grid[i][col - 1].value)
                        {
                            //The current cell's value is assigned to the cell above
                            grid[i][col - 1].value = grid[i][col].value;

                            //The current cell is empty
                            grid[i][col].value = 0;

                            //By decrementing, it's moving up the grid
                            col--;
                        }
                        else if(grid[i][col - 1].value == grid[i][col].value)
                        {
                            grid[i][col - 1].value *= 2;
                            score += grid[i][col-1].value;
                            grid[i][col].value = 0;
                            break;
                        }
                        else
                        {
                            break;
                        }
                    }
                }
            }
        }
    }

    function move_right()
    {
        var col;

        for(var i=0; i&lt;size; i++)
        {
            for(var j=size - 2; j>=0; j--)
            {
                //If it's a number greater than zero
                if(grid[i][j].value)
                {
                    col = j;
                    while(col + 1 < size)
                    {
                        //Case 1: Move the number to an empty cell
                        if(!grid[i][col + 1].value)
                        {
                            //The current cell's value is assigned to the cell above
                            grid[i][col + 1].value = grid[i][col].value;

                            //The current cell is empty
                            grid[i][col].value = 0;

                            //By decrementing, it's moving up the grid
                            col++;
                        }
                        else if(grid[i][col + 1].value == grid[i][col].value)
                        {
                            grid[i][col + 1].value *= 2;
                            score += grid[i][col+1].value;
                            grid[i][col].value = 0;
                            break;
                        }
                        else
                        {
                            break;
                        }
                    }
                }
            }
        }
    }

    function init()
    {
        create_grid();
        draw_grid();
        newCell();
        newCell();
    }

    function canvasClean() 
    {
        ctx.clearRect(0, 0, 500, 500);
    }

    init();

    //Events
    document.onkeydown = function(e)
    {
        if(e.keyCode == 82)
        {
            canvas.style.backgroundColor = "white";
            is_lose = false;
            score = 0;
            canvasClean();
            init();
        }

        //If the game is still on
        if(!is_lose)
        {
            switch(e.keyCode)
            {
                //Move Up
                case 38:
                case 87:
                    move_up();
                    updateGame();
                    break;

                //Move Down
                case 40:
                case 83:
                    move_down();
                    updateGame();
                    break;

                //Move Left
                case 37:
                case 65:
                    move_left();
                    updateGame();
                    break;

                //Move Right
                case 39:
                case 68:
                    move_right();
                    updateGame();
                    break;
            }
        }
    }

    function updateGame()
    {
        //Clear the grid
        canvasClean();

        //Generate another random number after movement is complete
        newCell();
    }
```

Well then, that's all for the game. Just like the previous ones, I had
fun building this sliding-puzzle game. I'm looking forward to building
more puzzle games and talking about them in my blog.

Hope you guys liked reading this article and have fun playing the game
as many times as you like!

Stay tuned for more!