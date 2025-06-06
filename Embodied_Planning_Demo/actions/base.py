from base.vla import vla
from base.vlm import vlm_check, vlm_find
from base.utils import wait

# --------------------------------------------------
# Base Robot API
# --------------------------------------------------

def execute(command: str) -> None:
    """Execute primitive robot action other than those defined
    
    Examples:
        execute("turn_right_90deg")
        execute("grab_object cup")
    
    """
    vla(command)
    
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

def pick_up(object: str) -> None:
    """Pick up an object
    Examples:
        pick_up("apple")
        pick_up("Coat")
    """
    vla(f"pick up {object}")

def put(object: str, location: str) -> None:
    """Put an object at a specified location
    Examples:
        put("apple", "table")
        put("Coat", "hanger")
    """
    vla(f"put {object} at {location}")

def open(object: str) -> None:
    """Open an object, such as a door or a container
    Examples:
        open("door")
        open("box")
    """
    vla(f"open {object}")

def close(object: str) -> None:
    """Close an object, such as a door or a container
    Examples:
        close("door")
        close("box")
    """
    vla(f"close {object}")

def toggle_on(object: str) -> None:
    """Turn on an object, such as a light or a machine
    Examples:
        toggle_on("light")
        toggle_on("machine")
    """
    vla(f"toggle on {object}")

def toggle_off(object: str) -> None:
    """Turn off an object, such as a light or a machine
    Examples:
        toggle_off("light")
        toggle_off("machine")
    """
    vla(f"toggle off {object}")

def slice(object: str) -> None:
    """Slice an object, such as food
    Examples:
        slice("apple")
        slice("bread")
    """
    vla(f"slice {object}")

def go_to(location: str) -> None:
    """Go to a specific location
    Examples:
        go_to("kitchen")
        go_to("room_2")
    """
    vla(f"go to {location}")

def take(object: str) -> None:
    """Take an object
    Examples:
        take("book")
        take("phone")
    """
    vla(f"take {object}")

def heat(object: str) -> None:
    """Heat an object, such as food
    Examples:
        heat("pizza")
        heat("water")
    """
    vla(f"heat {object}")

def cool(object: str) -> None:
    """Cool an object, such as food
    Examples:
        cool("pizza")
        cool("drink")
    """
    vla(f"cool {object}")

def clean(object: str) -> None:
    """Clean an object or surface
    Examples:
        clean("table")
        clean("floor")
    """
    vla(f"clean {object}")

def inventory() -> None:
    """Check the robot's inventory
    Examples:
        inventory()
    """
    vla("inventory")

def examine(object: str) -> None:
    """Examine an object in the environment
    Examples:
        examine("apple")
        examine("machine")
    """
    vla(f"examine {object}")

def navigate(direction: str) -> None:
    """Navigate in a specified direction
    Examples:
        navigate("north")
        navigate("left")
    """
    vla(f"navigate {direction}")

def place(object: str, location: str) -> None:
    """Place an object at a specified location
    Examples:
        place("apple", "table")
        place("Coat", "rack")
    """
    vla(f"place {object} at {location}")

def push(object: str) -> None:
    """Push an object
    Examples:
        push("box")
        push("door")
    """
    vla(f"push {object}")

def dip(object: str, container: str) -> None:
    """Dip an object into a container
    Examples:
        dip("spoon", "soup")
        dip("apple", "water")
    """
    vla(f"dip {object} into {container}")

def wipe(object: str) -> None:
    """Wipe an object or surface
    Examples:
        wipe("table")
        wipe("window")
    """
    vla(f"wipe {object}")

def switch_on(object: str) -> None:
    """Switch on a device or machine
    Examples:
        switch_on("light")
        switch_on("machine")
    """
    vla(f"switch on {object}")

def switch_off(object: str) -> None:
    """Switch off a device or machine
    Examples:
        switch_off("light")
        switch_off("machine")
    """
    vla(f"switch off {object}")

def put_down(object: str) -> None:
    """Put down an object
    Examples:
        put_down("book")
        put_down("bag")
    """
    vla(f"put down {object}")


def turn_on(object: str) -> None:
    """Turn on a device or system
    Examples:
        turn_on("air_conditioner")
        turn_on("fan")
    """
    vla(f"turn on {object}")

def turn_off(object: str) -> None:
    """Turn off a device or system
    Examples:
        turn_off("air_conditioner")
        turn_off("fan")
    """
    vla(f"turn off {object}")

def grab(object: str) -> None:
    """Grab a specific object
    Examples:
        grab("book")
        grab("pen")
    """
    vla(f"grab {object}")

def explore(area: str) -> None:
    """Explore a specified area
    Examples:
        explore("room")
        explore("garden")
    """
    vla(f"explore {area}")

def fill(container: str, liquid: str) -> None:
    """Fill a container with a specified liquid
    Examples:
        fill("cup", "water")
        fill("bottle", "juice")
    """
    vla(f"fill {container} with {liquid}")

def pour(container: str, liquid: str) -> None:
    """Pour a liquid from one container to another
    Examples:
        pour("bottle", "cup")
        pour("jug", "glass")
    """
    vla(f"pour {liquid} from {container}")

def power_off() -> None:
    """Power off the robot or system
    Examples:
        power_off()
    """
    vla("power off")

def power_on() -> None:
    """Power on the robot or system
    Examples:
        power_on()
    """
    vla("power on")

def wait(time: float) -> None:
    """Wait for a specified time
    Examples:
        wait(10)
    """
    vla(f"wait for {time} seconds")

def drink(container: str) -> None:
    """Drink from a container
    Examples:
        drink("cup")
        drink("bottle")
    """
    vla(f"drink from {container}")

def walk(destination: str) -> None:
    """Walk to a specific destination
    Examples:
        walk("door")
        walk("desk")
    """
    vla(f"walk to {destination}")

def look_at(object: str) -> None:
    """Look at a specific object
    Examples:
        look_at("tree")
        look_at("book")
    """
    vla(f"look at {object}")

def point_at(object: str) -> None:
    """Point at a specific object
    Examples:
        point_at("tree")
        point_at("book")
    """
    vla(f"point at {object}")

def put_on(object: str) -> None:
    """Put on an item of clothing or accessory
    Examples:
        put_on("hat")
        put_on("jacket")
    """
    vla(f"put on {object}")

def put_off(object: str) -> None:
    """Take off an item of clothing or accessory
    Examples:
        put_off("hat")
        put_off("jacket")
    """
    vla(f"put off {object}")

def greet(person: str) -> None:
    """Greet a person
    Examples:
        greet("John")
        greet("Alice")
    """
    vla(f"greet {person}")

def drop(object: str) -> None:
    """Drop an object
    Examples:
        drop("book")
        drop("bag")
    """
    vla(f"drop {object}")

def read(object: str) -> None:
    """Read an object, such as a book or a sign
    Examples:
        read("book")
        read("sign")
    """
    vla(f"read {object}")

def lie() -> None:
    """Lie down
    Examples:
        lie()
    """
    vla("lie down")

def type(command: str) -> None:
    """Type a command or text
    Examples:
        type("hello world")
    """
    vla(f"type {command}")

def pull(object: str) -> None:
    """Pull an object
    Examples:
        pull("door")
        pull("rope")
    """
    vla(f"pull {object}")

def move(direction: str) -> None:
    """Move in a specified direction
    Examples:
        move("forward")
        move("backward")
    """
    vla(f"move {direction}")

def wash(object: str) -> None:
    """Wash an object or surface
    Examples:
        wash("dish")
        wash("clothes")
    """
    vla(f"wash {object}")

def rinse(object: str) -> None:
    """Rinse an object
    Examples:
        rinse("plate")
        rinse("vegetables")
    """
    vla(f"rinse {object}")

def scrub(object: str) -> None:
    """Scrub an object or surface
    Examples:
        scrub("floor")
        scrub("pot")
    """
    vla(f"scrub {object}")

def squeeze(object: str) -> None:
    """Squeeze an object
    Examples:
        squeeze("sponge")
        squeeze("cloth")
    """
    vla(f"squeeze {object}")

def plug_in(device: str) -> None:
    """Plug in a device
    Examples:
        plug_in("charger")
        plug_in("laptop")
    """
    vla(f"plug in {device}")

def plug_out(device: str) -> None:
    """Unplug a device
    Examples:
        plug_out("charger")
        plug_out("laptop")
    """
    vla(f"plug out {device}")

def cut(object: str) -> None:
    """Cut an object, such as food
    Examples:
        cut("apple")
        cut("bread")
    """
    vla(f"cut {object}")

def eat(object: str) -> None:
    """Eat an object, such as food
    Examples:
        eat("apple")
        eat("sandwich")
    """
    vla(f"eat {object}")

def sleep() -> None:
    """Sleep
    Examples:
        sleep()
    """
    vla("sleep")

def wake_up() -> None:
    """Wake up
    Examples:
        wake_up()
    """
    vla("wake up")

def release(object: str) -> None:
    """Release an object
    Examples:
        release("ball")
        release("item")
    """
    vla(f"release {object}")
