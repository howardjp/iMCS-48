import iarm.exceptions
from ._meta import _Meta


class Memory(_Meta):
    def ADR(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDM(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDR(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDRB(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDRH(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDRSB(self, params):
        raise iarm.exceptions.NotImplementedError

    def LDRSH(self, params):
        raise iarm.exceptions.NotImplementedError

    def POP(self, params):
        raise iarm.exceptions.NotImplementedError

    def PUSH(self, params):
        raise iarm.exceptions.NotImplementedError

    def STM(self, params):
        raise iarm.exceptions.NotImplementedError

    def STR(self, params):
        raise iarm.exceptions.NotImplementedError

    def STRB(self, params):
        raise iarm.exceptions.NotImplementedError

    def STRH(self, params):
        raise iarm.exceptions.NotImplementedError

