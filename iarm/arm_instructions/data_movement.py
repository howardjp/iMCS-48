"""
This file contains all instructions related to moving data
on the CPU (register to register)
"""

import iarm.exceptions
from ._meta import _Meta


class DataMovement(_Meta):
    def MOV(self, params):
        Rx, Ry = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(any_register=(Rx, Ry))

        def MOV_func():
            self.register[Rx] = self.register[Ry]

        return MOV_func

    def MOVS(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        if self.is_immediate(Rb):
            self.check_arguments(low_registers=[Ra], imm8=[Rb])

            def MOVS_func():
                self.register[Ra] = int(Rb[1:])

                # Set N and Z status flags
                self.set_NZ_flags(Ra)

            return MOVS_func
        elif self.is_register(Rb):
            self.check_arguments(low_registers=(Ra, Rb))

            def MOVS_func():
                self.register[Ra] = self.register[Rb]

                self.set_NZ_flags(Ra)

            return MOVS_func
        else:
            raise iarm.exceptions.ParsingError("Unknown parameter: {}".format(Rb))

    def MRS(self, params):
        Rj, Rspecial = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(LR_or_general_purpose_registers=(Rj,), special_registers=(Rspecial,))

        def MRS_func():
            # TODO add combination registers IEPSR, IAPSR, and EAPSR
            # http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0553a/CHDBIBGJ.html
            if Rspecial == 'PSR':
                self.register[Rj] = self.register['APSR'] | self.register['IPSR'] | self.register['EPSR']
            else:
                self.register[Rj] = self.register[Rspecial]

        return MRS_func

    def MSR(self, params):
        Rspecial, Rj = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(LR_or_general_purpose_registers=(Rj,), special_registers=(Rspecial,))

        def MSR_func():
            # TODO add combination registers IEPSR, IAPSR, and EAPSR
            # http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0553a/CHDBIBGJ.html
            # TODO update N Z C V flags
            if Rspecial in ('PSR', 'APSR'):
                # PSR ignores writes to IPSR and EPSR
                self.register['APSR'] = self.register[Rj]
            else:
                # Do nothing
                pass

        return MSR_func

    def MVNS(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rb))

        def MVNS_func():
            self.register[Ra] = ~self.register[Rb]
            self.set_NZ_flags(Ra)

        return MVNS_func

    def REV(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rb))

        def REV_func():
            self.register[Ra] = int('{:032b}'.format(self.register[Rb])[::-1], 2)

        return REV_func

    def REV16(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(low_registers=(Ra, Rb))

        def REV16_func():
            # TODO is this correct?
            self.register[Ra] = int('{:016b}'.format(self.register[Rb] & 0xFFFF)[::-1], 2)

        return REV16_func

    def REVSH(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def REVSH_func():
            raise NotImplementedError

        return REVSH_func

    def SXTB(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def SXTB_func():
            raise NotImplementedError

        return SXTB_func

    def SXTH(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def SXTH_func():
            raise NotImplementedError

        return SXTH_func

    def UXTB(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTB_func():
            raise NotImplementedError

        return UXTB_func

    def UXTH(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func
