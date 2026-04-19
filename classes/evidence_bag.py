### Amir_H Javadi_B - 5717292
"""
evidence_bag.py

The player's evidence container. Holds up to MAX_SIZE items and
supports merge-sort ordering by evidence priority.
"""

import evidence as ev

class MaximumEvidenceReachedError(Exception):
    """Raised when a there are already 5 evidences in the bag 
    and add_evidence method is used."""
    pass


class EvidenceNotFoundError(Exception):
    """Raised when trying to remove an evidence which not exists in the bag
    trough remove_evidence method."""
    pass


class EvidenceBag:

    """Container for evidence items with a fixed capacity and merge-sort ordering."""
    MAX_SIZE: int = 5

    def __init__(self) -> None:
        """Create an empty evidence bag."""
        self.__data: list[ev.Evidence] = []
    
    def show(self):
        bag = []
        for evidence in self.__data:
            bag.append(evidence.name)
        print(bag)
    
    def add_evidence(self, evidence: ev.Evidence) -> None:
        """Add evidence to the bag if space is available.
    
        Duplicate checking is unnecessary as each evidence item exists
        only once in the game world. Raises MaximumEvidenceReachedError
        if the bag is full.
        """
        if len(self.__data) >= self.MAX_SIZE:
            raise MaximumEvidenceReachedError(f"Evidence bag is full (maximum {self.MAX_SIZE} items).")
        self.__data.append(evidence)

    def remove_evidence(self, evidence: ev.Evidence) -> None:
        """Remove specified evidence from the bag.
    
        Raises EvidenceNotFoundError if the evidence is not in the bag.
        """
        try:
            self.__data.remove(evidence)
        except ValueError:
            raise EvidenceNotFoundError(f"Evidence '{evidence.name}' is not in the bag.")            
        
    def _merge(self, first_sorted_bag_data: list[ev.Evidence], second_sorted_bag_data: list[ev.Evidence]) -> list[ev.Evidence]:
        """Merge two sorted lists of Evidence into one sorted list, comparing by priority."""
        if not first_sorted_bag_data:
            return second_sorted_bag_data
        if not second_sorted_bag_data:
            return first_sorted_bag_data
        first_pointer: int = 0
        second_pointer: int = 0        
        merged_bag_data: list[ev.Evidence] = []
        while first_pointer < len(first_sorted_bag_data) and second_pointer < len(second_sorted_bag_data):
            if first_sorted_bag_data[first_pointer].priority < second_sorted_bag_data[second_pointer].priority:
                merged_bag_data.append(first_sorted_bag_data[first_pointer])
                first_pointer += 1
            else:
                merged_bag_data.append(second_sorted_bag_data[second_pointer])
                second_pointer += 1
        
        merged_bag_data += first_sorted_bag_data[first_pointer:]
        merged_bag_data += second_sorted_bag_data[second_pointer:]
        return merged_bag_data
    
    def _merge_sort(self, bag_data: list[ev.Evidence]) -> list[ev.Evidence]:
        """Recursively sort a list of Evidence by priority using merge sort.
    
        Returns a new sorted list. Time complexity: O(n log n).
        """
        if len(bag_data) <= 1:
            return bag_data
        
        mid: int = len(bag_data) // 2
        return self._merge(self._merge_sort(bag_data[:mid]), self._merge_sort(bag_data[mid:]))
    
    def sort_by_priority(self) -> None:
        """Sort the evidence in this bag by priority (in place)."""
        self.__data = self._merge_sort(self.__data)
    
    def __len__(self) -> int:
        """Return the number of evidence items currently in the bag."""
        return len(self.__data)

    def __repr__(self) -> str:
        """Return a concise debug string showing bag occupancy."""
        return f"EvidenceBag({len(self.__data)}/{self.MAX_SIZE} items)"


##Testing 
bag = EvidenceBag()
bag.add_evidence(ev.tt)
bag.add_evidence(ev.cf)
bag.add_evidence(ev.de)
bag.add_evidence(ev.di)
bag.add_evidence(ev.mkl)
bag.show()
#bag.add_evidence(ev.le)
bag.remove_evidence(ev.tt)
bag.sort_by_priority()
#bag.remove_evidence(ev.tt)
bag.show()
bag.__data.append(ev.tt)
bag.show()
### Amir_H Javadi_B - 5717292