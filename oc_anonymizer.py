#!/usr/bin/python3.10

import datetime
import json
import os
from pathlib import Path
import plistlib
import time

class Colors():
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
class PlistStripper:
    def __init__(self) -> None:

        self.config_plist: Path = Path()
        self.plist: dict = dict()
        self.rules: dict = json.load(open('rules.json', 'r'))
        self.enabled_rules = [rule for rule in self.rules if rule['is_enabled']]
        self.run_patches: bool = False
        self.selected_config: bool = False

        self._init_sequence(sleep_time=0)
        self._grab_user_input()


    def _check_if_output_config_exists(self) -> bool:
        return Path('censored_config.plist').exists()

    # TODO: For each option, in case of older version of OpenCore where some options may be missing (e.g. Resizable BAR Support options), the script will display only the available options (e.g. missing Resizable BAR Support options, therefore "8" won't be selectable and the text will be displayed with a grey foreground text) (use conditionals 'key' in self.plist.keys())
    # TODO: In case of possible sensitive data (mainly PlatformInfo/Generic settings) a yellow/orange foreground text should be displayed, so the user knows that he's missing these important options.
    # TODO: When dumping "censored_config.plist", in case possible sensitive data censoring options are left unchecked, a warning message should be displayed, so the user can choose whether to ignore them, and therefore continue dumping, or fix them manually (by displaying a menu like done before).
    #BUG: When applying PlatformInfo/Generic/ROM rule, bytes-like object cannot be serialized. Therefore implement the following code described here: https://stackoverflow.com/a/40000564
    
    def _print_welcome_banner(self) -> None:
        """ Prints a welcome banner"""
        print(f"""{Colors.BLUE}
  ___    ___        ___                   _  _         _               
 / _ \  / __|      /   \ _ _   ___  _ _  | || | _ __  (_) ___ ___  _ _ 
| (_) || (__       | - || ' \ / _ \| ' \  \_. || '  \ | ||_ // -_)| '_|
 \___/  \___|      |_|_||_||_|\___/|_||_| |__/ |_|_|_||_|/__|\___||_|  
{Colors.RESET}""")
              
    
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
        
        time.sleep(1.5)
        exit(0)

    def _clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def _init_sequence(self, clear_screen:bool = True, print_welcome_banner:bool = True, print_rules_menu:bool = True, print_other_menu_entries:bool = True, sleep_time: int = 0.5) -> None:
            if clear_screen:
                self._clear_screen()
            if print_welcome_banner:
                self._print_welcome_banner()
            if print_rules_menu:
                self._print_rules_menu()
            if print_other_menu_entries:
                self._print_other_menu_entries()
            
            time.sleep(sleep_time)

    def _rule_validity(rule: dict, plist: dict) -> bool:
        path = rule.get(path)

    def _run_patches(self) -> None:

        if self.enabled_rules == list(): #If list is empty asks the user to select the required patches
            print(f'{Colors.RED}No rules are selected! Please select at least one, and then try again.')
            self._init_sequence(sleep_time=0.3)
        else:
            for rule in self.enabled_rules:
                _: dict = self._apply_rule(rule, self.plist)

    def _print_rules_menu(self) -> None:
        #TODO: Validate fields from config.plist, inside the _print_options_menu function, so unnecessary patches won't be applied again. Saves up more headache imho
        for rule in self.rules:
            for _,*_ in rule.items():
                print(f'{Colors.YELLOW} {self.rules.index(rule) + 1}) {rule["name"]} {f"{Colors.GREEN}[Enabled]{Colors.RESET}" if rule["is_enabled"] else f"{Colors.RED}[Disabled]{Colors.RESET}"}\n\t- {Colors.BLUE}{rule["description"]}{Colors.RESET}\n')
                break

    def _get_index_of_rule(self, rule: dict) -> int:
        return self.rules.index(rule)

    def _print_other_menu_entries(self) -> None:
        print(f'{"[ ]" if not self.selected_config else "[#]"} S. Select the config.plist {Colors.CYAN}{f"- {self.config_plist.as_posix()}" if self.selected_config else ""}{Colors.RESET}')
        print(f'{"[ ]" if not self.run_patches else "[#]"} R. Run the selected patches')
        print('[ ] D. Dump the config to censored_config.plist')
        print('\n[ ] Q. Quit the program')

    def _dump(self) -> None:
        """Saves to a file the newly censored config.plist"""

        self._init_sequence(print_rules_menu=False, print_other_menu_entries=False, sleep_time=0.3)

        if self._check_if_output_config_exists():
            overwrite_file:str = input(f'{Colors.RED}File already exists! Do you want to overwrite it? [y/N] {Colors.RESET}')
            if overwrite_file.lower() == 'y':
                with open('censored_config.plist', 'wb') as f:
                    try:
                        plistlib.dump(self.plist, f)
                        self._init_sequence(print_rules_menu=False, print_other_menu_entries=False, sleep_time=0)
                        print(f'{Colors.GREEN}Successfully overwritten anonymized config.plist to {os.path.realpath(f.name)}{Colors.RESET}')
                        self._init_sequence(clear_screen=False, print_welcome_banner=False, print_rules_menu=False, print_other_menu_entries=False)
                    except (Exception,):
                        print(f'{Colors.YELLOW}An error occurred while trying to save the censored config.plist file!{Colors.RESET}')
            else:
                self._init_sequence()
        else:
            with open('censored_config.plist', 'wb') as f:
                    try:
                        plistlib.dump(self.plist, f)
                        self._init_sequence(print_rules_menu=False, print_other_menu_entries=False, sleep_time=0.3)
                        print(f'{Colors.GREEN}Successfully exported anonymized config.plist to {os.path.realpath(f.name)}{Colors.RESET}')
                        self._init_sequence(clear_screen=False, print_welcome_banner=False, print_rules_menu=False, print_other_menu_entries=False)
                    except Exception as e:
                        print(f'{Colors.YELLOW}An error occurred while trying to save the censored config.plist file!{Colors.RESET}.')
                        input("Exception occurred while trying to save the file")

        self._init_sequence()

    # def _check_rule_validity(self, rule: dict) -> bool:
        # for key, value in rule.items():
            
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
        self._init_sequence(print_rules_menu=False,print_other_menu_entries=False,sleep_time=0)
        user_input: str = input('Drag your config.plist here: ').replace("'", '') #BUG: When dragging from VSCode terminal, quotes are applied to the user input string

        self.config_plist = Path(user_input)

        if self.config_plist.exists():
            self.selected_config = True
            self.plist: dict = plistlib.load(open(self.config_plist, 'rb'))

        self._init_sequence()

    def _grab_user_input(self) -> None:
        while True:
            user_input: int|str = input('\nSelect an option: ')

            if user_input.isnumeric():
                if not self.selected_config:
                    print('Warning, you must select a config before applying patches')
                    self._init_sequence(sleep_time=1)
                else:    
                    self.rules[int(user_input) - 1]['is_enabled'] = not self.rules[int(user_input) - 1]['is_enabled']
                    if not self.rules[int(user_input) - 1]['is_enabled']:
                        self.enabled_rules.remove(self.rules[int(user_input) - 1])
                    else:
                        self.enabled_rules.append(self.rules[int(user_input) - 1])

            elif user_input.lower() == 'q':
                self._quit_program()

            elif user_input.lower() == 'r':
                self._run_patches()

            elif user_input.lower() == 's':
                self._grab_plist_file()

            elif user_input.lower() == 'd': # If the user hasn't selected yet the config, it should be asked
                if self.selected_config:
                    self._dump()

            else:
                print('Unknown option, retry!')
                time.sleep(0.5)
                continue

            self._init_sequence()
            
if __name__ == '__main__':
    plist_stripper = PlistStripper()