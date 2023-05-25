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
        self.plist = plistlib.load(open(sys.argv[1], 'rb'))

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

    def reset_misc_boot(self) -> None:
        """ Sets Misc/Boot/LauncherOption to Disabled to avoid registering the launcher option in the firmware
        preferences for persistence"""

        self.plist['Misc']['Boot']['LauncherOption'] = 'Disabled'

    def delete_misc_blessoverride(self) -> None:
        """ Deletes custom BlessOverride entries from config.plist"""

        self.plist['Misc']['BlessOverride'] = []

    def reset_misc_debug(self) -> None:
        """ Sets Misc/Debug/Target to 3"""

        self.plist['Misc']['Debug']['Target'] = 3

    def delete_misc_entries(self) -> None:
        """ Deletes custom bootloader entries from config.plist"""

        self.plist['Misc']['Entries'] = []

    def reset_misc_security(self) -> None:
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

    def delete_platforminfo_generic(self) -> None:
        """Censors several SMBIOS identification fields"""

        self.plist['PlatformInfo']['Generic']['MLB'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['ROM'] = b'\x11"3DUf'
        self.plist['PlatformInfo']['Generic']['SystemSerialNumber'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['SystemUUID'] = 'XX-CHANGE_ME-XX'

    def disable_uefi_apfs(self) -> None:
        """ Sets minimal allowed APFS driver date and version to permit any release date and version to load"""

        self.plist['UEFI']['APFS']['MinDate'] = -1
        self.plist['UEFI']['APFS']['MinVersion'] = -1

    def dump(self):
        """Saves to a file the newly censored config.plist"""

        with open('censored_config.plist', 'wb') as f:
            try:
                plistlib.dump(self.plist, f)
                print(f"Successfully exported anonymized config.plist to {os.path.realpath(f.name)}")
            except (Exception,):
                print("An error occurred while trying to save the censored config.plist file!")

if __name__ == '__main__':
    plist_stripper = PlistStripper()
