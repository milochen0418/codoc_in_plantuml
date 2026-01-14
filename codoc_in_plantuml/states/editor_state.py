import reflex as rx
from pydantic import BaseModel, Field
from codoc_in_plantuml.utils.plantuml import PlantUML


class Snippet(BaseModel):
    label: str
    code: str
    description: str


class SubCategory(BaseModel):
    name: str
    snippets: list[Snippet] = Field(default_factory=list)


class Category(BaseModel):
    name: str
    icon: str
    color: str
    snippets: list[Snippet] = Field(default_factory=list)
    subcategories: list[SubCategory] = Field(default_factory=list)


class EditorState(rx.State):
    layout_mode: str = "split"
    show_sidebar: bool = True
    linking_source_id: str = ""
    expanded_categories: list[str] = ["Sequence", "Class", "Use Case", "JSON / YAML"]
    current_doc_id: str = ""

    @rx.event
    async def on_load(self):
        """Handle page load: redirect if no share_id, or link to shared state."""
        path = self.router.url.path or ""
        share_id = ""
        if path.startswith("/doc/"):
            share_id = path[len("/doc/") :].split("/", 1)[0]

        if not share_id:
            import random
            import string

            new_id = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
            return rx.redirect(f"/doc/{new_id}")
        sanitized_id = share_id.replace("_", "-")
        if sanitized_id != share_id:
            return rx.redirect(f"/doc/{sanitized_id}")
        self.current_doc_id = sanitized_id
        from codoc_in_plantuml.states.document_state import DocumentState

        doc_state = await self.get_state(DocumentState)
        linked_doc = await doc_state._link_to(self.current_doc_id)
        await linked_doc.join_room()

    @rx.event
    def copy_link(self):
        """Copy the current document URL to clipboard."""
        origin = self.router.url.origin
        if not origin and self.router.url.hostname:
            scheme = self.router.url.scheme or "http"
            port = f":{self.router.url.port}" if self.router.url.port else ""
            origin = f"{scheme}://{self.router.url.hostname}{port}"

        prefix = origin or ""
        yield rx.set_clipboard(f"{prefix}/doc/{self.current_doc_id}")
        yield rx.toast("Link copied to clipboard!")

    snippet_categories: list[Category] = [
        Category(
            name="Sequence",
            icon="arrow-right-left",
            color="text-blue-500",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Simple Message",
                            code="""@startuml
Alice -> Bob: Hello
@enduml""",
                            description="-> for sync call",
                        ),
                        Snippet(
                            label="Return Message",
                            code="""@startuml
Alice -> Bob: Request
Bob --> Alice: Response
@enduml""",
                            description="--> for response",
                        ),
                        Snippet(
                            label="Self-Message",
                            code="""@startuml
Alice -> Alice: Process Data
@enduml""",
                            description="Recursive call",
                        ),
                    ],
                ),
                SubCategory(
                    name="PARTICIPANTS",
                    snippets=[
                        Snippet(
                            label="Types",
                            code="""@startuml
actor User
boundary Web
control Logic
database DB
entity Data
User -> Web: Login
@enduml""",
                            description="Different visual shapes",
                        ),
                        Snippet(
                            label="Colors & Styles",
                            code="""@startuml
skinparam sequenceMessageAlign center
participant Alice #AliceBlue
participant Bob #technology
Alice -> Bob: Styled
@enduml""",
                            description="Customizing appearance",
                        ),
                    ],
                ),
                SubCategory(
                    name="CONTROL FLOW",
                    snippets=[
                        Snippet(
                            label="Alt/Else (Choices)",
                            code="""@startuml
Alice -> Bob: Action
alt Success
  Bob -> Alice: OK
else Error
  Bob -> Alice: Fail
end
@enduml""",
                            description="Conditional branching",
                        ),
                        Snippet(
                            label="Loop",
                            code="""@startuml
loop 10 times
  Alice -> Bob: Poll
end
@enduml""",
                            description="Iteration",
                        ),
                        Snippet(
                            label="Parallel (Par)",
                            code="""@startuml
par
  Alice -> Bob: Task 1
else
  Alice -> Charlie: Task 2
end
@enduml""",
                            description="Concurrent actions",
                        ),
                    ],
                ),
                SubCategory(
                    name="ADVANCED",
                    snippets=[
                        Snippet(
                            label="Activation",
                            code="""@startuml
Alice -> Bob: Run
activate Bob
Bob -> Alice: Done
deactivate Bob
@enduml""",
                            description="Show execution focus",
                        ),
                        Snippet(
                            label="Notes",
                            code="""@startuml
Alice -> Bob: Hi
note right: Simple note
note over Alice, Bob: Shared note
@enduml""",
                            description="Add explanations",
                        ),
                    ],
                ),
            ],
        ),
        Category(
            name="Use Case",
            icon="user",
            color="text-yellow-500",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Simple Use Case",
                            code="""@startuml
left to right direction
actor User
usecase "Login" as UC1
User --> UC1
@enduml""",
                            description="Actor and usecase",
                        )
                    ],
                ),
                SubCategory(
                    name="RELATIONSHIPS",
                    snippets=[
                        Snippet(
                            label="Include/Extend",
                            code="""@startuml
usecase "Checkout" as UC1
usecase "Verify Card" as UC2
usecase "Help" as UC3
UC1 ..> UC2 : <<include>>
UC3 ..> UC1 : <<extend>>
@enduml""",
                            description="Advanced relations",
                        )
                    ],
                ),
            ],
        ),
        Category(
            name="Class",
            icon="box",
            color="text-orange-500",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Simple Class",
                            code="""@startuml
class User {
  id: int
  name: string
}
@enduml""",
                            description="Definition with fields",
                        ),
                        Snippet(
                            label="Methods",
                            code="""@startuml
class Calculator {
  + add(a:int, b:int): int
  - reset(): void
}
@enduml""",
                            description="Functions with parameters",
                        ),
                    ],
                ),
                SubCategory(
                    name="VISIBILITY",
                    snippets=[
                        Snippet(
                            label="Access Levels",
                            code="""@startuml
class Access {
  + public
  - private
  # protected
  ~ package
}
@enduml""",
                            description="Standard UML access markers",
                        ),
                        Snippet(
                            label="Abstract/Static",
                            code="""@startuml
class Utils {
  {static} version: string
  {abstract} run(): void
}
@enduml""",
                            description="Keywords in braces",
                        ),
                    ],
                ),
                SubCategory(
                    name="RELATIONSHIPS",
                    snippets=[
                        Snippet(
                            label="Inheritance",
                            code="""@startuml
Animal <|-- Dog
@enduml""",
                            description="IS-A (Generalization)",
                        ),
                        Snippet(
                            label="Composition",
                            code="""@startuml
Car *-- Engine
@enduml""",
                            description="Whole-part (Strong)",
                        ),
                        Snippet(
                            label="Aggregation",
                            code="""@startuml
School o-- Teacher
@enduml""",
                            description="Whole-part (Weak)",
                        ),
                    ],
                ),
            ],
        ),
        Category(
            name="Object",
            icon="box-select",
            color="text-orange-400",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Instance",
                            code="""@startuml
object user1
object "user2 : User" as u2

user1 : name = "John"
u2 : name = "Jane"
@enduml""",
                            description="Concrete instances",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Activity",
            icon="git-fork",
            color="text-emerald-500",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Flow",
                            code="""@startuml
start
:Step 1;
:Step 2;
stop
@enduml""",
                            description="Simple linear flow",
                        )
                    ],
                ),
                SubCategory(
                    name="CONTROL FLOW",
                    snippets=[
                        Snippet(
                            label="If/Then/Else",
                            code="""@startuml
start
if (Test) then (yes)
  :A;
else (no)
  :B;
endif
stop
@enduml""",
                            description="Branching",
                        ),
                        Snippet(
                            label="While Loop",
                            code="""@startuml
start
while (Has Data?) is (yes)
  :Process;
endwhile (no)
stop
@enduml""",
                            description="Iteration",
                        ),
                    ],
                ),
                SubCategory(
                    name="ADVANCED",
                    snippets=[
                        Snippet(
                            label="Swimlanes",
                            code="""@startuml
|User|
start
:Login;
|Server|
:Validate;
|User|
:Result;
stop
@enduml""",
                            description="Responsibility lanes",
                        )
                    ],
                ),
            ],
        ),
        Category(
            name="Component",
            icon="package",
            color="text-yellow-600",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Components",
                            code="""@startuml
[First Component]
[Second Component] as Comp2
[First Component] ..> Comp2 : use
@enduml""",
                            description="Basic components",
                        )
                    ],
                ),
                SubCategory(
                    name="PACKAGES",
                    snippets=[
                        Snippet(
                            label="Grouping",
                            code="""@startuml
package "Backend" {
  [API]
  [Worker]
}
package "Frontend" {
  [Web App]
}
[Web App] --> [API]
@enduml""",
                            description="Package grouping",
                        )
                    ],
                ),
            ],
        ),
        Category(
            name="Deployment",
            icon="server",
            color="text-blue-600",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Nodes",
                            code="""@startuml
node "Web Server" {
  [Apache]
}
node "DB Server" {
  database MySQL
}
[Apache] --> MySQL
@enduml""",
                            description="Physical nodes",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="State",
            icon="circle-dot",
            color="text-purple-500",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Transitions",
                            code="""@startuml
[*] --> Idle
Idle -> Active : Start
Active -> [*] : Stop
@enduml""",
                            description="Start/Stop flow",
                        )
                    ],
                ),
                SubCategory(
                    name="ADVANCED",
                    snippets=[
                        Snippet(
                            label="Composite",
                            code="""@startuml
state Active {
  [*] --> Loading
  Loading --> Ready
}
@enduml""",
                            description="Nested states",
                        ),
                        Snippet(
                            label="Guards",
                            code="""@startuml
Idle -> Active : [auth == true]
@enduml""",
                            description="Conditional transitions",
                        ),
                    ],
                ),
            ],
        ),
        Category(
            name="Timing",
            icon="clock",
            color="text-gray-500",
            subcategories=[
                SubCategory(
                    name="BASICS",
                    snippets=[
                        Snippet(
                            label="Digital",
                            code="""@startuml
robust "Web Browser" as WB
concise "User" as U

@0
U is Idle
WB is Idle

@100
U is Waiting
WB is Processing

@300
WB is Idle
@enduml""",
                            description="Time-based state",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="JSON / YAML",
            icon="code-2",
            color="text-red-400",
            subcategories=[
                SubCategory(
                    name="DATA",
                    snippets=[
                        Snippet(
                            label="JSON View",
                            code="""@startjson
{
  "name": "Reflex",
  "tags": ["Web", "Python"],
  "active": true
}
@endjson""",
                            description="Visualize JSON",
                        ),
                        Snippet(
                            label="YAML View",
                            code="""@startyaml
name: PlantUML
version: 1.0
features:
  - simple
  - text-based
@endyaml""",
                            description="Visualize YAML",
                        ),
                    ],
                )
            ],
        ),
        Category(
            name="EBNF / Regex",
            icon="regex",
            color="text-purple-400",
            subcategories=[
                SubCategory(
                    name="GRAMMAR",
                    snippets=[
                        Snippet(
                            label="EBNF",
                            code="""@startebnf
group = "(" , expression , ")";
expression = term , { "+" | "-" , term };
term = factor , { "*" | "/" , factor };
@endebnf""",
                            description="Syntax grammar",
                        ),
                        Snippet(
                            label="Regex",
                            code="""@startregex
[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}
@endregex""",
                            description="Regex visualization",
                        ),
                    ],
                )
            ],
        ),
        Category(
            name="Network (nwdiag)",
            icon="network",
            color="text-cyan-600",
            subcategories=[
                SubCategory(
                    name="TOPOLOGY",
                    snippets=[
                        Snippet(
                            label="Simple Network",
                            code="""@startnwdiag
nwdiag {
  network dmz {
    address = "210.x.x.x/24"
    web01 [address = "210.x.x.1"];
    web02 [address = "210.x.x.2"];
  }
  network internal {
    web01;
    web02;
    db01;
  }
}
@endnwdiag""",
                            description="Network diagram",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="UI Mockups (Salt)",
            icon="layout-dashboard",
            color="text-gray-400",
            subcategories=[
                SubCategory(
                    name="WIREFRAMES",
                    snippets=[
                        Snippet(
                            label="Window",
                            code="""@startsalt
{
  Just plain text
  [This is my button]
  ()
  (X)
  [X] Checkbox
  "Input field"
  ^Droplist^
}
@endsalt""",
                            description="UI components",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Archimate",
            icon="building-2",
            color="text-yellow-700",
            subcategories=[
                SubCategory(
                    name="ENTERPRISE",
                    snippets=[
                        Snippet(
                            label="Basic",
                            code="""@startuml
archimate #Technology "VPN Server" as vpnServerA <<technology-device>>
archimate #Technology "VPN Server" as vpnServerB <<technology-device>>
package "Legacy" {
  node "Mainframe" as mainframe
}
vpnServerA --> mainframe
@enduml""",
                            description="Enterprise architecture",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="SDL",
            icon="file-text",
            color="text-indigo-400",
            subcategories=[
                SubCategory(
                    name="FLOW",
                    snippets=[
                        Snippet(
                            label="Process",
                            code="""@startuml
:start;
:message;
stop
@enduml""",
                            description="Specification lang",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Ditaa",
            icon="grid",
            color="text-green-600",
            subcategories=[
                SubCategory(
                    name="ASCII",
                    snippets=[
                        Snippet(
                            label="Blocks",
                            code="""@startditaa
+--------+   +-------+    +-------+
|        | --+ ditaa +--> |       |
|  Text  |   +-------+    |diagram|
|Document|   |!magic!|    |       |
|     {d}|   |       |    |       |
+---+----+   +-------+    +-------+
    :                         ^
    |       Lots of work      |
    +-------------------------+
@endditaa""",
                            description="ASCII art diagrams",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Gantt",
            icon="bar-chart-horizontal",
            color="text-blue-400",
            subcategories=[
                SubCategory(
                    name="PROJECT",
                    snippets=[
                        Snippet(
                            label="Timeline",
                            code="""@startgantt
[Prototype design] lasts 15 days
[Code prototype] lasts 10 days
[Write tests] lasts 5 days
[Code prototype] starts at [Prototype design]'s end
[Write tests] starts at [Code prototype]'s start
@endgantt""",
                            description="Project schedule",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Chronology",
            icon="calendar-clock",
            color="text-purple-600",
            subcategories=[
                SubCategory(
                    name="TIMELINE",
                    snippets=[
                        Snippet(
                            label="Events",
                            code="""@startuml
clock clk with period 1
binary "enable" as en

@0
en is low

@5
en is high

@10
en is low
@enduml""",
                            description="Chronological events (Timing)",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="MindMap",
            icon="brain-circuit",
            color="text-pink-500",
            subcategories=[
                SubCategory(
                    name="HIERARCHY",
                    snippets=[
                        Snippet(
                            label="Ideas",
                            code="""@startmindmap
* Root
** Idea 1
*** Sub Idea 1
** Idea 2
@endmindmap""",
                            description="Brainstorming",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="WBS",
            icon="workflow",
            color="text-orange-600",
            subcategories=[
                SubCategory(
                    name="WORK",
                    snippets=[
                        Snippet(
                            label="Breakdown",
                            code="""@startwbs
* Project
** Phase 1
*** Task 1
*** Task 2
** Phase 2
@endwbs""",
                            description="Work breakdown",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Mathematics",
            icon="sigma",
            color="text-gray-600",
            subcategories=[
                SubCategory(
                    name="FORMULAS",
                    snippets=[
                        Snippet(
                            label="AsciiMath",
                            code="""@startmath
f(t)=(a_0)/2 + sum_(n=1)^oo a_n cos((n pi t)/L) + sum_(n=1)^oo b_n \\sin((n pi t)/L)
@endmath""",
                            description="Mathematical equations",
                        )
                    ],
                )
            ],
        ),
        Category(
            name="Database (ER)",
            icon="database",
            color="text-indigo-500",
            subcategories=[
                SubCategory(
                    name="ENTITIES",
                    snippets=[
                        Snippet(
                            label="Basic Entity",
                            code="""@startuml
entity Table {
  * id: int <<PK>>
  --
  data: string
}
@enduml""",
                            description="Table definition",
                        ),
                        Snippet(
                            label="Relationships",
                            code="""@startuml
User ||--o{ Post : writes
@enduml""",
                            description="Cardinality notation",
                        ),
                    ],
                )
            ],
        ),
    ]

    @rx.event
    def toggle_sidebar(self):
        self.show_sidebar = not self.show_sidebar

    @rx.event
    def toggle_category(self, category_name: str):
        if category_name in self.expanded_categories:
            self.expanded_categories.remove(category_name)
        else:
            self.expanded_categories.append(category_name)

    @rx.event
    def set_layout(self, mode: str):
        self.layout_mode = mode

    @rx.event
    async def add_node(self, node_type: str):
        from codoc_in_plantuml.states.document_state import DocumentState

        doc = await self.get_state(DocumentState)
        doc.add_node(node_type)

    @rx.event
    async def delete_node(self, node_id: str):
        from codoc_in_plantuml.states.document_state import DocumentState

        doc = await self.get_state(DocumentState)
        doc.delete_node(node_id)

    @rx.event
    async def update_node_label(self, node_id: str, new_label: str):
        from codoc_in_plantuml.states.document_state import DocumentState

        doc = await self.get_state(DocumentState)
        doc.update_node_label(node_id, new_label)

    @rx.event
    def start_linking(self, node_id: str):
        if self.linking_source_id == node_id:
            self.linking_source_id = ""
        else:
            self.linking_source_id = node_id

    @rx.event
    async def complete_linking(self, target_id: str):
        if self.linking_source_id and self.linking_source_id != target_id:
            from codoc_in_plantuml.states.document_state import DocumentState

            doc = await self.get_state(DocumentState)
            doc.add_edge(self.linking_source_id, target_id)
        self.linking_source_id = ""

    @rx.event
    async def delete_edge(self, edge_id: str):
        from codoc_in_plantuml.states.document_state import DocumentState

        doc = await self.get_state(DocumentState)
        doc.delete_edge(edge_id)