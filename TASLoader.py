print(r"""
    
    
            ___               _____ ___   _____    _                     _           
           |_  |             |_   _/ _ \ /  ___|  | |                   | |          
    __   __  | | ___  _   _    | |/ /_\ \\ `--.   | |     ___   __ _  __| | ___ _ __ 
    \ \ / /  | |/ _ \| | | |   | ||  _  | `--. \  | |    / _ \ / _` |/ _` |/ _ \ '__|
     \ V /\__/ / (_) | |_| |   | || | | |/\__/ /  | |___| (_) | (_| | (_| |  __/ |   
      \_/\____/ \___/ \__, |   \_/\_| |_/\____/   \_____/\___/ \__,_|\__,_|\___|_|   
                       __/ |                                                         
                      |___/                                                          
  
  Primary authors:
  -  luminousLamp367
  Contributors:
  
""")
from helpstr import *
import pyvjoy
from time import sleep, perf_counter
import pathlib
my_dir = pathlib.Path(__file__).parent.absolute()
import pymem
loaded_file = ''
game = input("\nWhat game to load? \n> ")
while 1:
    if game.lower() == 'hue':
        try:
            from read_memory_hue import get_isEnabled
            break
        except pymem.exception.ProcessNotFound as e:
            s = input(f"\nERROR: unable to find Hue.exe. Please ensure Hue is open, then try again.\n")
    else: break
    game = input("\nWhat game to load? \n> ")
print()
import traceback
error_level = 0

class Controller:
    inputs = ('A','B','X','Y','LB','RB','LT','RT','SELECT','START','LSDOWN','RSDOWN','UP','DOWN','LEFT','RIGHT','RSx','RSy','LSx','LSy')
    buttons = ('A','B','X','Y','LB','RB','SELECT','START','LSDOWN','RSDOWN','UP','DOWN','LEFT','RIGHT')
    axes = ('RSx','RSy','LSx','LSy')
    sliders = ('LT','RT')
    def __init__(self):
        self.j = pyvjoy.VJoyDevice(2)
        self.A = 0
        self.B = 0
        self.X = 0
        self.Y = 0
        self.LB = 0
        self.RB = 0
        self.SELECT = 0
        self.START = 0
        self.LSDOWN = 0
        self.RSDOWN = 0
        self.UP = 0
        self.DOWN = 0
        self.LEFT = 0
        self.RIGHT = 0

        self.RSx = 0
        self.RSy = 0
        self.LSx = 0
        self.LSy = 0

        self.LT = 0
        self.RT = 0

    def set_buttons(self, A=0, B=0, X=0, Y=0, LB=0, RB=0, SELECT=0, START=0, LSDOWN=0, RSDOWN=0, UP=0, DOWN=0, LEFT=0, RIGHT=0):
        self.A = int(A)
        self.B = int(B)
        self.X = int(X)
        self.Y = int(Y)
        self.LB = int(LB)
        self.RB = int(RB)
        self.SELECT = int(SELECT)
        self.START = int(START)
        self.LSDOWN = int(LSDOWN)
        self.RSDOWN = int(RSDOWN)
        self.UP = int(UP)
        self.DOWN = int(DOWN)
        self.LEFT = int(LEFT)
        self.RIGHT = int(RIGHT)

    def set_joysticks(self, stick:int=0, x:float=0, y:float=0):
        if stick == 0:
            self.LSx = x
            self.LSy = y
        else:
            self.RSx = x
            self.RSy = y
            
    def set_sliders(self, LT:float=0, RT:float=0):
        self.LT = LT
        self.RT = RT

    def commit(self):
        self.j.data.lButtons = int(sum((
            self.A*1, self.B*2, self.X*4, self.Y*8, self.LB*16, self.RB*32, self.SELECT*64, self.START*128,
            self.LSDOWN*256, self.RSDOWN*512, self.UP*1024, self.DOWN*2048, self.LEFT*4096, self.RIGHT*8192)))
        self.j.data.wAxisX = int(0x4000 + 0x4000 * self.LSx)
        self.j.data.wAxisY = int(0x4000 - 0x4000 * self.LSy)
        self.j.data.wAxisZ = int(0x4000 + 0x4000 * self.RSx)
        self.j.data.wAxisXRot = int(0x4000 - 0x4000 * self.RSy)
        self.j.data.wSlider = int(0x8000 * self.LT)
        self.j.data.wDial = int(0x8000 * self.RT)
        return self.j.update()

    def reset(self):
        self.A = 0
        self.B = 0
        self.X = 0
        self.Y = 0
        self.LB = 0
        self.RB = 0
        self.SELECT = 0
        self.START = 0
        self.LSDOWN = 0
        self.RSDOWN = 0
        self.UP = 0
        self.DOWN = 0
        self.LEFT = 0
        self.RIGHT = 0

        self.RSx = 0
        self.RSy = 0
        self.LSx = 0
        self.LSy = 0

        self.LT = 0
        self.RT = 0

def is_float(string:str):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_int(string:str):
    try:
        int(string)
        return True
    except ValueError:
        return False

def create_steps(raw_steps:list, start=0) -> list:
    num = 0
    steps=[]
    skipping = False
    while num < len(raw_steps):
        step = raw_steps[num]
        if step[0] == '': pass
        elif step[0][:2] == '//': pass
        elif step[0][0] == '!':
            if step[0][1:] == 'tps': steps.append((step[0], int(step[1])));
        elif step[0] == 'SKIP': skipping = True
        elif skipping: skipping = step[0] != 'CONTINUE'
        elif step[0] == 'REPEAT':
            opened=1
            offset=0
            while opened: #find offset
                offset+=1
                if raw_steps[num+offset][0] == 'REPEAT': opened+=1
                if raw_steps[num+offset][0] == 'RESUME': opened-=1
            extra = create_steps(raw_steps[num+1:num+offset], start=num+1) #recursive call to get the steps inside the block
            for i in range(int(step[1])): steps.extend(extra) #add the steps inside the block for each repetition
            num+=offset+1 #Go to the next step after the block
        elif step[0] == 'wait': steps.append(('wait',start+num+1)) #the second number is the user line ref
        else: #If it gets to here, it is a controller step
            t = float(step[0])
            data = {}
            for arg in step[1:]:
                name, val = arg.split('=')
                data[name] = float(val)
            steps.append((t,data))
        num+=1
    return steps

def find_errors(steps:list):
    last_preamble=0
    open_skip = None
    open_repeats=[]
    for index in range(len(steps)):
        step = steps[index]
        if step[0] == '': last_preamble+=1; continue #ignore blanks
        if step[0][:2] == '//': last_preamble+=1; continue #ignore comments
        if step[0][0] == '!': #preamble
            if index != last_preamble: print(f"\nERROR in user script (line {index+1}):\n\tPreamble statements must proceed all other non-comment statements.\n");return True
            last_preamble+=1
            if step[0][1:] == 'tps':
                if len(step)==1:print(f"\nERROR in user script (line {index+1}):\n\tPreamble 'tps' requires argument [value (int)]..\n");return True
                if len(step)>2:print(f"\nERROR in user script (line {index+1}):\n\tPreamble 'tps' takes exactly one additional argument (got {len(step)-1}).\n");return True
                if not is_int(step[1]): print(f"\nERROR in user script (line {index+1}):\n\tArgument 'value' in preamble 'tps' must be an integer.\n");return True
                continue
            else: print(f"\nERROR in user script (line {index+1}):\n\tUnknown preamble '{step[0][1:]}'.\n");return True
        if step[0] == 'SKIP':
            if len(step) == 1: open_skip=(index,list(open_repeats)); continue
            else: print(f"\nERROR in user script (line {index+1}):\n\t'SKIP' takes no additional arguments.\n");return True
        if step[0] == 'CONTINUE':
            if open_skip is None: print(f"\nWARNING in user script (line {index + 1}):\n\t'CONTINUE' has no pairing 'SKIP'.\n")
            elif open_skip[1] != open_repeats:
                print(f"\nWARNING in user script (line {index + 1}):\n\t'CONTINUE' is in a different repetition block to its pairing 'SKIP' (from line {open_skip[0]+1}).\n")
            if len(step) == 1: open_skip=None; continue
            else: print(f"\nERROR in user script (line {index+1}):\n\t'CONTINUE' takes no additional arguments.\n");return True
        if step[0] == 'RESUME':
            if not open_repeats: print(f"\nERROR in user script (line {index+1}):\n\t'RESUME' has no pairing 'REPEAT'.\n");return True
            if len(step) == 1: open_repeats.pop(); continue
            else: print(f"\nERROR in user script (line {index+1}):\n\t'RESUME' takes no additional arguments.\n");return True
        if step[0] == 'REPEAT':
            if len(step) == 1: print(f"\nERROR in user script (line {index+1}):\n\t'REPEAT' requires argument [repetitions (int)].\n");return True
            elif len(step) > 2: print(f"\nERROR in user script (line {index+1}):\n\t'REPEAT' takes exactly one additional argument (got {len(step)-1}).\n");return True
            elif not is_int(step[1]): print(f"\nERROR in user script (line {index+1}):\n\targument [repetitions] in 'REPEAT' must be an integer.\n");return True
            else: open_repeats.append(index); continue
        if step[0] == 'wait':
            if game.lower() not in ('hue'): print(f"\nERROR in user script (line {index+1}):\n\t'wait' is not defined for game '{game}'.\n");return True
            elif len(step)>1: print(f"\nERROR in user script (line {index+1}):\n\t'wait' takes no additional arguments.\n");return True
            else: continue
        #If it is not a keyword, expect a step
        if not is_float(step[0]): print(f"\nERROR in user script (line {index+1}):\n\tUnknown keyword '{step[0]}'.\n");return True
        for arg in step[1:]:
            pair = arg.strip('\t ').replace(':','=').split('=',1)
            if pair[0] not in Controller.inputs: print(f"\nERROR in user script (line {index+1}):\n\tUnknown button {pair[0]}.\n");return True
            if len(pair)==1: print(f"\nERROR in user script (line {index+1}):\n\tButton/axis/slider {pair[0]} was never assigned a value.\n");return True
            if pair[1]=='': print(f"\nERROR in user script (line {index+1}):\n\tButton/axis/slider {pair[0]} was never assigned a value.\n");return True
            if pair[0] in Controller.buttons and not is_int(pair[1]):
                print(f"\nERROR in user script (line {index + 1}):Value of button {pair[0]} must be an integer\n\t.\n");return True
            if not is_float(pair[1]): print(f"\nERROR in user script (line {index+1}):Value of axis/slider {pair[0]} must be a number\n\t.\n");return True
            if pair[0] in Controller.buttons and int(pair[1]) not in (0,1):
                print(f"\nERROR in user script (line {index+1}):Value of button {pair[0]} must be 0 or 1\n\t.\n");return True
            if pair[0] in Controller.axes and not -1 <= float(pair[1]) <= 1:
                print(f"\nERROR in user script (line {index+1}):Value of axis {pair[0]} must be between -1 and 1\n\t.\n");return True
            if pair[0] in Controller.sliders and not 0 <= float(pair[1]) <= 1:
                print(f"\nERROR in user script (line {index+1}):Value of slider {pair[0]} must between 0 and 1\n\t.\n");return True
    if open_skip: print(f"\nWARNING in user script (line {open_skip[0]+1}):\n\t'SKIP' has no pairing 'CONTINUE'.\n")
    for rep in open_repeats:
        print(f"\nERROR in user script (line {rep+1}):\n\t'REPEAT' has no pairing 'RESUME'.\n")
    if open_repeats: return True

    return False

def load_instructions(filepath:str):
    try:
        with open(filepath,'r') as f:
            lines = [f_line.strip('\n\t; ').replace('\t',' ').split(' ') for f_line in f]
            if find_errors(lines): return None
            return create_steps(lines)

    except Exception as e:
        print(f"\nERROR: {traceback.format_exc() if error_level else e}.\n This is most likely an incorrect file path.\n")
        return None


def run_script(script:list):

    #Setup
    try:
        controller = Controller()
    except Exception as e:
        print(f"\n ERROR: {traceback.format_exc() if error_level else ''} Could not access controller successfully. Please ensure no vJoy windows are open.\n")
        return
    last_sync_time = perf_counter()
    completed_since_last_sync = 0

    #Execute the steps
    tps=0
    for step in script:
        try:
            if step[0] == '!tps': tps = step[1]
            elif step[0] == 'wait':
                controller.reset()
                controller.commit()
                if game.lower() == 'hue':
                    try:
                        last_isEnabled = get_isEnabled()
                    except Exception as e:
                        print(f"\nEXECUTION ABORTED: {traceback.format_exc() if error_level else ''} Hue.exe could not be found. Please ensure that Hue is open, then restart this program.\n")
                        return
                    slept_at = perf_counter()
                    while True:
                        new_isEnabled = get_isEnabled()
                        if not last_isEnabled and new_isEnabled:
                            break
                        last_isEnabled = new_isEnabled
                        sleep(0.0001)
                        if perf_counter() - slept_at > 10:
                            print(f"\nEXECUTION ABORTED: 'wait' took more than 10 seconds to return at line {step[1]} in user script.\n")
                            return
                last_sync_time = perf_counter()
                completed_since_last_sync = 0
            else:
                #set controller
                controller.reset()
                for pair in step[1].items():
                    controller.__setattr__(*pair)
                controller.commit()
                #wait
                if tps:
                    while (completed_since_last_sync + step[0])/tps > perf_counter() - last_sync_time:
                        sleep(0.0001)
                else:
                    while completed_since_last_sync + step[0] > perf_counter() - last_sync_time:
                        sleep(0.0001)
                #add its time to the offset
                completed_since_last_sync += step[0]

        except Exception as e:
            print(f"\nERROR: Exception \n{traceback.format_exc() if error_level else e}\nwas raised while running the script.\n")
            break
    controller.reset()
    controller.commit()

def total_time(script):
    # read preamble
    total = 0
    for step in script:
        try:
            total += step[0]
        except TypeError as e:
            continue
    return total

def scale_times(script, scale, filepath):
    for step in script:
        try:
            step[0] = str(int(float(step[0])*scale))
        except ValueError:
            pass
    with open(filepath, 'w') as f:
        f.write('\n'.join(' '.join(step) for step in script))

def steam_setup():
    l = input(
        f"\nGo into Steam Big Picture mode, then navigate to controller settings.\nIf there is a controller listed under 'Detected Controllers', enter 'y'. Otherwise, enter 'n'\n> ")
    if l == 'n':
        try:
            controller = Controller()
        except Exception as e:
            print(f"\n ERROR: {traceback.format_exc() if error_level else ''} Could not access controller successfully. Please ensure no vJoy windows are open.\n")
            return
        controller.set_buttons(A=1); controller.commit()
        sleep(0.1)
        controller.reset(); controller.commit()
        l = input("\nIf you now see a controller, enter 'y'. Otherwise, enter 'n'\n> ")
        if l == 'n': print("\nPlease ensure vJoy is set up properly, then retry.\n"); return
    l = input("\nClick on the controller. If this takes you to a screen that prompts you for inputting bindings, enter 'y'. Otherwise, enter 'n'\n> ")
    if l == 'n':
        input("\nClick on 'DEFINE LAYOUT' and then click on 'RESET'. This should take you to a blank bindings screen. Enter 'y' when done.\n> ")
    input("\nThis program will now guide you through the buttons. For each step, select the relevant box in the 'Button' column for the relevant 'Command' so that only the 'Button' portion of that line is highlighted.\nPlease note that it is normal for 'Guide' to not be bound.\nPress ENTER to begin.\n> ")
    try:
        controller = Controller()
    except Exception as e:
        print(f"\n ERROR: {traceback.format_exc() if error_level else ''} Could not access controller successfully. Please ensure no vJoy windows are open.\n")
        return
    for char in (
        ('A', 'Primary Action'), ('B', 'Go back'), ('Y', 'Tertiary Action'), ('X', 'Secondary Action'),
        ('START', 'Start'), ('SELECT', 'Back'), ('LSDOWN', 'Left Stick Click'), ('RSDOWN', 'Right Stick Click'),
        ('LB', 'Left Shoulder'), ('RB', 'Right Shoulder'), ('UP', 'DPAD Up'), ('LEFT', 'DPAD Left'),
        ('DOWN', 'DPAD Down'), ('RIGHT', 'DPAD Right'), ('LSx', 'Left Stick X'), ('LSy', 'Left Stick Y'),
        ('RSx', 'Right Stick X'), ('RSy', 'Right Stick Y'), ('LT', 'Left Trigger'), ('RT', 'Right Trigger')
    ):
        input(f"\nSelect the box for '{char[1]}' in the Steam window, then press ENTER in this window.\n> ")

        if char[0] in Controller.sliders: #Steam only accepts sliders if they slide by 1% increments for a certain distance
            for i in range(90):
                setattr(controller, char[0], 0.01*i); controller.commit()
                sleep(0.001)
        else:
            setattr(controller, char[0], 1); controller.commit()
            sleep(0.2)
        controller.reset(); controller.commit()
    input(f"\nNow you may save an exit, making sure that you set the controller as a generic gamepad. Press ENTER to end the setup walkthrough.\n> ")

if __name__ == '__main__':
    line = "line"
    current_script= None
    while line:
        line = input("""Enter:
        'load [filepath]' to load a script, 
        'reload' to reload the last script loaded, 
        'run [optional: preinstalled script name] [delay]' to run a script, 
        'rerun [delay]' to reload the last script and run it, 
        'time' to get the total time of the script (in the timing method of the script),
        'steam_setup' to step through Steam keybinds,
        'help' to get scripting information, 
        'exit' to exit.\n> """)
        try:
            if line.lower() == 'exit': break

            if line.lower()[:4] == 'load':
                current_script = load_instructions(line[5:])
                loaded_file = line[5:]
                if current_script is not None: print('\nScript successfully loaded.\n')

            elif line.lower()[:6] == 'reload':
                if current_script is None: print("\nERROR: No script loaded.\n"); continue
                current_script = load_instructions(loaded_file)
                if current_script is not None: print('\nScript successfully loaded.\n')

            elif line.lower()[:3] == 'run':
                if current_script is None: print("\nERROR: No script loaded.\n"); continue
                try: float(line[4:])
                except ValueError: print("\n ERROR: must supply a delay for 'run'.\n"); continue
                sleep(float(line[4:]))
                run_script(current_script)

            elif line.lower()[:5] == 'rerun':
                try:
                    float(line[6:])
                except ValueError:
                    print("\n ERROR: must supply a delay for 'rerun'.\n"); continue
                if current_script is None: print("\nERROR: No script loaded.\n"); continue
                current_script = load_instructions(loaded_file)
                if current_script is None: continue #Don't try to run erroneous script
                print('\nScript successfully loaded.\n')
                sleep(float(line[6:]))
                run_script(current_script)

            elif line.lower()[:4] == 'time':
                if current_script is None: print("\nERROR: No script loaded.\n"); continue
                print(f"\nTotal time of script: {total_time(current_script)}\n")

            elif line.lower().strip() == 'steam_setup':
                steam_setup()

            elif line.lower() == 'compiled':
                print('\n'.join(' '.join((str(i),str(current_script[i]))) for i in range(len(current_script))))

            elif line.lower() == 'help':
                if game.lower() == 'hue': print(helpstrHue)
                else: print(helpstrGeneral)

            elif line.lower()[:11] == 'debug_level':
                error_level = int(line.lower()[12:])

            else: print("\nNo commands of that name.\n")
        except Exception as e:
            print(f'\n ERROR: Unknown error of type {traceback.format_exc() if error_level else e}\n')