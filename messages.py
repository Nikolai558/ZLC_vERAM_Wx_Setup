from os import name, system


class TerminalMessageHandler():
    def __init__(self, max_cols):
        self.max_cols = max_cols

    def word_wrap(self, input_string):
        """
        Wrap long strings into a new line depending on max column size.
        :param input_string: string can be many lines (i.e \n) or just one big string
        :return: list of strings no-longer than max_cols.
        """
        output = ""
        list_output = []
        if len(input_string) > self.max_cols - 4:
            list_words = input_string.split(' ')
            total = 4

            for word in list_words:
                total += len(word) + 1
                if total >= self.max_cols - 4:
                    list_output.append(output)
                    output = word + " "
                    total = len(output) + 4
                    if total <= self.max_cols - 4:
                        continue
                    original_string = output
                    while total > self.max_cols - 4:
                        output = output[0: self.max_cols - 5] + "-"
                        list_output.append(output)
                        output = original_string[self.max_cols - 5: len(original_string)]
                        original_string = output
                        total = len(output) + 4
                else:
                    output += word + " "
            list_output.append(output)
            return list_output
        else:
            list_output.append(input_string)
            return list_output

    def formatter(self, text, filler=" ", centered=True, indented=False):
        """
        Format input text to fit nicely on the terminal screen.
        :param text: string
        :param filler: character to fill whitespace with.
        :param centered: boolean center the text in terminal
        :param indented: boolean add single \t before text
        :return: formatted string.
        """
        output = ""
        if indented:
            input_text = "        " + text.strip() + " "
        else:
            input_text = " " + text.strip() + " "

        if len(input_text.strip()) <= 0:
            input_text = ""

        if len(input_text) > self.max_cols:
            input(f"Formatter WARNING: {len(input_text)} is > than {self.max_cols}")
        else:
            if centered:
                output = '{:{}^{}}'.format(input_text, filler, self.max_cols)
            else:
                output = f"{input_text}{filler*(self.max_cols-len(input_text))}"
        return output

    def multi_formatter(self, list_text, filler=" ", centered=True, indented=False):
        """
        Formats a list of text to fit in the Terminal.
        :param list_text: list of strings, each item represents a new line.
        :param filler: filler for white space
        :param centered: boolean for centering text in terminal.
        :param indented: boolean for indenting text in terminal.
        :return: singe string formatted correctly.
        """
        output = ""

        for line in list_text:
            output += self.formatter(line, filler=filler, centered=centered, indented=indented) + "\n"

        return output

    def clear_screen(self):
        """
        Clear the terminal screen for both Linux/Mac and Windows OS.
        """
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def update_msg(self, update_available=False, prog_version="", gh_version=""):
        self.clear_screen()

        output = ""
        output += self.formatter("", filler="*")
        output += self.formatter("Checking for Updates")
        output += self.formatter("", filler="*")
        output += self.formatter("")

        if update_available:
            output += self.formatter("Your program version does not match GitHub Version.", centered=False)
            output += self.formatter("")
            output += self.formatter(f"Program Version: {prog_version}", centered=False, indented=True)
            output += self.formatter(f"GitHub Version: {gh_version}", centered=False, indented=True)
            output += self.multi_formatter(["","Would you like to continue? [Y/N]: "],centered=False)
        return output

    def warning_msg(self, select_file=False, backup_overwrite=False, cd_invalid_choice=False, cd_invalid_file=False,
                    process_exists=False, additional_data=""):
        self.clear_screen()
        output = ""

        if select_file:
            output += self.formatter("", "*")
            output += self.formatter("WARNING")
            output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["You did not select a file. (i.e. 'Cancel' or 'X' was pressed.)",
                                            "",
                                            "Press <ENTER> to Close."], centered=False)
        elif backup_overwrite:
            output += self.formatter("", "*")
            output += self.formatter("WARNING")
            output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["You currently have a 'BACKUP-vERAMConfig.xml' on your Desktop",
                                            "",
                                            "Would you like to overwrite it? [Y/N]:"], centered=False)
        elif cd_invalid_choice:
            output += self.formatter("", "*")
            output += self.formatter(f"WARNING - INVALID SELECTION '{additional_data}'")
            output += self.formatter("")
            output += self.custom_data_msg(include_header=False)
        elif process_exists:
            output += self.formatter("", "*")
            output += self.formatter("WARNING")
            output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["YOUR vERAM PROGRAM IS CURRENTLY OPEN.",
                                            "",
                                            "Please Close vERAM and then restart this Program.",
                                            "",
                                            "Press <ENTER> to Close."], centered=False)
        elif cd_invalid_file:
            output += self.formatter("", "*")
            output += self.formatter("WARNING DATA IN FILE NOT COMPLETE/ACCURATE!")
            output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["While reading the data in your Custom TEXT FILE,",
                                            "this program has come across an error. Please",
                                            "verify the data inside of your custom TEXT file."])
            output += self.formatter("")
            output += self.select_file_msg(veram=False, print_header=False)
        else:
            output += self.formatter("", "*")
            output += self.formatter("WARNING")
            output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["The program has received a WARNING call that is not handled properly.",
                                            "",
                                            "Please report your steps to get here on GitHub Issues.",
                                            "",
                                            "Press <ENTER> to Close."], centered=False)
            exit()

        return output

    def about_msg(self):
        self.clear_screen()
        output = ""
        output += self.formatter("", "*")
        output += self.formatter("ABOUT")
        output += self.formatter("", "*")
        output += self.formatter("")
        output += self.multi_formatter(["This Program will manipulate your vERAMConfig.xml file in order to add",
                                        "all of the standard weather stations and altimeter settings for your ARTCC.",
                                        "and altimeter settings for your ARTCC in a fast and efficient way.",
                                        "","You will be able to read from a text file, Manually Enter, or use",
                                        "default settings. (Default settings are only for ZLC ARTCC)",
                                        "",
                                        "IF THERE IS AN ISSUE AFTER RUNNING:"], centered=False)
        output += self.multi_formatter(["This Program will create a back-up config file onto your",
                                        "desktop prior to running, labeled: 'BACKUP-vERAMConfig.xml'",
                                        "",
                                        "Replace the contents of your vERAMConfig.xml file with the",
                                        "contents of that backup file.",
                                        "",
                                        ""], centered=False, indented=True)
        output += self.formatter("Press <ENTER> to Start.", centered=False)

        return output

    def select_file_msg(self, veram=True, print_header=True):
        self.clear_screen()
        output = ""

        if veram:
            if print_header:
                output += self.formatter("", "*")
                output += self.formatter("SELECTION REQUIRED")
                output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["Select the directory where the vERAMConfig.xml file is.",
                                            "","",
                                            "NOTE:"], centered=False)
            output += self.multi_formatter(["- If you right click on your vERAM.exe Shortcut, and select",
                                            "'Open File Location', then find and select vERAMConfig.xml",
                                            "in that directory. This is the file this program needs."],
                                           centered=False, indented=True)
        else:
            if print_header:
                output += self.formatter("", "*")
                output += self.formatter("SELECTION REQUIRED")
                output += self.formatter("", "*")
            output += self.formatter("")
            output += self.multi_formatter(["Select the file/directory where your custom data .txt file is.",
                                            "", "",
                                            "NOTE:"], centered=False)
            output += self.multi_formatter(["- Inside the file must be exactly as follows. Do NOT insert the",
                                            "'<' or '>' in the example listed below:", "",
                                            "ARTCC: <ARTCC ID here>",
                                            "ALT: <List of Altimeters separated by SPACES>",
                                            "WX: <List of Weather stations separated by SPACES>",
                                            "", "Example:",
                                            "ARTCC: ZLC",
                                            "ALT: KSLC KBOI KBZN KSUN",
                                            "WX: KSLC KU42 KBOI"], centered=False, indented=True)
        return output

    def custom_data_msg(self, include_header=True):
        output = ""
        if include_header:
            self.clear_screen()
            output += self.formatter("", "*")
        output += self.formatter("SELECTION REQUIRED")
        output += self.formatter("", "*")
        output += self.formatter("")
        output += self.multi_formatter(["To make a selection type the letter choice and press <ENTER>",
                                        "",
                                        "This program has the following options available:"], centered=False)
        output += self.multi_formatter(["R: Read custom WX and ALT data text file.",
                                        "M: Manually enter WX and ALT",
                                        "D: Defaults for ZLC ARTCC",
                                        "X: Quits Program",
                                        ""], centered=False, indented=True)
        output += self.formatter("Choice [R/M/D/X']: ", centered=False)
        return output

    def processing_msg(self):
        self.clear_screen()
        output = ""
        output += self.formatter("", "*")
        output += self.formatter("PROCESSING")
        output += self.formatter("", "*")
        return output

    def complete_msg(self):
        self.clear_screen()
        output = ""

        output += self.formatter("", "*")
        output += self.formatter("COMPLETE")
        output += self.formatter("", "*")
        output += self.multi_formatter(["Your ZLC vERAM Profile should now have all of the Standard/Selected",
                                        "Weather Stations and Altimeters.",
                                        "Relaunch vERAM and the ARTCC Profile you made changes to.",
                                        "",
                                        "REMINDER:"], centered=False)
        output += self.multi_formatter(["- A backup vERAMConfig.xml file can be found on your",
                                        "desktop just in case something went wrong.",
                                        ""], centered=False, indented=True)
        output += self.formatter("Press <ENTER> to close.", centered=False)
        return output

    def get_alt_data_input_msg(self, option, data=None):
        self.clear_screen()
        output = ""

        output += self.formatter("", "*")
        output += self.formatter("ENTER YOUR SPECIFIC INFORMATION")
        output += self.formatter("", "*")
        output += self.multi_formatter(["Do NOT insert the '<' or '>' in the example listed below.",
                                        "You can COPY and PASTE, You will be given a chance to Verify.","",
                                        "ARTCC: <ARTCC ID here>",
                                        "ALT: <List of Altimeters separated by SPACES>",
                                        "WX: <List of Weather stations separated by SPACES>",
                                        "",
                                        "Example:",
                                        "ARTCC: ZLC",
                                        "ALT: KSLC KBOI KBZN KSUN",
                                        "WX: KSLC KU42 KBOI","",""], centered=False)

        if option == "ARTCC":
            output += self.formatter("")
            output += self.formatter("ARTCC: ", centered=False)
            output += self.formatter("", centered=False)
        elif option == "WX":
            output += self.formatter("")
            output += self.formatter("Requested Weather Stations: ", centered=False)
            output += self.formatter("", centered=False)
        elif option == "ALT":
            output += self.formatter("")
            output += self.formatter("Requested Altimeters: ", centered=False)
            output += self.formatter("", centered=False)
        elif option == "VERIFY":
            output = ""
            output += self.formatter("", "*")
            output += self.formatter("VERIFY YOUR TYPED/IMPORTED INFORMATION!")
            output += self.formatter("", "*")
            output += self.formatter("")
            output += self.formatter(f"ARTCC: {data['ID']}", centered=False)
            output += self.formatter("")
            output += self.formatter(f"Weather Stations:", centered=False)
            output += self.multi_formatter(self.word_wrap(' '.join(data['WX'])), centered=False, indented=True)
            output += self.formatter("")
            output += self.formatter(f"Altimeters:", centered=False)
            output += self.multi_formatter(self.word_wrap(' '.join(data['ALT'])), centered=False, indented=True)
            output += self.multi_formatter(["",
                                            "",
                                            "Is everything correct? [Y/N]: ",
                                            ""], centered=False)
        return output
