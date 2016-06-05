import iarm.exceptions
from ._meta import _Meta


class UnconditionalBranch(_Meta):
    def B(self, params):
        label = self.get_one_parameter(self.ONE_PARAMETER, params)

        self.check_arguments(label_exists=(label,))
        # TODO check if label is within +- 2 KB

        # B label
        def B_func():
            if label == '.':
                raise iarm.exceptions.EndOfProgram("You have reached an infinite loop")
            self.register['PC'] = self.labels[label]

        return B_func

    def BAL(self, params):
        return self.B(params)

    def BL(self, params):
        label = self.get_one_parameter(self.ONE_PARAMETER, params)

        self.check_arguments(label_exists=(label,))
        # TODO check if label is within +- 16 MB

        # BL label
        def BL_func():
            self.register['LR'] = self.register['PC'] - 2
            self.register['PC'] = self.labels[label]

        return BL_func

    def BLX(self, params):
        Rj = self.get_one_parameter(self.ONE_PARAMETER, params)

        self.check_arguments(LR_or_general_purpose_registers=(Rj,))

        def BLX_func():
            self.register['LR'] = self.register['PC'] - 2
            self.register['PC'] = self.register[Rj]

        return BLX_func

    def BX(self, params):
        Rj = self.get_one_parameter(self.ONE_PARAMETER, params)

        self.check_arguments(LR_or_general_purpose_registers=(Rj,))

        def BX_func():
            self.register['PC'] = self.register[Rj]

        return BX_func
