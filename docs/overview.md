Overview
========



Instructions
------------

Instructions in IArm are simply python functions called with whatever
parameters are called with it (A closure to be more precise).
Each line of code is unpacked into labels, instructions, and parameters.
These are passed to functions that then decode what each is supposed to do,
and raises errors if there is a problem.
If everything went well, the closure is put into a list to be called later.
A program counter marks were we are currently in the list.



Registers and Memory
--------------------

Registers and memory are implemented as python dictionaries with a few extra
added features.
These features include the ability to randomly generate values if a value has
not been set (mimicking real hardware),
and the ability to link two entries (Like `LR` and `R14).
Registers are accessed by their string,
while memory is accessed by its byte address.



Lazy execution
--------------

One benefit to the interpreter is the lazy execution.
Code is set up but not executed until commanded.



Problems
--------

One of the major key differences between the ARMv6 implementation and the IArm
implementation is the fact that program memory and memory are separate.
IArm more closely follows a Harvard architecture, while ARM is a
Modified Harvard architecture.
This leads to one major downfall.
You cannot read an instruction value into a register with the `LDR` instruction
as you can with a normal ARM processor.

The PC points to the next instruction, much like in ARM THUMB.
This is unlike normal ARM, where PC points two instructions ahead.

Program memory is word addresses, not byte addressed.
This is because program memory is a list of functions,
not actual memory.
Therefor, the PC increments in sets of 1, not 4.

Since the code is not actually compiled,
we cannot produce a map file or listing file.
