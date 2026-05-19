import time


class RecoverySystem:

    def __init__(self):

        self.max_retries = 3


    def retry_action(
        self,
        action_function,
        validation_function=None,
        recovery_function=None,
        action_name="Unknown Action"
    ):

        for attempt in range(
            1,
            self.max_retries + 1
        ):

            print(
                f"\n[RECOVERY] "
                f"Attempt {attempt} "
                f"for {action_name}"
            )

            action_function()

            time.sleep(2)

            if validation_function:

                success = validation_function()

                if success:

                    print(
                        f"[RECOVERY] "
                        f"{action_name} succeeded."
                    )

                    return True

            else:

                return True


            print(
                f"[RECOVERY] "
                f"{action_name} failed."
            )

            if recovery_function:

                recovery_function()

                time.sleep(2)


        print(
            f"[RECOVERY] "
            f"{action_name} failed after retries."
        )

        return False