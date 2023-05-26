import os
import sys

rules = [
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
                    'is_enabled': False  
                }
        ]

def print_options() -> None:
     
    for rule in rules:
        for _,*_ in rule.items():
            print(f'[{"""#""" if rule["is_enabled"] else " "}] {rules.index(rule) + 1}.  {rule["name"]} - {rule["description"]}')
            break

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
            print_options()
            user_input = input('Select an option: ')

            #BUG: Thx to Python to only introduce in v3.10 match case syntax... I'll stick to the good old one if syntax...
            #BUG: Find a  
            if user_input == '1':
                print('1')
            elif user_input == '2':
                print('2')
            elif user_input == '3':
                print('3')
            elif user_input == '4':
                print('4')
            elif user_input == '5':
                print('5')
            elif user_input == '6':
                print('6')
            elif user_input == '7':
                print('7')
            elif user_input == '8':
                print('8')
            elif user_input.lower() == 'q':
                sys.exit(0)
            else:
                print('Unknown option, retry!')
                clear_screen()
                print_options()
                continue
            rules[int(user_input) - 1]['is_enabled'] = not rules[int(user_input) - 1]['is_enabled'] #BUG: not changing the value when selecting another entry
            