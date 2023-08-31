class PushRules:

    def __init__(self, commit_message_regex, branch_name_regex ):

        self.branch_name_regex = branch_name_regex
        self.commit_message_regex = commit_message_regex

    def castObject(self):

        pushRules = {

            "commit_message_regex": self.commit_message_regex,
            "branch_name_regex": self.branch_name_regex
        }

        return pushRules