# Angular Graph Database UI - Technical Specification

## Overview
Modern Angular web application for graph database visualization and management, connecting to the existing Flask REST API backend.

---

## Technology Stack

### Frontend
- **Framework**: Angular 17+ (latest stable)
- **Language**: TypeScript 5+
- **Build Tool**: Angular CLI
- **Package Manager**: npm
- **Graph Visualization**: 
  - D3.js (force-directed graphs)
  - Alternative: Cytoscape.js or vis-network
- **UI Components**: Angular Material
- **HTTP Client**: Angular HttpClient (RxJS)
- **State Management**: RxJS BehaviorSubjects / NgRx (optional)
- **Routing**: Angular Router

### Backend (Existing)
- **API**: Flask REST API at http://127.0.0.1:5000
- **Endpoints**: Already implemented (see API section below)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Angular Application                      │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Core Module                              │ │
│  │  - HTTP Interceptors                                  │ │
│  │  - Error Handling                                     │ │
│  │  - Authentication (future)                            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  Graph Module │  │ Chat Module  │  │  Admin Module   │ │
│  │               │  │              │  │                 │ │
│  │ - Visualization│  │ - NLP Input │  │ - Stats View   │ │
│  │ - Node Editor │  │ - Query Parser│  │ - Logs View    │ │
│  │ - Edge Editor │  │ - Results    │  │ - Import/Export│ │
│  └───────────────┘  └──────────────┘  └─────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Shared Services                          │ │
│  │  - GraphService  - ChatService  - AdminService       │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP
┌─────────────────────────────────────────────────────────────┐
│              Flask REST API (Port 5000)                     │
│  /api/graph/nodes | /api/graph/edges | /api/graph/stats   │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
angular-graph-ui/
├── src/
│   ├── app/
│   │   ├── core/                    # Singleton services, guards, interceptors
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts
│   │   │   │   └── error-handler.service.ts
│   │   │   ├── interceptors/
│   │   │   │   └── http-error.interceptor.ts
│   │   │   └── core.module.ts
│   │   │
│   │   ├── shared/                  # Shared components, directives, pipes
│   │   │   ├── components/
│   │   │   │   ├── loading-spinner/
│   │   │   │   └── error-message/
│   │   │   ├── models/
│   │   │   │   ├── node.model.ts
│   │   │   │   ├── edge.model.ts
│   │   │   │   └── graph-stats.model.ts
│   │   │   └── shared.module.ts
│   │   │
│   │   ├── features/
│   │   │   ├── graph/               # Graph visualization module
│   │   │   │   ├── components/
│   │   │   │   │   ├── graph-canvas/
│   │   │   │   │   ├── node-list/
│   │   │   │   │   ├── edge-list/
│   │   │   │   │   ├── node-detail/
│   │   │   │   │   └── edge-detail/
│   │   │   │   ├── services/
│   │   │   │   │   └── graph.service.ts
│   │   │   │   ├── graph-routing.module.ts
│   │   │   │   └── graph.module.ts
│   │   │   │
│   │   │   ├── chat/                # NLP chat interface
│   │   │   │   ├── components/
│   │   │   │   │   ├── chat-window/
│   │   │   │   │   ├── message-bubble/
│   │   │   │   │   └── query-input/
│   │   │   │   ├── services/
│   │   │   │   │   ├── chat.service.ts
│   │   │   │   │   └── nlp-parser.service.ts
│   │   │   │   ├── chat-routing.module.ts
│   │   │   │   └── chat.module.ts
│   │   │   │
│   │   │   └── admin/               # Admin/stats module
│   │   │       ├── components/
│   │   │       │   ├── stats-dashboard/
│   │   │       │   └── import-export/
│   │   │       ├── services/
│   │   │       │   └── admin.service.ts
│   │   │       ├── admin-routing.module.ts
│   │   │       └── admin.module.ts
│   │   │
│   │   ├── app-routing.module.ts
│   │   ├── app.component.ts
│   │   └── app.module.ts
│   │
│   ├── assets/
│   ├── environments/
│   │   ├── environment.ts           # API base URL configuration
│   │   └── environment.prod.ts
│   ├── styles.scss
│   └── index.html
│
├── angular.json
├── package.json
├── tsconfig.json
└── README.md
```

---

## Data Models

### TypeScript Interfaces

```typescript
// node.model.ts
export interface Node {
  id: string;
  data: {
    role?: string;
    team?: string;
    name?: string;
    [key: string]: any;
  };
}

// edge.model.ts
export interface Edge {
  from: string;
  to: string;
  weight?: number;
}

// graph-stats.model.ts
export interface GraphStats {
  node_count: number;
  edge_count: number;
  directed: boolean;
  weighted: boolean;
}

// graph-data.model.ts
export interface GraphData {
  nodes: Node[];
  edges: Edge[];
}

// api-response.model.ts
export interface ApiResponse<T> {
  success?: boolean;
  message?: string;
  error?: string;
  data?: T;
}
```

---

## API Integration

### Base API Service

```typescript
// core/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl; // http://127.0.0.1:5000

  constructor(private http: HttpClient) {}

  get<T>(endpoint: string): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}${endpoint}`);
  }

  post<T>(endpoint: string, data: any): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}${endpoint}`, data);
  }

  put<T>(endpoint: string, data: any): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}${endpoint}`, data);
  }

  delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}${endpoint}`);
  }
}
```

### Graph Service

```typescript
// features/graph/services/graph.service.ts
import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { Node, Edge, GraphStats, GraphData } from '../../../shared/models';

@Injectable({
  providedIn: 'root'
})
export class GraphService {
  private graphData$ = new BehaviorSubject<GraphData>({ nodes: [], edges: [] });
  
  constructor(private api: ApiService) {}

  // Observable for components to subscribe to
  getGraphData(): Observable<GraphData> {
    return this.graphData$.asObservable();
  }

  // Fetch all nodes
  loadNodes(): Observable<{ nodes: Node[] }> {
    return this.api.get<{ nodes: Node[] }>('/api/graph/nodes').pipe(
      tap(data => this.updateNodes(data.nodes))
    );
  }

  // Fetch visualization data (nodes + edges)
  loadVisualization(): Observable<GraphData> {
    return this.api.get<GraphData>('/api/graph/visualization').pipe(
      tap(data => this.graphData$.next(data))
    );
  }

  // Get stats
  getStats(): Observable<GraphStats> {
    return this.api.get<GraphStats>('/api/graph/stats');
  }

  // Add node
  addNode(id: string, data: any): Observable<any> {
    return this.api.post('/api/graph/node', { id, data }).pipe(
      tap(() => this.loadVisualization().subscribe())
    );
  }

  // Update node
  updateNode(id: string, data: any): Observable<any> {
    return this.api.put(`/api/graph/node/${id}`, { data }).pipe(
      tap(() => this.loadVisualization().subscribe())
    );
  }

  // Delete node
  deleteNode(id: string): Observable<any> {
    return this.api.delete(`/api/graph/node/${id}`).pipe(
      tap(() => this.loadVisualization().subscribe())
    );
  }

  // Add edge
  addEdge(from: string, to: string, weight?: number): Observable<any> {
    return this.api.post('/api/graph/edge', { from, to, weight }).pipe(
      tap(() => this.loadVisualization().subscribe())
    );
  }

  // Delete edge
  deleteEdge(from: string, to: string): Observable<any> {
    return this.api.delete(`/api/graph/edge?from=${from}&to=${to}`).pipe(
      tap(() => this.loadVisualization().subscribe())
    );
  }

  // Search nodes
  searchNodes(predicate: any): Observable<{ results: Node[] }> {
    return this.api.post<{ results: Node[] }>('/api/graph/search', { predicate });
  }

  // Find shortest path
  shortestPath(start: string, target: string): Observable<any> {
    return this.api.post('/api/graph/shortest_path', { start, target });
  }

  // BFS traversal
  bfs(start: string): Observable<any> {
    return this.api.post('/api/graph/bfs', { start });
  }

  private updateNodes(nodes: Node[]): void {
    const current = this.graphData$.value;
    this.graphData$.next({ ...current, nodes });
  }
}
```

---

## Component Details

### 1. Graph Canvas Component (D3.js Visualization)

**Purpose**: Interactive force-directed graph visualization

**Features**:
- Drag nodes to reposition
- Click nodes to view/edit details
- Hover to highlight connections
- Zoom and pan
- Auto-layout with force simulation
- Color-coded by node properties (team, role, etc.)

**Template**: `graph-canvas.component.html`
```html
<div class="graph-container">
  <svg #graphSvg class="graph-svg"></svg>
  
  <div class="graph-controls">
    <button mat-icon-button (click)="resetZoom()">
      <mat-icon>zoom_out_map</mat-icon>
    </button>
    <button mat-icon-button (click)="centerGraph()">
      <mat-icon>center_focus_strong</mat-icon>
    </button>
  </div>
</div>
```

**Component**: `graph-canvas.component.ts`
```typescript
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as d3 from 'd3';
import { GraphService } from '../../services/graph.service';

@Component({
  selector: 'app-graph-canvas',
  templateUrl: './graph-canvas.component.html',
  styleUrls: ['./graph-canvas.component.scss']
})
export class GraphCanvasComponent implements OnInit {
  @ViewChild('graphSvg', { static: true }) svgRef!: ElementRef;
  
  private svg: any;
  private simulation: any;
  
  constructor(private graphService: GraphService) {}
  
  ngOnInit(): void {
    this.initializeSvg();
    this.loadAndRenderGraph();
  }
  
  private initializeSvg(): void {
    // D3.js setup code
  }
  
  private loadAndRenderGraph(): void {
    this.graphService.getGraphData().subscribe(data => {
      this.renderGraph(data);
    });
  }
  
  private renderGraph(data: GraphData): void {
    // D3.js force simulation and rendering
  }
}
```

---

### 2. Chat Window Component

**Purpose**: Natural language query interface

**Features**:
- Message history
- Typing indicator
- Query suggestions
- Quick action buttons
- Syntax highlighting for results

**Template**: `chat-window.component.html`
```html
<mat-card class="chat-card">
  <mat-card-header>
    <mat-card-title>Graph Query Assistant</mat-card-title>
  </mat-card-header>
  
  <mat-card-content>
    <div class="messages-container" #messagesContainer>
      <app-message-bubble 
        *ngFor="let msg of messages"
        [message]="msg">
      </app-message-bubble>
      
      <div *ngIf="isTyping" class="typing-indicator">
        <mat-spinner diameter="20"></mat-spinner>
      </div>
    </div>
  </mat-card-content>
  
  <mat-card-actions>
    <app-query-input (querySubmitted)="handleQuery($event)"></app-query-input>
    
    <div class="quick-actions">
      <button mat-button (click)="quickQuery('show all nodes')">
        All Nodes
      </button>
      <button mat-button (click)="quickQuery('show stats')">
        Stats
      </button>
    </div>
  </mat-card-actions>
</mat-card>
```

---

### 3. Node List Component

**Purpose**: Tabular view of all nodes with filtering

**Features**:
- Material Data Table
- Search/filter
- Sort by columns
- Pagination
- Click to edit
- Bulk actions

**Template**: `node-list.component.html`
```html
<mat-card>
  <mat-card-header>
    <mat-card-title>Nodes</mat-card-title>
    <button mat-icon-button (click)="addNode()">
      <mat-icon>add</mat-icon>
    </button>
  </mat-card-header>
  
  <mat-card-content>
    <mat-form-field>
      <input matInput (keyup)="applyFilter($event)" placeholder="Filter">
    </mat-form-field>
    
    <table mat-table [dataSource]="dataSource" matSort>
      <ng-container matColumnDef="id">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>ID</th>
        <td mat-cell *matCellDef="let node">{{node.id}}</td>
      </ng-container>
      
      <ng-container matColumnDef="role">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>Role</th>
        <td mat-cell *matCellDef="let node">{{node.data.role}}</td>
      </ng-container>
      
      <ng-container matColumnDef="team">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>Team</th>
        <td mat-cell *matCellDef="let node">{{node.data.team}}</td>
      </ng-container>
      
      <ng-container matColumnDef="actions">
        <th mat-header-cell *matHeaderCellDef>Actions</th>
        <td mat-cell *matCellDef="let node">
          <button mat-icon-button (click)="editNode(node)">
            <mat-icon>edit</mat-icon>
          </button>
          <button mat-icon-button (click)="deleteNode(node.id)">
            <mat-icon>delete</mat-icon>
          </button>
        </td>
      </ng-container>
      
      <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
      <tr mat-row *matRowDef="let row; columns: displayedColumns"></tr>
    </table>
    
    <mat-paginator [pageSizeOptions]="[10, 25, 50]"></mat-paginator>
  </mat-card-content>
</mat-card>
```

---

## Routing Configuration

```typescript
// app-routing.module.ts
const routes: Routes = [
  { path: '', redirectTo: '/graph', pathMatch: 'full' },
  { 
    path: 'graph', 
    loadChildren: () => import('./features/graph/graph.module').then(m => m.GraphModule)
  },
  { 
    path: 'chat', 
    loadChildren: () => import('./features/chat/chat.module').then(m => m.ChatModule)
  },
  { 
    path: 'admin', 
    loadChildren: () => import('./features/admin/admin.module').then(m => m.AdminModule)
  },
  { path: '**', redirectTo: '/graph' }
];
```

---

## Environment Configuration

```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:5000',
  apiTimeout: 30000
};

// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://your-production-api.com',
  apiTimeout: 30000
};
```

---

## Styling with Angular Material

### Theme Configuration

```scss
// styles.scss
@import '@angular/material/prebuilt-themes/indigo-pink.css';

// Custom theme
@use '@angular/material' as mat;

$primary: mat.define-palette(mat.$indigo-palette);
$accent: mat.define-palette(mat.$pink-palette);
$warn: mat.define-palette(mat.$red-palette);

$theme: mat.define-light-theme((
  color: (
    primary: $primary,
    accent: $accent,
    warn: $warn,
  )
));

@include mat.all-component-themes($theme);
```

---

## Installation & Setup Steps

### Prerequisites
```bash
# Install Node.js (18+ recommended)
# Install Angular CLI
npm install -g @angular/cli
```

### Create Project
```bash
cd /Users/gp/c-work/getting-started/symmetrical-robot

# Create Angular app
ng new angular-graph-ui --routing --style=scss

cd angular-graph-ui

# Install dependencies
npm install @angular/material @angular/cdk
npm install d3 @types/d3
npm install rxjs
```

### Install Angular Material
```bash
ng add @angular/material
# Choose Indigo/Pink theme
# Enable typography: Yes
# Enable animations: Yes
```

### Generate Modules & Components
```bash
# Core module
ng generate module core

# Shared module
ng generate module shared

# Feature modules
ng generate module features/graph --routing
ng generate module features/chat --routing
ng generate module features/admin --routing

# Services
ng generate service core/services/api
ng generate service features/graph/services/graph
ng generate service features/chat/services/chat

# Components
ng generate component features/graph/components/graph-canvas
ng generate component features/graph/components/node-list
ng generate component features/graph/components/edge-list
ng generate component features/chat/components/chat-window
ng generate component features/chat/components/message-bubble
```

---

## Development Workflow

### Run Development Server
```bash
# Start Angular dev server
ng serve

# Open browser to http://localhost:4200
# Backend should be running on http://127.0.0.1:5000
```

### Build for Production
```bash
ng build --configuration production

# Output in dist/angular-graph-ui/
```

### CORS Configuration (Flask Backend)

Add to `graph_web_ui.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Angular development
```

---

## Testing Strategy

### Unit Tests
- Services: Test API calls with HttpClientTestingModule
- Components: Test rendering and user interactions
- Coverage target: 80%+

### E2E Tests
- Protractor or Cypress
- Test full user workflows

```bash
# Run unit tests
ng test

# Run e2e tests
ng e2e
```

---

## Performance Optimization

1. **Lazy Loading**: Load feature modules on demand
2. **OnPush Change Detection**: Reduce unnecessary checks
3. **Virtual Scrolling**: For large node lists
4. **Debounce**: Search inputs and API calls
5. **Caching**: Store frequently accessed data in service
6. **AOT Compilation**: Enabled by default in production

---

## Deployment Options

### Option 1: Serve from Flask
- Build Angular app
- Copy `dist/` to Flask `static/` folder
- Serve index.html from Flask

### Option 2: Separate Deployment
- Angular on Netlify/Vercel
- Flask API on separate server
- Configure CORS properly

---

## Next Steps

1. ✅ Review this specification
2. Create Angular project structure
3. Implement core services (API, Graph)
4. Build graph visualization component (D3.js)
5. Implement CRUD operations
6. Add chat interface
7. Styling with Angular Material
8. Testing
9. Production build

---

## Questions to Address

1. **Graph Library**: D3.js, Cytoscape.js, or vis-network?
2. **State Management**: Simple BehaviorSubjects or NgRx?
3. **Authentication**: Needed for production?
4. **Real-time Updates**: WebSocket integration?
5. **Mobile Responsive**: Touch gestures for graph?

---

## Estimated Timeline

- **Setup & Core (Week 1)**: Project setup, services, basic routing
- **Graph Module (Week 2)**: Visualization, node/edge CRUD
- **Chat Module (Week 3)**: NLP interface, query parsing
- **Polish & Testing (Week 4)**: Material design, testing, optimization

---

## Resources

- [Angular Documentation](https://angular.io/docs)
- [Angular Material](https://material.angular.io/)
- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [RxJS Documentation](https://rxjs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
