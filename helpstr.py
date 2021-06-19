helpstrHue = """
Setup video: https://youtu.be/S_gTSuccSwU 

Preamble: at the top of the file, in the form ![type] [arg1] [arg2]...
    (optional) tps: specify the tps for the TAS to match. Takes argument [value (int)].

Instructions:
    wait : will pause until the player has control
    // : A comment. Anything else on this line is ignored when run.
    SKIP : starts skipping all lines
    CONTINUE : stops skipping all lines

Controller Steps: defines an input to be held for a length of time
    Uses [time] [button/stick axis]=[value] [button/stick axis]=[value] ...
    where time is measured in ticks if a tps was given in the 
    preamble, otherwise measured in seconds.
    NOTE: The number of ticks will not necessarily be the same in-game if
          the framerate dips, as the TAS assumes the framerate is constant.
          However, it will resync to be accurate every time 'wait' is used.

Buttons: 1 is down, 0 is up.
    A : A button
    B : B button
    X : X button
    Y : Y button
    LB : left bumper
    RB : right bumper
    SELECT : select button
    START : start button
    LSDOWN : left stick pressed down
    RSDOWN : right stick pressed down
    UP : up on d-pad
    DOWN : down on d-pad
    LEFT : left on d-pad
    RIGHT : right on d-pad

Sticks: -1 is full left/full down, 1 is full right/full up
    RSx : horizontal input on right stick. 
    RSy : vertical input on right stick.
    LSx : horizontal input on left stick.
    LSy : vertical input on left stick.
    
Sliders: 1 is fully on, 0 is fully off
    LT: left trigger
    RT: right trigger
"""
helpstrGeneral = """
Setup video: https://youtu.be/S_gTSuccSwU (This is a video on Hue, but it will show enough of how to set it up)

Preamble: at the top of the file, in the form ![type] [arg1] [arg2]...
    (optional) tps: specify the tps for the TAS to match. Takes argument [value (int)].

Instructions:
    // : a comment. Anything else on this line is ignored when run.
    SKIP : starts skipping all lines
    CONTINUE : stops skipping all lines

Controller Steps: defines an input to be held for a length of time
    Uses [time] [button/stick axis]=[value] [button/stick axis]=[value] ...
    where time is measured in ticks if a tps was given in the 
    preamble, otherwise measured in seconds.
    NOTE: The number of ticks will not necessarily be the same in-game if
          the framerate dips, as the TAS assumes the framerate is constant.

Buttons: 1 is down, 0 is up.
    A : A button
    B : B button
    X : X button
    Y : Y button
    LB : left bumper
    RB : right bumper
    SELECT : select button
    START : start button
    LSDOWN : left stick pressed down
    RSDOWN : right stick pressed down
    UP : up on d-pad
    DOWN : down on d-pad
    LEFT : left on d-pad
    RIGHT : right on d-pad

Sticks: -1 is full left/full down, 1 is full right/full up
    RSx : horizontal input on right stick. 
    RSy : vertical input on right stick.
    LSx : horizontal input on left stick.
    LSy : vertical input on left stick.
    
Sliders: 1 is fully on, 0 is fully off
    LT: left trigger
    RT: right trigger
"""