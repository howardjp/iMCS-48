from test_iarm import TestArm
import iarm.exceptions
import unittest


class TestArmMemory(TestArm):
    def test_ADR(self):
        self.interp.labels['TextMessage'] = 1

        self.interp.evaluate(" ADR R1, TextMessage")
        self.interp.run()

        self.assertEqual(self.interp.register['R1'], 1)

        self.interp.evaluate(" ADR R3, [PC, #996")
        self.interp.run()

        self.assertEqual(self.interp.register['R3'], 1000)

        with iarm.exceptions.IarmError:
            # Label does not exist
            self.interp.evaluate(" ADR R2, DoesNotExist")

        with iarm.exceptions.IarmError:
            # Register out of range
            self.interp.evaluate(" ADR R8, TextMessage")

        with iarm.exceptions.IarmError:
            # data value within 1020 bytes
            self.interp.evaluate(" ADR R0, [PC, #1024]")

        with iarm.exceptions.IarmError:
            # data value is word aligned
            self.interp.evaluate(" ADR R0, [PC, #3]")

    @unittest.skip('No Test Defined')
    def test_LDM(self):
        pass

    def test_LDR(self):
        self.interp.memory[8] = 0x12
        self.interp.memory[9] = 0x34
        self.interp.memory[10] = 0x56
        self.interp.memory[11] = 0x78
        self.interp.memory[12] = 0x99
        self.interp.register['SP'] = 12
        self.interp.register['R4'] = 4
        self.interp.register['R6'] = 3

        self.interp.evaluate(" LDR R0, [R4, #4]")
        self.interp.run()

        self.assertEqual(self.interp.register['R0'], 0x78563412)

        self.interp.evaluate(" LDR R1, [SP, #0]")
        self.interp.run()

        self.assertEqual(self.interp.register['R1'], 0x00000099)

        self.interp.equates['TEST'] = 0x543210
        self.interp.evaluate(" LDR R2, =TEST")
        self.interp.run()

        self.assertEqual(self.interp.register['R2'], 0x543210)

        self.interp.labels['TEST2'] = 0x1234
        self.interp.evaluate(" LDR R2, =TEST2")
        self.interp.run()

        self.interp.evaluate(" LDR R2, [SP]")
        self.interp.run()

        self.assertEqual(self.interp.register['R2'], 0x00000099)

        with self.assertRaises(iarm.exceptions.IarmError):
            # Register within 0-7
            self.interp.evaluate(" LDR R8, [R1]")

        with self.assertRaises(iarm.exceptions.IarmError):
            # data within 0-1020
            self.interp.evaluate(" LDR R7, [R4, #1024]")

        with self.assertRaises(iarm.exceptions.IarmError):
            # data word aligned
            self.interp.evaluate(" LDR R7, [R4, #6]")

        with self.assertRaises(iarm.exceptions.HardFault):
            # address is not word aligned
            self.interp.evaluate(" LDR R7, [R6, #4]")
            self.interp.run()

        with self.assertRaises(iarm.exceptions.IarmError):
            self.interp.labels['TEST'] = 0x1024
            self.interp.evaluate(" LDR R4, TEST")

    @unittest.skip('No Test Defined')
    def test_LDRB(self):
        pass

    @unittest.skip('No Test Defined')
    def test_LDRH(self):
        pass

    @unittest.skip('No Test Defined')
    def test_LDRSB(self):
        pass

    @unittest.skip('No Test Defined')
    def test_LDRSH(self):
        pass

    @unittest.skip('No Test Defined')
    def test_POP(self):
        pass

    @unittest.skip('No Test Defined')
    def test_PUSH(self):
        pass

    @unittest.skip('No Test Defined')
    def test_STM(self):
        pass

    @unittest.skip('No Test Defined')
    def test_STR(self):
        pass

    @unittest.skip('No Test Defined')
    def test_STRB(self):
        pass

    @unittest.skip('No Test Defined')
    def test_STRH(self):
        pass

if __name__ == '__main_':
    unittest.main()
