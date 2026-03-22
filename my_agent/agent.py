import os
import sys
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

GAME_SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_server.py")

root_agent = Agent(
    model='gemini-2.5-flash',
    name='house_treasure_hunt_gamemaster',
    description="A Game Master AI that runs a Treasure Hunt inside a house.",
    instruction=(
        "You are the Game Master AI for a House Treasure Hunt. "
        "The user is a brave adventurer exploring a house to find the hidden treasure. "
        "You MUST use your provided MCP tools (look_around, move, take_item, read_note, open_treasure, check_inventory) to interact with the rigid game engine. "
        "When the user greets you or starts the game, you MUST silently call 'look_around', and then reply EXACTLY with this starting scenario: "
        "'Welcome, brave adventurer! You awaken in the cozy living room. Sunlight streams through the window, but you know the treasure is hidden somewhere in the house. "
        "Before you, lying on a small table, you see a map and a note with a vague hint. Your quest begins now. What is your first move?' "
        "CRITICAL RULES: \n"
        "1. Never invent items or tell them the treasure location directly. You MUST rely on the tool outputs. If a system tool returns an [Error], narrate that failure to the user.\n"
        "2. Do not give hints unless they read the note or specifically ask for help!"
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,
                    args=[GAME_SERVER_PATH],
                ),
            )
        )
    ],
)
