# Degrees of Separation

### 📋 Overview
This project implements a **Breadth-First Search (BFS)** algorithm to find the shortest path between two actors based on their shared movie credits. Inspired by the "Six Degrees of Kevin Bacon," the program identifies how many "steps" it takes to connect any two people in the Hollywood film industry.

### 🛠️ Technical Features
* **Algorithm:** Implements **Breadth-First Search (BFS)** to guarantee the shortest path in an unweighted graph.
* **Graph Representation:** Actors are treated as nodes, and movies are the edges connecting them.
* **Performance Optimization:** * Tracks "visited" nodes to prevent infinite loops and redundant searches.
    * Utilizes a custom `QueueFrontier` for efficient $O(1)$ removal of the next node to explore.
* **Data Handling:** Processes large-scale CSV datasets (thousands of rows) efficiently using Python's `csv` module.

### 🚀 Getting Started

#### Prerequisites
* Python 3.12 

#### Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/your-username/degrees-of-separation.git](https://github.com/your-username/degrees-of-separation.git)
   cd degrees-of-separation

### 🚀 Usage
Run the program by specifying the data directory (`small` or `large`):

```bash
python degrees.py small

When prompted, enter the names of two actors to find the shortest path between them:

**### Example Output**
```Plaintext
Name: Dustin Hoffman
Name: Tom Cruise
2 degrees of separation.
1: Dustin Hoffman and Tom Cruise starred in Rain Man
