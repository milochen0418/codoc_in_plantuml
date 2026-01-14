# PlantUML Visualization Web Application

## Phase 1: Core Split-Pane Editor Interface ✅
- [x] Set up split-pane layout with resizable left (code editor) and right (diagram preview) panes
- [x] Install and integrate reflex-monaco for syntax-highlighted PlantUML code editing
- [x] Create state management for PlantUML code input with real-time updates
- [x] Implement PlantUML diagram rendering using PlantUML server API
- [x] Add dynamic diagram type detection from syntax (Sequence, Class, State, etc.)

## Phase 2: Help/Examples Sidebar with Starter Snippets ✅
- [x] Build collapsible Help sidebar with diagram type categories
- [x] Create starter code snippets for each diagram type (Sequence, Class, State, Component, Activity, Use Case, MindMap, Gantt)
- [x] Implement click-to-load functionality for snippets into the editor
- [x] Add diagram type badges/indicators showing current detected diagram type
- [x] Style the help panel with icons and clear categorization

## Phase 3: Advanced Drag-and-Drop Visual Editor Mode ✅
- [x] Create toggle between Text Mode and Visual Mode in the navbar
- [x] Build draggable node palette with UML elements (classes, actors, states, etc.)
- [x] Implement canvas area for dropping and positioning nodes using reflex-enterprise DnD
- [x] Add context menu for connecting nodes and setting relationships
- [x] Synchronize visual canvas with PlantUML text editor (bidirectional updates)
- [x] Polish responsive design and overall UI/UX for beginners

## Phase 4: Real-Time Collaborative Editing with ShareLink ✅
- [x] Convert DocumentState to rx.SharedState for real-time multi-user synchronization
- [x] Add document ID based routing (e.g., /doc/[doc_id])
- [x] Implement auto-generation of new doc IDs when visiting root "/"
- [x] Add Share button with copy-to-clipboard functionality for document URLs
- [x] Display presence indicators showing active collaborators with random names/colors
- [x] Ensure all users see the same PlantUML code and diagram preview in real-time