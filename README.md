# City Route Finder Using BFS

**Institution:** Innovation University - Faculty of Computers and Information Technology  
**Visual identity:** University purple and original Innovation University logo used with the provided academic template.  

**Course:** Fundamentals of AI (CF321) — Search Algorithms  
**Department:** Computer Science (CS)  
**Team:**

| Student Name | Student ID | Department |
|---|---|---|
| Nour Hussein | 24030193 | CS |
| Mayar Ali | 24030066 | CS |
| Mariam Mohamed | 24030054 | CS |

## Project idea

City Route Finder is a Python application that finds a route with the **fewest connections** between two cities using **Breadth-First Search (BFS)**. It includes a Tkinter visual interface showing the network, visited cities, shortest route, route cost, and the number of explored nodes. It also works from the command line.

> **Important:** The graph is an **illustrative educational network** with manually defined bidirectional links. The diagram is not geographically scaled. The route is **not** the fastest or shortest driving route; it minimizes the number of edges in this sample graph.

## AI search problem formulation

| Requirement | Project definition |
|---|---|
| **State** | The city that the agent is currently in. |
| **Initial state** | The start city selected by the user. |
| **Goal state / goal test** | Reach the selected destination city. |
| **Available actions** | Move to any directly connected neighboring city. |
| **Transition cost** | Exactly 1 per link, in either direction. |
| **Search algorithm** | Breadth-First Search (BFS), using a FIFO queue. |
| **Solution** | A sequence of connected cities from start to goal. |
| **Solution cost** | Number of links (hops) in the returned route. |
| **Search measurement** | Number of nodes removed from the queue and explored. |

BFS explores cities **level by level**. Each city is marked discovered when it is first added to the queue, so no city is added twice. A parent reference is stored to reconstruct the route when the goal is reached. Because every link has an equal cost of 1, BFS returns a minimum-hop route.

**Complexity:** O(V + E) time and O(V) additional space, where V is the number of cities and E is the number of links.

## Requirements

- **Python 3.10+** (recommended: Python 3.11 or newer)
- **Tkinter** for the visual interface (ships with most Windows and macOS Python installations; on some Linux distributions, install `python3-tk`)
- **No pip packages required**. The BFS, CLI, and tests use only the Python standard library.

## How to run

Open a terminal **inside the project folder**.

**Graphical interface** (Windows, macOS, Linux with a desktop):

```bash
python main.py
```

**Console version:**

```bash
python main.py --cli
python main.py --cli --start Alexandria --goal Suez
python main.py --cli --start "6th of October" --goal "Port Said"
```

**List all available cities:**

```bash
python main.py --list-cities
```

**Run automated tests:**

```bash
python -m unittest discover -s tests -v
```

On some Windows installations, use `py` instead of `python`.

## How to use the GUI

1. Select a **Start City** and a **Destination**.
2. Click **Find Shortest Route** for the result immediately, or **Animate BFS** to watch the explored cities.
3. Inspect the highlighted route, cost (hops), and number of explored nodes.
4. Use **Swap** to reverse the route or **Reset** to remove the highlights.

## Example results

Using the included sample graph:

```text
Start city:        Cairo
Destination city:  Port Said
Search algorithm:  Breadth-First Search (BFS)
Path found:        Yes
Shortest route:    Cairo -> Ismailia -> Port Said
Path cost (hops):  2
```

The actual count of explored nodes is printed by the application and may depend on the order in which neighbors are added to the queue. The graph has **10 cities** and **13 bidirectional links**.

## Project files

```text
City_Route_Finder_BFS/
|-- main.py                     # Tkinter GUI and CLI
|-- bfs.py                      # Search algorithm / result model
|-- graph_data.py               # City network and its schematic positions
|-- assets/
|   `-- innovation_university_logo.png  # University logo (included)
|-- tests/
|   `-- test_bfs.py             # Unit tests, including edge cases
|-- screenshots/
|   |-- application.png         # Screenshot from the running GUI
|   `-- test_results.png        # Screenshot of terminal test results
|-- PROJECT_REPORT.pdf          # University-branded project report and evidence
|-- README.md                   # This documentation
`-- .gitignore
```

## GitHub submission

Create a new GitHub repository, e.g. `city-route-finder-bfs`, and upload the contents of this folder. A short example of Git commands is:

```bash
git init
git add .
git commit -m "Complete CF321 City Route Finder BFS project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/city-route-finder-bfs.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username, and create the empty remote repository first. Check that `README.md`, the Python files, tests, and report are all visible on GitHub.
