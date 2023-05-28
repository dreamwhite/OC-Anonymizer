#!/usr/bin/python3.10

import datetime
import json
import os
import plistlib
import time

class PlistStripper:
    def __init__(self):
        self.plist = plistlib.load(open('config.plist', 'rb')) #BUG: should be user defined by using D letter in the shell. Actually keeping it for testing purposes
        self.rules = json.load(open('rules.json', 'r'))
        self.selected_config = True if self.plist else False
        self._init_sequence()
        self._grab_user_input()
        #TODO: convert the next line to a user input, so it can be dinamycally changed
        


        # self.dump() options dumps the input config.plist, after applying the selected patches, onto a new censored_config.plist

        # TODO: create a shell-like behaviour where the user has to select the config.plist using S key, by dragging onto the terminal the desired config file.
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

        hr = datetime.datetime.now().time().hour
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

    def _apply_rule(self, rule: dict, plist: dict) -> dict:
        new_config = plist.copy()  # oil
        current_segment_value = new_config  # first memory reference

        for field in rule.get('fields', []):
            rule_path = field.get('path', '')

            segments = rule_path.split('/')
            last_segment = segments[-1]

            for index, segment in enumerate(segments):
                if index == len(segments) - 1:
                    break  # stop just before we reach the destination to allow key access / mutation later on

                current_segment_value = current_segment_value[segment]  # this should update the variable while keeping the reference

            for value in field.get('values', []):
                default = value.get('default', False)

                if default:
                    initial_value = current_segment_value.get(last_segment)
                    new_value = value.get('value', '')

                    initial_type = type(initial_value)
                    new_type = type(new_value)

                    if initial_value is not None:
                        if initial_type == new_type:
                            current_segment_value[last_segment] = new_value
                        else:
                            print(f'Type mismatch at {rule_path}; Expected {initial_type.__name__}, but got {new_type.__name__}')

        return new_config
    
    def _grab_plist_file(self) -> None:
        # Here I'll write the code for loading the plist file from a user input
        # plist_path
        # self.plist = plistlib.load(open(plist_path, 'rb'))
        self.selected_config = True
        self._init_sequence()

    def _grab_user_input(self) -> None:
        while True:
            user_input = input('Select an option: ')

            if user_input == '1':
                self._delete_misc_blessoverride()
            elif user_input == '2':
                self._reset_misc_boot()
            elif user_input == '3':
                self._reset_misc_debug()
            elif user_input == '4':
                self._delete_misc_entries()
            elif user_input == '5':
                self._reset_misc_security()
            elif user_input == '6':
                self._delete_platforminfo_generic()
            elif user_input == '7':
                self._disable_uefi_apfs()
            elif user_input == '8':
                self._disable_resizable_bar_support()
            elif user_input.lower() == 'q':
                self._quit_program()
            elif user_input.lower() == 's':
                self._grab_plist_file()
            else:
                print('Unknown option, retry!')
                time.sleep(0.5)
                continue
            self.rules[int(user_input) - 1]['is_enabled'] = not self.rules[int(user_input) - 1]['is_enabled']
            self._init_sequence()
            
              
    def _reset_misc_boot(self) -> None:
        """ Sets Misc/Boot/LauncherOption to Disabled to avoid registering the launcher option in the firmware
        preferences for persistence"""

        self.plist['Misc']['Boot']['LauncherOption'] = 'Disabled'

    def _delete_misc_blessoverride(self) -> None:
        """ Deletes custom BlessOverride entries from config.plist"""

        self.plist['Misc']['BlessOverride'] = []

    def _reset_misc_debug(self) -> None:
        """ Sets Misc/Debug/Target to 3"""

        self.plist['Misc']['Debug']['Target'] = 3

    def _delete_misc_entries(self) -> None:
        """ Deletes custom bootloader entries from config.plist"""

        self.plist['Misc']['Entries'] = []

    def _reset_misc_security(self) -> None:
        """Sets
            -> Misc/Security/ApECID to 0 to disallow using personalised Apple Secure Boot identifiers (unsupported from
                Monterey and later)
            -> Misc/Security/ScanPolicy = 0 to allow OpenCore's operating system detection policy
            -> Misc/Security/SecureBootModel = Disabled. Disables Apple Secure Boot hardware model to avoid issues during Installation. Re-enable in Post-Install so System Updates work when using an SMBIOS of a Mac model with a T2 Security Chip.
            -> Misc/Security/Vault = Optional to disable OpenCore's vaulting mechanism
        """

        self.plist['Misc']['Security']['ApECID'] = 0
        self.plist['Misc']['Security']['ScanPolicy'] = 0
        self.plist['Misc']['Security']['SecureBootModel'] = 'Disabled'
        self.plist['Misc']['Security']['Vault'] = 'Optional'

    def _delete_platforminfo_generic(self) -> None:
        """Censors several SMBIOS identification fields"""

        self.plist['PlatformInfo']['Generic']['MLB'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['ROM'] = b'\x11"3DUf'
        self.plist['PlatformInfo']['Generic']['SystemSerialNumber'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['SystemUUID'] = 'XX-CHANGE_ME-XX'

    def _disable_uefi_apfs(self) -> None:
        """ Sets minimal allowed APFS driver date and version to permit any release date and version to load"""

        self.plist['UEFI']['APFS']['MinDate'] = -1
        self.plist['UEFI']['APFS']['MinVersion'] = -1

    def _dump(self):
        """Saves to a file the newly censored config.plist"""

        with open('censored_config.plist', 'wb') as f:
            try:
                plistlib.dump(self.plist, f)
                print(f"Successfully exported anonymized config.plist to {os.path.realpath(f.name)}")
            except (Exception,):
                print("An error occurred while trying to save the censored config.plist file!")

if __name__ == '__main__':
    plist_stripper = PlistStripper()
