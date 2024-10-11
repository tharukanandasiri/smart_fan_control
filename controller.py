import pyfirmata


comport = 'COM3'
board = pyfirmata.Arduino(comport)


curr_speed = 0
saved_speed = 1  


motor_speed = board.get_pin('d:10:p')

def control(state):
    global curr_speed, saved_speed

    
    state_to_speed = {
        'Speed 1': 0.3,    #Low
        'Speed 2': 0.6,    #Medium
        'Speed 3': 1       #Full
    }

    
    if state == 'OFF':
        curr_speed = 0
        motor_speed.write(curr_speed)
        print(f"Fan turned off, speed saved: {saved_speed}")

    
    elif state in state_to_speed:
        saved_speed = state_to_speed[state]  
        if curr_speed != 0:
            curr_speed = saved_speed
            motor_speed.write(curr_speed)
            print(f"Motor speed updated to {curr_speed} for state '{state}'")
        else:
            print(f"Speed set to {saved_speed}, but fan is off. Speed will apply when turned on.")

    
    elif state == 'ON':
        if curr_speed == 0:  
            curr_speed = saved_speed  
            motor_speed.write(curr_speed)
            print(f"Fan turned on, motor speed set to {curr_speed}")