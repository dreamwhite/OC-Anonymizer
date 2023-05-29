rules = [
    {
    "name": "BlessOverride",
    "description": "Add custom scanning paths through the bless model",
    "fields": [
            {
            "values": [
            {
                "name": "0",
                "description": "Do not use Apple Enclave Identifier",
                "value": 0,
                "default": "True"
            }
            ],
            "path": "Misc/Security/ApECID"
        },
        {
            "values": [
            {
                "name": "0",
                "description": "Use default OpenCore scanning rules (APFS, SATA, NVMe mainly)",
                "value": 0,
                "default": "True"
            }
            ],
            "path": "Misc/Security/ScanPolicy"
        },
        {
            "values": [
            {
                "name": "Disabled",
                "description": "No model, Secure Boot will be disabled",
                "value": "Disabled",
                "default": True
            },
            {
                "name": "Default",
                "description": "Matching model for current SMBIOS",
                "value": "Default"
            }
            ],
            "path": "Misc/Security/SecureBootModel"
        },
        {
            "values": [
            {
                "name": "Optional",
                "description": "No vault is enforced, insecure",
                "value": "Optional",
                "default": True
            },
            {
                "name": "Basic",
                "description": "Require vault.plist file present in OC directory. This provides basic filesystem integrity verification and may protect from unintentional filesystem corruption",
                "value": "Basic"
            },
            {
                "name": "Secure",
                "description": "Require vault.sig signature file for vault.plist in OC directory. This includes Basic integrity checking but also attempts to build a trusted bootchain.",
                "value": "Secure"
            }
            ],
            "path": "Misc/Security/Vault"
        }
    ],
    "is_enabled": True
},
]

config_plist = {
    'Misc': {
        'Security': {
            'ScanPolicy': 6942378921738971,
            'ApECID': 1782637812637812,
            'SecureBootModel': 'DIOPORCO',
            'Vault': 'dioporco'
        },
    }
}

class InvalidRuleException(Exception):
    """Exception raised for errors in the rule.

    Attributes:
        rule -- input rule which caused the error
        message -- explanation of the error
    """
    def __init__(self, rule: dict, message: str) -> None:
        self.rule = rule
        self.message = message
        super().__init__(self.message)

def check_rule_validity(rule: dict) -> bool:
    
    #Check if basic rule keys exists...
    if 'name' not in rule.keys():
        raise InvalidRuleException(rule, 'A property is missing: name')
    if 'description' not in rule.keys():
        raise InvalidRuleException(rule, 'A property is missing: description')
    if 'fields' not in rule.keys():
        raise InvalidRuleException(rule, 'A property is missing: fields')
    if 'is_enabled' not in rule.keys():
        raise InvalidRuleException(rule, 'A property is missing: is_enabled')
    
    rule_schema = {

        'name': {
            'type': str
        },
        'description': {
            'type': str
        },

        'fields': {
            'type': list
        },

        'is_enabled': {
            'type': bool
        }
    }

    for schema,_ in rule_schema.items():
        name = rule.get('name')
        name_schema_type = rule_schema.get('name')['type']
        description = rule.get('description')
        fields = rule.get('fields')
        is_enabled = rule.get('is_enabled')

        #Then proceeds checking the type of each field

        for field in [name, description, fields, is_enabled]:
            if type(field) != str:
                raise InvalidRuleException(rule, f'Type mismatch at "{schema}" field; Expected {name_schema_type} but got {type(field)}')


        if fields == list():
            raise InvalidRuleException(rule, 'The rule doesn\'t contain any field')
        

check_rule_validity(rules[0])