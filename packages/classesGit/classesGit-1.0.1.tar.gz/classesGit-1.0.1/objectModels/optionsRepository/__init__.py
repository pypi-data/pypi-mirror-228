

class optionRepository:

    def __init__(self, cadence, enabled, keep_n, older_than, name_regex, name_regex_keep):
        self.cadence = cadence
        self.enabled = enabled
        self.keep_n = keep_n
        self.older_than = older_than
        self.name_regex = name_regex
        self.name_regex_keep = name_regex_keep

    def castObject(self):

        options = {
            'container_expiration_policy_attributes': {
                'cadence': self.cadence,
                'enabled': self.enabled,
                'keep_n': self.keep_n,
                'older_than': self.older_than,
                'name_regex': self.name_regex,
                'name_regex_keep': self.name_regex_keep
            }
        }

        return options
