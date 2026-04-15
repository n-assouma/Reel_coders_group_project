### Amir_H Javadi_B - 5717292
import room as rm
from collections import deque

list_of_rooms: list = [
    rm.police_station,
    rm.elenas_office,
    rm.security_booth,
    rm.marcuss_home,
    rm.lena_apartment,
    rm.victors_townhouse,
    rm.faculty_dinning_hall
    ]

# Global adjacency matrix - initialised empty, built by functions below
room_graph: dict = dict()

def build_room_graph() -> None:
    """
    Builds adjacency matrix for all rooms.
    Modifies the global room_graph in place.
    """
    # Build adjacency matrix - initialise each room with empty dict
    for room in list_of_rooms:
        room_graph[room] = dict()
    # set connections between rooms(1 for connected, 0 for not connected)
    for room1 in list_of_rooms:
        for room2 in list_of_rooms:
            if room2.name in room1.connected:       # TODO 1: check what is saved in the connected list (I assumed name)
                room_graph[room1][room2] = 1
            else:
                room_graph[room1][room2] = 0
    
def initial_room_locking() -> None:
    """
    Locks initially inaccessible rooms in the global room_graph.
    Sets locked connections to -1.
    """
    for room in list_of_rooms:
        if room.name in rm.victors_townhouse.connected:        # TODO 1
            room_graph[room][rm.victors_townhouse] = -1 
            room_graph[rm.victors_townhouse][room] = -1 
        if room.name in rm.faculty_dinning_hall.connected:     # TODO 1
            room_graph[room][rm.faculty_dinning_hall] = -1 
            room_graph[rm.faculty_dinning_hall][room] = -1 

def bfs_path_checking(origin_room: object, destination_room: object) -> bool: # TODO 2: retrurning the evidence needed when there are a locked room in the path 
    """
    checking whethere there is a available path between 
    the current location of the player and the room they are willing to go 
    Returning: False when there is no fully available path, True when there is a fully availabler path
    """
    queue: deque = deque()
    visited: list = []
    queue.append(origin_room)
    while len(queue) > 0:
        current_room = queue.popleft()
        if current_room == destination_room:
            return True
        for room in list_of_rooms:
            if room_graph[current_room][room] == 1 and room not in visited:
                queue.append(room)
        visited.append(current_room)
    return False

def unlock_room(locked_room: object) -> None:
    """
    unlocking the path of a locked room by changing the -1s to 1s in the room_graph
    """
    for room in list_of_rooms:
        if room_graph[locked_room][room] == -1:
            room_graph[locked_room][room] = 1
            room_graph[room][locked_room] = 1

        
