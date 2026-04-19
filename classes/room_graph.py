### Amir_H Javadi_B - 5717292
"""
room_graph.py

Graph data structure for The Hollow Witness. Implements an
adjacency-list room graph with separately tracked locked edges,
and breadth-first search for shortest-path navigation.
"""
import room as rm
from collections import deque
from typing import Optional 
#TODO: add an error for none existing edges
class RoomGraphError(Exception):
    """Raised when a graph operation receives an invalid room."""
    pass


class EdgeNotExistError(Exception):
    """Raised when a locked_edges operations receives an invalid edge."""
    pass


class RoomGraph:
    """Undirected room graph with lockable edges and BFS pathfinding."""

    def __init__(self, rooms: list[rm.Room]) -> None:
        """Build the adjacency list from a list of Room objects.
        Raises RoomGraphError if rooms is empty.
        """
        if not rooms:
            raise RoomGraphError("room graph cannot be built with no rooms.")
        self.graph: dict[rm.Room, set[rm.Room]] = {}
        self.locked_edges: set[frozenset[rm.Room]] = set()
    
    def build_graph(self, rooms: list[rm.Room]) -> None:
        for room in rooms:
            self.graph[room] = set(room.connections)
    
    def show_graph(self) -> None:
        for room in self.graph.keys():
            for adjacent in self.graph[room]:
                print(f"({room.name}, {adjacent.name})")

    def lock_edge(self, room_a: rm.Room, room_b: rm.Room) -> None:
        """Mark the edge between two rooms as locked. Idempotent."""
        self._validate(room_a, room_b)
        self.locked_edges.add(frozenset((room_a, room_b)))
       
    def unlock_edge(self, room_a: rm.Room, room_b: rm.Room) -> None:
        """Remove the lock from an edge"""
        self._validate(room_a, room_b)
        self.locked_edges.discard(frozenset((room_a, room_b)))
    
    def is_locked(self, room_a: rm.Room, room_b: rm.Room) -> bool:
        """returning True if the edge between two rooms is currently locked"""
        self._validate(room_a, room_b)
        return frozenset((room_a, room_b)) in self.locked_edges
    
    def show_locked_edges(self) -> None:
        for edge in self.locked_edges:
            print("(", end ="")
            for room in edge:
                print(room.name, end=" ")
            print(")")
    
    def _bfs(self, origin: rm.Room, destination: rm.Room, respect_locks: bool) -> Optional[list[rm.Room]]:
        """Return the shortest path from origin to destination, or None if unreachable.

                If respect_locks is True, locked edges are treated as impassable.
                If False, locked edges are traversed as if unlocked — used by
                route_with_blocker to find the structural path before identifying
                the first locked room along it.

                Time complexity: O(V + E).
                V: the number of vertices 
                E: the number of edges
                """
        is_found: bool = False
        shortest_path: list[rm.Room] = []
        child_parent: dict[rm.Room, Optional[rm.Room]] = {}
        queue: deque[rm.Room] = deque()
        queue.append(origin)
        child_parent[origin] = None
        
        while queue:
            current_room: rm.Room = queue.popleft()
            if current_room == destination:
                is_found = True
                break
            for room in self.graph[current_room]:
                if room not in child_parent and not(respect_locks and self.is_locked(current_room, room)):
                    queue.append(room)
                    child_parent[room] = current_room

        if not is_found:
            return None 
        
        path_room: rm.Room = destination 
        while path_room is not None:
            shortest_path.append(path_room)
            path_room = child_parent[path_room]
        
        return shortest_path[::-1]
    
    def is_reachable(self, origin: rm.Room, destination: rm.Room) -> bool:
        """Return True if a currently-passable route exists between the two rooms."""
        self._validate(origin, destination)
        return self._bfs(origin, destination, respect_locks=True) is not None
    
    def route_with_blocker(self, origin: rm.Room, destination: rm.Room) -> Optional[rm.Room]:
        """
        Find the first locked room blocking the shortest structural path.

        Intended to be used together with is_reachable() to distinguish:
            is_reachable True           -> path exists and is open
            returns a Room              -> that room is the first lock on the route
            returns None                -> no structural route exists at all

        Returns the first locked Room on the shortest path (ignoring locks),
        or None if the destination is unreachable even with all locks ignored.
        """
        self._validate(origin, destination)
        path: Optional[list[rm.Room]] = self._bfs(origin, destination, respect_locks=False)
        if path is None:
            return None 
        for i in range(len(path) - 1):
            if self.is_locked(path[i], path[i+1]):
                return path[i+1]

    def _validate(self, *rooms: rm.Room) -> None:
        """Raise RoomGraphError if any of the given rooms is not in the graph."""
        for room in rooms:
            if room not in self.graph:
                raise RoomGraphError(f"room {room.name}, is not in the graph.")
        
    def __repr__(self) -> str:
        """Return a concise debug string showing room count and lock count."""
        return f"RoomGraph(rooms={len(self.graph)}, locked={len(self.locked_edges)})"

## Testing 
rooms = rm.listt_of_rooms

room_graph = RoomGraph(rooms)
room_graph.build_graph(rooms)
#print(room_graph.graph)
#print(room_graph.graph)
#room_graph.show_graph()
"""room_graph.lock_edge(rm.la, rm.mh)
room_graph.lock_edge(rm.la, rm.hub)
room_graph.lock_edge(rm.mh, rm.vh)
room_graph.show_locked_edges()
print(room_graph.is_locked(rm.mh, rm.la))
print("-----------")
room_graph.unlock_edge(rm.mh, rm.la)
room_graph.unlock_edge(rm.hub, rm.mh)# doing nothing as its not in the locked_edges
print(room_graph.is_locked(rm.mh, rm.la))
room_graph.show_locked_edges()
print("----------")
room_graph.lock_edge(rm.not_room, rm.mh)#trying to add an locked edge for a room that is not in the graph"""

##Testing the bfs functions:
room_graph.lock_edge(rm.mh, rm.vh)
room_graph.lock_edge(rm.hub, rm.vh)
room_graph.lock_edge(rm.mh, rm.la)
room_graph.lock_edge(rm.hub, rm.la)
room_graph.lock_edge(rm.sb, rm.fdh)
room_graph.lock_edge(rm.fdh, rm.eo)
print(room_graph.is_reachable(rm.fdh, rm.eo))
print(room_graph.route_with_blocker(rm.fdh, rm.eo).name)
### Amir_H Javadi_B - 5717292
