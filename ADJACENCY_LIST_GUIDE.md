# Adjacency List - Theory and Examples

**A comprehensive guide to adjacency list representation of graphs**

---

## 📋 Table of Contents

1. [What is an Adjacency List?](#what-is-an-adjacency-list)
2. [Theory and Fundamentals](#theory-and-fundamentals)
3. [Adjacency List vs Other Representations](#adjacency-list-vs-other-representations)
4. [Implementation Approaches](#implementation-approaches)
5. [Practical Examples](#practical-examples)
6. [Time and Space Complexity](#time-and-space-complexity)
7. [Real-World Applications](#real-world-applications)
8. [Code Examples](#code-examples)

---

## 1. What is an Adjacency List?

An **adjacency list** is a way to represent a graph where each vertex stores a list of all vertices it is connected to (its "neighbors" or "adjacent" vertices).

### Visual Example

**Graph:**
```
    A ──→ B
    │     │
    ↓     ↓
    C ──→ D
```

**Adjacency List Representation:**
```
A → [B, C]
B → [D]
C → [D]
D → []
```

**In English:** 
- Vertex A has edges to B and C
- Vertex B has an edge to D
- Vertex C has an edge to D
- Vertex D has no outgoing edges

---

## 2. Theory and Fundamentals

### 2.1 Basic Concept

For a graph **G = (V, E)** where:
- **V** = set of vertices (nodes)
- **E** = set of edges (connections)

An adjacency list is an array or dictionary of lists:
- **Index/Key**: Each vertex
- **Value**: List of all vertices that vertex connects to

### 2.2 Types of Graphs

#### Directed Graph (Digraph)
```
A → B → C
↓       ↑
D ──────┘

Adjacency List:
A → [B, D]
B → [C]
C → []
D → [C]
```

One-way connections. If A→B exists, B→A may not exist.

#### Undirected Graph
```
A ─ B ─ C
│       │
D ───── E

Adjacency List:
A → [B, D]
B → [A, C]
C → [B, E]
D → [A, E]
E → [D, C]
```

Two-way connections. If A─B exists, both A→B and B→A are stored.

#### Weighted Graph
```
    2.5      3.0
A ─────→ B ─────→ C
│ 1.0           ↗ 4.5
↓              │
D ─────────────┘

Adjacency List with Weights:
A → [(B, 2.5), (D, 1.0)]
B → [(C, 3.0)]
C → []
D → [(C, 4.5)]
```

Edges have associated costs/weights/distances.

---

## 3. Adjacency List vs Other Representations

### 3.1 Adjacency Matrix

**Matrix Representation:**
```
    A  B  C  D
A [ 0  1  1  0 ]
B [ 0  0  0  1 ]
C [ 0  0  0  1 ]
D [ 0  0  0  0 ]
```

**List Representation:**
```
A → [B, C]
B → [D]
C → [D]
D → []
```

### 3.2 Comparison Table

| Aspect | Adjacency List | Adjacency Matrix |
|--------|----------------|------------------|
| **Space** | O(V + E) | O(V²) |
| **Add Vertex** | O(1) | O(V²) |
| **Add Edge** | O(1) | O(1) |
| **Remove Vertex** | O(E) | O(V²) |
| **Remove Edge** | O(E) | O(1) |
| **Check if edge exists** | O(degree) | O(1) |
| **Iterate neighbors** | O(degree) | O(V) |
| **Best for** | Sparse graphs | Dense graphs |
| **Memory efficient for** | Few edges | Many edges |

### 3.3 When to Use Adjacency List

✅ **Use adjacency list when:**
- Graph is sparse (few edges relative to vertices)
- Need to iterate over neighbors frequently
- Graph structure changes dynamically
- Memory is a concern
- Most real-world graphs (social networks, road maps, web pages)

❌ **Use adjacency matrix when:**
- Graph is dense (many edges)
- Need to quickly check if specific edge exists
- Graph is small
- Need matrix operations

---

## 4. Implementation Approaches

### 4.1 Array of Lists (C/C++)

```c
// Each vertex has an array/linked list of neighbors
typedef struct Node {
    int vertex;
    struct Node* next;
} Node;

Node* adjacencyList[MAX_VERTICES];

// A → [B, C]
adjacencyList[A] = createNode(B) → createNode(C) → NULL
```

**Pros:** Memory efficient, cache-friendly  
**Cons:** Fixed size, manual memory management

### 4.2 Dictionary of Lists (Python)

```python
# Vertex ID maps to list of neighbors
adjacency_list = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}
```

**Pros:** Dynamic, easy to use, readable  
**Cons:** Higher memory overhead than C

### 4.3 Hash Table of Lists (This Project)

```python
# Each vertex stored separately in SimpleDB
db.set("adj:A", json.dumps(["B", "C"]))
db.set("adj:B", json.dumps(["D"]))
db.set("adj:C", json.dumps(["D"]))
db.set("adj:D", json.dumps([]))
```

**Pros:** O(1) lookup, scalable, persistent  
**Cons:** Serialization overhead

---

## 5. Practical Examples

### Example 1: Social Network

**Scenario:** Who follows whom on Twitter

```
Alice follows: Bob, Charlie
Bob follows: Diana
Charlie follows: Bob, Diana
Diana follows: Alice

Adjacency List (Directed):
Alice   → [Bob, Charlie]
Bob     → [Diana]
Charlie → [Bob, Diana]
Diana   → [Alice]
```

**Queries:**
- Who does Alice follow? → `adjacency_list['Alice']` = [Bob, Charlie]
- Who follows Bob? → Search all lists for 'Bob' = [Alice, Charlie]
- Does Alice follow Diana? → 'Diana' in adjacency_list['Alice'] = False

### Example 2: Road Network

**Scenario:** Cities connected by roads (undirected, weighted)

```
NYC ─────── Philadelphia (95 miles)
 │              │
 │ 215          │ 140
 │              │
Boston      Washington

Adjacency List:
NYC          → [(Philadelphia, 95), (Boston, 215)]
Philadelphia → [(NYC, 95), (Washington, 140)]
Boston       → [(NYC, 215)]
Washington   → [(Philadelphia, 140)]
```

**Queries:**
- Cities directly connected to NYC? → [Philadelphia, Boston]
- Distance from NYC to Philadelphia? → 95 miles
- Can you drive from Boston to Washington? → Use graph traversal

### Example 3: Course Prerequisites

**Scenario:** What courses must be taken before others? (Directed, acyclic)

```
Intro_CS → [Data_Structures]
Data_Structures → [Algorithms, Databases]
Algorithms → [Advanced_Algorithms]
Databases → [Big_Data]
Advanced_Algorithms → []
Big_Data → []

Adjacency List:
Intro_CS            → [Data_Structures]
Data_Structures     → [Algorithms, Databases]
Algorithms          → [Advanced_Algorithms]
Databases           → [Big_Data]
Advanced_Algorithms → []
Big_Data            → []
```

**Queries:**
- What can I take after Data_Structures? → [Algorithms, Databases]
- What are all prerequisites for Big_Data? → Reverse traversal
- Course order? → Topological sort

### Example 4: Web Pages and Links

**Scenario:** Which pages link to which? (Directed)

```
index.html → [about.html, products.html, contact.html]
about.html → [team.html, history.html]
products.html → [product1.html, product2.html]
contact.html → []
team.html → [contact.html]
history.html → []
product1.html → [cart.html]
product2.html → [cart.html]
cart.html → [checkout.html]
checkout.html → [confirmation.html]
confirmation.html → []

Adjacency List (simplified):
index    → [about, products, contact]
about    → [team, history]
products → [product1, product2]
team     → [contact]
product1 → [cart]
product2 → [cart]
cart     → [checkout]
checkout → [confirmation]
```

**Queries:**
- How many clicks from index to confirmation? → Shortest path (BFS)
- Which pages link to cart? → Reverse search
- All paths from index to confirmation? → DFS with backtracking

### Example 5: File System Dependencies

**Scenario:** Which files import which? (Directed)

```
main.py → [utils.py, db.py, graph.py]
utils.py → [config.py]
db.py → [config.py]
graph.py → [db.py, utils.py]
config.py → []

Adjacency List:
main.py  → [utils.py, db.py, graph.py]
utils.py → [config.py]
db.py    → [config.py]
graph.py → [db.py, utils.py]
config.py → []
```

**Queries:**
- What does main.py depend on? → Direct: [utils, db, graph]
- What depends on config.py? → Reverse: [utils, db]
- Compilation order? → Topological sort (reverse)

---

## 6. Time and Space Complexity

### 6.1 Space Complexity

**For graph with V vertices and E edges:**

```
Adjacency List: O(V + E)

Example:
V = 5 vertices (A, B, C, D, E)
E = 6 edges

Storage needed:
- 5 vertex entries
- 6 edge references
Total: 11 items

In memory:
- Array of V pointers: V × pointer_size
- E edge structures: E × edge_size
Total: O(V + E)
```

### 6.2 Time Complexity

| Operation | Adjacency List | Notes |
|-----------|----------------|-------|
| **Check if edge exists** | O(V) worst | O(degree) average |
| **Add vertex** | O(1) | Add empty list |
| **Add edge** | O(1) | Append to list |
| **Remove vertex** | O(V + E) | Update all lists |
| **Remove edge** | O(V) | Search in one list |
| **Find all neighbors** | O(1) | Return list |
| **Iterate all neighbors** | O(degree) | Proportional to edges |
| **BFS/DFS traversal** | O(V + E) | Visit each vertex/edge once |

### 6.3 Degree

The **degree** of a vertex is the number of edges connected to it.

```
Graph:
A ─ B ─ C
│   │   │
D ─ E ─ F

Degrees:
A: 2 (connected to B, D)
B: 3 (connected to A, C, E)
C: 2 (connected to B, F)
D: 2 (connected to A, E)
E: 3 (connected to B, D, F)
F: 2 (connected to C, E)

Adjacency List sizes:
A → [B, D]           (2 items)
B → [A, C, E]        (3 items)
C → [B, F]           (2 items)
D → [A, E]           (2 items)
E → [B, D, F]        (3 items)
F → [C, E]           (2 items)
```

**Key insight:** List length = vertex degree

---

## 7. Real-World Applications

### 7.1 Social Networks

**Facebook Friends:**
```
Person → [Friend1, Friend2, Friend3, ...]
```

**Use cases:**
- Friend recommendations (friends of friends)
- Shortest connection path (degrees of separation)
- Community detection (clustering)
- Influence propagation

### 7.2 Navigation Systems

**GPS/Maps:**
```
Intersection → [(NextIntersection, Distance), ...]
```

**Use cases:**
- Shortest route (Dijkstra's algorithm)
- Alternative routes
- Traffic-aware routing
- Nearby points of interest

### 7.3 Recommendation Systems

**Amazon "Customers who bought this also bought:"**
```
Product → [RelatedProduct1, RelatedProduct2, ...]
```

**Use cases:**
- Product recommendations
- Similar items
- Frequently bought together
- Cross-selling opportunities

### 7.4 Computer Networks

**Network Topology:**
```
Router → [ConnectedRouter1, ConnectedRouter2, ...]
```

**Use cases:**
- Packet routing
- Network resilience (alternate paths)
- Bandwidth optimization
- Failure detection

### 7.5 Compilers and Build Systems

**Dependency Graph:**
```
SourceFile → [ImportedFile1, ImportedFile2, ...]
```

**Use cases:**
- Build order determination
- Incremental compilation
- Circular dependency detection
- Dead code elimination

---

## 8. Code Examples

### 8.1 Basic Implementation (Python)

```python
class Graph:
    def __init__(self):
        self.adjacency_list = {}
    
    def add_vertex(self, vertex):
        """Add a vertex to the graph"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, from_vertex, to_vertex):
        """Add a directed edge"""
        if from_vertex not in self.adjacency_list:
            self.add_vertex(from_vertex)
        if to_vertex not in self.adjacency_list:
            self.add_vertex(to_vertex)
        
        self.adjacency_list[from_vertex].append(to_vertex)
    
    def get_neighbors(self, vertex):
        """Get all neighbors of a vertex"""
        return self.adjacency_list.get(vertex, [])
    
    def print_graph(self):
        """Print adjacency list representation"""
        for vertex, neighbors in self.adjacency_list.items():
            print(f"{vertex} → {neighbors}")

# Example usage
graph = Graph()
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'D')
graph.add_edge('C', 'D')

graph.print_graph()
# Output:
# A → ['B', 'C']
# B → ['D']
# C → ['D']
# D → []
```

### 8.2 Weighted Graph

```python
class WeightedGraph:
    def __init__(self):
        self.adjacency_list = {}
    
    def add_edge(self, from_vertex, to_vertex, weight):
        """Add weighted edge"""
        if from_vertex not in self.adjacency_list:
            self.adjacency_list[from_vertex] = []
        
        # Store as tuple (neighbor, weight)
        self.adjacency_list[from_vertex].append((to_vertex, weight))
    
    def get_neighbors(self, vertex):
        """Get neighbors with weights"""
        return self.adjacency_list.get(vertex, [])

# Example usage
graph = WeightedGraph()
graph.add_edge('NYC', 'Boston', 215)
graph.add_edge('NYC', 'Philadelphia', 95)
graph.add_edge('Philadelphia', 'Washington', 140)

for city, destinations in graph.adjacency_list.items():
    print(f"{city}:")
    for dest, distance in destinations:
        print(f"  → {dest} ({distance} miles)")

# Output:
# NYC:
#   → Boston (215 miles)
#   → Philadelphia (95 miles)
# Philadelphia:
#   → Washington (140 miles)
```

### 8.3 Undirected Graph

```python
class UndirectedGraph:
    def __init__(self):
        self.adjacency_list = {}
    
    def add_edge(self, vertex1, vertex2):
        """Add undirected edge (both directions)"""
        # Ensure vertices exist
        if vertex1 not in self.adjacency_list:
            self.adjacency_list[vertex1] = []
        if vertex2 not in self.adjacency_list:
            self.adjacency_list[vertex2] = []
        
        # Add both directions
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)
        if vertex1 not in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].append(vertex1)

# Example usage
graph = UndirectedGraph()
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'C')

for vertex, neighbors in graph.adjacency_list.items():
    print(f"{vertex} ─ {neighbors}")

# Output:
# A ─ ['B', 'C']
# B ─ ['A', 'C']
# C ─ ['A', 'B']
```

### 8.4 Text Format (This Project)

```python
# Adjacency list text format parser

def parse_adjacency_list(text):
    """
    Parse text format into adjacency list
    
    Format:
    A -> B, C
    B -> D
    C -> D, E
    """
    adjacency_list = {}
    
    for line in text.strip().split('\n'):
        if '->' not in line:
            continue
        
        parts = line.split('->')
        vertex = parts[0].strip()
        
        # Parse neighbors
        neighbors = []
        if len(parts) > 1 and parts[1].strip():
            neighbors = [n.strip() for n in parts[1].split(',')]
        
        adjacency_list[vertex] = neighbors
    
    return adjacency_list

# Example usage
text = """
A -> B, C
B -> D
C -> D, E
D ->
E ->
"""

adj_list = parse_adjacency_list(text)
print(adj_list)
# Output:
# {
#     'A': ['B', 'C'],
#     'B': ['D'],
#     'C': ['D', 'E'],
#     'D': [],
#     'E': []
# }
```

### 8.5 BFS Traversal Using Adjacency List

```python
from collections import deque

def bfs(adjacency_list, start):
    """
    Breadth-First Search using adjacency list
    
    Returns nodes in BFS order
    """
    visited = set()
    queue = deque([start])
    result = []
    
    while queue:
        vertex = queue.popleft()
        
        if vertex in visited:
            continue
        
        visited.add(vertex)
        result.append(vertex)
        
        # Add all neighbors to queue
        for neighbor in adjacency_list.get(vertex, []):
            if neighbor not in visited:
                queue.append(neighbor)
    
    return result

# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

print(bfs(graph, 'A'))
# Output: ['A', 'B', 'C', 'D', 'E', 'F']
```

### 8.6 DFS Traversal Using Adjacency List

```python
def dfs(adjacency_list, start, visited=None):
    """
    Depth-First Search using adjacency list
    
    Returns nodes in DFS order
    """
    if visited is None:
        visited = set()
    
    result = []
    
    if start in visited:
        return result
    
    visited.add(start)
    result.append(start)
    
    # Recursively visit neighbors
    for neighbor in adjacency_list.get(start, []):
        result.extend(dfs(adjacency_list, neighbor, visited))
    
    return result

# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

print(dfs(graph, 'A'))
# Output: ['A', 'B', 'D', 'E', 'F', 'C']
```

---

## 9. Advanced Topics

### 9.1 Sparse vs Dense Graphs

**Sparse Graph** (Adjacency list is better):
```
100 vertices, 150 edges

Adjacency List: O(100 + 150) = 250 items
Adjacency Matrix: O(100²) = 10,000 items

Memory savings: 97.5%
```

**Dense Graph** (Adjacency matrix might be better):
```
100 vertices, 9,000 edges

Adjacency List: O(100 + 9000) = 9,100 items
Adjacency Matrix: O(100²) = 10,000 items

Matrix only 10% larger, but faster edge lookups
```

### 9.2 Space Optimization

**Technique 1: Shared storage for undirected graphs**
```python
# Instead of storing both A→B and B→A
# Store only smaller ID → larger ID
def add_undirected_edge(a, b):
    if a < b:
        adjacency_list[a].append(b)
    else:
        adjacency_list[b].append(a)
```

**Technique 2: Bit vectors for small vertex IDs**
```python
# If vertex IDs are 0-63, use a 64-bit integer
# Each bit represents an edge
adjacency_bitset = {
    0: 0b000110,  # Connected to vertices 1 and 2
    1: 0b001000,  # Connected to vertex 3
    # ...
}
```

### 9.3 Common Pitfalls

❌ **Forgetting to check if vertex exists**
```python
# Wrong:
neighbors = adjacency_list[vertex]  # KeyError if vertex doesn't exist

# Right:
neighbors = adjacency_list.get(vertex, [])
```

❌ **Not handling undirected edges properly**
```python
# Wrong (only one direction):
adjacency_list['A'].append('B')

# Right (both directions):
adjacency_list['A'].append('B')
adjacency_list['B'].append('A')
```

❌ **Modifying list during iteration**
```python
# Wrong:
for neighbor in adjacency_list[vertex]:
    adjacency_list[vertex].remove(neighbor)  # Skips elements!

# Right:
adjacency_list[vertex] = []  # Clear the list
# Or:
adjacency_list[vertex] = [n for n in adjacency_list[vertex] if condition]
```

---

## 10. Summary

### Key Takeaways

1. **Adjacency lists are the most common graph representation** for real-world applications
2. **Space efficient** for sparse graphs (most real-world graphs are sparse)
3. **Fast neighbor iteration** - critical for graph algorithms
4. **Flexible** - works for directed, undirected, weighted graphs
5. **Scales well** - used in production systems with millions of vertices

### When to Use

✅ Social networks  
✅ Road maps / navigation  
✅ Web page links  
✅ Dependency graphs  
✅ Recommendation systems  
✅ Any sparse graph  

### Best Practices

1. Use dictionary/hash map for O(1) vertex lookup
2. Store edge weights as tuples: (neighbor, weight)
3. Check vertex existence before accessing
4. For undirected graphs, maintain both directions
5. Consider space/time trade-offs for your use case

---

**References:**
- Introduction to Algorithms (CLRS) - Chapter 22
- Algorithm Design Manual (Skiena) - Chapter 5
- Graph Theory by Diestel
- Our implementation: `graph_db.py` (uses SimpleDB for storage)

**Related Documentation:**
- `GRAPH_DB_GUIDE.md` - Full API reference
- `ARCHITECTURE.md` - System design details
- `graph_examples.py` - Practical examples

**Version**: 1.0  
**Last Updated**: November 17, 2025
