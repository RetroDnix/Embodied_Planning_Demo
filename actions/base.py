from actions.vla import vla
from actions.vlm import vlm_check, vlm_find
from actions.utils import wait

# --------------------------------------------------
# Base Robot API
# --------------------------------------------------

def check(condition: str) -> bool:
    """Check if environment meets specified condition
    
    Examples:
        check("door_open")
        check("at_3rd_floor")
    
    """
    return vlm_check(condition)

def find(obj: str) -> bool:
    """Detect presence of specified object in environment

    Examples:
        find("emergency_exit")
        find("blue_helmet")

    
    """
    return len(vlm_find(obj)) > 0

def execute(command: str) -> None:
    """Execute primitive robot action
    
    Examples:
        execute("turn_right_90deg")
        execute("grab_object cup")
    
    """
    vla(command)
