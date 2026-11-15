"""City Route Finder - BFS | CF321 Fundamentals of AI.

GUI: python main.py
CLI: python main.py --cli --start Cairo --goal "Port Said"
Tests: python -m unittest discover -s tests -v
"""

import argparse
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from bfs import SearchResult, bfs_shortest_path
from graph_data import CITY_POSITIONS, EDGES, GRAPH


# Project team: Nour Hussein (24030193), Mayar Ali (24030066),
# Mariam Mohamed (24030054). Department: CS.

# Innovation University branding uses purple on white. The official wordmark
# is embedded in assets/ and loaded with Tkinter (no external packages).
COLORS = {
    "bg": "#f6f4fa",       # page background
    "panel": "#ffffff",    # white cards
    "card": "#f0ecf8",     # pale purple controls
    "canvas": "#ffffff",   # schematic map
    "line": "#d7cee9",     # fine borders / inactive links
    "grid": "#eeebf6",     # dot grid
    "text": "#262039",     # near-black purple text
    "muted": "#6a627c",
    "teal": "#6253a4",     # actual university brand purple
    "blue": "#7558c5",     # highlighted shortest route
    "purple": "#b49be9",   # explored nodes
    "green": "#188a6f",    # start city
    "amber": "#e38e24",    # destination
    "red": "#d94b70",
}


class CityRouteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Innovation University | City Route Finder - BFS")
        self.root.configure(bg=COLORS["bg"])
        self.root.geometry("1170x910")
        self.root.minsize(1060, 880)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.start_var = tk.StringVar(value="Cairo")
        self.goal_var = tk.StringVar(value="Port Said")
        self.message_var = tk.StringVar(value="Select a start and destination, then find a route.")
        self.path_var = tk.StringVar(value="--")
        self.cost_var = tk.StringVar(value="--")
        self.explored_var = tk.StringVar(value="--")
        self.visited: set[str] = set()
        self.result: SearchResult | None = None
        self.active_after: str | None = None
        self.animation_index = 0

        self.setup_styles()
        self.build_ui()
        self.root.after(250, self.find_route)

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Picker.TCombobox", font=("DejaVu Sans", 12), padding=9,
                        fieldbackground=COLORS["card"], background=COLORS["card"],
                        foreground=COLORS["text"], arrowcolor=COLORS["teal"],
                        bordercolor=COLORS["line"], lightcolor=COLORS["line"],
                        darkcolor=COLORS["line"])
        style.map("Picker.TCombobox", fieldbackground=[("readonly", COLORS["card"])],
                  foreground=[("readonly", COLORS["text"])],
                  selectbackground=[("readonly", COLORS["card"])],
                  selectforeground=[("readonly", COLORS["text"])])

    def label(self, parent, text, size=11, color="text", weight="normal", **kwargs):
        return tk.Label(parent, text=text, font=("DejaVu Sans", size, weight),
                        fg=COLORS.get(color, color), bg=parent.cget("bg"), **kwargs)

    def build_ui(self):
        header = tk.Frame(self.root, bg=COLORS["panel"])
        header.pack(fill="x")
        header_inner = tk.Frame(header, bg=COLORS["panel"])
        header_inner.pack(fill="x", padx=32, pady=(10, 8))
        title_area = tk.Frame(header_inner, bg=COLORS["panel"])
        title_area.pack(side="left", anchor="w")
        self.label(title_area, "CITY ROUTE FINDER", 21, "text", "bold").pack(anchor="w")
        self.label(title_area, "FUNDAMENTALS OF AI  /  CF321  /  BREADTH-FIRST SEARCH", 9, "teal", "bold").pack(anchor="w", pady=(4, 0))
        try:
            from pathlib import Path
            logo_path = Path(__file__).resolve().parent / "assets" / "innovation_university_logo.png"
            self.university_logo = tk.PhotoImage(file=str(logo_path))
            tk.Label(header_inner, image=self.university_logo, bg=COLORS["panel"], bd=0).pack(side="right", anchor="center")
        except tk.TclError:
            self.label(header_inner, "INNOVATION UNIVERSITY", 14, "teal", "bold").pack(side="right")
        tk.Frame(header, bg=COLORS["teal"], height=3).pack(fill="x")

        body = tk.Frame(self.root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=28, pady=(15, 6))

        sidebar = tk.Frame(body, bg=COLORS["panel"], width=305)
        sidebar.pack(side="left", fill="y", padx=(0, 16))
        sidebar.pack_propagate(False)
        controls = tk.Frame(sidebar, bg=COLORS["panel"])
        controls.pack(fill="x", padx=22, pady=(14, 8))
        self.label(controls, "ROUTE OPTIONS", 11, "teal", "bold").pack(anchor="w", pady=(0, 14))
        self.label(controls, "START CITY", 9, "muted", "bold").pack(anchor="w", pady=(0, 7))
        cities = list(CITY_POSITIONS)
        ttk.Combobox(controls, textvariable=self.start_var, values=cities,
                     state="readonly", style="Picker.TCombobox").pack(fill="x")
        self.label(controls, "DESTINATION", 9, "muted", "bold").pack(anchor="w", pady=(14, 7))
        ttk.Combobox(controls, textvariable=self.goal_var, values=cities,
                     state="readonly", style="Picker.TCombobox").pack(fill="x")

        self.button(controls, "FIND SHORTEST ROUTE", self.find_route, "teal", 12).pack(fill="x", pady=(18, 9))
        self.button(controls, "ANIMATE BFS", self.animate_bfs, "blue", 11).pack(fill="x", pady=(0, 9))
        buttons = tk.Frame(controls, bg=COLORS["panel"])
        buttons.pack(fill="x")
        self.button(buttons, "SWAP", self.swap, "card", 10).pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.button(buttons, "RESET", self.reset, "card", 10).pack(side="left", fill="x", expand=True, padx=(4, 0))

        tk.Frame(sidebar, bg=COLORS["line"], height=1).pack(fill="x", padx=22, pady=(9, 8))
        details = tk.Frame(sidebar, bg=COLORS["panel"])
        details.pack(fill="x", padx=22)
        self.label(details, "HOW IT WORKS", 10, "text", "bold").pack(anchor="w", pady=(0, 8))
        how = ("BFS explores nearby cities level by level.\n"
               "Each link has a cost of 1, so the first\n"
               "path found uses the fewest links.")
        self.label(details, how, 9, "muted", justify="left").pack(anchor="w")
        self.label(details, "LEGEND", 10, "text", "bold").pack(anchor="w", pady=(12, 8))
        for name, col in (("Start city", "green"), ("Destination", "amber"),
                          ("Shortest route", "blue"), ("Visited by BFS", "purple")):
            row = tk.Frame(details, bg=COLORS["panel"])
            row.pack(fill="x", pady=3)
            tk.Canvas(row, width=14, height=14, bg=COLORS["panel"], highlightthickness=0).pack(side="left")
            dot = tk.Canvas(row, width=12, height=12, bg=COLORS["panel"], highlightthickness=0)
            dot.place(x=1, y=0)
            dot.create_oval(1, 1, 11, 11, fill=COLORS[col], outline="")
            self.label(row, name, 9, "muted").pack(side="left", padx=(7, 0))
        tk.Frame(sidebar, bg=COLORS["line"], height=1).pack(fill="x", padx=22, pady=(8, 8))
        self.label(sidebar, "PROJECT TEAM  /  CS", 9, "teal", "bold").pack(anchor="w", padx=22)
        self.label(sidebar, "Nour Hussein  -  24030193\nMayar Ali  -  24030066\nMariam Mohamed  -  24030054",
                   9, "muted", justify="left").pack(anchor="w", padx=22, pady=(6, 0))

        right = tk.Frame(body, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)
        map_card = tk.Frame(right, bg=COLORS["canvas"])
        map_card.pack(fill="both", expand=True)
        map_heading = tk.Frame(map_card, bg=COLORS["canvas"])
        map_heading.pack(fill="x", padx=20, pady=(15, 0))
        self.label(map_heading, "SCHEMATIC CITY NETWORK", 12, "text", "bold").pack(side="left")
        self.label(map_heading, "10 CITIES  |  13 LINKS", 9, "teal", "bold").pack(side="right")
        self.canvas = tk.Canvas(map_card, bg=COLORS["canvas"], width=710, height=515,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(2, 0))
        self.canvas.bind("<Configure>", lambda _e: self.draw_graph())
        self.label(map_card, "Illustrative links and positions, not real road distances or a GPS map.",
                   9, "muted").pack(anchor="w", padx=20, pady=(0, 11))

        info = tk.Frame(right, bg=COLORS["panel"], height=131)
        info.pack(fill="x", pady=(13, 0))
        info.pack_propagate(False)
        stat_row = tk.Frame(info, bg=COLORS["panel"])
        stat_row.pack(fill="x", padx=20, pady=(13, 7))
        for title, variable, color in (("PATH COST / HOPS", self.cost_var, "teal"),
                                       ("NODES EXPLORED", self.explored_var, "blue")):
            stat = tk.Frame(stat_row, bg=COLORS["panel"])
            stat.pack(side="left", padx=(0, 38))
            self.label(stat, title, 9, "muted", "bold").pack(anchor="w")
            self.label(stat, "", 20, color, "bold", textvariable=variable).pack(anchor="w", pady=(1, 0))
        self.label(info, "", 10, "text", textvariable=self.path_var,
                   anchor="w", wraplength=700, justify="left").pack(fill="x", padx=20)
        self.label(self.root, "", 9, "muted", textvariable=self.message_var,
                   anchor="w").pack(fill="x", padx=32, pady=(3, 12))
        self.draw_graph()

    def button(self, parent, title, command, variant, font_size):
        if variant == "card":
            background, foreground = COLORS["card"], COLORS["text"]
        else:
            background, foreground = COLORS[variant], "#ffffff"
        return tk.Button(parent, text=title, command=command,
                         font=("DejaVu Sans", font_size, "bold"),
                         bg=background, fg=foreground,
                         activebackground=COLORS["line"], activeforeground=COLORS["text"],
                         relief="flat", cursor="hand2", padx=9, pady=12,
                         highlightthickness=0, bd=0)

    def canvas_coords(self, city):
        # Fit the 715 x 515 schematic graph to the available drawing area.
        x, y = CITY_POSITIONS[city]
        w = max(715, self.canvas.winfo_width())
        h = max(515, self.canvas.winfo_height())
        return ((w - 715) / 2 + x, (h - 515) / 2 + y)

    def draw_graph(self):
        if not hasattr(self, "canvas"):
            return
        c = self.canvas
        c.delete("all")
        w, h = max(c.winfo_width(), 715), max(c.winfo_height(), 515)
        for x in range(12, w, 30):
            for y in range(14, h, 30):
                c.create_oval(x, y, x + 2, y + 2, fill=COLORS["grid"], outline="")

        path_edges = set()
        if self.result and self.result.found:
            path_edges = {frozenset((left, right))
                          for left, right in zip(self.result.path, self.result.path[1:])}

        for left, right in EDGES:
            x1, y1 = self.canvas_coords(left)
            x2, y2 = self.canvas_coords(right)
            highlighted = frozenset((left, right)) in path_edges
            c.create_line(x1, y1, x2, y2,
                          fill=COLORS["blue"] if highlighted else COLORS["line"],
                          width=5 if highlighted else 2,
                          capstyle="round")

        path_cities = set(self.result.path) if self.result and self.result.found else set()
        for city in CITY_POSITIONS:
            x, y = self.canvas_coords(city)
            start, goal = self.start_var.get(), self.goal_var.get()
            if city == start:
                fill, stroke = COLORS["green"], COLORS["green"]
            elif city == goal:
                fill, stroke = COLORS["amber"], COLORS["amber"]
            elif city in path_cities:
                fill, stroke = COLORS["blue"], COLORS["blue"]
            elif city in self.visited:
                fill, stroke = COLORS["purple"], COLORS["purple"]
            else:
                fill, stroke = COLORS["card"], COLORS["line"]
            c.create_oval(x - 12, y - 12, x + 12, y + 12, fill=fill, outline=stroke, width=2)
            c.create_oval(x - 3, y - 3, x + 3, y + 3, fill=COLORS["canvas"] if fill != COLORS["card"] else COLORS["muted"], outline="")
            label_y = y - 26 if city in ("6th of October", "Giza", "Port Said", "Mansoura") else y + 26
            c.create_text(x, label_y, text=city, fill=COLORS["text"],
                          font=("DejaVu Sans", 10, "bold"), anchor="center")

    def cancel_animation(self):
        if self.active_after is not None:
            try:
                self.root.after_cancel(self.active_after)
            except tk.TclError:
                pass
            self.active_after = None

    def selection(self):
        start, goal = self.start_var.get(), self.goal_var.get()
        if start not in GRAPH or goal not in GRAPH:
            messagebox.showerror("Invalid city", "Choose both cities from the lists.")
            return None
        return start, goal

    def find_route(self):
        self.cancel_animation()
        selection = self.selection()
        if selection is None:
            return
        start, goal = selection
        self.result = bfs_shortest_path(GRAPH, start, goal)
        self.visited = set(self.result.explored_order)
        self.display_result()
        self.draw_graph()
        self.message_var.set("BFS completed. Purple links show the minimum-hop route.")

    def display_result(self):
        if self.result is None:
            self.path_var.set("--")
            self.cost_var.set("--")
            self.explored_var.set("--")
        elif self.result.found:
            self.path_var.set("ROUTE:  " + "  ->  ".join(self.result.path))
            self.cost_var.set(str(self.result.cost))
            self.explored_var.set(str(self.result.explored_nodes))
        else:
            self.path_var.set("No route found")
            self.cost_var.set("N/A")
            self.explored_var.set(str(self.result.explored_nodes))

    def animate_bfs(self):
        self.cancel_animation()
        selection = self.selection()
        if selection is None:
            return
        self.result = None
        self.visited.clear()
        self.display_result()
        self.draw_graph()
        start, goal = selection
        self.animation_result = bfs_shortest_path(GRAPH, start, goal)
        self.animation_index = 0
        self.message_var.set("Animating BFS: purple nodes are explored in queue order.")
        self.animation_step()

    def animation_step(self):
        if self.animation_index < len(self.animation_result.explored_order):
            city = self.animation_result.explored_order[self.animation_index]
            self.visited.add(city)
            self.animation_index += 1
            self.explored_var.set(str(self.animation_index))
            self.message_var.set(f"BFS visiting: {city}  ({self.animation_index} explored)")
            self.draw_graph()
            self.active_after = self.root.after(430, self.animation_step)
        else:
            self.active_after = None
            self.result = self.animation_result
            self.display_result()
            self.draw_graph()
            self.message_var.set("Animation finished: minimum-hop route highlighted in purple.")

    def swap(self):
        self.cancel_animation()
        start, goal = self.start_var.get(), self.goal_var.get()
        self.start_var.set(goal)
        self.goal_var.set(start)
        self.find_route()

    def reset(self):
        self.cancel_animation()
        self.visited.clear()
        self.result = None
        self.display_result()
        self.draw_graph()
        self.message_var.set("Visualization reset. Choose a new route to search.")

    def close(self):
        self.cancel_animation()
        self.root.destroy()


def run_cli(start: str, goal: str):
    result = bfs_shortest_path(GRAPH, start, goal)
    print("=" * 62)
    print("CITY ROUTE FINDER - BFS | CF321 FUNDAMENTALS OF AI")
    print("=" * 62)
    print(f"Start city:        {start}")
    print(f"Destination city:  {goal}")
    print(f"Search algorithm:  Breadth-First Search (BFS)")
    print(f"Path found:        {'Yes' if result.found else 'No'}")
    print(f"Shortest route:    {' -> '.join(result.path) if result.found else 'N/A'}")
    print(f"Path cost (hops):  {result.cost if result.cost is not None else 'N/A'}")
    print(f"Nodes explored:    {result.explored_nodes}")
    print(f"Explored order:    {' -> '.join(result.explored_order)}")
    print("NOTE: Illustrative network, not real driving distances.")
    return result


def main():
    parser = argparse.ArgumentParser(description="City Route Finder Using BFS (CF321)")
    parser.add_argument("--cli", action="store_true", help="Run in the console instead of the GUI")
    parser.add_argument("--start", default="Cairo", help="Starting city")
    parser.add_argument("--goal", default="Port Said", help="Destination city")
    parser.add_argument("--list-cities", action="store_true", help="Print the available city names")
    args = parser.parse_args()

    if args.list_cities:
        print("\n".join(CITY_POSITIONS))
        return 0

    if args.cli:
        try:
            run_cli(args.start, args.goal)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2
        return 0

    try:
        root = tk.Tk()
    except tk.TclError:
        print("A graphical display is unavailable. Try: python main.py --cli", file=sys.stderr)
        return 1
    CityRouteApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
