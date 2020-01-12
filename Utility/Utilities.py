class Utilities:
    text_package = ""
    text_input = ""
    run_through_terminal = False
    run_dialog = False

    def ask_action(self, terminal_output="... "):
        if self.run_through_terminal:
            action = input(terminal_output)
        else:
            self.text_package += terminal_output
            self.run_dialog = True
            action = self.text_input
        return action

    def print_text(self, text_to_print):
        if self.run_through_terminal:
            print(text_to_print)
        else:
            self.text_package = text_to_print
