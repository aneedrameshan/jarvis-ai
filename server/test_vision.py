from adb_controller import AndroidController
from vision_agent import VisionAgent
from state import StateManager


controller = AndroidController()

vision_agent = VisionAgent()

state = StateManager()


# TEST STATE
state.update_app("youtube")

state.update_search("Eminem songs")

state.update_action("search_text:Eminem songs")

state.set_media_playing(False)


controller.screenshot()


result = vision_agent.analyze_screen_for_action(

    "../screenshots/screen.png",

    "Play Eminem music on YouTube",

    state.get_state()

)


print("\nVISION RESULT:\n")

print(result)