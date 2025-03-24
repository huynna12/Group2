from picarx import Picarx
from time import sleep

px = Picarx()

# Please run ./calibration/grayscale_calibration.py to Auto calibrate grayscale values
# or manually modify reference value by following the code
px.set_line_reference([1400, 1400, 1400])

current_state = None
px_power = 2
offset = 20
last_state = "stop"

def outHandle():
    global last_state, current_state
    # Instead of moving backward, try turning to help the robot find the line again
    if last_state == 'left':
        px.set_dir_servo_angle(-offset)
        px.forward(px_power)  # Move forward with a slight left angle to adjust
    elif last_state == 'right':
        px.set_dir_servo_angle(offset)
        px.forward(px_power)  # Move forward with a slight right angle to adjust
    sleep(0.001)

def get_status(val_list):
    """Get the car's state based on grayscale values."""
    _state = px.get_line_status(val_list)  # [1 = line (black), 0 = background (white)]
    
    # Prioritize forward detection first (middle sensor sees black)
    if _state[1] == 1:  # middle sensor sees black (line detected)
        return 'forward'
    
    # Handle turning cases
    elif _state[0] == 1:  # Left sensor sees black (line detected)
        return 'left'
    elif _state[2] == 1:  # Right sensor sees black (line detected)
        return 'right'
    
    # If all sensors see white (no line detected)
    else:
        return 'stop'

def adjust_turn_direction(gm_state):
    """Adjust the turning behavior based on current state."""
    if gm_state == 'left':
        px.set_dir_servo_angle(-offset)  # turn left
        px.forward(px_power)  # move slightly forward while turning
    elif gm_state == 'right':
        px.set_dir_servo_angle(offset)  # turn right
        px.forward(px_power)  # move slightly forward while turning

if __name__=='__main__':
    try:
        while True:
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("gm_val_list: %s, %s"%(gm_val_list, gm_state))

            if gm_state != "stop":
                last_state = gm_state

            # Forward movement when the center sees the line (middle sensor sees black)
            if gm_state == 'forward':
                px.set_dir_servo_angle(0)  # center servo angle
                px.forward(px_power)
            
            # Turning left when the left sensor sees the line (left sensor sees black)
            elif gm_state == 'left':
                adjust_turn_direction('left')
            
            # Turning right when the right sensor sees the line (right sensor sees black)
            elif gm_state == 'right':
                adjust_turn_direction('right')
                
            # If no line is detected (all sensors see white)
            else:
                outHandle()

    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)