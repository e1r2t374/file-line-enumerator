import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText

# Arc-Darker theme colors because why not :)
bg_color = '#353945'
fg_color = '#d3dae3'
btn_color = '#3daee9'
menu_color = '#404552'
executed = False
lines = []
output = []

def open_file(lines, title_label, subtext_label, output_label, command_entry):
    lines.clear()
    # File dialog
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    # Open the file and read the lines
    with open(file_path, "r") as file:
        lines.extend(file.readlines())
    
    # Remove the title and subtext labels (After file opened)
    title_label.pack_forget()
    subtext_label.pack_forget()
    
    # Add command entry box
    command_entry.pack()
    
    # Add Execution screen(After file opened)
    execute_button = tk.Button(root, text="Execute", command=lambda: threading.Thread(target=execute, args=(lines, output, output_label, command_entry.get(), execute_button)).start(), bg=btn_color, fg=fg_color)
    execute_button.pack()

   # Add Clear Output button
    clear_button = tk.Button(root, text=" Clear ", command=lambda: [output_label.delete('1.0', tk.END), output.clear()], bg=btn_color, fg=fg_color)
    clear_button.pack()

def copy(output, root):
    root.clipboard_clear()
    root.clipboard_append(output_label.get('1.0', tk.END))
            
def execute(lines, output, output_label, command, execute_button):
    global executed
    output.clear()
    # Show loading screen
    loading_label = tk.Label(root, text="Loading...", bg=bg_color, fg=btn_color)
    loading_label.pack()
    
    # Enumerate the lines of text
    for i, line in enumerate(lines):
        cmd = f"{command or 'echo'} {line.strip()}"
        try:
            output.append(subprocess.check_output(cmd, shell=True, text=True))
        except Exception as e:
            output.append(str(e))
        
    # Update the output_label text
    output_label.insert(tk.END, '\n'.join(map(str,output))+'\n')
    
    # Remove loading screen
    loading_label.pack_forget()
    
    # Add menu options after first execution
    if not executed:
        edit = Menu(bar, tearoff = 0, bg=menu_color, fg=fg_color) 
        bar.add_cascade(label ='Edit', menu = edit)
        edit.add_command(label ='Copy to Clipboard', command=lambda: copy(output, root))
        edit.add_command(label ='Save as..', command=lambda: save_as(output_label))
        executed = True

def save_as(output_label):
    # Save dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    
    # Save the output to the file
    with open(file_path, "w") as file:
        file.write(output_label.get('1.0', tk.END))

root = tk.Tk()
root.title("File Line Enumerator")
root.configure(bg=bg_color)

# Add a FLE label
title_label = tk.Label(root, text="File Line Enumerator [FLE v1.0]", bg=bg_color, fg=fg_color, font=("Helvetica", 16))
title_label.pack()
subtext_label = tk.Label(root, text="Try opening a file to enumerate.\nFile>Open..", bg=bg_color, fg=fg_color, font=("Helvetica", 12))
subtext_label.pack()

# Create an output_label buffer
output_label = ScrolledText(root, bg=bg_color, fg=fg_color)
output_label.pack()

# Create a command entry box
command_entry = tk.Entry(root, bg=bg_color, fg=fg_color)
command_entry.insert(0, "echo")


# Menu
bar = Menu(root, bg=menu_color, fg=fg_color) 
file = Menu(bar, tearoff = 0, bg=menu_color, fg=fg_color) 
bar.add_cascade(label ='File', menu = file) 
file.add_command(label ='Open...', command=lambda: open_file(lines, title_label, subtext_label, output_label, command_entry)) 
file.add_separator() 
file.add_command(label ='Exit', command = root.destroy)

root.config(menu = bar)
root.mainloop()
