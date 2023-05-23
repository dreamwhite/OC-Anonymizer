![macOS](https://img.shields.io/badge/Supported_OC_build:-≥0.8.2-white.svg)

# OC Anonymizer – remove sensitive data from your config.plist

## About
Python Script for removing sensitive data from OpenCore's `config.plist`. Useful if you plan to share your Config/EFI online. Also resets some settings to default values used in sample.plist which should not be carried over to a differnt system. Check the feature list for more details.

## Features

### Full version

Changes the following Settings/Parameters in the **config.plist**:

- Removes MLB, ROM, Serials from **PlatformInfo/Generic**: 
	- `PlatformInfo/Generic/MLB`
	- `PlatformInfo/Generic/ROM`
	- `PlatformInfo/Generic/SystemSerialNumber`
	- `PlatformInfo/Generic/SystemUUID`
- **Security Settings**:
	- `Misc/Security/ApECID` = `0` &rarr; ApECID has to be generated in the target system itself!
	- `Misc/Security/ScanPolicy` = `0` &rarr; So the system sarchs all available volumes and file systems.
	- `Misc/Security/SecureBootModel` = `Disabled` &rarr; :warning: Disables Apple Secure Boot hardware model to avoid issues during Installation. Re-enable it in Post-Install so System Updates work when using an SMBIOS of a Mac model with a T2 Security Chip!
	- `Misc/Security/Vault` = `Optional` &rarr; Has to be created on the target system itself!
- **Other Settings**:
	- Changes `Boter/Quirks/ResizeAppleGpuBars` to `-1` &rarr; Disables Resizable BAR in macOS. Just in case the next user's GPU doesn't support it or it is disabled in BIOS.
	- Changes `UEFI/Quirks/ResizeGpuBars` to `-1` &rarr; Disables Resizable BAR in UEFI for the same reason.
	- Changes `Misc/Boot/LauncherOption` to `Disabled` &rarr; To avoid changing boot menu entries on the target system's Firmware/BIOS.
	- Removes custom entries from `Misc/BlessOverride` &rarr; These overrides have to be created on the target system.
	- Removes custom boot loader entries from `Misc/Entries`
	- Changes `Misc/Debug/Target` to `3` (Default)
	- `UEFI/APFS`:  Changes `MinDate` and `MinVersion` to `-1` to maximize macOS compatibility. Otherwise the APFS driver isn't loaded in macOS 10.15 or older so you won't see any entries of APFS drives in OpenCore's Boot Menu.

### Lite version

The lite version of this script will only anonymize SMBIOS and change APFS settings:

- Anonymizes entries in **PlatformInfo/Generic**:
	- `PlatformInfo/Generic/MLB`
	- `PlatformInfo/Generic/ROM`
	- `PlatformInfo/Generic/SystemSerialNumber`
	- `PlatformInfo/Generic/SystemUUID`

- Changes **APFS** settings: 
	- `UEFI/APFS`: Changes `MinDate` and `MinVersion` to `-1` to maximize macOS compatibility. Otherwise the APFS driver isn't loaded in macOS 10.15 or older so you won't see any entries of APFS drives in OpenCore's Boot Menu. 

## Instructions
- Install [**Python**](https://www.python.org/) if you haven't already
- Click on "Code" > "Download ZIP" and upack it.
- Run Terminal
- Enter:</br>
`cd ~/Downloads/OC-Anonymizer-master`
- Next, enter </br>`python3 oc_anonymizer_full.py PATH_TO_CONFIG.plist` (or drag and drop your config into the terminal window after ".py")
- For running the Lite Version, enter enter </br>`python3 oc_anonymizer_lite.py PATH_TO_CONFIG.plist`
- Hit `ENTER`

This will create a `censored_config.plist`in the oc_anonymizer folder without sensitive data and changed settings as described. Rename the file to config.plist and place it in the EFI folder you want to share with the worl

## Issues

If you encounter any issue, please file a bugreport [here](https://github.com/dreamwhite/bugtracker/issues/new?assignees=dreamwhite&labels=bug&template=generic.md&title=)

## Credits and Resources

- [Acidanthera](https://github.com/acidanthera) for [OpenCorePkg](https://github.com/acidanthera)
- [1alessandro1](https://github.com/1alessandro1) for the initial idea
- [Dreamwhite](https://github.com/dreamwhite) for the original Python script
- [Guide](https://github.com/5T33Z0/OC-Little-Translated/tree/main/M_EFI_Upload_Chklst) for removing sensitive data manually
