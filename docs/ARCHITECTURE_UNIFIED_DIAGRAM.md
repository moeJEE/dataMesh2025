# 🎨 DataMeesh - Unified Architecture Diagram

**One complete diagram showing the entire platform**

---

## 📐 Complete Architecture Diagram (All-in-One)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DataMeesh Platform                                 │
│                     (Kubernetes on Docker Desktop)                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            👥 USER LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    Browser → :30080              Browser → :30030              Browser     │
│         │                             │                            │        │
│         ▼                             ▼                            ▼        │
│  ┌─────────────┐              ┌─────────────┐             ┌──────────────┐ │
│  │ JupyterHub  │              │   Grafana   │             │   Minio      │ │
│  │             │              │             │             │  Console     │ │
│  │ • Python    │              │ • Dashboards│             │              │ │
│  │ • DBT       │              │ • Analytics │             │ • S3 Browser │ │
│  │ • Notebooks │              │ • Viz       │             │ • Upload     │ │
│  └──────┬──────┘              └──────┬──────┘             └──────────────┘ │
│         │                            │                                     │
└─────────┼────────────────────────────┼─────────────────────────────────────┘
          │                            │
          │                            │
┌─────────▼────────────────────────────▼─────────────────────────────────────┐
│                        🔗 QUERY & FEDERATION LAYER                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                        ┌───────────────────────┐                           │
│                        │   Trino Coordinator   │                           │
│                        │      :30808 (UI)      │                           │
│                        │                       │                           │
│                        │ • Query Planning      │                           │
│                        │ • Federation Engine   │                           │
│                        │ • Multiple Catalogs   │                           │
│                        └──────────┬────────────┘                           │
│                                   │                                         │
│                        ┌──────────▼────────────┐                           │
│                        │    Trino Worker       │                           │
│                        │                       │                           │
│                        │ • Query Execution     │                           │
│                        │ • Data Processing     │                           │
│                        └──────────┬────────────┘                           │
│                                   │                                         │
└───────────────────────────────────┼─────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
┌───────────────────▼───────────────▼───────────────▼─────────────────────────┐
│                          💾 DATA & STORAGE LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────────┐   │
│  │  Sales Domain   │    │Marketing Domain │    │   Data Lake Layer    │   │
│  │                 │    │                 │    │                      │   │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │  ┌──────────────┐   │   │
│  │ │  Sales DB   │ │    │ │ Marketing  │ │    │  │    Minio     │   │   │
│  │ │ PostgreSQL  │ │    │ │    DB      │ │    │  │   (S3 API)   │   │   │
│  │ │   :5432     │ │    │ │ PostgreSQL │ │    │  │   :30900     │   │   │
│  │ │             │ │    │ │   :5432    │ │    │  │              │   │   │
│  │ │ Tables:     │ │    │ │            │ │    │  │ Bucket:      │   │   │
│  │ │ • customers │ │    │ │ Tables:    │ │    │  │ • datalake   │   │   │
│  │ │ • orders    │ │    │ │ • leads    │ │    │  └──────┬───────┘   │   │
│  │ └─────────────┘ │    │ │ • campaigns│ │    │         │           │   │
│  │                 │    │ └─────────────┘ │    │  ┌──────▼───────┐   │   │
│  │ ┌─────────────┐ │    │                 │    │  │    Hive      │   │   │
│  │ │  Sales API  │ │    │                 │    │  │  Metastore   │   │   │
│  │ │   Flask     │ │    │                 │    │  │    :9083     │   │   │
│  │ │   :30081    │ │    │                 │    │  │              │   │   │
│  │ │             │ │    │                 │    │  │ • Metadata   │   │   │
│  │ │  + API DB   │ │    │                 │    │  │ • Schemas    │   │   │
│  │ │ PostgreSQL  │ │    │                 │    │  │ • Locations  │   │   │
│  │ └─────────────┘ │    │                 │    │  └──────────────┘   │   │
│  └─────────────────┘    └─────────────────┘    └──────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    🔄 TRANSFORMATION & DOCUMENTATION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JupyterHub ──────► DBT Models ──────► Trino ──────► Data Products         │
│                         │                                                   │
│                         │ dbt docs generate                                 │
│                         ▼                                                   │
│                  ┌──────────────┐                                           │
│                  │  DBT Docs    │                                           │
│                  │   (Nginx)    │                                           │
│                  │   :30082     │                                           │
│                  │              │                                           │
│                  │ • Lineage    │                                           │
│                  │ • Tests      │                                           │
│                  │ • Catalog    │                                           │
│                  └──────────────┘                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    📊 METADATA CATALOG (Optional)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                        ┌──────────────────┐                                 │
│                        │     DataHub      │                                 │
│                        │   :9002 (UI)     │                                 │
│                        │                  │                                 │
│                        │ • Metadata Graph │                                 │
│                        │ • Data Lineage   │                                 │
│                        │ • Data Discovery │                                 │
│                        │ • Governance     │                                 │
│                        │                  │                                 │
│                        │ Components:      │                                 │
│                        │ • Elasticsearch  │                                 │
│                        │ • Neo4j          │                                 │
│                        │ • Kafka          │                                 │
│                        └────────┬─────────┘                                 │
│                                 │                                           │
│                    ┌────────────┼────────────┐                              │
│                    │            │            │                              │
│         Ingests from: DBT    Trino    PostgreSQL                            │
│                                                                             │
│  ⚠️  Note: Requires 10-12GB RAM (Docker Compose)                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      🌐 NETWORK & ACCESS PORTS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  localhost:30080  → JupyterHub                                              │
│  localhost:30808  → Trino Web UI                                            │
│  localhost:30030  → Grafana                                                 │
│  localhost:30900  → Minio API                                               │
│  localhost:30901  → Minio Console                                           │
│  localhost:30082  → DBT Documentation                                       │
│  localhost:30081  → Sales API                                               │
│  localhost:9002   → DataHub (Optional)                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      🔐 KUBERNETES ORGANIZATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📦 Namespace: data-platform                                                │
│     • JupyterHub, Trino, Minio, Hive, Grafana, Nginx                       │
│                                                                             │
│  📦 Namespace: sales-domain                                                 │
│     • Sales DB, Sales API, Sales API DB                                    │
│                                                                             │
│  📦 Namespace: marketing-domain                                             │
│     • Marketing DB                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Draw.io Creation Guide

### Step-by-Step Instructions:

#### 1. **Setup Canvas**
```
- Open draw.io
- New Diagram → Blank
- Page Setup:
  * Format: A3 Landscape (or A2 for more space)
  * Grid: 10px
  * Snap to grid: ON
```

#### 2. **Create Main Containers (6 large boxes)**

**Container 1 - User Layer:**
```
Shape: Rectangle with thick border
Size: 700 x 180px
Fill: Light blue (#E3F2FD)
Border: 3px, #2196F3
Position: Top of diagram
```

**Container 2 - Query Layer:**
```
Shape: Rectangle with thick border
Size: 700 x 200px
Fill: Light orange (#FFF3E0)
Border: 3px, #FF9800
Position: Below User Layer
```

**Container 3 - Data Layer:**
```
Shape: Rectangle with thick border
Size: 700 x 280px
Fill: Light purple (#F3E5F5)
Border: 3px, #9C27B0
Position: Below Query Layer
```

**Container 4 - Transformation Layer:**
```
Shape: Rectangle with thick border
Size: 700 x 150px
Fill: Light green (#E8F5E9)
Border: 3px, #4CAF50
Position: Below Data Layer
```

**Container 5 - Metadata Catalog Layer (Optional):**
```
Shape: Rectangle with dashed border
Size: 700 x 180px
Fill: Light yellow (#FFF9C4)
Border: 3px dashed, #FBC02D
Position: Below Transformation Layer
```

**Container 6 - Network Layer:**
```
Shape: Rectangle with thick border
Size: 700 x 130px
Fill: Light gray (#F5F5F5)
Border: 2px, #757575
Position: Bottom of diagram
```

#### 3. **Add Components Inside Containers**

**In User Layer:**
```
- 3 rectangles (rounded corners):
  * JupyterHub: 150 x 100px, Green (#4CAF50)
  * Grafana: 150 x 100px, Blue (#2196F3)
  * Minio Console: 150 x 100px, Cyan (#00BCD4)
- Space them evenly (200px apart)
```

**In Query Layer:**
```
- 2 rectangles (rounded corners):
  * Trino Coordinator: 200 x 80px, Orange (#FF9800)
  * Trino Worker: 200 x 60px, Light Orange (#FFB74D)
- Stack vertically, centered
```

**In Data Layer:**
```
- 3 containers (nested rectangles):
  * Sales Domain: 200 x 220px
    - Sales DB: 150 x 60px inside
    - Sales API: 150 x 60px inside
  * Marketing Domain: 200 x 220px
    - Marketing DB: 150 x 60px inside
  * Data Lake: 200 x 220px
    - Minio: 150 x 60px inside
    - Hive: 150 x 60px inside
- Space them evenly (40px apart)
```

**In Transformation Layer:**
```
- Simple flow: 4 rectangles connected:
  * JupyterHub → DBT → Trino → Products
  * Size: 120 x 50px each
  * Color: Green gradient
- Below: DBT Docs box (150 x 80px)
```

**In Metadata Catalog Layer (Optional):**
```
- 1 large rectangle (centered):
  * DataHub: 250 x 140px, Yellow (#FBC02D)
  * Include small text listing components:
    - Elasticsearch
    - Neo4j
    - Kafka
- Add warning note below (red text):
  * "⚠️ Requires 10-12GB RAM"
```

**In Network Layer:**
```
- Text list (no boxes):
  * 8 lines showing ports (including DataHub)
  * Font: 11pt, monospace
  * Align left
```

#### 4. **Add Connections**

**Main Data Flow (bold arrows):**
```
1. JupyterHub → Trino Coordinator (2px, blue)
2. Grafana → Trino Coordinator (2px, blue)
3. Trino Coordinator → Trino Worker (2px, orange)
4. Trino Worker → Sales DB (2px, purple)
5. Trino Worker → Marketing DB (2px, purple)
6. Trino Worker → Minio (2px, cyan)
7. Minio → Hive (2px, dotted, cyan)
```

**Secondary Connections (thin arrows):**
```
- JupyterHub → DBT (1px, dashed, green)
- DBT → Trino (1px, dashed, green)
```

**Metadata Ingestion (dotted arrows - Optional):**
```
- DBT → DataHub (1px, dotted, yellow)
- Trino → DataHub (1px, dotted, yellow)
- PostgreSQL → DataHub (1px, dotted, yellow)
```

#### 5. **Add Labels**

**Layer titles (inside containers, top-left):**
```
Font: 14pt Bold
Color: Same as border color
Examples:
  - "👥 USER LAYER"
  - "🔗 QUERY & FEDERATION LAYER"
  - "💾 DATA & STORAGE LAYER"
  - "🔄 TRANSFORMATION & DOCUMENTATION"
  - "🌐 NETWORK & ACCESS PORTS"
```

**Component labels (inside boxes):**
```
Font: 11pt Regular
Examples:
  - "JupyterHub"
  - "• Python"
  - "• DBT"
  - ":30080"
```

#### 6. **Add Icons (Optional)**

If you want to make it prettier:
```
- Use draw.io icon library
- Add small icons next to component names:
  * Database icon for PostgreSQL
  * Gear icon for Trino
  * Chart icon for Grafana
  * Folder icon for Minio
```

---

## 🎨 Color Palette (Copy-Paste Ready)

```
User Layer Background:        #E3F2FD (light blue)
Query Layer Background:       #FFF3E0 (light orange)
Data Layer Background:        #F3E5F5 (light purple)
Transform Layer Background:   #E8F5E9 (light green)
Metadata Layer Background:    #FFF9C4 (light yellow) - Optional
Network Layer Background:     #F5F5F5 (light gray)

JupyterHub:    #4CAF50 (green)
Trino:         #FF9800 (orange)
Grafana:       #2196F3 (blue)
PostgreSQL:    #9C27B0 (purple)
Minio:         #00BCD4 (cyan)
DBT:           #66BB6A (light green)
DataHub:       #FBC02D (yellow) - Optional

Borders:       #424242 (dark gray)
Text:          #212121 (almost black)
Warning Text:  #D32F2F (red)
```

---

## 📏 Exact Dimensions

```
Canvas Size:           1400 x 1400px (taller for DataHub)
Main Container Width:  700px
Spacing Between Layers: 20px

Component Sizes:
- Large box:   250 x 140px (DataHub)
- Medium box:  200 x 100px
- Small box:   150 x 80px
- Tiny box:    120 x 60px

Arrow width:
- Primary flow:      2px
- Secondary flow:    1px (dashed)
- Metadata ingestion: 1px (dotted)
```

---

## ⏱️ Time Estimate

```
Total creation time: 30-35 minutes (with DataHub)

Breakdown:
1. Setup & containers:       5 min
2. Add components:           10 min (includes DataHub)
3. Add connections:          6 min (includes metadata flow)
4. Add labels & text:        6 min
5. Fine-tuning & alignment:  5 min

Without DataHub: 25-30 minutes
```

---

## 💡 Pro Tips

### 1. **Use Layers in draw.io**
```
Create layers for easier management:
- Layer 1: Background containers
- Layer 2: Components
- Layer 3: Connections
- Layer 4: Labels
```

### 2. **Copy & Paste for Consistency**
```
- Create one "perfect" component
- Copy it multiple times
- Just change the label
- This ensures consistent sizing
```

### 3. **Alignment Tools**
```
Select multiple shapes:
- Arrange → Align → Distribute Horizontally
- Arrange → Align → Distribute Vertically
- This makes everything neat!
```

### 4. **Group Related Items**
```
Select components that go together:
- Right-click → Group
- Now they move as one unit
- Example: Group "Trino Coordinator" + "Trino Worker"
```

### 5. **Use Grid for Perfect Alignment**
```
- View → Grid
- Set to 10px
- Enable snap to grid
- Components will align perfectly
```

---

## 📤 Export Settings

### For Presentations (PowerPoint, PDF):
```
Format: PNG
Resolution: 300 DPI
Border: 10px
Background: White
Transparent: NO
Quality: Maximum
```

### For Web/Documentation:
```
Format: SVG
Embed fonts: YES
Include links: NO
Size: Original
```

### For Printing:
```
Format: PDF
Page size: A3
Orientation: Landscape
Include: All layers
Quality: Print
```

---

## 🎯 What This Diagram Shows

✅ **All Components:** Every service in DataMeesh (including optional DataHub)  
✅ **All Connections:** How they communicate  
✅ **All Layers:** User, Query, Data, Transform, Metadata, Network  
✅ **All Ports:** How to access each service  
✅ **Kubernetes:** How it's organized in namespaces  
✅ **Data Flow:** From user to database and back  
✅ **Metadata Management:** DataHub for governance (optional)  

**But remains:** 
- Simple enough to understand at a glance
- Clean enough to present to executives
- Detailed enough for technical teams
- Easy to create in 30-35 minutes!

---

## 🚀 Quick Start Checklist

```
□ Open draw.io
□ Create 6 main containers (layers)
□ Add 3 components to User Layer
□ Add 2 components to Query Layer  
□ Add 9 components to Data Layer
□ Add 4 components to Transform Layer
□ Add 1 component to Metadata Layer (Optional - DataHub)
□ Add text list to Network Layer
□ Draw 7 main arrows
□ Draw 3 metadata arrows (if using DataHub)
□ Add all labels
□ Align everything
□ Export as PNG/SVG
```

**Done! You have a complete architecture diagram!** ✅

---

## 📸 Preview of Final Result

Your diagram will look like this:

- **Top to bottom flow:** Clear hierarchy
- **Color-coded layers:** Easy to distinguish
- **All components visible:** Nothing hidden
- **Professional appearance:** Ready for presentations
- **Single page:** Everything on one diagram
- **Print-friendly:** Works in black & white too

**Perfect for:**
- Academic presentations
- Technical documentation  
- Architecture reviews
- Stakeholder meetings
- Team onboarding

---

**🎨 Time to create your masterpiece in draw.io!**

*One diagram. Complete architecture (with optional DataHub). 30-35 minutes.* ⏱️

