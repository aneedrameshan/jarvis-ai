class StateManager:

    def __init__(self):

        self.current_app = None

        self.current_screen = None

        self.last_action = None

        self.last_search = None

        self.keyboard_open = False

        self.media_playing = False

        self.clicked_elements = []


    def update_app(self, app_name):

        self.current_app = app_name

        print(
            f"\n[STATE] Current app: "
            f"{app_name}"
        )


    def update_screen(self, screen_name):

        self.current_screen = screen_name

        print(
            f"\n[STATE] Current screen: "
            f"{screen_name}"
        )


    def update_action(self, action):

        self.last_action = action

        print(
            f"\n[STATE] Last action: "
            f"{action}"
        )


    def update_search(self, search):

        self.last_search = search

        print(
            f"\n[STATE] Last search: "
            f"{search}"
        )


    def set_keyboard(self, status):

        self.keyboard_open = status

        print(
            f"\n[STATE] Keyboard open: "
            f"{status}"
        )


    def set_media_playing(self, status):

        self.media_playing = status

        print(
            f"\n[STATE] Media playing: "
            f"{status}"
        )


    def get_state(self):

        return {

            "current_app":
                self.current_app,

            "current_screen":
                self.current_screen,

            "last_action":
                self.last_action,

            "last_search":
                self.last_search,

            "keyboard_open":
                self.keyboard_open,

            "media_playing":
                self.media_playing
        }
    def add_clicked_element(
        self,
        element
    ):

        self.clicked_elements.append(element)

        # Keep only last 10

        self.clicked_elements = (
            self.clicked_elements[-10:]
        )

    def was_clicked_recently(
        self,
        element
    ):

        element = element.lower()

        for item in self.clicked_elements:

            if item.lower() == element:

                return True

        return False