import base64
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


class VisionAgent:


    def analyze_screen_for_action(
        self,
        image_path,
        goal,
        state
    ):

        with open(image_path, "rb") as image_file:

            image_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")


        prompt = f"""
        You are an advanced Android AI agent.

        USER GOAL:
        {goal}

        CURRENT STATE:
        - Current app: {state.get('current_app')}
        - Last action: {state.get('last_action')}
        - Last search: {state.get('last_search')}
        - Media playing: {state.get('media_playing')}
        - Keyboard open: {state.get('keyboard_open')}

        Analyze the Android screenshot carefully.

        Your job:
        1. Understand the current workflow stage.
        2. Identify the MOST relevant clickable UI element.
        3. Decide the BEST next action.
        4. Avoid repeating completed actions.

        IMPORTANT:
        - If search results are already visible,
          DO NOT suggest opening search again.
        - If a playable video is visible,
          prioritize opening the video.
        - If a popup blocks interaction,
          prioritize closing the popup.
        - If an ad can be skipped,
          prioritize skipping the ad.
        - Focus ONLY on progressing the goal.

        IMPORTANT:
        ONLY return text that is EXACTLY visible on screen.

        DO NOT invent names like:
        - Search button
        - Video card
        - Music icon

        ONLY use exact visible text.

        IMPORTANT:

        You are controlling an Android device.

        Return ONLY ONE raw action.

        DO NOT explain.
        DO NOT add reasoning.
        DO NOT add extra text.
        DO NOT use markdown.

        Valid outputs:

        click_element:TEXT
        close_popup
        tap_search
        play_video
        scroll_down
        go_back
        skip_ad

        Examples:

        click_element:Eminem Songs
        click_element:Without Me
        click_element:Skip
        tap_search
        close_popup
        skip_ad
        """


        response = client.chat.completions.create(

            model="google/gemini-2.5-flash",

            messages=[

                {
                    "role": "user",
                    "content": [

                        {
                            "type": "text",
                            "text": prompt
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url":
                                f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )


        result = (
            response
            .choices[0]
            .message.content
            .strip()
        )

        first_line = result.split("\n")[0]

        return first_line