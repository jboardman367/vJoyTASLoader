# vJoyTASLoader
A program to load and execute simple scripts that control a vJoy virtual input controller. For this to work, the program/game that you want to control must be launched through Steam, whether as a Steam game or a non-Steam game, and it must be launched from Steam's Big Picture Mode.

## Instalation
To run this program, you must have [vJoy](https://github.com/shauleiz/vJoy/releases/tag/v2.1.8.39) installed on your device, and controller 2 active.
Once you have vJoy set up, simply run the executable to start the program.

## First time setup
Once vJoy is active and set up on your device and you have opened the program, use the `steam_setup` command and follow the directions to configure the controller.

## Use
To use the program, you must write your scripts in a text editor, such as Notepad, then load them into vJoyTASLoader using `load [filepath]`. 
Once the files are loaded, run the script using `run [delay]`, which will run the script after `delay` seconds.

To minimise the need to repeatedly load files, `reload` loads the last filepath that was loaded, and `rerun [delay]` reloads the last filepath loaded then runs the script after `delay` seconds.

To time the total length of the elements in the script that have a defined time, use `time`, which will return the total time in the same units that the script is in.

## Scripting
A script consists of an (optional) preamble, followed by a sequence of steps, functions, control structures, and comments. Each one of these should be on a new line, and arguments should be seperated by spaces.
Below is a description of all instructions:

### Preamble
Occurs at the top of the file, in the form `![type]` `[arg1]` `[arg2]`...
- (optional) `tps`: specify the tps for the TAS to match. Takes argument `[value (int)]`. If this is used, all times will be measured in ticks.

### Comment
Any line beginning with `//`. Anything on this line is ignored when the script is loaded.

### Control Structures
Come in pairs, and control the flow of the script
- `SKIP` \- `CONTINUE`: Anything between these lines will be ignored when the script is loaded. Useful for testing portions of a script seperately.
- `REPEAT [count]` \- `RESUME`: Anything between these lines will be repeated `count` times.

### Steps
Defines an input to be held for a length of time.  
Uses the form `[time]` `[button/stick axis/slider]=[value]` `[button/stick axis]=[value]`...  
where `time` is measured in ticks if a `tps` was given in the preamble, otherwise measured in seconds.
**NOTE:** The number of ticks will not necessarily be the same in-game if the framerate dips, as the TAS assumes the framerate is constant.

#### Buttons
1 is down, 0 is up.
- `A` : A button
- `B` : B button
- `X` : X button
- `Y` : Y button
- `LB` : left bumper
- `RB` : right bumper
- `SELECT` : select button
- `START` : start button
- `LSDOWN` : left stick pressed down
- `RSDOWN` : right stick pressed down
- `UP` : up on d-pad
- `DOWN` : down on d-pad
- `LEFT` : left on d-pad
- `RIGHT` : right on d-pad

#### Sticks
-1 is full left/full down, 1 is full right/full up
- `RSx` : horizontal input on right stick. 
- `RSy` : vertical input on right stick.
- `LSx` : horizontal input on left stick.
- `LSy` : vertical input on left stick.
    
#### Sliders
1 is fully on, 0 is fully off
- `LT`: left trigger
- `RT`: right trigger

### Game-specific functions
- `wait` (Hue): Will pause execution of the script until Hue becomes controllable. Will abort the script if it takes longer than 10 seconds

## Building
If you want to use the source files for the code, please note that I have made changes to the ReadWriteMemory module from the PyPi release in order to read boolean data as well as 4 byte int data. Also note that the pyvjoy library will only operate in 64-bit python, and includes a dll that the [repo](https://github.com/tidzo/pyvjoy) it is from doesn't provide. 
Bundling into an .exe: install PyInstaller with pip and do `pyinstaller --onefile --add-binary [some path]\TAS\src\pyvjoy\vJoyInterface.dll;. TASLoader.py` in the command line from inside `src`.
