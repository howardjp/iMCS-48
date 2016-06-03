import iarm.exceptions
from ._meta import _Meta


class Arithmetic(_Meta):
    def ADCS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rb, Rc))

        def ADCS_func():
            self.register[Ra] = self.register[Rb] + self.register[Rc]
            self.register[Ra] += 1 if (self.register['APSR'] & (1 << 29)) else 0
            self.set_NZCV_flags(self.register[Rb], self.register[Rc], self.register[Ra], 'add')

        return ADCS_func

    def ADD(self, params):
        Rx, Ry, Rz = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rz):
            # ADD Rx, Ry, Rz
            self.check_arguments(any_registers=(Rx, Ry, Rz))
            if Rx != Ry:
                raise iarm.exceptions.RuleError("Second parameter {} does not equal first parameter {}". format(Ry, Rx))

            def ADD_func():
                self.register[Rx] = self.register[Ry] + self.register[Rz]
        else:
            if Rx == 'SP':
                # ADD SP, SP, #imm9_4
                self.check_arguments(imm9_4=(Rz,))
                if Rx != Ry:
                    raise iarm.exceptions.RuleError("Second parameter {} is not SP".format(Ry))
            else:
                # ADD Rx, [SP, PC], #imm10_4
                self.check_arguments(any_registers=(Rx,), imm10_4=(Rz,))
                if Ry not in ('SP', 'PC'):
                    raise iarm.exceptions.RuleError("Second parameter {} is not SP or PC".format(Ry))

            def ADD_func():
                self.register[Rx] = self.register[Ry] + int(Rz[1:])

        return ADD_func

    def ADDS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rc):
            # ADDS Ra, Rb, Rc
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def ADDS_func():
                self.register[Ra] = self.register[Rb] + self.register[Rc]
                self.set_NZCV_flags(self.register[Rb], self.register[Rc], self.register[Ra], 'add')
        elif Ra == Rb:
            # ADDS Ra, Ra, #imm8
            self.check_arguments(low_registers=(Ra,), imm8=(Rc,))

            def ADDS_func():
                self.register[Ra] = self.register[Rb] + int(Rc[1:])
                self.set_NZCV_flags(self.register[Rb], self.register[Rc], self.register[Ra], 'add')
        else:
            # ADDS Ra, Rb, #imm3
            self.check_arguments(low_registers=(Ra, Rb), imm3=(Rc,))

            def ADDS_func():
                self.register[Ra] = self.register[Rb] + int(Rc[1:])
                self.set_NZCV_flags(self.register[Rb], self.register[Rc], self.register[Ra], 'add')

        return ADDS_func

    def CMN(self, params):
        Ra, Rb = self.get_two_parameters(self.TWO_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rb))

        def CMN_func():
            self.set_NZCV_flags(self.register[Ra], self.register[Rb],
                                self.register[Ra] + self.register[Rb], 'add')

        return CMN_func

    def CMP(self, params):
        Rm, Rn = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        if self.is_register(Rn):
            self.check_arguments(R0_thru_R14=(Rm, Rn))

            def CMP_func():
                self.set_NZCV_flags(self.register[Rm], self.register[Rn],
                                    self.register[Rm] - self.register[Rn], 'sub')
        else:
            self.check_arguments(R0_thru_R14=(Rm,), imm8=(Rn,))

            def CMP_func():
                self.set_NZCV_flags(self.register[Rm], int(Rn[1:]),
                                    self.register[Rm] - int(Rn[1:]), 'sub')

        return CMP_func

    def MULS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rb, Rc))
        if Ra != Rc:
            raise iarm.exceptions.RuleError("Third parameter {} is not the same as the first parameter {}".format(Rc, Ra))

        def MULS_func():
            self.register[Ra] = self.register[Rb] * self.register[Rc]
            self.set_NZ_flags(self.register[Ra])

        return MULS_func

    def NOP(self, params):
        # TODO check for no parameters
        def NOP_func():
            return
        return NOP_func

    def RSBS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rb))
        if Rc != '#0':
            raise iarm.exceptions.RuleError("Third parameter {} is not #0".format(Rc))

        def RSBS_func():
            self.register[Ra] = 0 - self.register[Rb]
            self.set_NZCV_flags(0, self.register[Rb], self.register[Ra], 'sub')

        return RSBS_func

    def SBCS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def SUB(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def SUBS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func
