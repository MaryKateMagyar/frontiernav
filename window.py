import tkinter as tk
from tkinter import ttk
from frontiernav import FrontierNav

class GUI:
    def __init__(self, game_data):
        self.__root = tk.Tk()
        self.__root.title("FrontierNav Probe Calculator")
        self.__root.geometry("1200x800")
        self.__root.resizable(True, True)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        processed_game_data = FrontierNav.load_game_data(game_data)
        self.frontier_nav = FrontierNav(processed_game_data)
        self.available_probes = self._get_available_probes()
        self.probe_dropdown_vars = {}

        self.setup_ui()
        self.run()

    def run(self):
        self.__root.mainloop()

    def close(self):
        self.__root.destroy()

    def _get_available_probes(self):
        probe_list = []

        for probe_type, generations in self.frontier_nav.probes.items():
            for gen_key, probe in generations.items():
                probe_list.append(probe.name)
        
        return probe_list

    def setup_ui(self):
        notebook = ttk.Notebook(self.__root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        for region in self.frontier_nav.nodes.keys():
            self.create_region_tab(notebook, region)

    def create_region_tab(self, notebook, region):
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text=region)

        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        header_label = ttk.Label(scrollable_frame, text=f"{region}", font=("Arial", 14, "bold"))
        header_label.grid(row=0, column=0, columnspan=2,pady=(0, 15))

        row = 1
        for node_id, node in self.frontier_nav.nodes[region].items():
            # Site name label
            site_label = ttk.Label(scrollable_frame, text=node.name)
            site_label.grid(row=row, column=0, sticky="w", padx=(0, 20), pady=5)

            # Probe dropdown list
            probe_var = tk.StringVar(value="Probe Slot Locked")
            probe_dropdown = ttk.Combobox(scrollable_frame, textvariable=probe_var, values=self.available_probes, state="readonly")
            probe_dropdown.grid(row=row, column=1, sticky="w", padx=(0, 10), pady=5)

            # Store the dropdown variable for access
            self.probe_dropdown_vars[f"{region}_{node_id}"] = probe_var

            probe_dropdown.bind('<<ComboboxSelected>>', lambda event, r=region, n=node_id: self.on_probe_changed(r, n))

            row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_probe_changed(self, region, node_id):
        selected_probe_name = self.probe_dropdown_vars[f"{region}_{node_id}"].get()
        selected_probe = self._find_probe_by_name(selected_probe_name)
        probe_slot = self.frontier_nav.slots[region][node_id]
        if selected_probe:
            probe_slot.install_probe(selected_probe)
        else:
            probe_slot.lock_probe()

    def _find_probe_by_name(self, probe_name):
        for probe_type, generations in self.frontier_nav.probes.items():
            for gen_key, probe in generations.items():
                if probe.name == probe_name:
                    return probe
        return None
