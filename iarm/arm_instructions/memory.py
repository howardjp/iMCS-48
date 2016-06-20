import iarm.exceptions
from ._meta import _Meta


class Memory(_Meta):
    THREE_PARAMETER_WITH_BRACKETS = r'\s*([^\s,]*),\s*\[([^\s,]*),\s*([^\s,]*)\](,\s*[^\s,]*)*\s*'

    def ADR(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDM(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDR(self, params):
        # TODO definition for PC is Ra <- M[PC + Imm10_4], Imm10_4 = PC - label, need to figure this one out
        # TODO implement LDR Ra, [PC, #Imm10_4]
        # TODO implement LDR Ra, label
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_WITH_BRACKETS, params)

        if self.is_immediate(Rc):
            if Rb == 'SP' or Rb == 'R15':
                self.check_arguments(low_registers=(Ra,), imm10_4=(Rc,))
            else:
                self.check_arguments(low_registers=(Ra, Rb), imm7_4=(Rc,))

            def LDR_func():
                # TODO does memory read up?
                self.register[Ra] = 0
                for i in range(4):
                    self.register[Ra] |= (self.memory[self.register[Rb] + int(Rc[1:]) + i] << (8 * i))
        else:
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def LDR_func():
                # TODO does memory read up?
                self.register[Ra] = 0
                for i in range(4):
                    self.register[Ra] |= (self.memory[self.register[Rb] + self.register[Rc] + i] << (8 * i))

        return LDR_func

    def LDRB(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_WITH_BRACKETS, params)

        if self.is_immediate(Rc):
            self.check_arguments(low_registers=(Ra, Rb), imm5=(Rc,))

            def LDRB_func():
                self.register[Ra] = self.memory[self.register[Rb] + int(Rc[1:])]
        else:
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def LDRB_func():
                self.register[Ra] = self.memory[self.register[Rb] + self.register[Rc]]

        return LDRB_func

    def LDRH(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_WITH_BRACKETS, params)

        if self.is_immediate(Rc):
            self.check_arguments(low_registers=(Ra, Rb), imm6_2=(Rc,))

            def LDRH_func():
                # TODO does memory read up?
                self.register[Ra] = 0
                for i in range(2):
                    self.register[Ra] |= (self.memory[self.register[Rb] + int(Rc[1:]) + i] << (8 * i))
        else:
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def LDRH_func():
                # TODO does memory read up?
                self.register[Ra] = 0
                for i in range(2):
                    self.register[Ra] |= (self.memory[self.register[Rb] + self.register[Rc] + i] << (8 * i))

        return LDRH_func

    def LDRSB(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDRSH(self, params):
        raise iarm.exceptions.NotImplementedError

    def POP(self, params):
        # TODO verify pop order
        # TODO pop list is comma separate, right?
        RPopList = self.get_one_parameter(r'\s*{(.*)}', params).split(',')
        RPopList.reverse()
        RPopList = [i.strip() for i in RPopList]

        def POP_func():
            for register in RPopList:
                # Get 4 bytes
                value = 0
                for i in range(4):
                    # TODO use memory width instead of constants
                    value |= self.memory[self.register['SP'] + i] << (8 * i)

                self.register[register] = value
                self.register['SP'] += 4

        return POP_func

    def PUSH(self, params):
        RPushList = self.get_one_parameter(r'\s*{(.*)}(.*)*', params).split(',')
        RPushList = [i.strip() for i in RPushList]

        def PUSH_func():
            for register in RPushList:
                self.register['SP'] -= 4

                for i in range(4):
                    # TODO is this the same as with POP?
                    self.memory[self.register['SP'] + i] = ((self.register[register] >> (8 * i)) & 0xFF)

        return PUSH_func

    def STM(self, params):
        raise iarm.exceptions.NotImplementedError

    def STR(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_WITH_BRACKETS, params)

        if self.is_immediate(Rc):
            if Rb == 'SP':
                self.check_arguments(low_registers=(Ra,), imm10_4=(Rc,))
            else:
                self.check_arguments(low_registers=(Ra, Rb), imm7_4=(Rc,))

            def STR_func():
                for i in range(4):
                    self.memory[self.register[Rb] + int(Rc[1:]) + i] = ((self.register[Ra] >> (8 * i)) & 0xFF)
        else:
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def STR_func():
                for i in range(4):
                    self.memory[self.register[Rb] + self.register[Rc] + i] = ((self.register[Ra] >> (8 * i)) & 0xFF)

        return STR_func

    def STRB(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_WITH_BRACKETS, params)

        if self.is_immediate(Rc):
            self.check_arguments(low_registers=(Ra, Rb), imm5=(Rc,))

            def STRB_func():
                self.memory[self.register[Rb] + int(Rc[1:])] = (self.register[Ra] & 0xFF)
        else:
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def STRB_func():
                self.memory[self.register[Rb] + self.register[Rc]] = (self.register[Ra] & 0xFF)

        return STRB_func

    def STRH(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_WITH_BRACKETS, params)

        if self.is_immediate(Rc):
            self.check_arguments(low_registers=(Ra, Rb), imm5=(Rc,))

            def STRH_func():
                for i in range(2):
                    self.memory[self.register[Rb] + int(Rc[1:]) + i] = ((self.register[Ra] >> (8 * i)) & 0xFF)
        else:
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def STRH_func():
                for i in range(2):
                    self.memory[self.register[Rb] + self.register[Rc] + i] = ((self.register[Ra] >> (8 * i)) & 0xFF)

        return STRH_func
