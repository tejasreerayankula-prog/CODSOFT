import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import threading
import time
import json

TASK_FILE = "tasks.json"

# Load tasks from file with backward compatibility
def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            loaded_tasks = json.load(file)
            # Ensure every task has a priority field
            for task in loaded_tasks:
                if "priority" not in task:
                    task["priority"] = "Medium"
            return loaded_tasks
    except:
        return []

# Save tasks to file
def save_tasks():
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file)

# Background reminder checker
def check_reminders():
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for task in tasks:
            if task["reminder"] == now and not task["notified"]:
                messagebox.showinfo("Reminder", f"Reminder: {task['task']}")
                task["notified"] = True
                save_tasks()
        time.sleep(30)

# Add new task
def add_task():
    task_text = task_entry.get()
    if task_text:
        priority = priority_var.get()
        tasks.append({
            "task": task_text,
            "done": False,
            "reminder": "",
            "notified": False,
            "priority": priority
        })
        update_listbox()
        task_entry.delete(0, tk.END)
        save_tasks()

# Delete selected task
def delete_task():
    selected = listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        update_listbox()
        save_tasks()

# Mark selected task as complete/incomplete
def mark_complete():
    selected = listbox.curselection()
    if selected:
        tasks[selected[0]]["done"] = not tasks[selected[0]]["done"]
        update_listbox()
        save_tasks()

# Update selected task text
def update_task():
    selected = listbox.curselection()
    if selected:
        new_task = simpledialog.askstring("Update Task", "Enter new task text:")
        if new_task:
            tasks[selected[0]]["task"] = new_task
            update_listbox()
            save_tasks()

# Set reminder for selected task
def set_reminder():
    selected = listbox.curselection()
    if selected:
        time_input = simpledialog.askstring("Set Reminder", "Enter reminder time (YYYY-MM-DD HH:MM):")
        try:
            datetime.datetime.strptime(time_input, "%Y-%m-%d %H:%M")
            tasks[selected[0]]["reminder"] = time_input
            tasks[selected[0]]["notified"] = False
            update_listbox()
            save_tasks()
        except ValueError:
            messagebox.showerror("Invalid Format", "Please use YYYY-MM-DD HH:MM format.")

# Search tasks
def search_tasks():
    query = search_entry.get().lower()
    listbox.delete(0, tk.END)
    for task in tasks:
        if query in task["task"].lower():
            insert_task(task)

# Sort tasks by done + priority
def sort_tasks():
    tasks.sort(key=lambda x: (x["done"], {"High": 1, "Medium": 2, "Low": 3}[x["priority"]]))
    update_listbox()

# Insert one task into listbox with formatting
def insert_task(task):
    status = "✓" if task["done"] else "✗"
    reminder_info = f" [⏰ {task['reminder']}]" if task["reminder"] else ""
    priority = task.get("priority", "Medium")
    display_text = f"{status} ({priority}) {task['task']}{reminder_info}"

    idx = listbox.size()
    listbox.insert(tk.END, display_text)

    # Highlight overdue tasks
    if task["reminder"]:
        try:
            reminder_time = datetime.datetime.strptime(task["reminder"], "%Y-%m-%d %H:%M")
            if reminder_time < datetime.datetime.now() and not task["done"]:
                listbox.itemconfig(idx, {'fg': 'red'})
        except:
            pass

# Refresh listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        insert_task(task)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("To-Do List with Reminder & Priority")

# Task entry
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

# Priority dropdown
priority_var = tk.StringVar(value="Medium")
tk.OptionMenu(root, priority_var, "High", "Medium", "Low").pack(pady=5)

# Buttons frame
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Add", command=add_task).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_task).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Mark Done", command=mark_complete).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Update", command=update_task).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Set Reminder", command=set_reminder).grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="Sort", command=sort_tasks).grid(row=0, column=5, padx=5)

# Search bar
search_entry = tk.Entry(root, width=40)
search_entry.pack(pady=5)
tk.Button(root, text="Search", command=search_tasks).pack(pady=2)

# Task list display
listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)

# Load existing tasks
tasks = load_tasks()
update_listbox()

# Start reminder thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

root.mainloop()
