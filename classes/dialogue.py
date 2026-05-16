# dialogue tree class - branching conversations between detective, npcs, and chief
# 5750779

import json
import os


class DialogueNode:
    # one line of dialogue with a speaker and the text they say

    def __init__(self, speaker, text):
        # who is talking (marcus, victor, lena, waiter, detective, or chief)
        self.speaker = speaker
        # the line they say
        self.text = text
        # children nodes - empty for now, used later for branching
        self.children = []
        # an optional evidence requirement for this node to be visible
        # (not used yet but ready for future branching)
        self.required_evidence = None
        # if True, this node is only chosen when the branching condition is met
        # (currently: laptop password has been found)
        self.requires_condition = False

    def add_child(self, node):
        # add a child node to the list
        self.children.append(node)


class DialogueTree:
    # a tree of dialogue nodes used during suspect interrogations

    def __init__(self, root_node):
        # the first node of the conversation
        self.root = root_node
        # where we are in the conversation right now
        self.current = root_node

    def get_current(self):
        # return the current node so the UI can show it
        return self.current

    def advance(self, condition=False):
        """Move to the next node, picking the right branch when there are
        multiple children.

        condition is True when the branching condition is met
        (currently: laptop password has been found).
        Returns True if there was a next node, False if the dialogue is over.
        """
        if not self.current.children:
            return False

        if len(self.current.children) == 1:
            # linear - only one path forward
            self.current = self.current.children[0]
            return True

        # branch point: prefer the conditional child when condition is met,
        # otherwise fall back to the default (requires_condition=False) child
        default_child = None
        for child in self.current.children:
            if child.requires_condition and condition:
                self.current = child
                return True
            if not child.requires_condition:
                default_child = child

        if default_child is not None:
            self.current = default_child
            return True

        return False

    def is_finished(self):
        # true if we are at a leaf node (no children)
        return len(self.current.children) == 0

    def reset(self):
        # go back to the start of the dialogue
        self.current = self.root


# helper function to build a linear dialogue tree from a list of nodes
# this is what we will use when loading from json (each suspect_reaction
# entry is a flat list of {speaker, text} dicts)
def build_linear_tree(node_list):
    # node_list is a list of dicts like [{"speaker": "marcus", "text": "..."}, ...]
    # returns a DialogueTree where each node has exactly one child (the next one)
    if len(node_list) == 0:
        return None

    # create the root node from the first item
    first = node_list[0]
    root = DialogueNode(first["speaker"], first["text"])

    # chain the rest as children
    parent = root
    for i in range(1, len(node_list)):
        item = node_list[i]
        child = DialogueNode(item["speaker"], item["text"])
        parent.add_child(child)
        parent = child

    # wrap in a DialogueTree and return
    tree = DialogueTree(root)
    return tree


def build_tree_from_dict(node_dict):
    """Recursively build a DialogueNode from a nested dict.

    The dict format is:
        {
            "speaker": "...",
            "text": "...",
            "condition": true,   # optional - marks a conditional branch
            "branches": [...]    # optional - child node dicts
        }
    """
    node = DialogueNode(node_dict["speaker"], node_dict["text"])
    node.requires_condition = node_dict.get("condition", False)

    for branch_dict in node_dict.get("branches", []):
        node.add_child(build_tree_from_dict(branch_dict))

    return node


# load a dialogue tree from chief_hints.json by its key name
# returns None if the key is missing or json fails to load
def load_dialogue_from_json(dialogue_key):
    # path to the chief hints json file
    path = os.path.join("data", "chief_hints.json")

    # try to read the file
    try:
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
    except FileNotFoundError:
        print("chief_hints.json not found at " + path)
        return None
    except json.JSONDecodeError:
        print("chief_hints.json is not valid JSON")
        return None

    # make sure the suspect_reaction section exists
    if "suspect_reaction" not in data:
        print("suspect_reaction section missing")
        return None

    # look up the dialogue by key
    section = data["suspect_reaction"]
    if dialogue_key not in section:
        # no dialogue for this evidence + npc combo
        return None

    entry = section[dialogue_key]

    # flat list = linear dialogue; dict with "branches" = branching dialogue
    if isinstance(entry, list):
        if len(entry) == 0:
            return None
        return build_linear_tree(entry)

    root = build_tree_from_dict(entry)
    return DialogueTree(root)


# helper to build the dialogue key from evidence and npc names
# e.g. make_dialogue_key("tweed_thread", "marcus") -> "tweed_thread_to_marcus"
def make_dialogue_key(evidence_name, npc_name):
    # join with _to_ to match the keys in chief_hints.json
    return evidence_name + "_to_" + npc_name
