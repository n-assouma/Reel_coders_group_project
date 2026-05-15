### Amir_H Javadi_B - 5717292 - start

from collections import deque
from typing import Optional

from . import room as rm


class RoomGraphError(Exception):
    """Raised when a graph operation receives an invalid room."""

    pass


class EdgeNotExistError(Exception):
    """Raised when a locked_edges operation receives an invalid edge."""

    pass


class RoomGraph:
    """Undirected room graph with lockable edges and BFS pathfinding.

    Rooms are stored as adjacency-list graph nodes. Edges can be locked
    individually or by room. BFS is used for shortest-path navigation.
    """

    def __init__(self, rooms: list[rm.Room]) -> None:
        """Build the adjacency list from a list of Room objects.

        Raises RoomGraphError if rooms is empty.

        Args:
            rooms: List of Room objects to include in the graph.
        """
        if not rooms:
            raise RoomGraphError("room graph cannot be built with no rooms.")

        # Adjacency list mapping each room to its set of connected rooms
        self.__graph: dict[rm.Room, set[rm.Room]] = {}

        # Set of frozen pairs representing locked edges between rooms
        self.__locked_edges: set[frozenset[rm.Room]] = set()

    def build_graph(self, rooms: list[rm.Room]) -> None:
        """Populate the adjacency list using each room's connections.

        Should be called after __init__ to fill the graph with edges.

        Args:
            rooms: List of Room objects whose connections define the edges.
        """
        for room in rooms:
            self.__graph[room] = set(room.connections)

    def show_graph(self) -> None:
        """Print all edges in the graph (debug utility)."""
        for room in self.__graph.keys():
            for adjacent in self.__graph[room]:
                print(f"({room.name}, {adjacent.name})")

    def _lock_edge(self, room_a: rm.Room, room_b: rm.Room) -> None:
        """Mark the edge between two rooms as locked. Idempotent.

        Args:
            room_a: One end of the edge.
            room_b: The other end of the edge.
        """
        self._room_validate(room_a, room_b)
        self._edge_validate((room_a, room_b))

        # frozenset ensures the pair is order-independent
        self.__locked_edges.add(frozenset((room_a, room_b)))

    def lock_room(self, room: rm.Room) -> None:
        """Lock all edges connected to a room.

        Args:
            room: The Room whose edges should all be locked.
        """
        self._room_validate(room)
        for adjacent in room.connections:
            self._lock_edge(room, adjacent)

    def _unlock_edge(self, room_a: rm.Room, room_b: rm.Room) -> None:
        """Remove the lock from an edge between two rooms.

        Args:
            room_a: One end of the edge.
            room_b: The other end of the edge.
        """
        self._room_validate(room_a, room_b)
        self._edge_validate((room_a, room_b))
        self.__locked_edges.discard(frozenset((room_a, room_b)))

    def unlock_room(self, room: rm.Room) -> None:
        """Unlock all edges connected to a room.

        Args:
            room: The Room whose edges should all be unlocked.
        """
        self._room_validate(room)
        for adjacent in room.connections:
            self._unlock_edge(room, adjacent)

    def is_locked(self, room_a: rm.Room, room_b: rm.Room) -> bool:
        """Return True if the edge between two rooms is currently locked.

        Args:
            room_a: One end of the edge.
            room_b: The other end of the edge.
        """
        self._room_validate(room_a, room_b)
        self._edge_validate((room_a, room_b))
        return frozenset((room_a, room_b)) in self.__locked_edges

    def is_room_locked(self, room: rm.Room) -> bool:
        """Return True if all edges of a room are currently locked.

        Args:
            room: The Room to check.
        """
        self._room_validate(room)
        for adjacent in room.connections:
            if not self.is_locked(room, adjacent):
                return False
        return True

    def show_locked_edges(self) -> None:
        """Print all currently locked edges (debug utility)."""
        for edge in self.__locked_edges:
            print("(", end="")
            for room in edge:
                print(room.name, end=" ")
            print(")")

    def _bfs(
        self,
        origin: rm.Room,
        destination: rm.Room,
        respect_locks: bool
    ) -> Optional[list[rm.Room]]:
        """Return the shortest path from origin to destination, or None.

        If respect_locks is True, locked edges are treated as impassable.
        If False, locked edges are traversed as if unlocked — used by
        route_with_blocker to find the structural path before identifying
        the first locked room along it.

        Time complexity: O(V + E)
            V: number of vertices, E: number of edges.

        Args:
            origin: The starting Room.
            destination: The target Room.
            respect_locks: Whether to skip locked edges during traversal.

        Returns:
            Ordered list of rooms from origin to destination, or None.
        """
        is_found: bool = False
        shortest_path: list[rm.Room] = []

        # Maps each visited room to the room it was reached from
        child_parent: dict[rm.Room, Optional[rm.Room]] = {}
        queue: deque[rm.Room] = deque()
        queue.append(origin)
        child_parent[origin] = None

        while queue:
            current_room: rm.Room = queue.popleft()

            if current_room == destination:
                is_found = True
                break

            for room in self.__graph[current_room]:
                # Skip visited rooms and locked edges if respecting locks
                already_visited = room in child_parent
                edge_locked = respect_locks and self.is_locked(
                    current_room, room
                )
                if not already_visited and not edge_locked:
                    queue.append(room)
                    child_parent[room] = current_room

        if not is_found:
            return None

        # Reconstruct the path by walking back through child_parent
        path_room: rm.Room = destination
        while path_room is not None:
            shortest_path.append(path_room)
            path_room = child_parent[path_room]

        # Reverse to get origin-to-destination order
        return shortest_path[::-1]

    def is_reachable(self, origin: rm.Room, destination: rm.Room) -> bool:
        """Return True if a currently-passable route exists between two rooms.

        Args:
            origin: The starting Room.
            destination: The target Room.
        """
        self._room_validate(origin, destination)
        return self._bfs(origin, destination, respect_locks=True) is not None

    def route_with_blocker(
        self,
        origin: rm.Room,
        destination: rm.Room
    ) -> Optional[rm.Room]:
        """Find the first locked room blocking the shortest structural path.

        Intended to be used together with is_reachable() to distinguish:
            is_reachable True  -> path exists and is open
            returns a Room     -> that room is the first lock on the route
            returns None       -> no structural route exists at all

        Args:
            origin: The starting Room.
            destination: The target Room.

        Returns:
            The first locked Room on the path, or None if no path exists.
        """
        self._room_validate(origin, destination)

        # Find the path ignoring locks to get the structural route
        path: Optional[list[rm.Room]] = self._bfs(
            origin, destination, respect_locks=False
        )
        if path is None:
            return None

        # Walk the path and return the first room behind a locked edge
        for i in range(len(path) - 1):
            if self.is_locked(path[i], path[i + 1]):
                return path[i + 1]

    def _room_validate(self, *rooms: rm.Room) -> None:
        """Raise RoomGraphError if any of the given rooms is not in the graph.

        Args:
            rooms: One or more Room objects to validate.
        """
        for room in rooms:
            if room not in self.__graph:
                raise RoomGraphError(
                    f"room {room.name}, is not in the graph."
                )

    def _edge_validate(self, *edges: list[rm.Room]) -> None:
        """Raise EdgeNotExistError if any given edge is not in the graph.

        Args:
            edges: One or more (room_a, room_b) pairs to validate.
        """
        for edge in edges:
            if edge[1] not in self.__graph[edge[0]]:
                raise EdgeNotExistError(
                    f"the edge between {edge[0].name} and "
                    f"{edge[1].name} does not exist in the graph."
                )

    def __repr__(self) -> str:
        """Return a concise debug string showing room count and lock count."""
        return (
            f"RoomGraph(rooms={len(self.__graph)}, "
            f"locked={len(self.__locked_edges)})"
        )
### Amir_H Javadi_B - 5717292 - end
