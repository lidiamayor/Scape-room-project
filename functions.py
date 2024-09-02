import re

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game(game_state, object_relations):
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    explore_room(game_state["current_room"], object_relations) # explore the current room
    play_room(game_state["current_room"], game_state, object_relations) # play the current room

def play_room(room, game_state, object_relations):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room # update game state with new current room
    if(game_state["current_room"] == game_state["target_room"]): # check if the room being played is the target room
        print("Congrats! You escaped the room!") # player has found the target room and wins
    else: # if the room being played is not the target room
        examine_item(input("What would you like to examine? ").strip().lower(), game_state, object_relations) # examine the item that the player wants to examine
        linebreak()

def explore_room(room, object_relations):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]] # get the items in the room
    print("This is " + room["name"] + ". You find " + ", ".join(items)) # list the items

def get_next_room_of_door(door, current_room, object_relations):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]] # get the rooms connected to the door
    for room in connected_rooms: # for each room
        if(not current_room == room): # if the room is not the current room
            return room # return the new room

def unlock_door(door, current_room, object_relations):
    """
    Unlock the door
    """
    next_room = get_next_room_of_door(door, current_room, object_relations) # get the next room of the door
    return next_room

def examine_item(item_name, game_state, object_relations):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"] # get the current room
    next_room = "" # initialize the next room
    output = None # initialize the output

    for item in object_relations[current_room["name"]]: # for each item in the current room
        if(item["name"] == item_name): # if the item is the intended item
            output = "You examine " + item_name + ". " # output the item name
            if(item["type"] == "door"): # if the item is a door
                have_key = False
                for key in game_state["keys_collected"]: # check if the player has the key
                    if(key["target"] == item): # if the key is the intended key
                        have_key = True # the player has the key
                if(have_key): # if the player has the key
                    output += "You unlock it with a key you have." # output the unlock message
                    next_room = unlock_door(item, current_room, object_relations) # unlock the door
                else: # if the player does not have the key
                    output += "It is locked but you don't have the key." # output the locked message

            else: # if the item is not a door
                if (item["type"] == "safe"): # if the item is safe
                    print()
                    print("You find a box. The box is locked. You should guess the password.") # ask the player to guess the password
                    print("Here, you have some clues:") # output the clues
                    print("The first value is the total number of rooms.")
                    print("The second value is the number of furniture in the previous room")
                    print("The third value is the total number of bedrooms")
                    password = input("Now, enter the password: ") # ask the player to enter the password
                    patter = r"[512]" # pattern to match the password
                    while password != "512": # while the password is not correct
                        result = re.findall(patter, password) # find the pattern in the password
                        password = input(f"The password entered is incorrect. You have guess {len(result)} numbers. Try again: ") # ask the player to enter the password and give the number of guesses
                    print("You have guess the password!") # the player has guessed the password

                if(item["name"] in object_relations and len(object_relations[item["name"]])>0): # if the item contains keys
                    item_found = object_relations[item["name"]].pop()  # get the key
                    game_state["keys_collected"].append(item_found) # add the key to the game state
                    output += "You find " + item_found["name"] + "." # output the key name
                else: # if the item does not contain keys
                    output += "There isn't anything interesting about it." # output the not interesting message
            print(output)
            break

    if(output is None): # if the item is not found
        print("The item you requested is not found in the current room.") # output the not found message

    if(next_room): # if the next room is not empty
        print()
        explore_room(next_room, object_relations) # explore the next room
        play_room(next_room, game_state, object_relations) # play the next room
    else: # if the next room is empty
        play_room(current_room, game_state, object_relations) # play the current room

