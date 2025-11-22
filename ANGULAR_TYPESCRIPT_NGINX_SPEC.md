# Technical Specification: Angular TypeScript Web Interface on Nginx

## 1. Overview

This document specifies the architecture and implementation of a modern Angular/TypeScript web interface for the Graph Database API, deployed and served by Nginx.

### 1.1 Purpose
Provide a responsive, production-grade web interface using Angular framework with TypeScript for type safety, running on Nginx reverse proxy and static file server.

### 1.2 Scope
- Angular 18+ SPA (Single Page Application)
- TypeScript strict mode implementation
- Graph visualization and interaction
- Real-time API communication via JSON-RPC
- Nginx configuration for production deployment
- Build optimization and performance
- Responsive design with Angular Material

---

## 2. Architecture

### 2.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Client Browser                            │
│  (Chrome, Firefox, Safari, Edge - ES2020+ Compatible)        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ├─► HTTP/HTTPS
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  Nginx Reverse Proxy                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Static File Server                                   │  │
│  │  - index.html                                         │  │
│  │  - JavaScript bundles (main.*.js)                     │  │
│  │  - CSS bundles (styles.*.css)                         │  │
│  │  - Assets (images, fonts)                             │  │
│  │  - Source maps (development)                          │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  API Proxy                                            │  │
│  │  - /api/* → Flask Backend (http://localhost:5000)    │  │
│  │  - Load balancing (optional)                          │  │
│  │  - Caching headers                                    │  │
│  │  - CORS headers                                       │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────▼────────────────┐      ┌────────────▼──────────┐
│  Static Assets         │      │  Flask Backend API    │
│  (dist/ folder)        │      │  (http:5000)          │
│                        │      │                       │
│  - Angular bundles     │      │  - JSON-RPC methods   │
│  - Vendor libraries    │      │  - Graph DB           │
│  - App styles          │      │  - Business logic     │
│  - Images & fonts      │      │                       │
└────────────────────────┘      └───────────────────────┘
```

### 2.2 Component Breakdown

#### Nginx Server
- Static file serving for SPA
- Reverse proxy for API requests
- SSL/TLS termination
- Request routing and caching
- Compression (gzip)
- CORS and security headers

#### Angular Application
- Component-based architecture
- TypeScript strict mode
- Reactive Forms with RxJS
- Services for API communication
- State management
- Error handling and logging

#### Build Pipeline
- Angular CLI build process
- AOT (Ahead-of-Time) compilation
- Tree shaking and minification
- Source map generation
- Production optimization

---

## 3. Project Structure

### 3.1 Angular Project Layout

```
angular-graph-ui/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts
│   │   │   │   ├── graph.service.ts
│   │   │   │   ├── notification.service.ts
│   │   │   │   └── auth.service.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   ├── error.interceptor.ts
│   │   │   │   └── logging.interceptor.ts
│   │   │   └── guards/
│   │   │       └── auth.guard.ts
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── navbar/
│   │   │   │   ├── sidebar/
│   │   │   │   └── loading-spinner/
│   │   │   ├── models/
│   │   │   │   ├── graph.models.ts
│   │   │   │   ├── api.models.ts
│   │   │   │   └── error.models.ts
│   │   │   └── pipes/
│   │   │       └── date-format.pipe.ts
│   │   ├── features/
│   │   │   ├── graph/
│   │   │   │   ├── graph.module.ts
│   │   │   │   ├── components/
│   │   │   │   │   ├── graph-canvas/
│   │   │   │   │   ├── node-editor/
│   │   │   │   │   ├── edge-editor/
│   │   │   │   │   └── traversal-panel/
│   │   │   │   └── graph.component.ts
│   │   │   ├── explorer/
│   │   │   │   ├── explorer.module.ts
│   │   │   │   ├── components/
│   │   │   │   └── explorer.component.ts
│   │   │   └── dashboard/
│   │   │       ├── dashboard.module.ts
│   │   │       └── dashboard.component.ts
│   │   ├── store/ (NgRx)
│   │   │   ├── actions/
│   │   │   ├── reducers/
│   │   │   ├── selectors/
│   │   │   └── effects/
│   │   ├── app.component.ts
│   │   ├── app.routing.module.ts
│   │   └── app.module.ts
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   ├── styles/
│   │   ├── global.scss
│   │   ├── variables.scss
│   │   ├── mixins.scss
│   │   └── themes/
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   ├── index.html
│   └── main.ts
├── angular.json
├── tsconfig.json
├── tsconfig.app.json
├── package.json
├── package-lock.json
└── nginx.conf

```

### 3.2 Build Output Structure

```
dist/
├── index.html
├── main.[hash].js
├── polyfills.[hash].js
├── runtime.[hash].js
├── styles.[hash].css
├── assets/
│   ├── images/
│   ├── icons/
│   └── fonts/
└── 3rdpartylicenses.txt
```

---

## 4. Angular Application Architecture

### 4.1 Module Structure

#### App Module (app.module.ts)
```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routing.module';

// Material
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';

// Core Services
import { ApiService } from './core/services/api.service';
import { GraphService } from './core/services/graph.service';

// Interceptors
import { AuthInterceptor } from './core/interceptors/auth.interceptor';
import { ErrorInterceptor } from './core/interceptors/error.interceptor';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    MatSidenavModule,
    MatToolbarModule
  ],
  providers: [
    ApiService,
    GraphService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

### 4.2 Core Services

#### API Service (api.service.ts)
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { tap, catchError, timeout } from 'rxjs/operators';
import { environment } from '@env/environment';

interface JsonRpcRequest {
  jsonrpc: '2.0';
  method: string;
  params: Record<string, any>;
  id: number;
}

interface JsonRpcResponse<T> {
  jsonrpc: '2.0';
  result?: T;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
  id: number;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private requestId = 0;
  private apiUrl = `${environment.apiUrl}/api/rpc`;

  constructor(private http: HttpClient) {}

  /**
   * Execute a JSON-RPC method
   */
  call<T = any>(
    method: string,
    params: Record<string, any> = {}
  ): Observable<T> {
    const id = ++this.requestId;
    const request: JsonRpcRequest = {
      jsonrpc: '2.0',
      method,
      params,
      id
    };

    return this.http.post<JsonRpcResponse<T>>(this.apiUrl, request).pipe(
      timeout(30000),
      tap(response => {
        if (response.error) {
          throw new Error(`[${response.error.code}] ${response.error.message}`);
        }
      }),
      catchError(error => {
        console.error('API Error:', error);
        throw error;
      })
    );
  }

  /**
   * Batch JSON-RPC requests
   */
  batch<T = any>(requests: Array<{
    method: string;
    params?: Record<string, any>;
  }>): Observable<T[]> {
    const batchRequests = requests.map((req, index) => ({
      jsonrpc: '2.0',
      method: req.method,
      params: req.params || {},
      id: ++this.requestId
    }));

    return this.http.post<JsonRpcResponse<T>[]>(this.apiUrl, batchRequests);
  }

  /**
   * Health check
   */
  healthCheck(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/health`).pipe(
      timeout(5000)
    );
  }
}
```

#### Graph Service (graph.service.ts)
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';

interface Node {
  id: string;
  label: string;
  data: Record<string, any>;
  x?: number;
  y?: number;
}

interface Edge {
  source: string;
  target: string;
  weight?: number;
  directed?: boolean;
}

interface Graph {
  id: string;
  nodes: Node[];
  edges: Edge[];
  directed: boolean;
  weighted: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class GraphService {
  private currentGraph$ = new BehaviorSubject<Graph | null>(null);
  private selectedNode$ = new BehaviorSubject<Node | null>(null);

  constructor(private apiService: ApiService) {}

  /**
   * Create a new graph
   */
  createGraph(directed: boolean = true, weighted: boolean = false): Observable<Graph> {
    return this.apiService.call('graph.create', { directed, weighted }).pipe(
      map(result => ({
        ...result,
        nodes: [],
        edges: []
      }))
    );
  }

  /**
   * Add a node to the graph
   */
  addNode(graphId: string, nodeId: string, data: Record<string, any> = {}): Observable<any> {
    return this.apiService.call('graph.add_node', {
      graph_id: graphId,
      node_id: nodeId,
      data
    });
  }

  /**
   * Add an edge to the graph
   */
  addEdge(
    graphId: string,
    source: string,
    target: string,
    weight: number = 1,
    directed: boolean = true
  ): Observable<any> {
    return this.apiService.call('graph.add_edge', {
      graph_id: graphId,
      source,
      target,
      weight,
      directed
    });
  }

  /**
   * Get node information
   */
  getNode(graphId: string, nodeId: string): Observable<Node> {
    return this.apiService.call('graph.get_node', {
      graph_id: graphId,
      node_id: nodeId
    });
  }

  /**
   * Delete a node
   */
  deleteNode(graphId: string, nodeId: string): Observable<any> {
    return this.apiService.call('graph.delete_node', {
      graph_id: graphId,
      node_id: nodeId
    });
  }

  /**
   * Delete an edge
   */
  deleteEdge(graphId: string, source: string, target: string): Observable<any> {
    return this.apiService.call('graph.delete_edge', {
      graph_id: graphId,
      source,
      target
    });
  }

  /**
   * BFS traversal
   */
  bfsTraversal(graphId: string, startNode: string, maxDepth: number = 10): Observable<any> {
    return this.apiService.call('graph.bfs', {
      graph_id: graphId,
      start_node: startNode,
      max_depth: maxDepth
    });
  }

  /**
   * DFS traversal
   */
  dfsTraversal(graphId: string, startNode: string, maxDepth: number = 10): Observable<any> {
    return this.apiService.call('graph.dfs', {
      graph_id: graphId,
      start_node: startNode,
      max_depth: maxDepth
    });
  }

  /**
   * Find shortest path
   */
  shortestPath(graphId: string, source: string, target: string): Observable<any> {
    return this.apiService.call('graph.shortest_path', {
      graph_id: graphId,
      source,
      target
    });
  }

  getCurrentGraph(): Observable<Graph | null> {
    return this.currentGraph$.asObservable();
  }

  setCurrentGraph(graph: Graph): void {
    this.currentGraph$.next(graph);
  }

  getSelectedNode(): Observable<Node | null> {
    return this.selectedNode$.asObservable();
  }

  selectNode(node: Node | null): void {
    this.selectedNode$.next(node);
  }
}
```

### 4.3 TypeScript Configuration

#### tsconfig.json
```json
{
  "compileOnSave": false,
  "compilerOptions": {
    "baseUrl": "./",
    "outDir": "./dist/out-tsc",
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "sourceMap": true,
    "declaration": false,
    "downlevelIteration": true,
    "experimentalDecorators": true,
    "moduleResolution": "node",
    "importHelpers": true,
    "target": "ES2020",
    "module": "ES2020",
    "useDefineForClassFields": false,
    "lib": ["ES2020", "dom"],
    "paths": {
      "@env/*": ["src/environments/*"],
      "@core/*": ["src/app/core/*"],
      "@shared/*": ["src/app/shared/*"],
      "@features/*": ["src/app/features/*"]
    }
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}
```

---

## 5. Nginx Configuration

### 5.1 Production Nginx Configuration

#### nginx.conf
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss 
               application/rss+xml font/truetype font/opentype 
               application/vnd.ms-fontobject image/svg+xml;
    gzip_disable "msie6";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=50r/s;

    # Upstream backend
    upstream api_backend {
        server localhost:5000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    # HTTP redirect to HTTPS
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name graph-ui.example.com;

        # SSL certificates (use Let's Encrypt in production)
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        ssl_stapling on;
        ssl_stapling_verify on;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

        root /var/www/angular-graph-ui/dist;
        index index.html;

        # Cache control for static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 30d;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # Cache busted index.html
        location = /index.html {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
            expires -1;
        }

        # SPA routing: redirect all requests to index.html
        location / {
            try_files $uri $uri/ /index.html;
            add_header Cache-Control "no-cache, no-store, must-revalidate";
        }

        # API proxy
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://api_backend;
            proxy_http_version 1.1;

            # Proxy headers
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";

            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;

            # Buffering
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
            proxy_busy_buffers_size 8k;

            # CORS headers (if not handled by Flask)
            add_header Access-Control-Allow-Origin "*" always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;

            # Handle preflight requests
            if ($request_method = 'OPTIONS') {
                return 204;
            }
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 '{"status": "ok"}';
            add_header Content-Type application/json;
        }

        # Deny access to sensitive files
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }

        location ~ ~$ {
            deny all;
            access_log off;
            log_not_found off;
        }
    }
}
```

### 5.2 Development Nginx Configuration

#### nginx.dev.conf
```nginx
server {
    listen 4200;
    server_name localhost;

    root /path/to/angular-graph-ui/dist;
    index index.html;

    # Development: no caching
    add_header Cache-Control "no-cache, no-store, must-revalidate";

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy to Flask backend
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Allow source maps
    location ~* \.js\.map$ {
        add_header Content-Type application/json;
    }
}
```

---

## 6. Build Configuration

### 6.1 angular.json

```json
{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "angular-graph-ui": {
      "projectType": "application",
      "schematics": {
        "@schematics/angular:component": {
          "style": "scss"
        }
      },
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular/build:browser",
          "options": {
            "outputPath": "dist",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.app.json",
            "inlineStyleLanguage": "scss",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles/global.scss"
            ],
            "scripts": [],
            "vendorChunk": true,
            "extractLicenses": false,
            "sourceMap": true,
            "namedChunks": true
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "500kb",
                  "maximumError": "1mb"
                },
                {
                  "type": "anyComponentStyle",
                  "maximumWarning": "2kb",
                  "maximumError": "4kb"
                }
              ],
              "outputHashing": "all",
              "aot": true,
              "optimization": true,
              "buildOptimizer": true,
              "sourceMap": false,
              "namedChunks": false,
              "extractLicenses": true,
              "vendorChunk": false
            },
            "development": {
              "buildOptimizer": false,
              "optimization": false,
              "vendorChunk": true,
              "extractLicenses": false,
              "sourceMap": true,
              "namedChunks": true
            }
          },
          "defaultConfiguration": "production"
        },
        "serve": {
          "builder": "@angular/build:dev-server",
          "configurations": {
            "production": {
              "buildTarget": "angular-graph-ui:build:production"
            },
            "development": {
              "buildTarget": "angular-graph-ui:build:development"
            }
          },
          "defaultConfiguration": "development"
        },
        "lint": {
          "builder": "@angular-eslint/builder:lint",
          "options": {
            "lintFilePatterns": [
              "src/**/*.ts",
              "src/**/*.html"
            ]
          }
        }
      }
    }
  }
}
```

### 6.2 package.json

```json
{
  "name": "angular-graph-ui",
  "version": "1.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "build:prod": "ng build --configuration production",
    "watch": "ng build --watch --configuration development",
    "test": "ng test",
    "test:coverage": "ng test --code-coverage",
    "lint": "ng lint",
    "e2e": "ng e2e",
    "format": "prettier --write \"src/**/*.{ts,html,scss}\"",
    "format:check": "prettier --check \"src/**/*.{ts,html,scss}\""
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^18.0.0",
    "@angular/common": "^18.0.0",
    "@angular/compiler": "^18.0.0",
    "@angular/core": "^18.0.0",
    "@angular/forms": "^18.0.0",
    "@angular/material": "^18.0.0",
    "@angular/platform-browser": "^18.0.0",
    "@angular/platform-browser-dynamic": "^18.0.0",
    "@angular/router": "^18.0.0",
    "@ngrx/store": "^18.0.0",
    "@ngrx/effects": "^18.0.0",
    "rxjs": "^7.8.0",
    "tslib": "^2.6.0",
    "zone.js": "^0.14.0",
    "d3": "^7.8.0",
    "vis-network": "^9.1.0"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^18.0.0",
    "@angular/cli": "^18.0.0",
    "@angular/compiler-cli": "^18.0.0",
    "@angular-eslint/builder": "^18.0.0",
    "@angular-eslint/eslint-plugin": "^18.0.0",
    "@angular-eslint/eslint-plugin-template": "^18.0.0",
    "@angular-eslint/schematics": "^18.0.0",
    "@angular-eslint/template-parser": "^18.0.0",
    "@types/d3": "^7.4.0",
    "@types/jasmine": "^5.1.0",
    "@types/node": "^20.0.0",
    "jasmine-core": "^5.1.0",
    "karma": "^6.4.0",
    "karma-chrome-launcher": "^3.2.0",
    "karma-coverage": "^2.2.0",
    "karma-jasmine": "^5.1.0",
    "karma-jasmine-html-reporter": "^2.1.0",
    "prettier": "^3.0.0",
    "typescript": "^5.2.0",
    "typescript-eslint": "^7.0.0"
  }
}
```

---

## 7. Component Examples

### 7.1 Graph Canvas Component

#### graph-canvas.component.ts
```typescript
import { Component, OnInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { GraphService } from '@core/services/graph.service';
import * as d3 from 'd3';

interface D3Node extends d3.SimulationNodeDatum {
  id: string;
  label: string;
}

interface D3Link extends d3.SimulationLinkDatum<D3Node> {
  source: D3Node;
  target: D3Node;
  weight?: number;
}

@Component({
  selector: 'app-graph-canvas',
  templateUrl: './graph-canvas.component.html',
  styleUrls: ['./graph-canvas.component.scss']
})
export class GraphCanvasComponent implements OnInit, OnDestroy {
  @ViewChild('canvas', { static: false }) canvasRef!: ElementRef<SVGSVGElement>;

  private destroy$ = new Subject<void>();
  private nodes: D3Node[] = [];
  private links: D3Link[] = [];
  private svg: d3.Selection<SVGSVGElement, unknown, HTMLElement, any> | null = null;
  private simulation: d3.Simulation<D3Node, D3Link> | null = null;

  constructor(private graphService: GraphService) {}

  ngOnInit(): void {
    this.graphService.getCurrentGraph()
      .pipe(takeUntil(this.destroy$))
      .subscribe(graph => {
        if (graph) {
          this.initializeCanvas();
          this.renderGraph(graph);
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private initializeCanvas(): void {
    if (!this.canvasRef) return;

    const svg = d3.select(this.canvasRef.nativeElement);
    svg.selectAll('*').remove();

    const width = this.canvasRef.nativeElement.clientWidth;
    const height = this.canvasRef.nativeElement.clientHeight;

    this.svg = svg
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`);

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    const g = this.svg.append('g');

    // Add arrow marker for directed edges
    this.svg.append('defs').append('marker')
      .attr('id', 'arrow')
      .attr('markerWidth', 10)
      .attr('markerHeight', 10)
      .attr('refX', 9)
      .attr('refY', 3)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,0 L0,6 L9,3 z')
      .attr('fill', '#000');
  }

  private renderGraph(graph: any): void {
    if (!this.svg) return;

    // Convert data to D3 format
    this.nodes = graph.nodes.map((node: any) => ({
      id: node.id,
      label: node.label || node.id,
      fx: node.x,
      fy: node.y
    }));

    this.links = graph.edges.map((edge: any) => ({
      source: this.nodes.find(n => n.id === edge.source)!,
      target: this.nodes.find(n => n.id === edge.target)!,
      weight: edge.weight
    }));

    this.simulation = d3.forceSimulation(this.nodes)
      .force('link', d3.forceLink(this.links).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(
        this.canvasRef.nativeElement.clientWidth / 2,
        this.canvasRef.nativeElement.clientHeight / 2
      ));

    const g = this.svg!.select('g');

    // Draw links
    const link = g.selectAll('.link')
      .data(this.links)
      .enter()
      .append('line')
      .attr('class', 'link')
      .attr('stroke-width', d => d.weight ? Math.sqrt(d.weight) : 1)
      .attr('marker-end', 'url(#arrow)');

    // Draw nodes
    const node = g.selectAll('.node')
      .data(this.nodes)
      .enter()
      .append('circle')
      .attr('class', 'node')
      .attr('r', 10)
      .attr('fill', 'steelblue')
      .call(d3.drag<SVGCircleElement, D3Node>()
        .on('start', this.dragStarted.bind(this))
        .on('drag', this.dragged.bind(this))
        .on('end', this.dragEnded.bind(this)));

    // Add labels
    g.selectAll('.label')
      .data(this.nodes)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('text-anchor', 'middle')
      .text(d => d.label);

    // Update positions on simulation tick
    this.simulation.on('tick', () => {
      link
        .attr('x1', d => (d.source as D3Node).x || 0)
        .attr('y1', d => (d.source as D3Node).y || 0)
        .attr('x2', d => (d.target as D3Node).x || 0)
        .attr('y2', d => (d.target as D3Node).y || 0);

      node
        .attr('cx', d => d.x || 0)
        .attr('cy', d => d.y || 0);

      g.selectAll('.label')
        .attr('x', d => d.x || 0)
        .attr('y', d => (d.y || 0) - 15);
    });
  }

  private dragStarted(event: any, d: D3Node): void {
    if (!event.active) {
      this.simulation!.alphaTarget(0.3).restart();
    }
    d.fx = d.x;
    d.fy = d.y;
  }

  private dragged(event: any, d: D3Node): void {
    d.fx = event.x;
    d.fy = event.y;
  }

  private dragEnded(event: any, d: D3Node): void {
    if (!event.active) {
      this.simulation!.alphaTarget(0);
    }
    d.fx = null;
    d.fy = null;
  }
}
```

#### graph-canvas.component.html
```html
<div class="graph-container">
  <svg #canvas class="graph-canvas"></svg>
</div>
```

#### graph-canvas.component.scss
```scss
.graph-container {
  width: 100%;
  height: 100%;
  border: 1px solid #ddd;
  background-color: #fafafa;

  .graph-canvas {
    width: 100%;
    height: 100%;
    background-color: white;
  }
}

:deep(.link) {
  stroke: #999;
  stroke-opacity: 0.6;
}

:deep(.node) {
  stroke: white;
  stroke-width: 2px;
  cursor: pointer;
  transition: fill 0.3s ease;

  &:hover {
    fill: #1976d2;
  }
}

:deep(.label) {
  font-size: 12px;
  pointer-events: none;
}
```

---

## 8. Deployment

### 8.1 Build for Production

```bash
# Install dependencies
npm install

# Run lint
npm run lint

# Build application
npm run build:prod

# Output: dist/ folder ready for deployment
```

### 8.2 Nginx Deployment

```bash
# Copy build output to Nginx root
sudo cp -r dist/* /var/www/angular-graph-ui/dist/

# Check Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# Verify deployment
curl https://graph-ui.example.com/health
```

### 8.3 Docker Deployment

#### Dockerfile
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build:prod

# Runtime stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  angular-ui:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - flask-api

  flask-api:
    image: graph-api:latest
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
```

---

## 9. Performance Optimization

### 9.1 Build Optimization
- AOT (Ahead-of-Time) compilation
- Tree shaking to eliminate unused code
- Minification of JavaScript and CSS
- Lazy loading of feature modules
- Code splitting for route-based modules

### 9.2 Runtime Optimization
- OnPush change detection strategy
- Trackby functions in *ngFor loops
- Unsubscribe from observables using takeUntil
- Virtual scrolling for large lists
- Image lazy loading

### 9.3 Network Optimization
- Gzip compression (handled by Nginx)
- HTTP/2 support (configured in Nginx)
- Service Worker for offline support
- Asset caching with versioning
- API response caching where applicable

---

## 10. Security Best Practices

### 10.1 Application Security
- Content Security Policy (CSP) headers
- X-Frame-Options to prevent clickjacking
- X-Content-Type-Options to prevent MIME sniffing
- Referrer Policy for privacy
- Strict-Transport-Security for HTTPS

### 10.2 API Communication
- HTTPS only in production
- API request validation
- Error handling without exposing internals
- Token-based authentication (JWT)
- CORS configuration in Flask backend

### 10.3 Code Security
- TypeScript strict mode enforced
- Input sanitization via Angular sanitizer
- No inline scripts
- Dependency scanning for vulnerabilities
- Regular security updates

---

## 11. Monitoring & Logging

### 11.1 Client-Side Logging
- Console logging in development
- Error tracking service (e.g., Sentry)
- Performance monitoring
- User analytics

### 11.2 Server-Side Monitoring
- Nginx access/error logs
- Flask application logs
- API response time metrics
- Resource utilization monitoring

---

## 12. Development Workflow

### 12.1 Development Server
```bash
ng serve --open
```

### 12.2 Building and Testing
```bash
ng lint
ng test
ng test --code-coverage
```

### 12.3 Production Build
```bash
ng build --configuration production
```

---

## Document Information

- **Version:** 1.0
- **Created:** 2025-11-18
- **Status:** Final
- **Framework:** Angular 18+
- **Language:** TypeScript 5.2+
- **Server:** Nginx

