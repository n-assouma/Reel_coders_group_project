# Dialogue System — How It Works

## Overview

All dialogue content lives in `data/chief_hints.json`. The system has two separate
loading paths depending on whether the content is a simple one-line hint or a
multi-line conversation between characters.

---

## `chief_hints.json` structure

```
{
  "_meta": { ... },           // ignored at runtime
  "object_hint":   { key: string },         // one line per interactable object
  "npc_greeting":  { key: string },         // one line shown when near an NPC
  "suspect_reaction": {                     // multi-line conversations
      "tweed_thread_to_marcus": [
          {"speaker": "marcus", "text": "..."},
          {"speaker": "chief",  "text": "..."}
      ],
      ...
  },
  "room_unlocks_hint": { key: string },     // one line shown when a room unlocks
  "ending":            { key: string }      // one line per ending outcome
}
```

Suspect reaction keys follow the pattern `{evidence_name}_to_{npc_name}`, e.g.
`master_key_log_to_victor`. The helper `make_dialogue_key(evidence, npc)` in
`classes/dialogue.py` builds these strings.

Some entries (introductions, waiter testimony) do not follow the `_to_` pattern
and are called directly by name: `marcus_introduction`, `victor_introduction`,
`lena_introduction`, `waiter_testimony`.

---

## Path 1 — Simple one-line hints (`ChiefOfPoliceHint`)

**File:** `classes/chief_of_police_hint.py`

`ChiefOfPoliceHint.load_hints()` is called once at startup. It reads the JSON
and stores three sections as plain `dict[str, str]`:

| Attribute | JSON key | Usage |
|---|---|---|
| `self.object_hints` | `"object_hint"` | shown when player is near an object |
| `self.npc_greetings` | `"npc_greeting"` | shown when player is near an NPC |
| `self.room_unlocks_hints` | `"room_unlocks_hint"` | shown when a locked room opens |

Lookup is a direct dict key access — e.g. `self.object_hints["master_key_log"]`
returns the hint string immediately. The `suspect_reaction` and `ending` sections
are **not** loaded here.

The hint string is then passed to `set_hint()`, which stores it in
`self.current_hint`. The `draw()` method renders `self.current_hint` into the
HUD panel every frame, word-wrapping it to fit the panel width.

---

## Path 2 — Multi-line conversations (`DialogueTree`)

**Files:** `classes/dialogue.py`, `game.py`

### Data structure

Each `suspect_reaction` entry is a flat list of `{speaker, text}` dicts.
`build_linear_tree()` converts this list into a **singly-linked list** of
`DialogueNode` objects:

```
DialogueNode  (speaker, text, children=[next])
  └── DialogueNode  (speaker, text, children=[next])
        └── DialogueNode  (speaker, text, children=[])  ← leaf = end of dialogue
```

Although `children` is a list (allowing branching in theory), `build_linear_tree`
always adds exactly one child per node. `advance()` always follows `children[0]`.
In practice this is a linked list, not a tree. The `required_evidence` field on
each node is also unused — it is a stub for future branching that was never
implemented.

### Loading

`load_dialogue_from_json(dialogue_key)` in `classes/dialogue.py`:
1. Opens `data/chief_hints.json` and parses it with `json.load()`.
2. Looks up `dialogue_key` inside the `"suspect_reaction"` section.
3. Passes the resulting list to `build_linear_tree()` and returns a `DialogueTree`.
4. Returns `None` if the file is missing, the JSON is invalid, or the key does
   not exist (the caller in `game.py` shows a fallback message in that case).

The file is re-opened from disk on every call (no caching).

### Two triggers in `game.py`

**1. Player drops evidence on an NPC** — `try_start_dialogue(drop_pos)`

```
player drags evidence → drops on NPC rect
  → make_dialogue_key(evidence_name, npc_name)  →  e.g. "master_key_log_to_victor"
  → load_dialogue_from_json(key)
  → store tree in self.active_dialogue
  → show first node in HUD panel
```

**2. Player presses E next to an NPC** — `start_npc_dialogue(dialogue_key)`

Calls `load_dialogue_from_json` directly with a hardcoded key
(`"marcus_introduction"`, `"victor_introduction"`, etc.).

### Advancing through the dialogue

While `self.active_dialogue is not None`, the game loop is frozen (player cannot
move). Each press of Space calls `active_dialogue.advance()`:

- If a next node exists → update the HUD panel with the new speaker and text.
- If no next node (leaf reached) → set `self.active_dialogue = None`, unfreeze
  the game, hide the `[SPACE]` hint.

The HUD panel shows `[SPACE] to continue` or `[SPACE] to close` depending on
whether `is_finished()` is true.

---

## Speaker display

Both paths resolve the speaker key to a human-readable title and colour via two
dicts in `classes/chief_of_police_hint.py`:

```python
SPEAKER_TITLES  = { "chief": "CHIEF OF POLICE", "marcus": "MARCUS HALE", ... }
SPEAKER_COLOURS = { "chief": (120,180,230), "marcus": (220,110,90), ... }
```

`set_speaker(speaker_key)` updates the panel title, accent colour, and portrait
sprite in one call. Portraits are loaded from `assets/hud/` at startup and
stored in `self.portraits` keyed by speaker name. Missing portrait files are
skipped silently; `"officer"` is the fallback for `chief`, `detective`, and any
unknown speaker.