# OC Anyonymizer – remove sensitive Data from your config.plist

The following script was created to censor sensitive fields in OpenCore's config.plist

The reason why I created it is that many EFI I find online contain sensitive fields such as SMBIOS data.
With this script you won't have any prob at all

# Usage

```bash
$> python3 oc_anonymizer.py PATH_TO_CONFIG.plist
```

It'll create `censored_config.plist` with the stripped sensitive data

# Credits

- [acidanthera](https://github.com/acidanthera) for [OpenCorePkg](https://github.com/acidanthera)
- [1alessandro1](https://github.com/1alessandro1) for the initial idea
- my self for trying to escape from my daemons while coding. appreciate that
