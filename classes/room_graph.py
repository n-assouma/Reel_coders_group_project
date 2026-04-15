### Amir_H Javadi_B - 5717292
import room as rm

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
            if room2.name in room1.connected:       # TODO 1:  check what is saved in the connected list (I assumed name)
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
