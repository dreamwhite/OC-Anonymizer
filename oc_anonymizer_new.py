#!/usr/bin/python3.10

import os
import plistlib
import sys


# def load_plist() -> dict:
#     """ Loads .plist XML like file and returns the opened buffer

#     :return: dict-like object of the loaded plist
#     """
#     return plistlib.load(open(sys.argv[1], 'rb'))


class PlistStripper:
    def __init__(self):
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

        # TODO: display a welcome banner
        # TODO: display checkboxes like following
        #           1. Delete Misc/BlessOverride settings
        #           2. Reset Misc/Boot settings
        #                 - Set LauncherOption to "Disabled"
        #           3. Reset Misc/Debug settings
        #                 - Set Target to 3
        #           4. Delete Misc/Entries settings
        #           5. Reset Misc/Security settings
        #                 - Set ApECID to 0
        #                 - Set ScanPolicy to 0
        #                 - Set SecureBootModel to "Disabled"
        #                 - Set Vault to "Optional"
        #           6. Censor PlatformInfo/Generic settings
        #                 - Set MLB to "M0000000000000001"
        #                 - Set ROM to b'\x11"3DUf'
        #                 - Set SystemSerialNumber to "W00000000001"
        #                 - Set SystemUUID to "00000000-0000-0000-0000-000000000000"
        #           7. Reset UEFI/APFS settings
        #                 - Set MinDate to -1
        #                 - Set MinVersion to -1
        #           8. Disable Resizable BAR Support
        #                 - Set Booter/Quirks/ResizeAppleGpuBars to -1
        #                 - Set UEFI/Quirks/ResizeGpuBars to -1
        
        # TODO: create a shell-like behaviour where the user has to select the config.plist using S key, by dragging onto the terminal the desired config file.
        # BUG: For each option, in case of older version of OpenCore where some options may be missing (e.g. Resizable BAR Support options), the script will display only the available options (e.g. missing Resizable BAR Support options, therefore "8" won't be selectable and the text will be displayed with a grey foreground text) (use conditionals 'key' in self.plist.keys())
        # BUG: In case of possible sensitive data (mainly PlatformInfo/Generic settings) a yellow/orange foreground text should be displayed, so the user knows that he's missing these important options.
        # BUG: When dumping "censored_config.plist", in case possible sensitive data censoring options are left unchecked, a warning message should be displayed, so the user can choose whether to ignore them, and therefore continue dumping, or fix them manually (by displaying a menu like done before).
        # TODO: When the user selects the desired policies to apply on the resulting "censored_config.plist", the enabled options should have a green foreground text, while the disabled one a red, or a white foreground text.
        # TODO: Do not delete any of the currently available settings (e.g. reset_misc_boot etc) because they'll be used when dumping the resulting "censored_config.plist"

    def _print_welcome_banner(self) -> None:
        """ Prints a welcome banner"""
        print("""
  ___    ___        ___                   _  _         _               
 / _ \  / __|      /   \ _ _   ___  _ _  | || | _ __  (_) ___ ___  _ _ 
| (_) || (__       | - || ' \ / _ \| ' \  \_. || '  \ | ||_ // -_)| '_|
 \___/  \___|      |_|_||_||_|\___/|_||_| |__/ |_|_|_||_|/__|\___||_|  
""")
              
    
    def _print_goodbye_banner(self) -> None:
        ...

    def _print_options_menu(self) -> None:
        for rule in self.rules:
            for key,value in rule.items():
                print(f'[{"""#""" if rule["is_enabled"] else " "}] {self.rules.index(rule) + 1}.  {rule["name"]} - {rule["description"]}')
                break

    def _get_index_of_rule(self, rule: int):
        return self.rules.index(rule)

    def _grab_user_input(self) -> None:
        while True:
            user_input = input('Select an option: ')

            #BUG: Thx to Python to only introduce in v3.10 match case syntax... I'll stick to the good old one if syntax...
            #BUG: How tf am I supposed to identify the rule index among the other rules? 10:17 PM rn

            if user_input == '1':
                self.delete_misc_blessoverride()
            if user_input == '2':
                self.reset_misc_boot()
            if user_input == '3':
                self.reset_misc_debug()
            if user_input == '4':
                self.delete_misc_entries()
            if user_input == '5':
                self.reset_misc_security()
            if user_input == '6':
                self.delete_platforminfo_generic()
            if user_input == '7':
                self.disable_uefi_apfs()
            if user_input == '8':
                self.disable_resizable_bar_support()
            if user_input == 'Q':
                self._print_goodbye_banner()
                sys.exit(0)
              
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
