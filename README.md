![macOS](https://img.shields.io/badge/Supported_OC_build:-≥0.8.2-white.svg)

# OC Anonymizer – remove sensitive Data from your config.plist

## About
Python Script for removing sensitive Data from OpenCore's `config.plist` and reset some settings to default before sharing your Config/EFI folder online. Basically it removes all those settings specific to your system and user preferences which may not be desireble to have on a different machine, such as: ScanPolicy, Custom Entries, LauncherOptions, etc. See details below.

## Features

Changes the following Settings/Parameters in the **config.plist**:

- **SMBIOS** data:
	- Deletes `PlatformInfo/Generic/MLB`
	- Deletes `PlatformInfo/Generic/ROM`
	- Deletes `PlatformInfo/Generic/SystemSerialNumber`
	- Deletes `PlatformInfo/Generic/SystemUUID`
- **Security Settings**:
	- `Misc/Security/ApECID` = `0`
	- `Misc/Security/ScanPolicy` = `0`
	- `Misc/Security/SecureBootModel` = `Disabled` &rarr; Disables Apple Secure Boot hardware model to avoid issues during Installation. Re-enable in Post-Install so System Updates work when using an SMBIOS of a Mac model with a T2 Security Chip.
	- `Misc/Security/Vault` = `Optional` 
- **Other Settings**:
	- Sets `Misc/Boot/LauncherOption` to `Disabled` &rarr; To avoid changing Boot Menu entries on the target system
	- Deletes custom entries from `Misc/BlessOverride`
	- Deletes custom boot loader entries from `Misc/Entries`
	- Sets `Misc/Debug/Target` to `3` (Default)

## Instructions
- Install [**Python**](https://www.python.org/) if you haven't already
- Download [**OC Anonymizer**](https://github.com/5T33Z0/OC-Anonymizer/archive/refs/heads/master.zip) and unpack it
- Copy/move the **OC-Anonymizer-master** folder to your Desktop
- Start Terminal
- Enter:</br>
`cd desktop/OC-Anonymizer-master`
- Next, enter </br>`python3 oc_anonymizer.py PATH_TO_CONFIG.plist` (you can also drag and drop the config into the terminal)
- Hit `ENTER`

This will create a `censored_config.plist`in the oc_anonymizer folder without sensitive data and changed settings as described. 

## Credits and Resources

- [Acidanthera](https://github.com/acidanthera) for [OpenCorePkg](https://github.com/acidanthera)
- [1alessandro1](https://github.com/1alessandro1) for the initial idea
- [Dreamwhite](https://github.com/dreamwhite) for the original Python script
- [Guide](https://github.com/5T33Z0/OC-Little-Translated/tree/main/M_EFI_Upload_Chklst) for removing sensitive data manually
