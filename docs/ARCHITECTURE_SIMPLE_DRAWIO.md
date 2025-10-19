# 🎨 DataMeesh - Simple Architecture for Draw.io

**Minimalist diagrams ready to recreate in draw.io**

---

## 📐 Diagram 1: High-Level Overview (Simplest)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                    👨‍💻 Data Scientist                    │
│                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │                         │
         │      JupyterHub         │
         │   (Python + DBT)        │
         │                         │
         └────────┬────────────────┘
                  │
                  ▼
         ┌─────────────────────────┐
         │                         │
         │        Trino            │
         │   (Query Engine)        │
         │                         │
         └────┬──────────┬─────────┘
              │          │
       ┌──────▼───┐   ┌──▼──────┐
       │          │   │         │
       │ Sales DB │   │Marketing│
       │          │   │   DB    │
       └──────────┘   └─────────┘
```

### Draw.io Instructions:
1. **Shapes to use:**
   - Rectangle (rounded corners) for all boxes
   - Arrow connectors for relationships

2. **Colors:**
   - User: Light blue (#E3F2FD)
   - JupyterHub: Green (#C8E6C9)
   - Trino: Orange (#FFE0B2)
   - Databases: Purple (#E1BEE7)

3. **Layout:** 
   - Vertical flow (top to bottom)
   - Equal spacing: 80px between components

---

## 📐 Diagram 2: 3-Layer Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   USER LAYER                               │
│                                                            │
│   ┌──────────────┐              ┌──────────────┐          │
│   │  JupyterHub  │              │   Grafana    │          │
│   └──────────────┘              └──────────────┘          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                  QUERY LAYER                               │
│                                                            │
│                 ┌──────────────┐                           │
│                 │    Trino     │                           │
│                 └──────────────┘                           │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                  DATA LAYER                                │
│                                                            │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│   │ Sales DB │  │Marketing │  │  Minio   │               │
│   │          │  │    DB    │  │ (Lake)   │               │
│   └──────────┘  └──────────┘  └──────────┘               │
└────────────────────────────────────────────────────────────┘
```

### Draw.io Instructions:
1. **Layout:**
   - 3 horizontal swim lanes
   - Each lane: 150px height

2. **Colors:**
   - User Layer: Light blue background
   - Query Layer: Light orange background
   - Data Layer: Light purple background

3. **Connections:**
   - JupyterHub → Trino
   - Grafana → Trino
   - Trino → All databases

---

## 📐 Diagram 3: Data Flow (Minimal)

```
User Query
    │
    ▼
┌─────────┐
│ Trino   │──┐
└─────────┘  │
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐       ┌─────────┐
│Sales DB │       │Marketing│
└─────────┘       └─────────┘
    │                 │
    └────────┬────────┘
             │
             ▼
         Results
```

### Draw.io Instructions:
1. **Shapes:**
   - Start/End: Rounded rectangle (100x40px)
   - Process: Rectangle (120x60px)
   - Arrows: Default connectors

2. **Flow direction:** Top to bottom

3. **Style:** Simple black & white

---

## 📐 Diagram 4: Components Overview

```
┌─────────────────────────────────────────────────────┐
│                 DataMeesh Platform                  │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │JupyterHub │  │   Trino   │  │  Grafana  │      │
│  │  :30080   │  │  :30808   │  │  :30030   │      │
│  └───────────┘  └───────────┘  └───────────┘      │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │ Sales DB  │  │Marketing  │  │   Minio   │      │
│  │  :5432    │  │    DB     │  │  :30900   │      │
│  └───────────┘  └───────────┘  └───────────┘      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Draw.io Instructions:
1. **Container:**
   - Large rectangle with dashed border
   - Label at top: "DataMeesh Platform"

2. **Components:**
   - All same size: 100x80px
   - 2 rows, 3 columns
   - Grid layout

3. **Style:**
   - Solid borders
   - Different color per component
   - Port numbers in smaller font

---

## 📐 Diagram 5: Domain-Oriented Architecture

```
                    ┌─────────────┐
                    │ Data Mesh   │
                    │  Platform   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │  Sales Domain    │      │ Marketing Domain │
    │                  │      │                  │
    │  ┌──────────┐    │      │  ┌──────────┐    │
    │  │Sales DB  │    │      │  │Marketing │    │
    │  └──────────┘    │      │  │   DB     │    │
    │                  │      │  └──────────┘    │
    │  ┌──────────┐    │      │                  │
    │  │Sales API │    │      │                  │
    │  └──────────┘    │      │                  │
    └──────────────────┘      └──────────────────┘
```

### Draw.io Instructions:
1. **Domain boxes:**
   - Container shape with thick border
   - Size: 200x180px

2. **Internal components:**
   - Smaller rectangles inside
   - Size: 120x50px

3. **Connections:**
   - Bidirectional arrows from platform to domains

---

## 📐 Diagram 6: User Workflow (Ultra Simple)

```
1. Login
   ↓
2. Write Query
   ↓
3. Trino Executes
   ↓
4. Get Results
   ↓
5. Visualize
```

### Draw.io Instructions:
1. **Style:** Vertical flowchart
2. **Shapes:** 
   - Rounded rectangles (150x40px)
   - Arrows between each step
3. **Colors:** Gradient from blue to green

---

## 📐 Diagram 7: Federated Query (Concept)

```
        ┌──────────────────┐
        │  Single Query    │
        │  (Federation)    │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │      Trino       │
        └────────┬─────────┘
                 │
      ┌──────────┼──────────┐
      │          │          │
      ▼          ▼          ▼
  ┌─────┐    ┌─────┐    ┌─────┐
  │DB 1 │    │DB 2 │    │Lake │
  └─────┘    └─────┘    └─────┘
      │          │          │
      └──────────┼──────────┘
                 │
                 ▼
           Combined Results
```

### Draw.io Instructions:
1. **Key concept:** Show that one query accesses multiple sources
2. **Highlight:** Trino as central component (larger box, bold)
3. **Arrows:** Bidirectional to show read/return

---

## 🎨 Draw.io Color Palette

Use these colors for consistency:

```
JupyterHub:    #4CAF50  (Green)
Trino:         #FF9800  (Orange)
Grafana:       #2196F3  (Blue)
Databases:     #9C27B0  (Purple)
Data Lake:     #00BCD4  (Cyan)
User:          #FFC107  (Amber)

Backgrounds:
- Layer 1: #E8F5E9  (Light green)
- Layer 2: #FFF3E0  (Light orange)
- Layer 3: #F3E5F5  (Light purple)
```

---

## 📏 Draw.io Settings Recommendations

### Grid & Layout:
```
Grid size: 10px
Snap to grid: ON
Page size: A4 Landscape
Margins: 20px
```

### Default Shapes:
```
Rectangle:
- Width: 120px
- Height: 60px
- Rounded corners: 5px
- Border: 2px
- Font: Helvetica, 12pt

Arrow:
- Width: 2px
- End: Standard arrow
- Color: #424242 (Dark gray)
```

### Text:
```
Title: 16pt Bold
Component name: 12pt Regular
Port/details: 10pt Regular
```

---

## 📋 Quick Start Guide for Draw.io

### Creating Diagram 1 (High-Level):

**Step 1:** Open draw.io → Blank diagram

**Step 2:** Add shapes
- Drag "Rectangle" from left panel (4 times)
- Apply rounded corners (Format panel → Rounded)

**Step 3:** Add text
- Double-click each rectangle
- Enter: "Data Scientist", "JupyterHub", "Trino", "Sales DB"

**Step 4:** Apply colors
- Select shape → Format panel → Fill color
- Use color palette above

**Step 5:** Add arrows
- Select connector tool
- Click source → drag → click target

**Step 6:** Arrange
- Select all → Arrange → Vertical spacing → 80px

**Done!** ✅

---

## 📐 Diagram 8: Technology Stack (Icon View)

```
┌─────────────────────────────────────────────┐
│         DataMeesh Technology Stack          │
├─────────────────────────────────────────────┤
│                                             │
│  Workspace:     [JupyterHub] [Python]       │
│                                             │
│  Query:         [Trino]                     │
│                                             │
│  Transform:     [DBT]                       │
│                                             │
│  Storage:       [PostgreSQL] [Minio]        │
│                                             │
│  Visualization: [Grafana]                   │
│                                             │
│  Orchestration: [Kubernetes]                │
│                                             │
└─────────────────────────────────────────────┘
```

### Draw.io Instructions:
1. **Layout:** List format (vertical)
2. **Each tech:** Small rounded rectangle (80x30px)
3. **Categories:** Left-aligned text (bold)
4. **Background:** Light gray (#F5F5F5)

---

## 📐 Diagram 9: Deployment View (Kubernetes)

```
┌────────────────────────────────────────────┐
│         Kubernetes Cluster                 │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │     Namespace: data-platform     │     │
│  │                                  │     │
│  │  [JupyterHub] [Trino] [Grafana] │     │
│  └──────────────────────────────────┘     │
│                                            │
│  ┌────────────────┐ ┌─────────────────┐   │
│  │ sales-domain   │ │marketing-domain │   │
│  │                │ │                 │   │
│  │  [Sales DB]    │ │ [Marketing DB]  │   │
│  └────────────────┘ └─────────────────┘   │
│                                            │
└────────────────────────────────────────────┘
```

### Draw.io Instructions:
1. **Cluster:** Large container (dashed border)
2. **Namespaces:** Medium containers (solid border)
3. **Pods:** Small rectangles inside namespaces
4. **Colors:** Blue for platform, Green/Purple for domains

---

## 📐 Diagram 10: Access Ports (Network)

```
Browser (localhost)
        │
        ├─── :30080 ──► JupyterHub
        │
        ├─── :30808 ──► Trino UI
        │
        ├─── :30030 ──► Grafana
        │
        ├─── :30900 ──► Minio API
        │
        └─── :30901 ──► Minio Console
```

### Draw.io Instructions:
1. **Style:** Tree diagram
2. **Root:** Browser (circle shape)
3. **Branches:** Arrows with port numbers as labels
4. **Services:** Rounded rectangles at the end
5. **Colors:** All services same color (blue)

---

## 🎯 Recommended Diagram Order

For presentations, use this order:

1. **Diagram 1** - High-Level Overview
   - *Show first* to introduce the concept

2. **Diagram 2** - 3-Layer Architecture
   - Explain separation of concerns

3. **Diagram 7** - Federated Query
   - Show the "magic" of Trino

4. **Diagram 5** - Domain-Oriented
   - Explain Data Mesh principles

5. **Diagram 10** - Access Ports
   - Practical: How to access services

---

## 💡 Tips for Draw.io

1. **Use Templates:**
   - File → New from Template → Cloud Architecture

2. **Import Icons:**
   - Use "AWS Architecture Icons" library
   - Or download Kubernetes icons pack

3. **Consistent Styling:**
   - Create one shape with your style
   - Copy/paste it (keeps formatting)

4. **Alignment:**
   - Select multiple shapes → Arrange → Align
   - Use "Distribute horizontally/vertically"

5. **Export:**
   - File → Export as → PNG (for presentations)
   - Resolution: 300 DPI
   - Transparent background: OFF

---

## 📥 Export Settings

For best quality:

```
Format: PNG
Border width: 10px
Resolution: 300 DPI
Grid: Hidden
Page view: Hidden
Transparent: No (white background)
```

For web documentation:

```
Format: SVG
Embed fonts: Yes
```

---

**🎉 Ready to create beautiful architecture diagrams in draw.io!**

*Each diagram takes 5-10 minutes to create.*

