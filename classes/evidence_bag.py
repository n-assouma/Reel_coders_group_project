### Amir_H Javadi_B - 5717292

class evidence_bag:

    def __init__(self) -> None:
        self.data: list = []
        self.max_size: int = 5
    
    def add_evidence(self, evidence: object) -> bool:
        """
        Adds evidence to the bag if space is available.
        Duplicate checking is unnecessary as each evidence 
        item exists only once in the game world.
        Returns: True if evidence was added, False if bag is full.
        """
        if len(self.data) == self.max_size:
            return False
        self.data.append(evidence)
        return True

    def remove_evidence(self, evidence: object) -> bool:
        """
        Removes specified evidence from the bag if it exists.
        Returns: True if evidence was removed, False if not found.
        """
        if evidence in self.data:
            self.data.remove(evidence)
            return True
        return False
    
    def merge(self, first_sorted_bag_data: list, second_sorted_bag_data: list) -> list:
        """
        a recursive function for merging two sorted list of evidence based on their priority (lower number means higher priority)
        this function is for using in the merge_sort() function 
        Returns: a merged sorted list of evidences (objects)
        """
        if not len(first_sorted_bag_data):
            return second_sorted_bag_data
        if not len(second_sorted_bag_data):
            return first_sorted_bag_data
        first_pointer, second_pointer: int = 0, 0
        merged_bag_data: list = []
        while True:
            if first_sorted_bag_data[first_pointer].priority < second_sorted_bag_data[second_pointer].priority:
                merged_bag_data.append(first_sorted_bag_data[first_pointer])
                first_pointer += 1
            else:
                merged_bag_data.append(second_sorted_bag_data[second_pointer])
                second_pointer += 1
            
            if first_pointer == len(first_sorted_bag_data) + 1:
                break
            if second_pointer == len(second_sorted_bag_data) + 1:
                break
        
        merged_bag_data += first_sorted_bag_data[first_pointer:]
        merged_bag_data += second_sorted_bag_data[second_pointer:]
        return merged_bag_data
    
    def merge_sort(self, bag_data: list) -> list:
        """
        A recursive function for sorting the evidence_bag data based on their priority 
        Returning a sorted list of evidences (objects)
        """
        if len(bag_data) <= 1:
            return bag_data
        
        mid: int = len(bag_data) // 2
        return self.merge(self.merge_sort(bag_data[:mid]), self.merge_sort(bag_data[mid:]))