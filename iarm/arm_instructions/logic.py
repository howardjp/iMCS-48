import iarm.exceptions
from ._meta import _Meta

class Logic(_Meta):
    def ANDS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def BICS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def EORS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def ORRS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def TST(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func