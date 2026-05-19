import subprocess


class AndroidController:

    def run_adb(self, command):
        full_command = f'adb {command}'

        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True
        )

        return result.stdout


    def home(self):
        return self.run_adb(
            "shell input keyevent 3"
        )


    def back(self):
        return self.run_adb(
            "shell input keyevent 4"
        )


    def recent_apps(self):
        return self.run_adb(
            "shell input keyevent 187"
        )


    def tap(self, x, y):
        return self.run_adb(
            f"shell input tap {x} {y}"
        )


    def swipe(self, x1, y1, x2, y2):
        return self.run_adb(
            f"shell input swipe {x1} {y1} {x2} {y2}"
        )


    def type_text(self, text):
        text = text.replace(" ", "%s")

        return self.run_adb(
            f"shell input text {text}"
        )


    def open_youtube(self):
        return self.run_adb(
            "shell monkey "
            "-p com.google.android.youtube "
            "-c android.intent.category.LAUNCHER 1"
        )
    def screenshot(self):

        self.run_adb(
            "exec-out screencap -p > ../screenshots/screen.png"
    )

        print("Screenshot captured.")

    def open_file_manager(self):

        return self.run_adb(
            "shell monkey "
            "-p com.mi.android.globalFileexplorer "
            "-c android.intent.category.LAUNCHER 1"
        )


    def open_phone(self):

        return self.run_adb(
            "shell monkey "
            "-p com.google.android.dialer "
            "-c android.intent.category.LAUNCHER 1"
        )


    def open_whatsapp(self):

        return self.run_adb(
            "shell monkey "
            "-p com.whatsapp "
            "-c android.intent.category.LAUNCHER 1"
        )


    def open_chrome(self):

        return self.run_adb(
            "shell monkey "
            "-p com.android.chrome "
            "-c android.intent.category.LAUNCHER 1"
        )
    def youtube_search_button(self):

        return self.tap(950, 170)
    
    def press_enter(self):

        return self.run_adb(
            "shell input keyevent 66"
        )
    def search_text(self, text):

        self.type_text(text)

        self.press_enter()