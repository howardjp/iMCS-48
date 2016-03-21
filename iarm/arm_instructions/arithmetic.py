import iarm.exceptions


class Arithmetic(object):
    def ADCS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def ADCS_func():
            raise NotImplementedError

        return ADCS_func

    def ADD(self, params):
        Rx, Ry, Rz = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        # TODO implement ADD Rx, Rt, #imm10_4
        # TODO implement ADD Sp, SP, #imm9_4
        self.check_arguments(high_registers=(Rx, Ry, Rz))
        def ADD_func():
            self.register[Rx] = self.register[Ry] + self.register[Rz]
        return ADD_func

    def ADDS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def ADDS_func():
            raise NotImplementedError

        return ADDS_func

    def CMN(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def CMP(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def MULS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def NOP(self, params):
        def NOP_func():
            return
        return NOP_func

    def RSBS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

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
