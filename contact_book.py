import tkinter as tk
from tkinter import messagebox, ttk

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("650x520")
        self.root.config(bg="#f8f9fa")
        self.root.resizable(False, False)
        self.contacts = []

        # ---------- Style ----------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Helvetica", 10, "bold"),
                        padding=6,
                        background="#1F77B4",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#1565C0")],
                  relief=[("pressed", "groove")])

        # ---------- Title ----------
        title = tk.Label(root, text="Contact Book", bg="#1F77B4", fg="white",
                         font=("Helvetica", 20, "bold"), pady=10)
        title.pack(fill="x")

        # ---------- Input Frame ----------
        frame = tk.Frame(root, bg="#f8f9fa")
        frame.pack(pady=20)

        labels = ["Name:", "Phone:", "Email:", "Address:"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(frame, text=text, font=("Helvetica", 11), bg="#f8f9fa", anchor="e").grid(row=i, column=0, sticky="e", padx=10, pady=8)
            var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var, width=40)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.entries[text[:-1].lower()] = var

        self.name_var = self.entries["name"]
        self.phone_var = self.entries["phone"]
        self.email_var = self.entries["email"]
        self.addr_var = self.entries["address"]

        # ---------- Buttons ----------
        btn_frame = tk.Frame(root, bg="#f8f9fa")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Update", command=self.update_contact).grid(row=0, column=1, padx=6)
        ttk.Button(btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=6)

        # ---------- Search ----------
        search_frame = tk.Frame(root, bg="#f8f9fa")
        search_frame.pack(pady=15)
        tk.Label(search_frame, text="Search:", font=("Helvetica", 11), bg="#f8f9fa").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=35).grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_contact).grid(row=0, column=2, padx=5)

        # ---------- List Frame ----------
        list_frame = tk.Frame(root, bg="#f8f9fa")
        list_frame.pack(pady=10)

        columns = ("Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=140)

        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.selected_index = None

        # ---------- Footer ----------
        footer = tk.Label(root, text="Designed by Bhavya Sree", bg="#f8f9fa",
                          font=("Helvetica", 9, "italic"), fg="#6c757d")
        footer.pack(side="bottom", pady=8)

    # ---------- Functions ----------
    def add_contact(self):
        contact = (self.name_var.get(), self.phone_var.get(), self.email_var.get(), self.addr_var.get())
        if not contact[0] or not contact[1]:
            messagebox.showwarning("Incomplete Data", "Name and Phone are required!")
            return
        self.contacts.append(contact)
        self.refresh_list()
        self.clear_entries()

    def refresh_list(self, contacts=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        display_contacts = contacts if contacts is not None else self.contacts
        for c in display_contacts:
            self.tree.insert("", "end", values=c)

    def clear_entries(self):
        for var in self.entries.values():
            var.set('')
        self.selected_index = None

    def on_select(self, event):
        try:
            selected_item = self.tree.selection()[0]
            index = self.tree.index(selected_item)
            self.selected_index = index
            selected = self.contacts[index]
            self.name_var.set(selected[0])
            self.phone_var.set(selected[1])
            self.email_var.set(selected[2])
            self.addr_var.set(selected[3])
        except IndexError:
            pass

    def update_contact(self):
        if self.selected_index is not None:
            updated = (self.name_var.get(), self.phone_var.get(), self.email_var.get(), self.addr_var.get())
            self.contacts[self.selected_index] = updated
            self.refresh_list()
            self.clear_entries()
        else:
            messagebox.showinfo("Select Contact", "Please select a contact to update.")

    def delete_contact(self):
        if self.selected_index is not None:
            self.contacts.pop(self.selected_index)
            self.refresh_list()
            self.clear_entries()
        else:
            messagebox.showinfo("Select Contact", "Please select a contact to delete.")

    def search_contact(self):
        keyword = self.search_var.get().lower()
        if not keyword:
            self.refresh_list()
            return
        filtered = [c for c in self.contacts if keyword in c[0].lower() or keyword in c[1]]
        self.refresh_list(filtered)


# ---------- Main ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
