#!/usr/bin/python3.10

import datetime
import os
import plistlib
from pprint import pprint
import sys
import time

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
                            'type': list,
                            'values': [
                                {
                                    'name': 'Empty list',
                                    'description': 'No custom scanning paths through the bless model',
                                    'type': str,
                                    'value': '',
                                    'default': True
                                }
                            ],
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
                            'type': str,
                            'values': [
                                {
                                    'name': 'Disabled',
                                    'description': 'Do not register the launcher option in the firmware preferences for persistence',
                                    'type': str,
                                    'value': 'Disabled',
                                    'default': True
                                },
                                {
                                    'name': 'Full',
                                    'description': 'Create or update the top priority boot option in UEFI variable storage at bootloader startup',
                                    'type': str,
                                    'value': 'Full',
                                },
                                {
                                    'name': 'Short',
                                    'description': 'Create a short boot option instead of a complete one. Useful for Insyde H2O BIOS that are unable to manage full device paths',
                                    'type': str,
                                    'value': 'Short',
                                },
                                {
                                    'name': 'System',
                                    'description': 'Create no boot option but assume specified custom option is blessed. Useful when relying on ForceBooterSignature quirk',
                                    'type': str,
                                    'value': 'System',
                                },
                            ],
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
                            'type': int,
                            'values': [
                                {
                                    'name': '3',
                                    'description': 'Enable basic logging without writing to file',
                                    'type': int,
                                    'value': 3,
                                    'default': True
                                },
                                {
                                    'name': '67',
                                    'description': 'Enable file logging by writing to opencore-YYYY-MM-DD-HHMMSS.txt',
                                    'type': int,
                                    'value': 67
                                }
                            ],
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
                            'type': list,
                            'values': list(),
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
                            'type': int,
                            'values': [
                                {
                                    'name': '0',
                                    'description': 'Do not use Apple Enclave Identifier',
                                    'type': int,
                                    'value': 0,
                                    'default': 'True'
                                }
                            ],
                            'path': 'Misc/Security'
                        },
                        {
                            'name': 'ScanPolicy',
                            'type': int,
                            'values': [
                                {
                                    'name': '0',
                                    'description': 'Use default OpenCore scanning rules (APFS, SATA, NVMe mainly)',
                                    'type': int,
                                    'value': 0,
                                    'default': 'True'
                                }
                            ],
                            'path': 'Misc/Security'
                        },                        
                        {
                            'name': 'SecureBootModel',
                            'type': str,
                            'fields': [
                                {
                                    'name': 'SecureBootModel',
                                    'type': str,
                                    'values': [
                                        {
                                            'name': 'Disabled',
                                            'description': 'No model, Secure Boot will be disabled',
                                            'type': str,
                                            'value': 'Disabled',
                                            'default': True
                                        },
                                        {
                                            'name': 'Default',
                                            'description': 'Matching model for current SMBIOS',
                                            'type': str,
                                            'value': 'Default',
                                        },
                                    ],
                                    'path': 'Misc/Security'
                                }
                            ]
                        },
                        {
                            'name': 'Vault',
                            'type': str,
                            'values': [
                                {
                                    'name': 'Optional',
                                    'description': 'No vault is enforced, insecure',
                                    'type': str,
                                    'value': 'Optional',
                                    'default': True
                                },
                                {
                                    'name': 'Basic',
                                    'description': 'Require vault.plist file present in OC directory. This provides basic filesystem integrity verification and may protect from unintentional filesystem corruption',
                                    'type': str,
                                    'value': 'Basic',
                                },
                                {
                                    'name': 'Secure',
                                    'description': 'Require vault.sig signature file for vault.plist in OC directory. This includes Basic integrity checking but also attempts to build a trusted bootchain.',
                                    'type': str,
                                    'value': 'Secure',
                                },

                            ],
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
                            'type': str,
                            'values': [
                                {
                                    'name': 'Generic MLB',
                                    'description': 'Use a generic MLB for sharing purposes',
                                    'type': str,
                                    'value': 'M0000000000000001',
                                    'default': True
                                }
                            ],
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                        {
                            'name': 'ROM',
                            'type': bytes,
                            'values': [
                                {
                                    'name': 'Generic ROM',
                                    'description': 'Use a generic ROM for sharing purposes',
                                    'type': bytes,
                                    'value': b'\x11"3DUf',
                                    'default': True
                                }
                            ],
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                        {
                            'name': 'SystemSerialNumber',
                            'type': str,
                            'values': [
                                {
                                    'name': 'Generic SystemSerialNumber',
                                    'description': 'Use a generic SystemSerialNumber for sharing purposes',
                                    'type': str,
                                    'value': 'W00000000001',
                                    'default': True
                                }
                            ],
                            'path': 'PlatformInfo/Generic' #BUG: In case a user doesn't use Generic section of PlatformInfo, this doesn't work
                        },
                        {
                            'name': 'SystemUUID',
                            'type': str,
                            'values': [
                                {
                                    'name': 'Generic SystemUUID',
                                    'description': 'Use a generic SystemUUID for sharing purposes',
                                    'type': str,
                                    'value': '00000000-0000-0000-0000-000000000000',
                                    'default': True
                                }
                            ],
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
                            'type': int,
                            'values': [
                                {
                                    'name': 'MinDate',
                                    'description': 'Minimal allowed APFS driver date',
                                    'type': int,
                                    'value': -1,
                                    'default': True
                                }
                            ],
                            'path': 'UEFI/APFS'
                        },
                        {
                            'name': 'MinVersion',
                            'type': int,
                            'values': [
                                {
                                    'name': 'MinDate',
                                    'description': 'Minimal allowed APFS driver version',
                                    'type': int,
                                    'value': -1,
                                    'default': True
                                }
                            ],
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
                            'type': int,
                            'values': [
                                {
                                    'name': 'ResizeAppleGpuBars',
                                    'description': 'Disable ResizeAppleGpuBars quirk',
                                    'type': int,
                                    'value': -1,
                                    'default': True
                                }
                            ],
                            'path': 'Booter/Quirks'
                        },
                        {
                            'name': 'ResizeGpuBars',
                            'type': int,
                            'values': [
                                {
                                    'name': 'ResizeGpuBars',
                                    'description': 'Disable custom GPU PCI BAR custom sizes',
                                    'type': int,
                                    'value': -1,
                                    'default': True
                                }
                            ],
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
            self._print_options_menu()
    
    def _print_options_menu(self) -> None:
        #TODO: Validate fields from config.plist, inside the _print_options_menu function, so unnecessary patches won't be applied again. Saves up more headache imho
        for rule in self.rules:
            for _,*_ in rule.items():
                print(f'[{"""#""" if rule["is_enabled"] else " "}] {self.rules.index(rule) + 1}.  {rule["name"]} - {rule["description"]}')
                break

    def _get_index_of_rule(self, rule: dict) -> int:
        return self.rules.index(rule)

    def _grab_plist_file(self) -> None:
        ...

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
