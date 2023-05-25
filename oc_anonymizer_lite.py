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
        self.delete_platforminfo_generic()
        self.reset_misc_security()
        self.disable_uefi_apfs()
        self.dump()

    def delete_platforminfo_generic(self) -> None:
        """Censors several SMBIOS identification fields"""

        self.plist['PlatformInfo']['Generic']['MLB'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['ROM'] = b'\x11"3DUf'
        self.plist['PlatformInfo']['Generic']['SystemSerialNumber'] = 'XX-CHANGE_ME-XX'
        self.plist['PlatformInfo']['Generic']['SystemUUID'] = 'XX-CHANGE_ME-XX'

    def reset_misc_security(self) -> None:
        """Sets
            -> Misc/Security/ScanPolicy = 0 to allow OpenCore's operating system detection policy
        """

        self.plist['Misc']['Security']['ScanPolicy'] = 0

    def disable_uefi_apfs(self) -> None:
        """Disables minimal APFS driver version checks, so it can be loaded on macOS Catalina and older. Otherwise, APFS drives won't show in BootPicker."""

        self.plist['UEFI']['APFS']['MinDate'] = -1
        self.plist['UEFI']['APFS']['MinVersion'] = -1

    def dump(self):
        """Saves the dleaned config.plist to a new file."""

        with open('censored_config.plist', 'wb') as f:
            try:
                plistlib.dump(self.plist, f)
                print(f"Successfully exported anonymized config.plist to {os.path.realpath(f.name)}")
            except (Exception,):
                print("An error occurred while trying to save the censored config.plist file!")



if __name__ == '__main__':
    plist_stripper = PlistStripper()
