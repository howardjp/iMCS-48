import iarm.exceptions
from ._meta import _Meta


class Shift(_Meta):
    def ASRS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rc):
            # ASRS Ra, Ra, Rb
            self.check_arguments(low_registers=(Ra, Rc))
            if Ra != Rb:
                raise iarm.exceptions.RuleError("First parameter {} does not match second parameter {}".format(Ra, Rb))

            def ASRS_func():
                # Set the C flag, or the last shifted out bit
                if (self.register[Rc] > 0) and (self.register[Rb] & (1 << (self.register[Rc] - 1))):
                    self.set_APSR_flag_to_value('C', 1)
                else:
                    self.set_APSR_flag_to_value('C', 0)

                if self.register[Ra] & (1 << (self._bit_width - 1)):
                    self.register[Ra] = (self.register[Ra] >> self.register[Rc]) | (
                        int('1' * self.register[Rc], 2) << (self._bit_width - self.register[Rc]))
                else:
                    self.register[Ra] = self.register[Ra] >> self.register[Rc]
                self.set_NZ_flags(self.register[Ra])
        else:
            # ASRS Ra, Rb, #imm5_counting
            self.check_arguments(low_registers=(Ra, Rb), imm5_counting=(Rc,))
            shift_amount = self.check_immediate(Rc)

            def ASRS_func():
                # Set the C flag, or the last shifted out bit
                if self.register[Rb] & (1 << (shift_amount - 1)):
                    self.set_APSR_flag_to_value('C', 1)
                else:
                    self.set_APSR_flag_to_value('C', 0)

                if self.register[Ra] & (1 << (self._bit_width - 1)):
                    self.register[Ra] = (self.register[Ra] >> shift_amount) | (
                        int('1' * shift_amount, 2) << (self._bit_width - shift_amount))
                else:
                    self.register[Ra] = self.register[Rb] >> shift_amount
                self.set_NZ_flags(self.register[Ra])

        return ASRS_func

    def LSLS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rc):
            # LSLS Ra, Ra, Rb
            self.check_arguments(low_registers=(Ra, Rc))
            if Ra != Rb:
                raise iarm.exceptions.RuleError("First parameter {} does not match second parameter {}".format(Ra, Rb))

            def LSLS_func():
                # Set the C flag, or the last shifted out bit
                if (self.register[Rc] < self._bit_width) and (self.register[Ra] & (1 << (self._bit_width - self.register[Rc]))):
                    self.set_APSR_flag_to_value('C', 1)
                else:
                    self.set_APSR_flag_to_value('C', 0)

                self.register[Ra] = self.register[Ra] << self.register[Rc]
                self.set_NZ_flags(self.register[Ra])
        else:
            # LSLS Ra, Rb, #imm5
            self.check_arguments(low_registers=(Ra, Rb), imm5=(Rc,))
            shift_amount = self.check_immediate(Rc)

            def LSLS_func():
                # Set the C flag, or the last shifted out bit
                if (shift_amount < self._bit_width) and (self.register[Rb] & (1 << (self._bit_width - shift_amount))):
                    self.set_APSR_flag_to_value('C', 1)
                else:
                    self.set_APSR_flag_to_value('C', 0)

                self.register[Ra] = self.register[Rb] << shift_amount
                self.set_NZ_flags(self.register[Ra])

        return LSLS_func

    def LSRS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rc):
            # LSRS Ra, Ra, Rb
            self.check_arguments(low_registers=(Ra, Rc))
            if Ra != Rb:
                raise iarm.exceptions.RuleError("First parameter {} does not match second parameter {}".format(Ra, Rb))

            def LSRS_func():
                # Set the C flag, or the last shifted out bit
                if (self.register[Rc] > 0) and (self.register[Rb] & (1 << (self.register[Rc] - 1))):
                    self.set_APSR_flag_to_value('C', 1)
                else:
                    self.set_APSR_flag_to_value('C', 0)

                self.register[Ra] = self.register[Ra] >> self.register[Rc]
                self.set_NZ_flags(self.register[Ra])
        else:
            # LSRS Ra, Rb, #imm5_counting
            self.check_arguments(low_registers=(Ra, Rb), imm5_counting=(Rc,))
            shift_amount = self.check_immediate(Rc)

            def LSRS_func():
                # Set the C flag, or the last shifted out bit
                if self.register[Rb] & (1 << (shift_amount - 1)):
                    self.set_APSR_flag_to_value('C', 1)
                else:
                    self.set_APSR_flag_to_value('C', 0)

                self.register[Ra] = self.register[Rb] >> shift_amount
                self.set_NZ_flags(self.register[Ra])

        return LSRS_func

    def RORS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        # TODO implement this function
        # TODO figure out the last shifted bit
        # TODO figure out how to wrap bits around
        raise iarm.exceptions.NotImplementedError

        # RORS Ra, Ra, Rb
        self.check_arguments(low_registers=(Ra, Rc))
        if Ra != Rb:
            raise iarm.exceptions.RuleError("First parameter {} does not match second parameter {}".format(Ra, Rb))

        def RORS_func():
            raise NotImplementedError

        return RORS_func
