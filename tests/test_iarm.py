import unittest
import iarm.arm
import iarm.exceptions
import random


class TestArm(unittest.TestCase):
    """The base class for all arm tests"""
    def setUp(self):
        self.interp = iarm.arm.Arm(32, 16, 1024, 8, False)


class TestArmParsing(TestArm):
    """
    Test all parsing exceptions
    """
    def test_bad_parameter(self):
        with self.assertRaises(iarm.exceptions.ParsingError):
            self.interp.evaluate(' MOVS R1, 123')

    def test_no_parameters(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS')
        self.assertIn('None', str(cm.exception))

    def test_missing_first_parameter(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS ,')
        self.assertIn('first', str(cm.exception))

    def test_one_parameters(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS R1,')
        self.assertIn('second', str(cm.exception))

    def test_extra_argument(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS R1, #123, 456')
        self.assertIn('Extra', str(cm.exception))

    def test_missing_comma(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS R1 #123')
        self.assertIn('comma', str(cm.exception))

    def test_unknown_parameter(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS abc, 123')
        self.assertIn('Unknown', str(cm.exception))


class TestArmValidation(TestArm):
    """
    Test validation errors
    """
    def test_bad_instruction(self):
        with self.assertRaises(iarm.exceptions.ValidationError):
            self.interp.evaluate(' BADINST')


class TestArmRules(TestArm):
    """
    Test all validation rules
    """
    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_none(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(' MOVS')

    def test_parameter_not_register(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            self.interp.evaluate(' MOVS #1, #3')
        self.assertIn('not a register', str(cm.exception))

    def test_parameter_register_not_defined(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            self.interp.evaluate(' MOVS R{}, #3'.format(self.interp._max_registers+1))
        self.assertIn('greater', str(cm.exception))

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_not_an_immediate(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_not_an_immediate_unsigned(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_immediate_out_of_range(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_immediate_not_multiple_of(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_low_register(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass


class TestArmArithmetic(TestArm):
    """
    Test all arithmetic instructions
    """


class TestArmLinkedRegisters(TestArm):
    """
    Make sure that PC, LR, and SP are linked to R15, R14, and R13 respectively
    """
    def test_PC_register_link(self):
        REG1 = 'PC'
        REG2 = 'R15'
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG1] = 0
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG2] = 1
        self.assertEqual(self.interp.register[REG1], 1)
        self.interp.register[REG1] = random.randint(0, 2**self.interp._bit_width-1)
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])

    def test_LR_register_link(self):
        REG1 = 'LR'
        REG2 = 'R14'
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG1] = 0
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG2] = 1
        self.assertEqual(self.interp.register[REG1], 1)
        self.interp.register[REG1] = random.randint(0, 2 ** self.interp._bit_width - 1)
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])

    def test_SP_register_link(self):
        REG1 = 'SP'
        REG2 = 'R13'
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG1] = 0
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG2] = 1
        self.assertEqual(self.interp.register[REG1], 1)
        self.interp.register[REG1] = random.randint(0, 2 ** self.interp._bit_width - 1)
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])


class TestArmDataMovement(TestArm):
    def test_MOV(self):
        self.interp.register['R0'] = 5
        self.interp.register['R1'] = 0
        self.assertEqual(self.interp.register['R1'], 0)

        self.interp.evaluate(" MOV R1, R0")
        self.interp.run()

        self.assertEqual(self.interp.register['R1'], 5)

    def test_MOV_imm(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" MOV R1, #3")

    # TODO test high and special registers

    def test_MOVS_zero_register(self):
        self.interp.register['R0'] = 5
        self.interp.register['R1'] = 0
        self.assertEqual(self.interp.register['R0'], 5)

        self.interp.evaluate(" MOVS R0, R1")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 0)
        self.assertTrue(self.interp.register['APSR'] & (1 << 30))
        self.assertFalse(self.interp.register['APSR'] & (1 << 31))

    def test_MOVS_zero_imm(self):
        self.interp.register['R0'] = 5
        self.assertEqual(self.interp.register['R0'], 5)

        self.interp.evaluate(" MOVS R0, #0")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 0)
        self.assertTrue(self.interp.register['APSR'] & (1 << 30))
        self.assertFalse(self.interp.register['APSR'] & (1 << 31))

    def test_MOVS_negative_register(self):
        self.interp.register['R0'] = 0
        self.interp.register['R1'] = -1
        self.assertEqual(self.interp.register['R0'], 0)

        self.interp.evaluate(" MOVS R0, R1")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], -1)
        self.assertFalse(self.interp.register['APSR'] & (1 << 30))
        self.assertTrue(self.interp.register['APSR'] & (1 << 31))

    def test_MOVS_positive_register(self):
        self.interp.register['R1'] = 0
        self.interp.register['R1'] = 5
        self.assertEqual(self.interp.register['R0'], 0)

        self.interp.evaluate(" MOVS R0, R1")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 5)
        self.assertFalse(self.interp.register['APSR'] & (1 << 30))
        self.assertFalse(self.interp.register['APSR'] & (1 << 31))

    def test_MOVS_positive_imm(self):
        self.interp.register['R1'] = 0
        self.assertEqual(self.interp.register['R0'], 0)

        self.interp.evaluate(" MOVS R0, #5")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 5)
        self.assertFalse(self.interp.register['APSR'] & (1 << 30))
        self.assertFalse(self.interp.register['APSR'] & (1 << 31))

    def test_MOVS_high_register(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" MOVS R9, R1")

    def test_MRS_low_register(self):
        self.interp.evaluate(" MOVS R0, #0")  # Set the Z flag
        self.interp.evaluate(" MRS R1, APSR")
        self.interp.run()

        self.assertEqual(self.interp.register['APSR'], (1 << 30))
        self.assertEqual(self.interp.register['R1'], (1 << 30))

    def test_MRS_LR_register(self):
        self.interp.evaluate(" MOVS R0, #0")  # Set the Z flag
        self.interp.evaluate(" MRS LR, APSR")
        self.interp.run()

        self.assertEqual(self.interp.register['APSR'], (1 << 30))
        self.assertEqual(self.interp.register['LR'], (1 << 30))

    def test_MRS_PSR(self):
        self.interp.evaluate(" MOVS R0, #0")  # Set the Z flag
        self.interp.evaluate(" MRS R14, PSR")  # R14 is also LR
        self.interp.run()

        self.assertEqual(self.interp.register['APSR'], (1 << 30))
        self.assertEqual(self.interp.register['R14'], (1 << 30))

    def test_MSR_register(self):
        self.interp.register['R0'] = (15 << 28)
        self.interp.evaluate(" MSR APSR, R0")
        self.interp.run()

        self.assertEqual(self.interp.register['APSR'], (15 << 28))

    def test_MVNS(self):
        self.interp.register['R0'] = -5
        self.interp.evaluate(" MVNS R1, R0")
        self.interp.evaluate(" MVNS R2, R1")
        self.interp.run()

        self.assertEqual(self.interp.register['R1'], 4)
        self.assertEqual(self.interp.register['R2'], -5)

    def test_MVNS_high_register(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" MVNS R9, R0")

    def test_REV(self):
        self.interp.register['R7'] = 0xABC
        self.interp.register['R5'] = 0xF
        self.interp.evaluate(" REV R6, R7")
        self.interp.evaluate(" REV R4, R5")
        self.interp.run()

        self.assertEqual(self.interp.register['R6'], 0x3D500000)
        self.assertEqual(self.interp.register['R4'], 0xF0000000)

    def test_REV_high_register(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" REV R4, R10")

    def test_REV16(self):
        self.interp.register['R7'] = 0xABC
        self.interp.register['R5'] = 0xF
        self.interp.evaluate(" REV16 R6, R7")
        self.interp.evaluate(" REV16 R4, R5")
        self.interp.run()

        self.assertEqual(self.interp.register['R6'], 0x3D50)
        self.assertEqual(self.interp.register['R4'], 0xF000)

    def test_REV16_high_register(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(" REV R2, R11")

if __name__ == '__main_':
    unittest.main()
