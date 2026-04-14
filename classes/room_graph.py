### Amir_H Javadi_B - 5717292
import room as rm

list_of_rooms = [
    rm.police_station,
    rm.elenas_office,
    rm.security_booth,
    rm.marcuss_home,
    rm.lena_apartment,
    rm.victors_townhouse,
    rm.faculty_dinning_hall
    ]

# room_graph is a two-dimensional dictionary (adjacency matrix)
# room_graph[room1][room2] shows whether the player can move from room1 to room2
# values:
# -1 -> path exists but is locked
#  0 -> no connection
#  1 -> path is available

room_graph = dict()

for room in list_of_rooms:
    room_graph[room] = dict()

for room1 in list_of_rooms:
    for room2 in list_of_rooms:
        if room2.name in room1.connected:       # TODO 1:  check what is saved in the connected list (I assumed name)
            room_graph[room1][room2] = 1
        else:
            room_graph[room1][room2] = 0
# locking the connections which initially are locked 
for room in list_of_rooms:
    if room.name in rm.victors_townhouse.connected:        # TODO 1
        room_graph[room][rm.victors_townhouse] = -1 
        room_graph[rm.victors_townhouse][room] = -1 
    if room.name in rm.faculty_dinning_hall.connected:     # TODO 1
        room_graph[room][rm.faculty_dinning_hall] = -1 
        room_graph[rm.faculty_dinning_hall][room] = -1 
