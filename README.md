# The Hollow Witness

The Hollow Witness is a detective mystery game made with Python and Pygame. You play as Detective Rowe, who is called in after Dr. Elena, a biochemistry researcher at Ashworth University, is found dead in her office late at night. Three suspects had reasons to want her gone: her ex-husband, her research partner and the university dean. By walking through seven locations around the city, examining objects, collecting evidence and questioning the suspects with what you find, you must work out who the killer is. Choose carefully, as the evidence you gather and the person you accuse decide how the case ends.

See [setup](##setup) and [how to play](#how-to-play) sections for more information.

## Setup 

Pyton 3.14.0 (or newer)

### 1. Clone the repository
```bash
git clone <repo-url>
cd Reel_coders_group_project
```

### 2. Create a virtual environment

**Git Bash:**
```bash
python -m venv venv
```

**PowerShell:**
```powershell
python3 -m venv venv
```

### 3. Activate the virtual environment

**Git Bash:**
```bash
source venv/Scripts/activate
```

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

**Git Bash:**
```bash
pip install -r requirements.txt
```

**PowerShell:**
```powershell
pip install -r requirements.txt
```

### 5. Run the project

**Git Bash:**
```bash
python3 main.py
```

**PowerShell:**
```powershell
python3 main.py
```

# How to Play

After running the game, please wait for the game to finish loading. The game will start in the first room, which is the Police Station.

## Walking

- In each room, the player can walk by pressing the W, A, S, and D keys on the keyboard, which move the detective up, left, down, and right respectively.
- If the walking sound is annoying, you can mute your device, it will not affect the rest of the game.

## Interactable objects

- If you get close to any interactable object, its name will be shown above it, and by pressing the E key on your keyboard you can interact with it.

## Evidence bag

- In each room, at the bottom right corner of the screen, there is your evidence bag.
- You can open and close it by clicking on it.
- When it is open, the evidence you have collected is shown.
- You collect evidence by interacting with it in the room.
- The bag has a maximum capacity of 5 pieces of evidence.
- To remove an item, drag it from the evidence bag and drop it on the bin. The evidence will reappear in the same position where you originally found it.

## Chief of Police

- The Chief of Police is located in the bottom left corner of the screen while you are in a room.
- The Chief gives you information when you get close to an interactive object.
- More detailed information is given when you interact with the object.
- If you interact with an NPC, a conversation will begin.
- You can also ask suspects about evidence by dragging an item from the evidence bag and dropping it on the NPC.
- The Chief of Police will show you their reactions and give you further information based on their response.
- Conversations may contain more than one line of text, you can advance through them by pressing either Space or Enter.

## Map

- There is a map icon located at the bottom of the game screen.
- You can open the city map by clicking on this icon, or by interacting with the map inside the Police Station.
- The small detective figure on the map shows which room you are currently in.
- The locks on the map indicate which rooms are still locked.
- By hovering over a building with your mouse, you can see its name.
- By clicking on a building, you can travel to it if it is reachable.
- You can also click on the room you are currently in (this will simply reload the same room).
- If a room is not reachable, an error message will pop up telling you which room must be unlocked first.
- Rooms can be unlocked by finding the corresponding evidence.

## Laptop

- In Victor's House, there is a laptop the player can interact with.
- You have to find the correct password to open the laptop.
- Type the password using your keyboard the same way you would normally type on your device.
- You can type and delete your answer as many times as you wish until you find the correct password.
- You can exit the laptop screen by clicking the close (X) button in the top right corner.

## Ending

- When you are sure you have identified the murderer, return to the Police Station.
- Interact with the suspects board and choose your accusation.
- If you choose the wrong person, the innocent suspect will be arrested and you lose.
- If you choose the correct person but have not collected enough evidence, you will not be able to make the arrest.
- If you choose the correct person and have collected enough evidence, you win and the murderer is arrested.
