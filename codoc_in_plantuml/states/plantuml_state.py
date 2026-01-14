import reflex as rx
import zlib
import base64
import logging
from typing import TypedDict, Optional, Any
import time
import random
import string


def plantuml_encode(text: str) -> str:
    """Encode PlantUML source to URL-safe format for the public server."""
    if not text:
        return ""
    plantuml_alphabet = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    )
    standard_alphabet = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    )
    try:
        compressed = zlib.compress(text.encode("utf-8"), 9)[2:-4]
    except Exception as e:
        logging.exception(f"Error compressing PlantUML text: {e}")
        return ""
    encoded = base64.b64encode(compressed).decode("ascii")
    result = ""
    for char in encoded:
        if char == "=":
            continue
        try:
            idx = standard_alphabet.index(char)
            result += plantuml_alphabet[idx]
        except ValueError as e:
            logging.exception(f"Error mapping character during PlantUML encoding: {e}")
            continue
    return result


class VisualNode(TypedDict):
    id: str
    type: str
    label: str
    x: int
    y: int


class VisualConnection(TypedDict):
    id: str
    from_id: str
    to_id: str
    label: str


class PlantUMLState(rx.State):
    visual_mode: bool = False
    visual_nodes: list[VisualNode] = []
    visual_connections: list[VisualConnection] = []
    mouse_x: int = 0
    mouse_y: int = 0
    connection_start_node_id: str | None = None
    code: str = """@startuml
Alice -> Bob: Hello Bob!
Bob --> Alice: Hello Alice!
@enduml"""
    diagram_type: str = "Sequence"
    templates: dict[str, str] = {
        "Sequence": """@startuml
actor User
participant "First Class" as A
participant "Second Class" as B

User -> A: DoWork
activate A

A -> B: Create Request
activate B

B --> A: Request Created
deactivate B

A --> User: Done
deactivate A
@enduml""",
        "Use Case": """@startuml
left to right direction
actor "Food Critic" as fc
rectangle Restaurant {
  usecase "Eat Food" as UC1
  usecase "Pay for Food" as UC2
  usecase "Drink" as UC3
}
fc --> UC1
fc --> UC2
fc --> UC3
@enduml""",
        "Class": """@startuml
class Car {
  - engine: Engine
  + start(): void
  + stop(): void
}

class Engine {
  - power: int
  + start(): void
}

Car *-- Engine
@enduml""",
        "Activity": """@startuml
start
:Hello world;
:This is defined on
multiple lines;
stop
@enduml""",
        "Component": """@startuml
package "Some Group" {
  HTTP - [First Component]
  [Another Component]
}

node "Other Groups" {
  FTP - [Second Component]
  [First Component] --> FTP
} 
@enduml""",
        "State": """@startuml
[*] --> State1
State1 --> [*]
State1 : this is a string
State1 : this is another string

State1 -> State2
State2 --> [*]
@enduml""",
        "Object": """@startuml
object Object01
object Object02
object Object03

Object01 <|-- Object02
Object03 *-- Object01
@enduml""",
    }

    @rx.var
    def encoded_url(self) -> str:
        """Computed var that returns the full URL for the image."""
        if not self.code:
            return ""
        encoded = plantuml_encode(self.code)
        return f"http://www.plantuml.com/plantuml/svg/{encoded}"

    @rx.var
    def detected_type(self) -> str:
        """Simple heuristic to detect diagram type."""
        code_lower = self.code.lower()
        if "class " in code_lower:
            return "Class"
        elif (
            "actor " in code_lower or "participant " in code_lower or "->" in code_lower
        ):
            return "Sequence"
        elif "usecase " in code_lower:
            return "Use Case"
        elif "start" in code_lower and "stop" in code_lower:
            return "Activity"
        elif "package " in code_lower or "node " in code_lower:
            return "Component"
        elif "[*]" in code_lower:
            return "State"
        elif "object " in code_lower:
            return "Object"
        return "Unknown"

    sidebar_open: bool = False
    is_confirming_clear: bool = False

    @rx.var
    def source_data_uri(self) -> str:
        """Generate a Data URI for downloading the source code."""
        b64_code = base64.b64encode(self.code.encode("utf-8")).decode("ascii")
        return f"data:text/plain;base64,{b64_code}"

    @rx.var
    def template_list(self) -> list[dict[str, str]]:
        """Return list of templates with metadata for the sidebar."""
        descriptions = {
            "Sequence": "Interactions between objects over time",
            "Use Case": "System functionality and actors",
            "Class": "Static structure and relationships",
            "Activity": "Workflows and logic flow",
            "Component": "Physical system components",
            "State": "State transitions of an object",
            "Object": "Instance view of a system",
        }
        return [
            {"name": name, "description": descriptions.get(name, "Diagram template")}
            for name in self.templates.keys()
        ]

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def set_sidebar(self, value: bool):
        self.sidebar_open = value

    @rx.event
    def set_template(self, template_name: str):
        """Set the code editor to a specific template."""
        if template_name in self.templates:
            self.code = self.templates[template_name]
            self.diagram_type = template_name
            self.sidebar_open = False

    @rx.event
    def update_code(self, new_code: str):
        self.code = new_code
        self.is_confirming_clear = False

    @rx.event
    def copy_to_clipboard(self):
        yield rx.set_clipboard(self.code)
        yield rx.toast("Code copied to clipboard!", duration=2000)

    @rx.event
    def request_clear(self):
        self.is_confirming_clear = True

    @rx.event
    def cancel_clear(self):
        self.is_confirming_clear = False

    @rx.event
    def confirm_clear(self):
        self.code = """@startuml

@enduml"""
        self.visual_nodes = []
        self.visual_connections = []
        self.is_confirming_clear = False

    @rx.event
    def toggle_visual_mode(self):
        self.visual_mode = not self.visual_mode

    @rx.event
    def update_mouse_pos(self, mouse_data: dict[str, int]):
        self.mouse_x = mouse_data.get("clientX", 0)
        self.mouse_y = mouse_data.get("clientY", 0)

    @rx.event
    def handle_canvas_drop(self, item: dict[str, Any]):
        """Handle dropping a node onto the canvas."""
        if "id" in item and (not item.get("is_new", False)):
            node_id = item["id"]
            new_nodes = []
            for node in self.visual_nodes:
                if node["id"] == node_id:
                    node["x"] = max(0, self.mouse_x - 60)
                    node["y"] = max(0, self.mouse_y - 40)
                new_nodes.append(node)
            self.visual_nodes = new_nodes
        elif "type" in item:
            unique_id = "".join(random.choices(string.ascii_lowercase, k=6))
            new_node: VisualNode = {
                "id": unique_id,
                "type": item["type"],
                "label": item.get("label", item["type"]),
                "x": max(0, self.mouse_x - 60),
                "y": max(0, self.mouse_y - 40),
            }
            self.visual_nodes.append(new_node)
        self.regenerate_code_from_visual()

    @rx.event
    def handle_node_click(self, node_id: str):
        """Handle clicking a node to start or end a connection."""
        if self.connection_start_node_id is None:
            self.connection_start_node_id = node_id
            yield rx.toast("Select another node to connect")
        else:
            if self.connection_start_node_id != node_id:
                exists = False
                for conn in self.visual_connections:
                    if (
                        conn["from_id"] == self.connection_start_node_id
                        and conn["to_id"] == node_id
                    ):
                        exists = True
                        break
                if not exists:
                    conn_id = "".join(random.choices(string.ascii_lowercase, k=6))
                    new_conn: VisualConnection = {
                        "id": conn_id,
                        "from_id": self.connection_start_node_id,
                        "to_id": node_id,
                        "label": "",
                    }
                    self.visual_connections.append(new_conn)
                    self.regenerate_code_from_visual()
            self.connection_start_node_id = None

    @rx.event
    def delete_node(self, node_id: str):
        """Delete a node and its connections."""
        self.visual_nodes = [n for n in self.visual_nodes if n["id"] != node_id]
        self.visual_connections = [
            c
            for c in self.visual_connections
            if c["from_id"] != node_id and c["to_id"] != node_id
        ]
        self.regenerate_code_from_visual()

    @rx.event
    def update_node_label(self, node_id: str, new_label: str):
        new_nodes = []
        for node in self.visual_nodes:
            if node["id"] == node_id:
                node["label"] = new_label
            new_nodes.append(node)
        self.visual_nodes = new_nodes
        self.regenerate_code_from_visual()

    @rx.event
    def regenerate_code_from_visual(self):
        """Generate PlantUML code from visual state."""
        lines = ["@startuml"]
        for node in self.visual_nodes:
            safe_label = node["label"].replace('"', "")
            node_type = node["type"]
            if node_type == "actor":
                lines.append(f'''actor "{safe_label}" as {node["id"]}''')
            elif node_type == "usecase":
                lines.append(f'''usecase "{safe_label}" as {node["id"]}''')
            elif node_type == "component":
                lines.append(f'''component "{safe_label}" as {node["id"]}''')
            elif node_type == "state":
                lines.append(f'''state "{safe_label}" as {node["id"]}''')
            elif node_type == "class":
                lines.append(f'''class "{safe_label}" as {node["id"]}''')
            else:
                lines.append(f'''rectangle "{safe_label}" as {node["id"]}''')
        lines.append("")
        for conn in self.visual_connections:
            lines.append(f"{conn['from_id']} --> {conn['to_id']}")
        lines.append("@enduml")
        self.code = """
""".join(lines)