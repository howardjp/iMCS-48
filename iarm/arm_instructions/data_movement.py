"""
This file contains all instructions related to moving data
on the CPU (register to register)
"""

import iarm.exceptions
from ._meta import _Meta


class DataMovement(_Meta):
    def MOV(self, params):
        Rx, Ry = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        self.check_arguments(high_registers=(Rx, Ry))
        def MOV_func():
            self.register[Rx] = self.register[Ry]

        return MOV_func

    def MOVS(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        if self.is_immediate(Rb):
            self.check_arguments(low_registers=[Ra], imm8=[Rb])
            def MOVS_func():
                # TODO update APSR
                self.register[Ra] = int(Rb[1:])
            return MOVS_func
        elif self.is_register(Rb):
            self.check_arguments(low_registers=(Ra, Rb))
            def MOVS_func():
                # TODO update APSR
                self.register[Ra] = self.register[Rb]
            return MOVS_func
        else:
            raise iarm.exceptions.ParsingError("Unknown parameter: {}".format(Rb))

    def MRS(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def MRS_func():
            raise NotImplementedError

        return MRS_func

    def MSR(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def MSR_func():
            raise NotImplementedError

        return MSR_func

    def MVNS(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def MVNS_func():
            raise NotImplementedError

        return MVNS_func

    def REV(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def REV_func():
            raise NotImplementedError

        return REV_func

    def REV12(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def REV12_func():
            raise NotImplementedError

        return REV12_func

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
