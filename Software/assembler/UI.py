import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from parsers.line_parser import LineParser
from encoders.i_encoder import ITypeEncoder
from encoders.r_encoder import RTypeEncoder
from encoders.sp_encoder import SBTypeEncoder
import re
from contentGUI import Text
from PIL import Image, ImageTk

class PinkAssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pink Custom Assembler")
        self.root.geometry("1280x800")
        self.root.configure(bg='#ffebee')
        self.encoders = {'RType': RTypeEncoder(),'IType': ITypeEncoder(),'SBType': SBTypeEncoder()}
        self.current_file = None
        self.symbol_table = {}
        self.memory = {}
        self.register_state = {f'R{i}': 0 for i in range(32)}
        self.register_state['PC'] = 0
        self.register_state['RZ'] = 0
        
        #home page
        self.create_home_page()
        
    def create_home_page(self):
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        try:
            gif_path = "assembler/media/stnsans.gif" 
            self.bg_image = Image.open(gif_path)
        except Exception as e:
            self.home_frame.configure(bg='#ffebee')
        
        title_label = tk.Label(self.home_frame,text="RISC 32 BIT ASSEMBLER",font=('Segoe UI', 48, 'bold'),fg='#880e4f',bg='#fce4ec' if not hasattr(self, 'bg_label') else '',)
        title_label.pack(pady=(100, 50))
        button_frame = tk.Frame(self.home_frame, bg='' if hasattr(self, 'bg_label') else '#fce4ec')
        button_frame.pack(pady=50)
        button_style = {'font': ('Segoe UI', 24, 'bold'),'width': 15,'height': 2,'bg': '#f48fb1','fg': 'white','activebackground': '#ad1457','activeforeground': 'white','bd': 0,'highlightthickness': 0,'relief': 'flat'}
        self.assemble_home_btn = tk.Button(button_frame,text="ASSEMBLE",command=self.show_assembler,**button_style)
        self.assemble_home_btn.pack(side=tk.LEFT, padx=40, pady=20)
        self.journey_btn = tk.Button(button_frame,text="JOURNEY",command=self.show_journey,**button_style)
        self.journey_btn.pack(side=tk.LEFT, padx=40, pady=20)
        for btn in [self.assemble_home_btn, self.journey_btn]:
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#ad1457'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#f48fb1'))
    
    def create_journey_page(self):
        self.journey_frame = tk.Frame(self.root)
        self.journey_frame.pack(fill=tk.BOTH, expand=True)
        try:
            journey_gif_path = "media/journey_bg.gif" 
            self.journey_bg_image = Image.open(journey_gif_path)
            self.journey_bg_frames = []
            try:
                while True:
                    frame = ImageTk.PhotoImage(self.journey_bg_image.copy().resize((1280, 800)))
                    self.journey_bg_frames.append(frame)
                    self.journey_bg_image.seek(len(self.journey_bg_frames))
            except EOFError:
                pass
            
            self.journey_bg_label = tk.Label(self.journey_frame, image=self.journey_bg_frames[0])
            self.journey_bg_label.image = self.journey_bg_frames[0]
            self.journey_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.current_journey_frame = 0
            self.animate_journey_bg()
        except Exception as e:
            self.journey_frame.configure(bg='#ffebee')
        overlay = tk.Frame(self.journey_frame, bg='#fce4ec', bd=0)
        overlay.place(relx=0.5, rely=0.5, anchor='center', width=1000, height=600)
        content_frame = tk.Frame(overlay, bg='#fce4ec', bd=0)
        content_frame.place(relx=0.5, rely=0.5, anchor='center', width=980, height=580)
        journey_title = tk.Label(content_frame,text="ISA Documentation",font=('Segoe UI', 32, 'bold'),fg='#880e4f',bg='#fce4ec')
        journey_title.pack(pady=(20, 10))
        text_frame = tk.Frame(content_frame, bg='#fce4ec')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        journey_text = scrolledtext.ScrolledText(text_frame,wrap=tk.WORD,font=('Segoe UI', 12),bg='#fce4ec',padx=20,pady=20,bd=0,highlightthickness=0)
        journey_text.pack(fill=tk.BOTH, expand=True)
        journey_content = Text.text
        journey_text.insert(tk.END, journey_content)
        journey_text.config(state='disabled')
        back_btn = tk.Button(content_frame,text="← Back to Home",command=self.show_home_screen,font=('Segoe UI', 12, 'bold'),bg='#f48fb1',fg='white',activebackground='#ad1457',activeforeground='white',bd=0,highlightthickness=0,relief='flat',padx=15,pady=5)
        back_btn.pack(side=tk.BOTTOM, pady=20)
        back_btn.bind('<Enter>', lambda e: back_btn.config(bg='#ad1457'))
        back_btn.bind('<Leave>', lambda e: back_btn.config(bg='#f48fb1'))
    
    def animate_home_bg(self):
        if hasattr(self, 'bg_label'):
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.bg_label.config(image=self.bg_frames[self.current_frame])
            self.bg_label.image = self.bg_frames[self.current_frame]
            self.root.after(100, self.animate_home_bg)
    
    def animate_journey_bg(self):
        if hasattr(self, 'journey_bg_label'):
            self.current_journey_frame = (self.current_journey_frame + 1) % len(self.journey_bg_frames)
            self.journey_bg_label.config(image=self.journey_bg_frames[self.current_journey_frame])
            self.journey_bg_label.image = self.journey_bg_frames[self.current_journey_frame]
            self.root.after(100, self.animate_journey_bg)
    
    def show_assembler(self):
        if hasattr(self, 'home_frame'):
            self.home_frame.pack_forget()
        if hasattr(self, 'journey_frame'):
            self.journey_frame.pack_forget()
        if hasattr(self, 'bg_label'):
            self.bg_label.place_forget()
            self.root.after_cancel(self.animate_home_bg)
        if hasattr(self, 'journey_bg_label'):
            self.journey_bg_label.place_forget()
            self.root.after_cancel(self.animate_journey_bg)
        if not hasattr(self, 'style'):
            self.setup_styles()
            self.create_widgets()
            self.setup_menus()
    
    def show_journey(self):
        if hasattr(self, 'home_frame'):
            self.home_frame.pack_forget()
        if hasattr(self, 'bg_label'):
            self.bg_label.place_forget()
            self.root.after_cancel(self.animate_home_bg)
        if not hasattr(self, 'journey_frame'):
            self.create_journey_page()
        else:
            self.journey_frame.pack(fill=tk.BOTH, expand=True)
        self.journey_frame.lift()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_create('pink', parent='clam', settings=Text.settings_GUI)
        self.style.theme_use('pink')
        self.tag_config = Text.tag_config
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_panel = ttk.Frame(main_frame, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        back_frame = ttk.Frame(left_panel)
        back_frame.pack(fill=tk.X, pady=(0, 10))
        self.back_btn = tk.Button(back_frame,text="← Back to Home",command=self.show_home_screen,font=('Segoe UI', 10, 'bold'),bg='#f48fb1',fg='white',activebackground='#ad1457',activeforeground='white',bd=0,highlightthickness=0,relief='flat',padx=10,pady=5)
        self.back_btn.pack(side=tk.LEFT)
        self.back_btn.bind('<Enter>', lambda e: self.back_btn.config(bg='#ad1457'))
        self.back_btn.bind('<Leave>', lambda e: self.back_btn.config(bg='#f48fb1'))
        
        # Code editor 
        editor_container = ttk.Frame(left_panel)
        editor_container.pack(fill=tk.BOTH, expand=True)
        self.line_numbers = tk.Text(editor_container,width=4,padx=5,pady=5,takefocus=0,border=0,background='#fce4ec',foreground='#880e4f',state='disabled',font=('Consolas', 10))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        editor_frame = ttk.Frame(editor_container)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.editor_label = ttk.Label(editor_frame, text="Assembly Code:", font=('Segoe UI', 11, 'bold'))
        self.editor_label.pack(anchor=tk.W, pady=(0, 5))
        self.editor = scrolledtext.ScrolledText(editor_frame,wrap=tk.WORD,font=('Consolas', 11),undo=True,maxundo=-1,padx=5,pady=5,selectbackground='#f48fb1',selectforeground='white',inactiveselectbackground='#f8bbd0')
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.editor.bind('<KeyRelease>', self.on_editor_change)
        self.update_line_numbers()
        self.editor.bind('<Configure>', lambda e: self.update_line_numbers())
        self.editor.bind('<KeyRelease>', lambda e: self.update_line_numbers())
        self.output_label = ttk.Label(left_panel, text="Machine Code:", font=('Segoe UI', 11, 'bold'))
        self.output_label.pack(anchor=tk.W, pady=(10, 5))
        self.output_text = scrolledtext.ScrolledText(left_panel,wrap=tk.WORD,font=('Consolas', 10),state='disabled',height=10,padx=5,pady=5,background='white')
        self.output_text.pack(fill=tk.BOTH, expand=False)
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(left_panel,textvariable=self.status_var,relief=tk.SUNKEN,anchor=tk.W,font=('Segoe UI', 9),foreground='white',background='#ad1457',padding=5)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        self.create_right_panel(right_panel)
        for tag, config in self.tag_config.items():
            self.editor.tag_config(tag, **config)
    
    def create_right_panel(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        symbols_frame = ttk.Frame(notebook)
        self.symbols_tree = ttk.Treeview(symbols_frame,columns=('value'),show='headings',height=10)
        self.symbols_tree.heading('#0', text='Symbol')
        self.symbols_tree.heading('value', text='Address')
        scrollbar = ttk.Scrollbar(symbols_frame, orient="vertical", command=self.symbols_tree.yview)
        self.symbols_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.symbols_tree.pack(fill=tk.BOTH, expand=True)
        notebook.add(symbols_frame, text='Symbols')
        registers_frame = ttk.Frame(notebook)
        self.registers_tree = ttk.Treeview( registers_frame,columns=('value'),show='headings', height=15)
        self.registers_tree.heading('#0', text='Register')
        self.registers_tree.heading('value', text='Value')
        scrollbar = ttk.Scrollbar(registers_frame, orient="vertical", command=self.registers_tree.yview)
        self.registers_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.registers_tree.pack(fill=tk.BOTH, expand=True)
        for reg in sorted(self.register_state.keys()):
            self.registers_tree.insert('', 'end', text=reg, values=('0x00000000',))
        notebook.add(registers_frame, text='Registers')
        memory_frame = ttk.Frame(notebook)
        self.memory_tree = ttk.Treeview(memory_frame,columns=('value'),show='headings',height=15)
        self.memory_tree.heading('#0', text='Address')
        self.memory_tree.heading('value', text='Instruction/Data')
        scrollbar = ttk.Scrollbar(memory_frame, orient="vertical", command=self.memory_tree.yview)
        self.memory_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.memory_tree.pack(fill=tk.BOTH, expand=True)
        notebook.add(memory_frame, text='Memory')
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=10)
        button_style = {'font': ('Segoe UI', 10, 'bold'), 'background': '#f48fb1', 'foreground': 'white', 'activebackground': '#ad1457','borderwidth': 0, 'highlightthickness': 0, 'padx': 10, 'pady': 8}
        self.assemble_btn = tk.Button(btn_frame,text="Assemble",command=self.assemble,**button_style)
        self.assemble_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.step_btn = tk.Button(btn_frame,text="Step",command=self.step_execution,**button_style)
        self.step_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.reset_btn = tk.Button(btn_frame,text="Reset",command=self.reset_simulation,**button_style)
        self.reset_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        for btn in [self.assemble_btn, self.step_btn, self.reset_btn]:
            btn.bind('<Enter>', lambda e, b=btn: b.config(background='#ad1457'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(background='#f48fb1'))
    
    def setup_menus(self):
        menubar = tk.Menu(self.root, bg='#fce4ec', fg='#880e4f', activebackground='#f48fb1', activeforeground='white')
        file_menu = tk.Menu(menubar, tearoff=0, bg='#fce4ec', fg='#880e4f', activebackground='#f48fb1', activeforeground='white')
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.load_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Save Output", command=self.save_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(menubar, tearoff=0, bg='#fce4ec', fg='#880e4f', activebackground='#f48fb1', activeforeground='white')
        edit_menu.add_command(label="Undo", command=self.editor.edit_undo)
        edit_menu.add_command(label="Redo", command=self.editor.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.editor.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=self.clear)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        view_menu = tk.Menu(menubar, tearoff=0, bg='#fce4ec', fg='#880e4f', activebackground='#f48fb1', activeforeground='white')
        view_menu.add_checkbutton(label="Line Numbers", command=self.toggle_line_numbers)
        view_menu.add_command(label="Home Screen", command=self.show_home_screen)
        menubar.add_cascade(label="View", menu=view_menu)
        help_menu = tk.Menu(menubar, tearoff=0, bg='#fce4ec', fg='#880e4f', activebackground='#f48fb1', activeforeground='white')
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    def show_home_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        self.create_home_page()
    
    def update_line_numbers(self, event=None):
        lines = self.editor.get("1.0", "end-1c").split("\n")
        line_numbers_text = "\n".join(str(i) for i in range(1, len(lines) + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")
        self.editor.tag_remove("current_line", "1.0", "end")
        current_line = self.editor.index(tk.INSERT).split('.')[0]
        self.editor.tag_add("current_line", f"{current_line}.0", f"{current_line}.end")
    
    def on_editor_change(self, event=None):
        self.highlight_syntax()
        self.update_line_numbers()
    
    def highlight_syntax(self):
        for tag in self.tag_config.keys():
            if tag != 'current_line':  # Don't remove current line highlight
                self.editor.tag_remove(tag, "1.0", tk.END)
        text = self.editor.get("1.0", tk.END)
        lines = text.split('\n')
        for i, line in enumerate(lines, 1):
            start = f"{i}.0"
            end = f"{i}.end"
            clean_line = line.strip()
            if not clean_line:
                continue
            if '#' in line:
                comment_start = line.index('#')
                self.editor.tag_add('comment', f"{i}.{comment_start}", f"{i}.end")
            if ':' in clean_line:
                label_part = clean_line.split(':')[0].strip()
                label_start = line.index(label_part)
                label_end = label_start + len(label_part)
                self.editor.tag_add('label', f"{i}.{label_start}", f"{i}.{label_end}")
            parts = re.split(r'[,\s]+', clean_line)
            if parts and parts[0] in [*RTypeEncoder.FUNCTIONS.keys(), *ITypeEncoder.OPCODES.keys(), *SBTypeEncoder.OPCODES.keys()]:
                opcode_start = line.index(parts[0])
                opcode_end = opcode_start + len(parts[0])
                self.editor.tag_add('opcode', f"{i}.{opcode_start}", f"{i}.{opcode_end}")
                for part in parts[1:]:
                    if not part:
                        continue
                    try:
                        part_pos = line.index(part)
                        part_end = part_pos + len(part)
                        
                        if part.upper().startswith('R') and part[1:].isdigit():
                            self.editor.tag_add('register', f"{i}.{part_pos}", f"{i}.{part_end}")
                        elif part.replace('-', '').isdigit():
                            self.editor.tag_add('immediate', f"{i}.{part_pos}", f"{i}.{part_end}")
                    except ValueError:
                        pass
    
    def assemble(self):
        assembly_code = self.editor.get("1.0", tk.END)
        try:
            for tag in self.tag_config.keys():
                if tag != 'current_line':
                    self.editor.tag_remove(tag, "1.0", tk.END)
            self.symbol_table = {}
            current_pc = 0
            lines = assembly_code.split('\n')
            line_objects = []
            for line_num, line in enumerate(lines, 1):
                line_obj = LineParser.parse(line, line_num)
                line_objects.append(line_obj)
                if line_obj.label:
                    self.symbol_table[line_obj.label.name] = current_pc
                if line_obj.instruction:
                    current_pc += 1
            output_lines = []
            self.memory = {}
            current_pc = 0
            for line_obj in line_objects:
                if line_obj.instruction:
                    instruction = line_obj.instruction
                    opcode = instruction.opcode
                    try:
                        if opcode in RTypeEncoder.FUNCTIONS:
                            encoder = self.encoders['RType']
                        elif opcode in ITypeEncoder.OPCODES:
                            encoder = self.encoders['IType']
                        elif opcode in SBTypeEncoder.OPCODES:
                            encoder = self.encoders['SBType']
                        else:
                            raise ValueError(f"Unknown opcode: {opcode}")
                        machine_code = encoder.encode(instruction, self.symbol_table, current_pc)
                        hex_code = f"{machine_code:08X}"
                        self.memory[current_pc] = {'hex': hex_code,'instruction': instruction,'source': line_obj.content.strip()}
                        original_asm = line_obj.content.strip()
                        output_lines.append(f"0x{current_pc:08X}: {hex_code}    {original_asm}")
                        current_pc += 1
                    except Exception as e:
                        line_start = f"{line_obj.line_number}.0"
                        line_end = f"{line_obj.line_number}.end"
                        self.editor.tag_add('error', line_start, line_end)
                        raise e
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "\n".join(output_lines))
            self.output_text.config(state='disabled')
            self.update_symbol_table()
            self.update_memory_view()
            self.reset_simulation()
            self.status_var.set(f"✓ Assembly successful - {len(output_lines)} instructions")
            self.status_bar.configure(style='Success.TLabel')
        except Exception as e:
            self.status_var.set(f"✗ Assembly error: {str(e)}")
            self.status_bar.configure(style='Error.TLabel')
            messagebox.showerror("Assembly Error", f"Error during assembly:\n{str(e)}")
    
    def update_symbol_table(self):
        self.symbols_tree.delete(*self.symbols_tree.get_children())
        for symbol, addr in sorted(self.symbol_table.items()):
            self.symbols_tree.insert('', 'end', text=symbol, values=(f"0x{addr:08X}",))
    
    def update_memory_view(self):
        self.memory_tree.delete(*self.memory_tree.get_children())
        for addr in sorted(self.memory.keys()):
            data = self.memory[addr]
            self.memory_tree.insert('', 'end', text=f"0x{addr:08X}", values=(f"{data['hex']} ({data['source']})",))
    
    def update_register_view(self):
        for reg in self.register_state:
            for child in self.registers_tree.get_children():
                if self.registers_tree.item(child, 'text') == reg:
                    self.registers_tree.item(child, values=(f"0x{self.register_state[reg]:08X}",))
                    break
    
    def step_execution(self):
        if not self.memory:
            messagebox.showwarning("Execution", "No program loaded. Please assemble first.")
            return
        pc = self.register_state['PC']
        if pc not in self.memory:
            messagebox.showinfo("Execution", "Program execution completed.")
            return
        instruction = self.memory[pc]['instruction']
        try:
            self.simulate_instruction(instruction)
            self.update_register_view()
            self.register_state['PC'] += 4
            self.highlight_current_instruction()
            self.status_var.set(f"Executed: {instruction.opcode} at 0x{pc:08X}")
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error during execution:\n{str(e)}")
    
    def highlight_current_instruction(self):
        pc = self.register_state['PC']
        for child in self.memory_tree.get_children():
            addr_text = self.memory_tree.item(child, 'text')
            if addr_text == f"0x{pc:08X}":
                self.memory_tree.selection_set(child)
                self.memory_tree.focus(child)
                self.memory_tree.tag_configure('current', background='#f8bbd0')
                self.memory_tree.item(child, tags=('current',))
                break
    
    def reset_simulation(self):
        for reg in self.register_state:
            self.register_state[reg] = 0
        self.register_state['PC'] = min(self.memory.keys()) if self.memory else 0
        self.update_register_view()
        self.highlight_current_instruction()
        self.status_var.set("Simulation reset")
    
    def new_file(self):
        self.editor.delete(1.0, tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.current_file = None
        self.root.title("Pink Custom Assembler")
        self.status_var.set("New file created")
        self.update_line_numbers()
    
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(tk.END, content)
                    self.current_file = file_path
                    self.root.title(f"Pink Custom Assembler - {file_path}")
                    self.status_var.set(f"Loaded: {file_path}")
                    self.highlight_syntax()
                    self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load file:\n{str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w') as f:
                    f.write(self.editor.get(1.0, tk.END))
                self.status_var.set(f"Saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".asm",filetypes=[("Assembly Files", "*.asm"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.editor.get(1.0, tk.END))
                self.current_file = file_path
                self.root.title(f"Pink Custom Assembler - {file_path}")
                self.status_var.set(f"Saved as: {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
    
    def save_output(self):
        if not self.output_text.get("1.0", "end-1c"):
            messagebox.showwarning("Save Error", "No output to save")
            return
            
        file_path = filedialog.asksaveasfilename(defaultextension=".hex",filetypes=[("Hex Files", "*.hex"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.output_text.get("1.0", tk.END))
                self.status_var.set(f"Output saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
    
    def toggle_line_numbers(self):
        if self.line_numbers.winfo_ismapped():
            self.line_numbers.pack_forget()
        else:
            self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.update_line_numbers()
    
    def clear(self):
        self.editor.delete(1.0, tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.current_file = None
        self.root.title("Pink Custom Assembler")
        self.status_var.set("Cleared editor")
        self.update_line_numbers()
    
    def show_about(self):
        messagebox.showinfo(
            "About Risc-32bit Assembler",
            "Assembler\n\n"
            "A beautiful and functional assembler GUI\n"
            "The GUI Simulate the Processor ISA shown on journey bar.\n\n"
            "Version 1.0\n"
            "© 2025 RISC32 Assembler Project"
        )

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap('pink_assembler.ico')
    except:
        pass
    
    app = PinkAssemblerGUI(root)
    root.mainloop()