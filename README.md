![macOS](https://img.shields.io/badge/Supported_OC_build:-≥0.8.2-white.svg)

# OC Anonymizer – remove sensitive data from your config.plist

## About
Python Script for removing sensitive data from OpenCore's `config.plist`. Useful if you plan to share your Config/EFI online. Also resets some settings to default values which should not be carried over to a differnt system. Check the feature list for more details.

## Features

Changes the following Settings/Parameters in the **config.plist**:

- Anonymizes **SMBIOS** data for:
	- `PlatformInfo/Generic/MLB`
	- `PlatformInfo/Generic/ROM`
	- `PlatformInfo/Generic/SystemSerialNumber`
	- `PlatformInfo/Generic/SystemUUID`
- **Security Settings**:
	- `Misc/Security/ApECID` = `0`
	- `Misc/Security/ScanPolicy` = `0`
	- `Misc/Security/SecureBootModel` = `Disabled` &rarr; :warning: Disables Apple Secure Boot hardware model to avoid issues during Installation. Re-enable it in Post-Install so System Updates work when using an SMBIOS of a Mac model with a T2 Security Chip.
	- `Misc/Security/Vault` = `Optional` 
- **Other Settings**:
	- Sets `Misc/Boot/LauncherOption` to `Disabled` &rarr; To avoid changing boot menu entries on the target system's Firmware/BIOS.
	- Removes custom entries from `Misc/BlessOverride`
	- Removes custom boot loader entries from `Misc/Entries`
	- Sets `Misc/Debug/Target` to `3` (Default)
	- `UEFI/APFS`: Changes `MinDate` and `MinVersion` to `-1` to maximize macOS compatibility

## Instructions
- Install [**Python**](https://www.python.org/) if you haven't already
- Click on "Code" > "Download ZIP" and upack it.
- Copy/move the **OC-Anonymizer-master** folder to your Desktop
- Start Terminal
- Enter:</br>
`cd desktop/OC-Anonymizer-master`
- Next, enter </br>`python3 oc_anonymizer.py PATH_TO_CONFIG.plist` (you can also drag and drop the config into the terminal)
- Hit `ENTER`

This will create a `censored_config.plist`in the oc_anonymizer folder without sensitive data and changed settings as described. 

## Issues

If you encounter any issue, please file a bugreport [here](https://github.com/dreamwhite/bugtracker/issues/new?assignees=dreamwhite&labels=bug&template=generic.md&title=)

## Credits and Resources

- [Acidanthera](https://github.com/acidanthera) for [OpenCorePkg](https://github.com/acidanthera)
- [1alessandro1](https://github.com/1alessandro1) for the initial idea
- [Dreamwhite](https://github.com/dreamwhite) for the original Python script
- [Guide](https://github.com/5T33Z0/OC-Little-Translated/tree/main/M_EFI_Upload_Chklst) for removing sensitive data manually
