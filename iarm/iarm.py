#!/usr/bin/env python3

import iarm.cpu
import iarm.exceptions
import iarm.arm_instructions as instructions


class Arm(instructions.DataMovement, instructions.Arithmetic,
          instructions.Logic, instructions.Shift, instructions.Memory,
          instructions.ConditionalBranch, instructions.UnconditionalBranch,
          instructions.Misc):

    def evaluate(self, code):
        parsed = self.parse_lines(code)

        # Find all labels (don't need to have them point to anything yet
        temp_labels = {line[0]: None for line in parsed if line[0]}
        self.labels.update(temp_labels)  # These will exist eventually in this code block

        # Validate the code and get back a function to execute that instruction
        program = []
        labels = {}
        for line in parsed:
            if not any(line):
                continue  # We have a blank line
            label, op, params = line

            # Set the label to the next instruction
            if label:
                labels[label] = len(self.program) + len(program)

            # If the op lookup fails, it was a bad instruction
            try:
                func = self.ops[op]
            except KeyError:
                [self.labels.pop(i, None) for i in temp_labels]  # Clean up the added labels
                raise iarm.exceptions.ValidationError("Instruction {} does not exist".format(op))

            # Run the instruction, if it raised an error, roll back the labels
            try:
                instruction = func(params)
            except iarm.exceptions.IarmError:
                [self.labels.pop(i, None) for i in temp_labels]  # Clean up the added labels
                raise

            program.append(instruction)  # It validated, add it to the temp instruction list

        # Code block was successfully validated, update the main program
        self.program += program
        self.labels.update(labels)


if __name__ == '__main__':
    interp = Arm(32, 15, 1024, 8, False)
