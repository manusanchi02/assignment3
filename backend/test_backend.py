#Enum per stati del sistema
from enum import Enum
class State(Enum):
    NORMAL = 0, "Normal"
    ALARM_TOO_LOW = 1, "Alarm too low"
    PRE_ALARM_TOO_HIGH = 2, "Pre-alarm too high"
    ALARM_TOO_HIGH = 3, "Alarm too high"
    ALARM_TOO_HIGH_CRITIC = 4, "Alarm too high critic"
    
state = State.NORMAL

print("stato: " + str(state.value[1]))    

print("stato1: " + str(State.NORMAL.value[1]))