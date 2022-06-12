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
        self.censor_misc_boot()
        self.censor_misc_debug()
        self.censor_misc_security()
        self.censor_platforminfo_generic()
        self.censor_uefi_apfs()
        self.dump()

    def censor_misc_boot(self) -> None:
        """ Sets Misc/Boot/LauncherOption to Disabled to avoid registering the launcher option in the firmware
        preferences for persistence"""

        self.plist['Misc']['Boot']['LauncherOption'] = 'Disabled'

    def censor_misc_debug(self) -> None:
        """ Sets Misc/Debug/Target to 3"""

        self.plist['Misc']['Debug']['Target'] = 3

    def censor_misc_security(self) -> None:
        """Sets
            -> Misc/Security/ApECID to 0 to disallow using personalised Apple Secure Boot identifiers (unsupported from
                Monterey and later)
            -> Misc/Security/ScanPolicy = 0 to allow OpenCore's operating system detection policy
            -> Misc/Security/SecureBootModel = Default to configure Apple Secure Boot hardware model
            -> Misc/Security/Vault = Optional to disable OpenCore's vaulting mechanism
        """

        self.plist['Misc']['Security']['ApECID'] = 0
        self.plist['Misc']['Security']['ScanPolicy'] = 0
        self.plist['Misc']['Security']['SecureBootModel'] = 'Default'
        self.plist['Misc']['Security']['Vault'] = 'Optional'

    def censor_platforminfo_generic(self) -> None:
        """Censors several SMBIOS identification fields"""

        self.plist['PlatformInfo']['Generic']['MLB'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['ROM'] = b'\x11"3DUf'
        self.plist['PlatformInfo']['Generic']['SystemSerialNumber'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['SystemUUID'] = 'XX-CHANGE_ME-XX'

    def censor_uefi_apfs(self) -> None:
        """ Sets minimal allowed APFS driver date and version to permit any release date and version to load"""

        self.plist['UEFI']['APFS']['MinDate'] = -1
        self.plist['UEFI']['APFS']['MinVersion'] = -1

    def dump(self):
        """Saves to a file the newly censored config.plist"""

        with open('censored_config.plist', 'wb') as f:
            try:
                plistlib.dump(self.plist, f)
                print(f"Successfully exported censored config.plist in {os.path.realpath(f.name)}")
            except (Exception,):
                print("An error occurred while trying to save the censored config.plist file!")


if __name__ == '__main__':
    plist_stripper = PlistStripper()
