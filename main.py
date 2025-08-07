import customtkinter as ctk
import tkinter as tk
import database

# Display setup
app = ctk.CTk()
app.title("To-Do Application")
app.geometry("500x500")
separator_color = "#444444"

def color_mode(mode):
    global separator_color
    ctk.set_appearance_mode(mode)
    if mode == "Dark":
        separator_color = "#444444"
    else:
        separator_color = "#CCCCCC"
    refresh_tasks()

def refresh_tasks():
    for widget in frame_tasks.winfo_children():
        widget.destroy()

    tasks = database.get_task()
    for task_id, title, completed in tasks:
        task_row = ctk.CTkFrame(frame_tasks, fg_color="transparent")
        task_row.pack(fill="x", padx=10, pady=5)

        checkbox_var = ctk.BooleanVar(value=bool(completed))

        # Checkbox
        checkbox = ctk.CTkCheckBox(
            task_row,
            text="",  # empty text, we'll use a label instead
            variable=checkbox_var,
            command=lambda t=task_id, v=checkbox_var: toggle_task_status(t, v.get()),
            width=20
        )
        checkbox.pack(side="left", padx=(5, 0))

        # Task label next to checkbox with wrapping
        task_label = ctk.CTkLabel(
            task_row,
            text=title,
            wraplength=300,
            anchor="w",
            justify="left"
        )
        task_label.pack(side="left", padx=(10, 0), fill="x", expand=True)

        # Optional: gray out completed task
        if completed:
            task_label.configure(text_color="gray")

        # Delete Button
        btn_del = ctk.CTkButton(task_row, text="❌", width=40, command=lambda t=task_id: delete_task(t))
        btn_del.pack(side="right", padx=5)

        # Separator (below task row)
        separator = ctk.CTkFrame(frame_tasks, height=2, fg_color=separator_color)
        separator.pack(fill="x", padx=10, pady=(0, 5))


def add_task():
    title = task_input.get()
    if not title.strip():
        tk.messagebox.showerror("Error", "Task cannot be empty")
        return
    database.add_task(title.strip())
    task_input.delete(0,ctk.END)
    refresh_tasks()

def delete_task(task_id):
    database.delete_task(task_id)
    refresh_tasks()

def toggle_task_status(task_id, is_done):
    database.mark_task_done(task_id, is_done)
    refresh_tasks()

# GUI PART
switch_var = ctk.StringVar(value="light")
switch = ctk.CTkSwitch(app, text="Light mode", command=lambda: color_mode(switch_var.get()), variable=switch_var, onvalue="Light", offvalue="Dark")
switch.pack(pady = 10)

task_input = ctk.CTkEntry(app, placeholder_text="Enter new task")
task_input.pack(pady = 10, padx = 20, fill = "x")

add_btn = ctk.CTkButton(app, text="Add Task", command=add_task)
add_btn.pack(pady = 5)

# Frame for task list
frame_tasks = ctk.CTkScrollableFrame(app, width=400, height=350)
frame_tasks.pack(padx=20, pady=10, fill="both", expand=True)

refresh_tasks()

app.mainloop()