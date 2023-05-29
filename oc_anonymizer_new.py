#!/usr/bin/python3.10

import datetime
import json
import os
from pathlib import Path
import plistlib
import time

class PlistStripper:
    def __init__(self) -> None:
        self.plist: dict = dict()
        self.rules: dict = json.load(open('rules.json', 'r'))
        self.selected_config: bool = False
        self._init_sequence()
        self._grab_user_input()
        # self.dump() options dumps the input config.plist, after applying the selected patches, onto a new censored_config.plist

        # BUG: For each option, in case of older version of OpenCore where some options may be missing (e.g. Resizable BAR Support options), the script will display only the available options (e.g. missing Resizable BAR Support options, therefore "8" won't be selectable and the text will be displayed with a grey foreground text) (use conditionals 'key' in self.plist.keys())
        # BUG: In case of possible sensitive data (mainly PlatformInfo/Generic settings) a yellow/orange foreground text should be displayed, so the user knows that he's missing these important options.
        # BUG: When dumping "censored_config.plist", in case possible sensitive data censoring options are left unchecked, a warning message should be displayed, so the user can choose whether to ignore them, and therefore continue dumping, or fix them manually (by displaying a menu like done before).
        # TODO: When the user selects the desired policies to apply on the resulting "censored_config.plist", the enabled options should have a green foreground text, while the disabled one a red, or a white foreground text.

    def _print_welcome_banner(self) -> None:
        """ Prints a welcome banner"""
        print("""
  ___    ___        ___                   _  _         _               
 / _ \  / __|      /   \ _ _   ___  _ _  | || | _ __  (_) ___ ___  _ _ 
| (_) || (__       | - || ' \ / _ \| ' \  \_. || '  \ | ||_ // -_)| '_|
 \___/  \___|      |_|_||_||_|\___/|_||_| |__/ |_|_|_||_|/__|\___||_|  
""")
              
    
    def _quit_program(self) -> None:
        self._clear_screen()
        #Corp Hippity hoppity, your code is now my property haha
        print('by dreamwhite\n')
        print('Thanks for testing it out, for bugs/comments/complaints')
        print('send me a message on Reddit, or check out my GitHub:\n')
        print('www.reddit.com/u/dreamwhite')
        print('www.github.com/dreamwhite\n')

        hr: int = datetime.datetime.now().time().hour
        if hr > 3 and hr < 12:
            print('Have a nice morning!\n\n')
        elif hr >= 12 and hr < 17:
            print('Have a nice afternoon!\n\n')
        elif hr >= 17 and hr < 21:
            print('Have a nice evening!\n\n')
        else:
            print('Have a nice night!\n\n')
        
        time.sleep(3)
        exit(0)

    def _clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def _init_sequence(self) -> None:
            self._clear_screen()
            self._print_welcome_banner()
            self._print_rules_menu()
            self._print_other_menu_entries()
    
    def _print_rules_menu(self) -> None:
        #TODO: Validate fields from config.plist, inside the _print_options_menu function, so unnecessary patches won't be applied again. Saves up more headache imho
        for rule in self.rules:
            for _,*_ in rule.items():
                print(f'[{"""#""" if rule["is_enabled"] else " "}] {self.rules.index(rule) + 1}.  {rule["name"]} - {rule["description"]}')
                break

    def _get_index_of_rule(self, rule: dict) -> int:
        return self.rules.index(rule)

    def _print_other_menu_entries(self) -> None:
        print('\n[ ] Q. Quit the program')
        print(f'{"[ ]" if not self.selected_config else "[#]"} S. Select the config.plist')
        print('[ ] D. Dump the config to censored_config.plist')

    def _dump(self) -> None:
        """Saves to a file the newly censored config.plist"""

        with open('censored_config.plist', 'wb') as f:
            try:
                plistlib.dump(self.plist, f)
                print(f"Successfully exported anonymized config.plist to {os.path.realpath(f.name)}")
            except (Exception,):
                print("An error occurred while trying to save the censored config.plist file!")

    def _check_rule_validity(self, rule: dict) -> bool:
        for key, value in rule.items():
            
    def _apply_rule(self, rule: dict, plist: dict) -> dict:
        new_config: dict = plist.copy()  # oil

        for field in rule.get('fields', []):
            rule_path = field.get('path', '')

            segments: str = rule_path.split('/')
            last_segment: str = segments[-1]

            current_segment_value: dict = new_config  # first memory reference
            for index, segment in enumerate(segments):
                if index == len(segments) - 1:
                    break  # stop just before we reach the destination to allow key access / mutation later on

                current_segment_value = current_segment_value[segment]  # this should update the variable while keeping the reference

            for value in field.get('values', []):
                default: bool = value.get('default', False)

                if default:
                    initial_value = current_segment_value.get(last_segment)
                    new_value: bool|bytes|dict|int|str = value.get('value', '')

                    initial_type: type = type(initial_value)
                    new_type: type = type(new_value)

                    if initial_value is not None:
                        if initial_type == new_type:
                            current_segment_value[last_segment] = new_value
                        else:
                            print(f'Type mismatch at {rule_path}; Expected {initial_type.__name__}, but got {new_type.__name__}')

        return new_config
    
    def _grab_plist_file(self) -> dict:

        user_input: str = input('Drag your config.plist here: ').replace("'", '') #BUG: When dragging from macOS terminal, quotes are applied to the user input string

        config_plist: Path = Path(user_input)

        if config_plist.exists():
            self.selected_config = True
            self.plist: dict =plistlib.load(open(config_plist, 'rb'))

        self._init_sequence()

    def _grab_user_input(self) -> None:
        while True:
            user_input: int|str = input('\nSelect an option: ')

            if user_input.isnumeric():
                self.rules[int(user_input) - 1]['is_enabled'] = not self.rules[int(user_input) - 1]['is_enabled']
                _: dict = self._apply_rule(self.rules[int(user_input) - 1], self.plist)

            elif user_input.lower() == 'q':
                self._quit_program()
            elif user_input.lower() == 's':
                self._grab_plist_file()
            elif user_input.lower() == 'd':
                self._dump()
            else:
                print('Unknown option, retry!')
                time.sleep(0.5)
                continue
            self._init_sequence()
            


if __name__ == '__main__':
    plist_stripper = PlistStripper()
