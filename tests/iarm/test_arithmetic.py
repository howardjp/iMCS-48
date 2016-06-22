from .test_iarm import TestArm
import iarm.exceptions
import unittest


class TestArmArithmetic(TestArm):
    """
    Test all arithmetic instructions
    """

    def test_ADCS(self):
        self.interp.register['R0'] = 1
        self.interp.register['R2'] = 3

        self.interp.evaluate(" ADCS R0, R0, R2")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 4)
        # TODO check for status registers
        # TODO check for carry bit

        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" ADCS R0, R1, R2")

    def test_ADD(self):
        self.interp.register['R0'] = 1
        self.interp.register['R2'] = 3

        self.interp.evaluate(" ADD R0, R0, R2")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 4)

    def test_ADD_different_registers(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" ADD R0, R1, R2")

    def test_ADD_PC(self):
        self.interp.register['R0'] = 1
        self.interp.register['PC'] = 1

        self.interp.evaluate(" ADD R0, PC, #4")
        self.interp.evaluate(" ADD R0, PC, #4")  # Need a second instruction because PC == 1
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 5)

    def test_ADD_SP(self):
        self.interp.register['SP'] = 1

        self.interp.evaluate(" ADD SP, SP, #4")
        self.interp.run()

        self.assertEqual(self.interp.register['SP'], 5)

    def test_ADDS_different_register(self):
        self.interp.register['R0'] = 1
        self.interp.register['R1'] = 2
        self.interp.register['R2'] = 3

        self.interp.evaluate(" ADDS R0, R1, R2")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 5)
        # TODO test flags
        # TODO test overflow

    def test_ADDS_same_reg_imm(self):
        self.interp.register['R0'] = 1

        self.interp.evaluate(" ADDS R0, R0, #255")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 256)
        # TODO test flags
        # TODO test overflow

    def test_ADDS_diff_reg_imm(self):
        self.interp.register['R0'] = 1
        self.interp.register['R1'] = 2

        self.interp.evaluate(" ADDS R0, R1, #7")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 9)
        # TODO test flags
        # TODO test overflow

    def test_ADDS_same_reg_imm_error(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" ADDS R0, R0, #256")

    def test_ADDS_diff_reg_imm_error(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" ADDS R0, R1, #8")

    def test_CMN(self):
        self.interp.register['R0'] = 0
        self.interp.register['R1'] = 0

        self.interp.evaluate(" CMN R0, R1")
        self.interp.run()

        self.assertTrue(self.interp.register['APSR'] & (1 << 30))
        # TODO test other cases

    def test_CMP(self):
        self.interp.register['R0'] = 1
        self.interp.register['R1'] = 1

        self.interp.evaluate(" CMP R0, R1")
        self.interp.run()

        self.assertTrue(self.interp.is_Z_set())
        # TODO test other cases

    def test_MULS(self):
        self.interp.register['R0'] = 2
        self.interp.register['R1'] = 5

        self.interp.evaluate(" MULS R0, R1, R0")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 10)
        # TODO test flags

    def test_MULS_rule(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" MULS R0, R1, R2")

    @unittest.skip("No Test Defined")
    def test_RSBS(self):
        # TODO write some tests for this
        pass

    @unittest.skip('No Test Defined')
    def test_SBCS(self):
        # TODO write a test
        pass

    @unittest.skip('No Test Defined')
    def test_SUB(self):
        # TODO wrte a test
        pass

    @unittest.skip('No Test Defined')
    def test_SUBS(self):
        # TODO write a test
        pass

if __name__ == '__main_':
    unittest.main()
