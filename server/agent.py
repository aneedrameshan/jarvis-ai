from openai import OpenAI
from dotenv import load_dotenv
from rapidfuzz import fuzz

import os
import time

from adb_controller import AndroidController
from vision import Vision
from tts import TextToSpeech
from state import StateManager
from recovery import RecoverySystem
from vision_agent import VisionAgent


load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


controller = AndroidController()

vision = Vision()

tts = TextToSpeech()

state = StateManager()

recovery = RecoverySystem()

vision_agent = VisionAgent()


class JarvisAgent:


    def run_command(self, user_input):

        prompt = f"""
        You are an Android AI assistant.

        Decide actions to complete the task.

        AVAILABLE ACTIONS:

        - open_youtube
        - open_chrome
        - open_whatsapp
        - open_phone
        - open_file_manager
        - home
        - back
        - recent_apps

        SEARCH:
        search_text:QUERY

        TAP:
        tap_text:TEXT

        OPEN RESULT:
        open_result:TEXT

        IMPORTANT:
        If user wants to play music/videos,
        ALWAYS use:

        open_youtube|search_text:QUERY|open_result:QUERY

        User request:
        {user_input}

        Return ONLY actions.
        """


        response = client.chat.completions.create(

            model="google/gemini-2.5-flash",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        action_response = (
            response
            .choices[0]
            .message.content
            .strip()
        )


        print(
            f"\nAI RESPONSE: "
            f"{action_response}\n"
        )


        actions = action_response.split("|")


        for action in actions:

            action = action.strip()

            state.update_action(action)

            print(
                f"\n[STATE] Last action: "
                f"{action}"
            )

            print(
                f"\nAI Action: "
                f"{action}\n"
            )


            # OPEN YOUTUBE

            if action == "open_youtube":

                tts.speak(
                    "Opening YouTube."
                )

                recovery.retry_action(

                    action_function=
                        controller.open_youtube,

                    validation_function=
                        self.validate_youtube_open,

                    action_name=
                        "Open YouTube"
                )

                state.update_app(
                    "youtube"
                )

                time.sleep(3)


            # SEARCH TEXT

            elif action.startswith(
                "search_text:"
            ):

                query = action.replace(
                    "search_text:",
                    ""
                )

                state.update_search(
                    query
                )

                tts.speak(
                    f"Searching for {query}"
                )


                if state.current_app == "youtube":

                    tts.speak(
                        "Opening YouTube search."
                    )

                    controller.tap(
                        950,
                        170
                    )

                    time.sleep(2)


                elif state.current_app == "chrome":

                    controller.tap(
                        500,
                        170
                    )

                    time.sleep(2)


                else:

                    self.tap_text(
                        "Search"
                    )


                state.set_keyboard(True)

                controller.type_text(
                    query
                )

                time.sleep(2)

                controller.tap(
                    500,
                    350
                )

                state.set_keyboard(False)

                time.sleep(5)


            # OPEN RESULT

            elif action.startswith(
                "open_result:"
            ):

                target = action.replace(
                    "open_result:",
                    ""
                )

                goal = (
                    f"Play {target} "
                    f"on YouTube"
                )

                self.autonomous_goal_loop(
                    goal
                )


            # HOME

            elif action == "home":

                controller.home()

                state.update_app(
                    "home"
                )


            # BACK

            elif action == "back":

                controller.back()


            # RECENT APPS

            elif action == "recent_apps":

                controller.recent_apps()


    def autonomous_goal_loop(

        self,

        goal,

        max_steps=8

    ):

        tts.speak(
            "Starting autonomous execution."
        )


        for step in range(max_steps):

            print(
                f"\n[AUTONOMOUS LOOP] "
                f"Step {step + 1}"
            )

            controller.screenshot()


            vision_action = (

                vision_agent
                .analyze_screen_for_action(

                    "../screenshots/screen.png",

                    goal,

                    state.get_state()

                )

            )


            print(
                f"\n[VISION DECISION] "
                f"{vision_action}"
            )


            success = self.execute_vision_action(
                vision_action
            )


            if not success:

                print(
                    "\n[AUTONOMOUS LOOP] "
                    "Action failed."
                )

                controller.swipe(
                    500,
                    1700,
                    500,
                    900,
                    300
                )

                time.sleep(2)

                continue


            time.sleep(3)


            if self.validate_media_playing():

                tts.speak(
                    "Goal completed."
                )

                state.set_media_playing(
                    True
                )

                return True


        tts.speak(
            "Autonomous execution ended."
        )

        return False


    def execute_vision_action(

        self,

        vision_action

    ):

        print(
            f"\n[VISION ACTION] "
            f"{vision_action}"
        )


        # CLICK ELEMENT

        if vision_action.startswith(
            "click_element:"
        ):

            target = vision_action.replace(
                "click_element:",
                ""
            ).strip()


            # MEMORY CHECK

            if state.was_clicked_recently(
                target
            ):

                print(
                    f"\n[MEMORY] "
                    f"Already clicked "
                    f"{target}"
                )

                return False


            success = self.tap_text(
                target
            )


            if success:

                state.add_clicked_element(
                    target
                )


            return success


        # TAP SEARCH

        elif vision_action == "tap_search":

            controller.tap(
                950,
                170
            )

            return True


        # PLAY VIDEO

        elif vision_action == "play_video":

            controller.tap(
                540,
                960
            )

            return True


        # SCROLL

        elif vision_action == "scroll_down":

            controller.swipe(
                500,
                1700,
                500,
                900,
                300
            )

            return True


        # GO BACK

        elif vision_action == "go_back":

            controller.back()

            return True


        # SKIP AD

        elif vision_action == "skip_ad":

            return self.tap_text(
                "Skip"
            )


        # CLOSE POPUP

        elif vision_action == "close_popup":

            controller.tap(
                980,
                140
            )

            return True


        return False


    def validate_youtube_open(self):

        controller.screenshot()

        screen_text = vision.read_screen(
            "../screenshots/screen.png"
        ).lower()


        indicators = [

            "shorts",
            "subscriptions",
            "youtube",
            "library"

        ]


        for indicator in indicators:

            if indicator in screen_text:

                return True


        return False


    def validate_media_playing(self):

        controller.screenshot()

        screen_text = vision.read_screen(
            "../screenshots/screen.png"
        ).lower()


        # AD DETECTION

        ad_indicators = [

            "skip ad",
            "visit site",
            "install",
            "sponsored",
            "advertisement"

        ]


        for ad in ad_indicators:

            if ad in screen_text:

                print(
                    "\n[VALIDATION] "
                    "Advertisement detected."
                )

                return False


        # PLAYBACK DETECTION

        playback_indicators = [

            "pause",
            "playing",
            "subscribers"

        ]


        score = 0


        for indicator in playback_indicators:

            if indicator in screen_text:

                score += 1


        if score >= 2:

            print(
                "\n[VALIDATION] "
                "Playback detected."
            )

            return True


        return False


    def build_phrase_candidates(

        self,

        data

    ):

        candidates = []

        words = data["text"]


        for i in range(len(words)):

            word1 = words[i].strip()

            if word1 == "":

                continue


            x1 = data["left"][i]
            y1 = data["top"][i]
            w1 = data["width"][i]
            h1 = data["height"][i]


            # SINGLE WORD

            candidates.append({

                "text": word1,

                "x": x1 + w1 // 2,

                "y": y1 + h1 // 2

            })


            # TWO WORD PHRASE

            if i + 1 < len(words):

                word2 = words[i + 1].strip()

                if word2 != "":

                    phrase2 = (
                        f"{word1} {word2}"
                    )

                    candidates.append({

                        "text": phrase2,

                        "x": x1 + w1 // 2,

                        "y": y1 + h1 // 2

                    })


            # THREE WORD PHRASE

            if i + 2 < len(words):

                word2 = words[i + 1].strip()

                word3 = words[i + 2].strip()

                if (
                    word2 != ""
                    and
                    word3 != ""
                ):

                    phrase3 = (
                        f"{word1} "
                        f"{word2} "
                        f"{word3}"
                    )

                    candidates.append({

                        "text": phrase3,

                        "x": x1 + w1 // 2,

                        "y": y1 + h1 // 2

                    })


        return candidates


    def find_text_on_screen(

        self,

        target_text

    ):

        time.sleep(2)

        controller.screenshot()


        data = vision.get_text_data(
            "../screenshots/screen.png"
        )


        candidates = (
            self.build_phrase_candidates(
                data
            )
        )


        best_match = None

        best_score = 0


        target_clean = (
            target_text
            .lower()
            .strip()
        )


        for candidate in candidates:

            candidate_text = (
                candidate["text"]
                .lower()
                .strip()
            )


            score = fuzz.ratio(

                target_clean,

                candidate_text

            )


            print(
                f"Matching "
                f"'{target_clean}' "
                f"with "
                f"'{candidate_text}' "
                f"= {score}"
            )


            if score > best_score:

                best_score = score

                best_match = candidate


        if best_match and best_score >= 75:

            print(
                f"\nBest score: "
                f"{best_score}"
            )

            print(
                f"Selected candidate: "
                f"{best_match['text']}"
            )

            return (

                best_match["x"],

                best_match["y"]

            )


        print(
            "\nNo reliable match found."
        )

        return None


    def tap_text(

        self,

        target_text

    ):

        result = self.find_text_on_screen(
            target_text
        )


        if result:

            x, y = result

            tts.speak(
                f"Tapping {target_text}"
            )

            controller.tap(
                x,
                y
            )

            return True


        else:

            tts.speak(
                f"I could not find "
                f"{target_text}"
            )

            return False


    def analyze_screen(self):

        controller.screenshot()

        screen_text = vision.read_screen(
            "../screenshots/screen.png"
        )


        prompt = f"""
        Analyze this Android screen.

        1. Identify app
        2. Important UI elements
        3. Best next actions

        Keep concise.

        Screen:
        {screen_text}
        """


        response = client.chat.completions.create(

            model="google/gemini-2.5-flash",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        analysis = (
            response
            .choices[0]
            .message.content
        )


        print(
            "\nSCREEN ANALYSIS:\n"
        )

        print(analysis)

        tts.speak(analysis)

        return analysis