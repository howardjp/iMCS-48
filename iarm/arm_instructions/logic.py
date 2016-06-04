import iarm.exceptions
from ._meta import _Meta


class Logic(_Meta):
    def ANDS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rc))
        if Ra != Rb:
            raise iarm.exceptions.RuleError("First parametere {} does not match second parameter {}".format(Ra, Rb))

        # ANDS Ra, Ra, Rb
        def ANDS_func():
            self.register[Ra] = self.register[Ra] & self.register[Rc]
            self.set_NZ_flags(self.register[Ra])

        return ANDS_func

    def BICS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rc))
        if Ra != Rb:
            raise iarm.exceptions.RuleError("First parametere {} does not match second parameter {}".format(Ra, Rb))

        # BICS Ra, Ra, Rb
        def BICS_func():
            self.register[Ra] = self.register[Ra] & (~self.register[Rc])
            self.set_NZ_flags(self.register[Ra])

        return BICS_func

    def EORS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rc))
        if Ra != Rb:
            raise iarm.exceptions.RuleError("First parametere {} does not match second parameter {}".format(Ra, Rb))

        # EORS Ra, Ra, Rb
        def EORS_func():
            self.register[Ra] = self.register[Ra] ^ self.register[Rc]
            self.set_NZ_flags(self.register[Ra])

        return EORS_func

    def ORRS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rc))
        if Ra != Rb:
            raise iarm.exceptions.RuleError("First parametere {} does not match second parameter {}".format(Ra, Rb))

        # ORRS Ra, Ra, Rb
        def ORRS_func():
            self.register[Ra] = self.register[Ra] | self.register[Rc]
            self.set_NZ_flags(self.register[Ra])

        return ORRS_func

    def TST(self, params):
        Ra, Rb = self.get_two_parameters(self.TWO_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rb))

        def TST_func():
            result = self.register[Ra] & self.register[Rb]
            self.set_NZ_flags(result)

        return TST_func
