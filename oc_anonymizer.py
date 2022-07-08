#!/usr/bin/python3.10

import os
import plistlib
import sys


def load_plist() -> dict:
    """ Loads .plist XML like file and returns the opened buffer

    :return: dict-like object of the loaded plist
    """
    return plistlib.load(open(sys.argv[1], 'rb'))


class PlistStripper:
    def __init__(self):
        self.plist = load_plist()
        print(self.plist['PlatformInfo']['Generic']['ROM'])
        self.reset_misc_boot()
        self.delete_misc_blessoverride()
        self.reset_misc_debug()
        self.delete_misc_entries()
        self.reset_misc_security()
        self.delete_platforminfo_generic()
        self.disable_uefi_apfs()
        self.dump()

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
            -> Misc/Security/SecureBootModel = Disables Apple Secure Boot hardware model to avoid issues during Installation. Re-enable in Post-Install so System Updates work when using an SMBIOS of a Mac model with a T2 Security Chip.
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
