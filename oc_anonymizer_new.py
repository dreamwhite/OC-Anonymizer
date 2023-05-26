#!/usr/bin/python3.10

import datetime
import os
import plistlib
from pprint import pprint
import sys
import time


# def load_plist() -> dict:
#     """ Loads .plist XML like file and returns the opened buffer

#     :return: dict-like object of the loaded plist
#     """
#     return plistlib.load(open(sys.argv[1], 'rb'))


class PlistStripper:
    def __init__(self):
        self.plist = plistlib.load(open('config.plist', 'rb')) #BUG: should be user defined by using D letter in the shell. Actually keeping it for testing purposes

        self.rules = [
                {
                    'name': 'Delete Misc/BlessOverride settings',
                    'description': 'Add custom scanning paths through the bless model',
                    'fields': [
                        {
                            'name': 'BlessOverride',
                            'field_type': list,
                            'field_value': [],
                            'path': 'Misc/BlessOverride',
                        }
                    ],
                    'is_enabled': True
                },
                {
                    'name': 'Reset Misc Boot settings',
                    'description': 'Sets Misc/Boot/LauncherOption to Disabled to avoid registering the launcher option in the firmware preferences for persistence',
                    'fields': [
                        {
                            'name': 'LauncherOption',
                            'field_type': str,
                            'field_value': 'Disabled',
                            'path': 'Misc/Boot'
                        },
                    ],
                    'is_enabled': True
                },
                {
                    'name': 'Reset Misc Debug settings',
                    'description': 'Sets Misc/Debug/Target to 3',
                    'fields': [
                        {
                            'name': 'Target',
                            'field_type': int,
                            'field_value': 3,
                            'path': 'Misc/Debug'
                        },
                    ],
                    'is_enabled': True
                },
                {
                    'name': 'Delete Misc/Entries settings',
                    'description': 'Deletes custom bootloader entries from config.plist',
                    'fields': [
                        {
                            'name': 'Entries',
                            'field_type': list,
                            'field_value': list(),
                            'path': 'Misc/Entries'
                        },
                    ],
                    'is_enabled': True  
                },
                {
                    'name': 'Delete Misc/Security settings',
                    'description': 'Various security settings to fix from config.plist',
                    'fields': [
                        {
                            'name': 'ApECID',
                            'field_type': int,
                            'field_value': 0,
                            'path': 'Misc/Security'
                        },
                        {
                            'name': 'ScanPolicy',
                            'field_type': int,
                            'field_value': 0,
                            'path': 'Misc/Security'
                        },                        
                        {
                            'name': 'SecureBootModel',
                            'field_type': str,
                            'field_value': 'Disabled',
                            'path': 'Misc/Security'
                        },
                        {
                            'name': 'Vault',
                            'field_type': str,
                            'field_value': 'Optional',
                            'path': 'Misc/Security'
                        },
                    ],
                    'is_enabled': True  
                },
                {
                    'name': 'Censor PlatformInfo settings',
                    'description': 'Censors several SMBIOS identification fields',
                    'fields': [
                        {
                            'name': 'MLB',
                            'field_type': str,
                            'field_value': 'M0000000000000001',
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                        {
                            'name': 'ROM',
                            'field_type': bytes,
                            'field_value': b'\x11"3DUf',
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                        {
                            'name': 'SystemSerialNumber',
                            'field_type': str,
                            'field_value': 'W00000000001',
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                        {
                            'name': 'SystemUUID',
                            'field_type': str,
                            'field_value': '00000000-0000-0000-0000-000000000000',
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                    ],
                    'is_enabled': True  
                },
                {
                    'name': 'Change APFS settings',
                    'description': 'Sets minimal allowed APFS driver date and version to permit any release date and version to load',
                    'fields': [
                        {
                            'name': 'MinDate',
                            'field_type': int,
                            'field_value': -1,
                            'path': 'UEFI/APFS'
                        },
                        {
                            'name': 'MinVersion',
                            'field_type': int,
                            'field_value': -1,
                            'path': 'UEFI/APFS'
                        },
                    ],
                    'is_enabled': True  
                },
                {
                    'name': 'Disable Resizable BAR Support',
                    'description': 'Sets two quirks in config.plist to disable Resizable BAR support if it\' disabled in system firmware settings',
                    'fields': [
                        {
                            'name': 'ResizeAppleGpuBars',
                            'field_type': int,
                            'field_value': -1,
                            'path': 'Booter/Quirks'
                        },
                        {
                            'name': 'ResizeGpuBars',
                            'field_type': int,
                            'field_value': -1,
                            'path': 'UEFI/Quirks'
                        },
                    ],
                    'is_enabled': True  
                }
        ]
        self._print_welcome_banner()
        self._print_options_menu()
        self._grab_user_input()
        #TODO: convert the next line to a user input, so it can be dinamycally changed
        # self.plist = plistlib.load(open(sys.argv[1], 'rb'))


        # self.delete_misc_blessoverride()
        # self.reset_misc_boot()
        # self.reset_misc_debug()
        # self.delete_misc_entries()
        # self.reset_misc_security()
        # self.delete_platforminfo_generic()
        # self.disable_uefi_apfs()
        # self.dump()

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
            self._print_options_menu()
    
    def _print_options_menu(self) -> None:
        for rule in self.rules:
            for key,value in rule.items():
                print(f'[{"""#""" if rule["is_enabled"] else " "}] {self.rules.index(rule) + 1}.  {rule["name"]} - {rule["description"]}')
                break

    def _get_index_of_rule(self, rule: dict) -> int:
        return self.rules.index(rule)

    def _grab_plist_file(self) -> None:
        ...
    def _grab_user_input(self) -> None:
        while True:
            user_input = input('Select an option: ')

            #BUG: Thx to Python to only introduce in v3.10 match case syntax... I'll stick to the good old one if syntax...
            #BUG: Find a  
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
            else:
                print('Unknown option, retry!')
                time.sleep(0.5)
                self._init_sequence()
                continue
            self._init_sequence()
            self.rules[int(user_input) - 1]['is_enabled'] = not self.rules[int(user_input) - 1]['is_enabled'] #BUG: not changing the value when selecting another entry
            
              
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
