import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from sequence import FullMove  # import your class here


class StateEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("State Sequence Editor")
        self.geometry("950x650")
        self.states: list[FullMove] = []
        self.current_index = None

        # Layout setup
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)

        # List of states
        self.state_listbox = tk.Listbox(main_frame, height=15, width=50)
        self.state_listbox.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.state_listbox.bind("<<ListboxSelect>>", self.on_state_select)

        # Scrollbars (optional)
        scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=self.state_listbox.yview)
        self.state_listbox.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=0, rowspan=12, sticky="nse")

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=12, column=0, pady=10)
        ttk.Button(btn_frame, text="Add State", command=self.add_state).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Delete State", command=self.delete_state).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Save Sequence", command=self.save_sequence).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Load Sequence", command=self.load_sequence).grid(row=0, column=3, padx=5)

        # State editor area
        self.slider_vars = {}
        self.entry_widgets = {}
        editor_frame = ttk.LabelFrame(main_frame, text="Edit State", padding=10)
        editor_frame.grid(row=0, column=1, rowspan=12, padx=20, sticky="nsew")

        for i in range(12):
            key = f"L{i+1}"
            ttk.Label(editor_frame, text=key, width=4).grid(row=i, column=0, sticky="e")

            var = tk.DoubleVar(value=0)
            self.slider_vars[key] = var

            slider = ttk.Scale(editor_frame, from_=-180, to=180, orient="horizontal", variable=var,
                               command=lambda v, k=key: self.update_entry_from_slider(k))
            slider.grid(row=i, column=1, padx=5, sticky="ew")

            entry = ttk.Entry(editor_frame, width=7)
            entry.grid(row=i, column=2, padx=5)
            entry.insert(0, "0")
            entry.bind("<Return>", lambda e, k=key: self.update_slider_from_entry(k))
            self.entry_widgets[key] = entry

        editor_frame.columnconfigure(1, weight=1)

        # Send button
        self.send_btn = ttk.Button(main_frame, text="Send Current State", command=self.send_state)
        self.send_btn.grid(row=13, column=1, pady=10)

    # ------------------- State management -------------------

    def add_state(self):
        state = FullMove([0] * 12)
        self.states.append(state)
        self.refresh_state_list()
        self.state_listbox.select_set(len(self.states) - 1)
        self.on_state_select()

    def delete_state(self):
        selection = self.state_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        del self.states[idx]
        self.refresh_state_list()
        self.clear_editor()

    def refresh_state_list(self):
        self.state_listbox.delete(0, tk.END)
        for i, state in enumerate(self.states):
            display = f"State {i+1}: " + ", ".join(str(int(v)) for v in state.values)
            self.state_listbox.insert(tk.END, display[:90])  # truncate display

    def on_state_select(self, event=None):
        selection = self.state_listbox.curselection()
        if not selection:
            self.current_index = None
            return
        self.current_index = selection[0]
        self.load_state_to_editor(self.states[self.current_index])

    def load_state_to_editor(self, state: FullMove):
        for i, val in enumerate(state.values):
            key = f"L{i+1}"
            self.slider_vars[key].set(val)
            self.entry_widgets[key].delete(0, tk.END)
            self.entry_widgets[key].insert(0, str(val))

    def clear_editor(self):
        for key in self.slider_vars:
            self.slider_vars[key].set(0)
            self.entry_widgets[key].delete(0, tk.END)
            self.entry_widgets[key].insert(0, "0")

    # ------------------- Sync sliders & entries -------------------

    def update_entry_from_slider(self, key):
        val = round(self.slider_vars[key].get(), 2)
        self.entry_widgets[key].delete(0, tk.END)
        self.entry_widgets[key].insert(0, str(val))
        self.update_current_state(key, val)

    def update_slider_from_entry(self, key):
        try:
            val = float(self.entry_widgets[key].get())
            if val < -180 or val > 180:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", f"Value for {key} must be between -180 and 180.")
            return
        self.slider_vars[key].set(val)
        self.update_current_state(key, val)

    def update_current_state(self, key, value):
        if self.current_index is not None:
            i = int(key[1:]) - 1
            self.states[self.current_index].values[i] = value
            self.refresh_state_list()
            self.state_listbox.select_set(self.current_index)

    # ------------------- File operations -------------------

    def save_sequence(self):
        if not self.states:
            messagebox.showinfo("Nothing to Save", "No states to save.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not filepath:
            return
        json_data = [s.to_json() for s in self.states]
        with open(filepath, "w") as f:
            json.dump(json_data, f, indent=4)
        messagebox.showinfo("Saved", f"Sequence saved to {filepath}")

    def load_sequence(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filepath:
            return
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            self.states = [FullMove.from_json(d) for d in data]
            self.refresh_state_list()
            self.clear_editor()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    # ------------------- Dummy send -------------------

    def send_state(self):
        if self.current_index is None:
            messagebox.showinfo("No State Selected", "Please select a state to send.")
            return
        state = self.states[self.current_index]
        self.dummy_send(state)

    def dummy_send(self, state: FullMove):
        print(f"Sending state:\n{json.dumps(state.to_json(), indent=2)}")


if __name__ == "__main__":
    app = StateEditor()
    app.mainloop()
