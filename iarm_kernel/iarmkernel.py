from ipykernel.kernelbase import Kernel
from iarm.arm import Arm
import re
import warnings
import iarm.exceptions


class ArmKernel(Kernel):
    implementation = 'IArm'
    implementation_version = '0.1'
    language = 'ARM'
    language_version = '0.1'
    language_info = {
        'name': 'ARM Coretex M0+ Thumb Assembly',
        'mimetype': 'text/x-asm',
        'file_extension': '.s'
    }
    banner = "Interpreted ARM"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interpreter = Arm(1024)  # 1K memory
        self.magics = {
            'run': self.magic_run,
            'register': self.magic_register,
            'reg': self.magic_register,
            'memory': self.magic_memory,
            'mem': self.magic_memory,
            'signed': self.magic_signed_rep
                       }

        self.signed_representation = False

    def convert_to_signed_int(self, i):
        if i & (1 << self.interpreter._bit_width - 1):
            return -((~i + 1) & (2**self.interpreter._bit_width - 1))

    def magic_signed_rep(self, line):
        line = line.strip().lower()
        if line == '1' or line == 'true' or not line:
            self.signed_representation = True
        else:
            self.signed_representation = False

    def magic_register(self, line):
        message = ""
        for reg in [i.strip() for i in line.replace(',', '').split()]:
            if '-' in reg:
                # We have a range (Rn-Rk)
                r1, r2 = reg.split('-')
                # TODO do we want to allow just numbers?
                n1 = re.search(self.interpreter.REGISTER_REGEX, r1).groups()[0]
                n2 = re.search(self.interpreter.REGISTER_REGEX, r2).groups()[0]
                n1 = self.interpreter.convert_to_integer(n1)
                n2 = self.interpreter.convert_to_integer(n2)
                for i in range(n1, n2+1):
                    val = self.interpreter.register[r1[0] + str(i)]
                    if self.signed_representation:
                        val = self.convert_to_signed_int(val)
                    message += "{}: {}\n".format(r1[0] + str(i), val)
            else:
                val = self.interpreter.register[reg]
                if self.signed_representation:
                    val = self.convert_to_signed_int(val)
                message += "{}: {}\n".format(reg, val)
        stream_content = {'name': 'stdout', 'text': message}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def magic_memory(self, line):
        message = ""
        for address in [i.strip() for i in line.replace(',', '').split()]:
            if '-' in address:
                # We have a range (n-k)
                m1, m2 = address.split('-')
                n1 = re.search(self.interpreter.IMMEDIATE_NUMBER, m1).groups()[0]
                n2 = re.search(self.interpreter.IMMEDIATE_NUMBER, m2).groups()[0]
                n1 = self.interpreter.convert_to_integer(n1)
                n2 = self.interpreter.convert_to_integer(n2)
                for i in range(n1, n2 + 1):
                    message += "{}: {}\n".format(str(i), self.interpreter.memory[i])
            else:
                # TODO fix what is the key for memory (currently it's an int, but registers are strings, should it be the same?)
                message += "{}: {}\n".format(address, self.interpreter.memory[self.interpreter.convert_to_integer(address)])
        stream_content = {'name': 'stdout', 'text': message}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def magic_run(self, line):
        i = float('inf')
        if line.strip():
            i = int(line)

        try:
            with warnings.catch_warnings(record=True) as w:
                self.interpreter.run(i)
                for warning_message in w:
                    # TODO should this be stdout or stderr
                    stream_content = {'name': 'stdout', 'text': 'Warning: ' + str(warning_message.message) + '\n'}
                    self.send_response(self.iopub_socket, 'stream', stream_content)
        except iarm.exceptions.EndOfProgram as e:
            f_name = self.interpreter.program[self.interpreter.register['PC'] - 1].__name__
            f_name = f_name[:f_name.find('_')]
            message = "Error in {}: ".format(f_name)
            stream_content = {'name': 'stdout', 'text': message + str(e) + '\n'}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        except Exception as e:
            for err in e.args:
                stream_content = {'name': 'stderr', 'text': str(err)}
                self.send_response(self.iopub_socket, 'stream', stream_content)
            return {'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': type(e).__name__,
                    'evalue': str(e),
                    'traceback': '???'}

    # TODO add support for outputing hex values, signed values, anc access to the generate random and postpone execution vars

    def run_magic(self, line):
        # TODO allow magics at end of code block
        # TODO allow more than one magic per block
        if line.startswith('%'):
            loc = line.find(' ')
            params = ""
            if loc > 0:
                params = line[loc + 1:]
                op = line[1:loc]
            else:
                op = line[1:]
            return self.magics[op](params)

    def run_code(self, code):
        if not code:
            return
        try:
            with warnings.catch_warnings(record=True) as w:
                self.interpreter.evaluate(code)
                for warning_message in w:
                    # TODO should this be stdout or stderr
                    stream_content = {'name': 'stdout', 'text': 'Warning: ' + str(warning_message.message) + '\n'}
                    self.send_response(self.iopub_socket, 'stream', stream_content)
        except Exception as e:
            for err in e.args:
                stream_content = {'name': 'stderr', 'text': str(err)}
                self.send_response(self.iopub_socket, 'stream', stream_content)
            return {'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': type(e).__name__,
                    'evalue': str(e),
                    'traceback': '???'}

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        instructions = ""
        for line in code.split('\n'):
            if line.startswith('%'):
                # TODO run current code, run magic, then continue
                ret = self.run_code(instructions)
                if ret:
                    return ret
                instructions = ""
                ret = self.run_magic(line)
                if ret:
                    return ret
            else:
                instructions += line + '\n'
        ret = self.run_code(instructions)
        if ret:
            return ret

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ArmKernel)
