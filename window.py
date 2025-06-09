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
        main_container = ttk.Frame(self.__root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(main_container)
        notebook.pack(side="left", fill="both", expand=True, padx=(0, 10))

        for region in self.frontier_nav.nodes.keys():
            self.create_region_tab(notebook, region)

        self.create_side_panel(main_container)

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

    def create_side_panel(self, parent):
        side_panel = ttk.Frame(parent)
        side_panel.pack(side="right", fill="y", padx=(10, 0))

        totals_frame = ttk.LabelFrame(side_panel, text="Total Production", padding="10")
        totals_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.miranium_label = ttk.Label(totals_frame, text="Miranium: 0", font=("Arial", 12))
        self.miranium_label.pack(anchor="w", pady=2)

        self.credits_label = ttk.Label(totals_frame, text="Credits: 0", font=("Arial", 12))
        self.credits_label.pack(anchor="w", pady=2)

        self.storage_label = ttk.Label(totals_frame, text="Storage: 6000", font=("Arial", 12))
        self.storage_label.pack(anchor="w", pady=2)
        
        self.resources_label = ttk.Label(totals_frame, text="Possible Precious Resources: None", font=("Arial", 12))
        self.resources_label.pack(anchor="w", pady=2)

        self.cost_label = ttk.Label(totals_frame, text="Cost: 0", font=("Arial", 12))
        self.cost_label.pack(anchor="w", pady=2)
        self.cost_warning = ttk.Label(totals_frame, text="(Warning: Excludes Cost of Battle Probes)", font=("Arial", 6))
        self.cost_warning.pack(anchor="w", pady=2)

        calculate_button = ttk.Button(side_panel, text="Calculate Totals", command=self.update_totals)
        calculate_button.pack(pady=(10, 0))

        install_basic_button = ttk.Button(side_panel, text="Install All Basic Probes", command=self.install_basic_probes)
        install_basic_button.pack()

    def update_totals(self):
        totals = self.frontier_nav.calculate_total()

        self.miranium_label.config(text=f"Miranium: {totals["total miranium"]}")
        self.credits_label.config(text=f"Credits: {totals["total credits"]}")
        self.storage_label.config(text=f"Storage: {totals["total storage"]}")

        resources_text = "Possible Precious Resources: "
        if totals["possible resources"]:
            for resource in totals["possible resources"]:
                resources_text += f"\n* {resource}"
        else:
            resources_text += "None"
        self.resources_label.config(text=resources_text)

        self.cost_label.config(text=f"Cost: {totals["total cost"]}")

    def install_basic_probes(self):
        basic_probe = self.frontier_nav.probes["basic"][0]

        for region in self.frontier_nav.nodes.keys():
            for node_id, node in self.frontier_nav.nodes[region].items():
                node.probe_slot.install_probe(basic_probe)
                probe_var = self.probe_dropdown_vars[f"{region}_{node_id}"]
                probe_var.set(basic_probe.name)
        
        self.update_totals()
