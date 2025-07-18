import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("300x100")
tk.Label(root, text="This is a test window").pack(pady=20)
root.mainloop()
