# Amir_H Javadi_B - 5717292

import os
import pygame

from .evidence import Evidence


class MaximumEvidenceReachedError(Exception):
    """Raised when the bag is full and add_evidence is called."""

    pass


class EvidenceNotFoundError(Exception):
    """Raised when remove_evidence is called with an item not in the bag."""

    pass


class EvidenceBag:
    """Container for evidence items with a fixed capacity and merge-sort ordering.

    Evidence is stored privately to prevent direct mutation from outside.
    Items can be sorted in place by priority using merge sort.
    """

    MAX_SIZE: int = 5

    def __init__(self) -> None:
        """Create an empty evidence bag and load all required UI assets."""
        # Private list — double underscore triggers name mangling to
        # prevent accidental access from outside the class
        self.__data: list[Evidence] = []
        self.is_open: bool = False

        # Closed bag icon shown in the HUD when the bag is not open
        closed_bag_path = os.path.join(
            "assets", "evidence_bag", "closed_bag.png"
        )
        self.closed_bag_image = pygame.image.load(
            closed_bag_path
        ).convert_alpha()
        self.closed_bag_image = pygame.transform.scale(
            self.closed_bag_image, (150, 150)
        )

        # Open bag icon shown when the bag is open but has no items
        empty_opened_bag_path = os.path.join(
            "assets", "evidence_bag", "empty_opened_bag.png"
        )
        self.empty_opened_bag_image = pygame.image.load(
            empty_opened_bag_path
        ).convert_alpha()
        self.empty_opened_bag_image = pygame.transform.scale(
            self.empty_opened_bag_image, (150, 150)
        )

        # Open bag icon shown when the bag has at least one item
        full_opened_bag_path = os.path.join(
            "assets", "evidence_bag", "full_opened_bag.png"
        )
        self.full_opened_bag_image = pygame.image.load(
            full_opened_bag_path
        ).convert_alpha()
        self.full_opened_bag_image = pygame.transform.scale(
            self.full_opened_bag_image, (150, 150)
        )

        # Trash can icon used to remove evidence from the bag
        trash_can_path = os.path.join(
            "assets", "evidence_bag", "trash_can.png"
        )
        self.trash_can_image = pygame.image.load(
            trash_can_path
        ).convert_alpha()
        self.trash_can_image = pygame.transform.scale(
            self.trash_can_image, (150, 150)
        )

        # Rects used for click detection on the HUD icons
        self.rect = self.closed_bag_image.get_rect()
        self.trash_can_rect = self.trash_can_image.get_rect()

    def show(self) -> None:
        """Print the names of all evidence items in the bag (debug utility)."""
        bag = []
        for evidence in self.__data:
            bag.append(evidence.name)
        print(bag)

    def add_evidence(self, evidence: Evidence) -> None:
        """Add evidence to the bag if space is available.

        Duplicate checking is unnecessary as each evidence item exists
        only once in the game world. Raises MaximumEvidenceReachedError
        if the bag is full.

        Args:
            evidence: The Evidence item to add.
        """
        if len(self.__data) >= self.MAX_SIZE:
            raise MaximumEvidenceReachedError(
                f"Evidence bag is full (maximum {self.MAX_SIZE} items)."
            )
        self.__data.append(evidence)

    def remove_evidence(self, evidence: Evidence) -> None:
        """Remove specified evidence from the bag.

        Raises EvidenceNotFoundError if the evidence is not in the bag.

        Args:
            evidence: The Evidence item to remove.
        """
        try:
            self.__data.remove(evidence)
        except ValueError:
            raise EvidenceNotFoundError(
                f"Evidence '{evidence.name}' is not in the bag."
            )

    def evidence_exists(self, evidence_name: str) -> bool:
        """Return True if an evidence with the given name is in the bag.

        Args:
            evidence_name: The name of the evidence to look up.
        """
        for evidence in self.__data:
            if evidence.name == evidence_name:
                return True
        return False

    def _merge(
        self,
        first_sorted_bag_data: list[Evidence],
        second_sorted_bag_data: list[Evidence]
    ) -> list[Evidence]:
        """Merge two sorted Evidence lists into one sorted list by priority.

        Args:
            first_sorted_bag_data: First sorted list of Evidence items.
            second_sorted_bag_data: Second sorted list of Evidence items.

        Returns:
            A new sorted list containing all items from both inputs.
        """
        # Base cases: if either half is empty, return the other
        if not first_sorted_bag_data:
            return second_sorted_bag_data
        if not second_sorted_bag_data:
            return first_sorted_bag_data

        first_pointer: int = 0
        second_pointer: int = 0
        merged_bag_data: list[Evidence] = []

        # Compare items from both halves and append the lower-priority one
        while (first_pointer < len(first_sorted_bag_data)
               and second_pointer < len(second_sorted_bag_data)):
            first_priority = first_sorted_bag_data[first_pointer].priority
            second_priority = second_sorted_bag_data[second_pointer].priority
            if first_priority < second_priority:
                merged_bag_data.append(first_sorted_bag_data[first_pointer])
                first_pointer += 1
            else:
                merged_bag_data.append(second_sorted_bag_data[second_pointer])
                second_pointer += 1

        # Append any remaining items from whichever half is not exhausted
        merged_bag_data += first_sorted_bag_data[first_pointer:]
        merged_bag_data += second_sorted_bag_data[second_pointer:]
        return merged_bag_data

    def _merge_sort(self, bag_data: list[Evidence]) -> list[Evidence]:
        """Recursively sort a list of Evidence by priority using merge sort.

        Returns a new sorted list. Time complexity: O(n log n).

        Args:
            bag_data: The list of Evidence items to sort.
        """
        # Base case: a list of 0 or 1 items is already sorted
        if len(bag_data) <= 1:
            return bag_data

        mid: int = len(bag_data) // 2
        return self._merge(
            self._merge_sort(bag_data[:mid]),
            self._merge_sort(bag_data[mid:])
        )

    def sort_by_priority(self) -> None:
        """Sort the evidence in this bag by priority (in place)."""
        self.__data = self._merge_sort(self.__data)

    def __len__(self) -> int:
        """Return the number of evidence items currently in the bag."""
        return len(self.__data)

    @property
    def items(self) -> list[Evidence]:
        """Return a copy of the list of evidence items in the bag."""
        return self.__data.copy()

    def __repr__(self) -> str:
        """Return a concise debug string showing bag occupancy."""
        return f"EvidenceBag({len(self.__data)}/{self.MAX_SIZE} items)"
# Amir_H Javadi_B - 5717292
