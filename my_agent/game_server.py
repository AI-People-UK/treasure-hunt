from mcp.server.fastmcp import FastMCP

# Create the MCP Server
mcp = FastMCP("HouseTreasureHunt")

# --- Secure Game State ---
# The LLM cannot access this directly, it must use tools.
state = {
    "current_location": "living_room",
    "inventory": [],
    "treasure_found": False
}

locations = {
    "living_room": {
        "description": "A cozy living room. Sunlight streams through the window, but you know the treasure is hidden somewhere in the house.",
        "items": ["map", "note"]
    },
    "kitchen": {
        "description": "A spotless modern kitchen. The smell of old coffee lingers in the air.",
        "items": ["flashlight"]
    },
    "garden": {
        "description": "A beautifully overgrown garden with a small, dark shed. In the center sits a heavy treasure_chest.",
        "items": ["key"]
    }
}

# --- Exposed MCP Tools ---

@mcp.tool()
def look_around() -> str:
    """Returns the description of the current location and any visible items."""
    loc_name = state["current_location"]
    loc = locations[loc_name]
    
    desc = f"[Entering {loc_name.replace('_', ' ').title()}]: {loc['description']}"
    
    if loc["items"]:
        desc += f"\n\nBefore you, you see the following items: {', '.join(loc['items'])}"
    else:
        desc += "\n\nThere are no obvious items to take here."
        
    return desc

@mcp.tool()
def move(location_name: str) -> str:
    """Moves the player to a new location ('living_room', 'kitchen', 'garden')."""
    location_name = location_name.lower().replace(" ", "_")
    if location_name not in locations:
        return f"[System Error]: Invalid location. You can only move to: {', '.join(locations.keys())}"
    
    state["current_location"] = location_name
    return f"You walked to the {location_name.replace('_', ' ')}.\n\n{look_around()}"

@mcp.tool()
def take_item(item_name: str) -> str:
    """Picks up an item from the current location and puts it in the inventory."""
    loc = locations[state["current_location"]]
    
    if item_name in loc["items"]:
        loc["items"].remove(item_name)
        state["inventory"].append(item_name)
        return f"[Success]: You picked up the '{item_name}'."
    else:
        return f"[Error]: There is no '{item_name}' here to take."

@mcp.tool()
def read_note() -> str:
    """Reads the hint note if it is in the inventory or the current room."""
    if "note" in state["inventory"] or "note" in locations[state["current_location"]]["items"]:
        return "[Note Contents]: 'The key lies where the flowers bloom. But it's dark in the shed... you'll need the flashlight from the kitchen to find it.'"
    return "[Error]: You don't see a note to read here."

@mcp.tool()
def open_treasure() -> str:
    """Attempts to open the treasure_chest. You MUST be in the garden!"""
    if state["current_location"] != "garden":
        return "[Error]: The treasure_chest is in the garden! You are not there."
        
    if "key" not in state["inventory"]:
        return "[Game Engine Rejection]: The chest is locked shut! You need the 'key' to open it."
        
    if not state["treasure_found"]:
        state["treasure_found"] = True
        state["inventory"].append("ultimate_treasure")
        return "[VICTORY]: You inserted the key, turned it, and grabbed the ultimate treasure! YOU WIN THE GAME!"
    else:
        return "You already opened the chest. It's empty now."

@mcp.tool()
def check_inventory() -> str:
    """Returns the player's current inventory."""
    if state["inventory"]:
         return f"Your inventory: {', '.join(state['inventory'])}"
    else:
         return "Your inventory is currently empty."

if __name__ == "__main__":
    mcp.run(transport='stdio')
