class Text:
        def __init__(self):
                pass
        
        text = """
        Overview
This Instruction Set Architecture (ISA) defines 3 instruction formats:

R-Type: Register to Register operations

I-Type: Register to Immediate operations

SB-Type: Branch and Store operations

All instructions have an associated Op (Opcode) value.
Some instructions also have a F (Function) field to further specify the operation.

Instruction Formats

Type	Fields
R-Type	F(Function), RS2, RS1, Rd, OP
I-Type	Immediate/Shift Amount, RS1, Rd, OP
SB-Type	Immediate Upper, RS2, RS1, Immediate Lower, OP
R-Type Instructions (OP = 0)

Instruction	Description	F	Format
SLL Rd	Shift Left Logical (RS1 << RS2[4:0])	0	2 S1 S2 Rd OP
SRL Rd	Shift Right Logical (RS1 >> RS2[4:0])	1	2 S1 S2 Rd OP
SRA Rd	Shift Right Arithmetic (signed RS1 >> RS2[4:0])	2	2 S1 S2 Rd OP
ROR Rd	Rotate Right (RS1 rotate right by RS2[4:0])	3	2 S1 S2 Rd OP
ADD Rd	RS1 + RS2	4	2 S1 S2 Rd OP
SUB Rd	RS1 - RS2	5	2 S1 S2 Rd OP
SLT Rd	Set if RS1 < RS2 (signed comparison)	6	2 S1 S2 Rd OP
SLTU Rd	Set if RS1 < RS2 (unsigned comparison)	7	2 S1 S2 Rd OP
SEQ Rd	Set if RS1 == RS2	8	2 S1 S2 Rd OP
XOR Rd	RS1 XOR RS2	9	2 S1 S2 Rd OP
OR Rd	RS1 OR RS2	10	2 S1 S2 Rd OP
AND Rd	RS1 AND RS2	11	2 S1 S2 Rd OP
NOR Rd	NOT (RS1 OR RS2)	12	2 S1 S2 Rd OP
MUL Rd	(RS1 * RS2) [31:0]	13	2 S1 S2 Rd OP
I-Type Instructions (Immediate or Shift Operations)

Instruction	Description	OP	Format
SLLI Rd	Shift Left Logical (RS1 << Sa)	1	0 Sa RS1 Rd OP
SRLI Rd	Shift Right Logical (RS1 >> Sa)	2	0 Sa RS1 Rd OP
SRAI Rd	Shift Right Arithmetic (signed RS1 >> Sa)	3	0 Sa RS1 Rd OP
RORI Rd	Rotate Right (RS1 rotated by Sa)	4	0 Sa RS1 Rd OP
ADDI Rd	RS1 + sign-extended Imm16	5	Imm16 RS1 Rd OP
SLTI Rd	Set if RS1 < Imm16 (signed)	6	Imm16 RS1 Rd OP
SLTIU Rd	Set if RS1 < Imm16 (unsigned)	7	Imm16 RS1 Rd OP
SEQI Rd	Set if RS1 == Imm16 (signed)	8	Imm16 RS1 Rd OP
XORI Rd	RS1 XOR zero-extended Imm16	9	Imm16 RS1 Rd OP
ORI Rd	RS1 OR zero-extended Imm16	10	Imm16 RS1 Rd OP
ANDI Rd	RS1 AND zero-extended Imm16	11	Imm16 RS1 Rd OP
NORI Rd	NOT (RS1 OR zero-extended Imm16)	12	Imm16 RS1 Rd OP
SET Rd	Set Rd to sign-extended Imm16	13	Imm16 0 Rd OP
SSET Rd	Concatenate Rd[31:16] with Imm16	14	Imm16 0 Rd OP
JALR Rd	PC = RS1 + sign-extended Imm16, Rd = PC+1	15	Imm16 RS1 Rd OP
LW Rd	Load Word from Mem[RS1 + sign-extended Imm16]	16	Imm16 RS1 Rd OP
SB-Type Instructions (Branch/Store)

Instruction	Description	OP	Format
SW	Store Word: Mem[RS1 + sign-extended (ImmU, ImmL)] = RS2	17	ImmU RS2 RS1 ImmL OP
BEQ	Branch if RS1 == RS2	18	ImmU RS2 RS1 ImmL OP
BNE	Branch if RS1 != RS2	19	ImmU RS2 RS1 ImmL OP
BLT	Branch if RS1 < RS2 (signed)	20	ImmU RS2 RS1 ImmL OP
BGE	Branch if RS1 >= RS2 (signed)	21	ImmU RS2 RS1 ImmL OP
BLTU	Branch if RS1 < RS2 (unsigned)	22	ImmU RS2 RS1 ImmL OP
BGEU	Branch if RS1 >= RS2 (unsigned)	23	ImmU RS2 RS1 ImmL OP
Notes
Shift Amount (Sa): Only lowest 5 bits used (Sa[4:0]).

Imm16: Immediate 16-bit value. Sign-extended or zero-extended based on instruction.

Memory Access: Address is computed as base (RS1) + sign-extended immediate.

Branches: PC-relative addressing using combined upper and lower immediates (ImmU + ImmL).

Summary Table of Opcodes

OP	Meaning	Instruction Types
0	R-Type	SLL, SRL, SRA, ROR, ADD, SUB, SLT, SLTU, SEQ, XOR, OR, AND, NOR, MUL
1–16	I-Type	Shifts, Arithmetics, Comparisons, Memory Load
17–23	SB-Type	Stores and Branches
        """

        settings_GUI = {
            'TFrame': {'configure': {'background': '#ffebee','borderwidth': 0,'relief': 'flat'}},
            'TLabel': {'configure': {'background': '#ffebee','foreground': '#880e4f','font': ('Segoe UI', 10)}},
            'TButton': {'configure': {'background': '#f8bbd0','foreground': '#880e4f','font': ('Segoe UI', 10, 'bold'),'borderwidth': 1,'relief': 'raised','padding': 8},
                'map': {'background': [('active', '#f48fb1')],'foreground': [('active', '#560027')]}},
            'TNotebook': {'configure': {'background': '#fce4ec','tabmargins': [5, 5, 0, 0]}},
            'TNotebook.Tab': {'configure': {'background': '#f8bbd0','foreground': '#880e4f','padding': [10, 5],'font': ('Segoe UI', 9, 'bold')},
                'map': {'background': [('selected', '#fce4ec')],'expand': [('selected', [1, 1, 1, 0])]}},
            'Treeview': {'configure': {'fieldbackground': '#fce4ec','background': 'white','foreground': '#880e4f','rowheight': 25,'font': ('Consolas', 9)}},
            'Treeview.Heading': {
                'configure': {
                    'background': '#f48fb1',
                    'foreground': 'white',
                    'font': ('Segoe UI', 9, 'bold')
                }
            },
            'Vertical.TScrollbar': {
                'configure': {
                    'background': '#f8bbd0',
                    'arrowcolor': '#880e4f',
                    'troughcolor': '#fce4ec'
                }
            }
        }

        tag_config = {
            'opcode': {'foreground': '#1565c0', 'font': ('Consolas', 10, 'bold')},
            'register': {'foreground': '#2e7d32', 'font': ('Consolas', 10, 'bold')},
            'immediate': {'foreground': '#6a1b9a'},
            'label': {'foreground': '#ef6c00', 'font': ('Consolas', 10, 'bold')},
            'comment': {'foreground': '#757575', 'font': ('Consolas', 10, 'italic')},
            'error': {'background': '#ffcdd2', 'underline': True},
            'current_line': {'background': '#f8bbd0'}
        }