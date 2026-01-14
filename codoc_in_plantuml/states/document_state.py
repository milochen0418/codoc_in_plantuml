import reflex as rx
import random
import string
import asyncio
from typing import Any
from codoc_in_plantuml.utils.plantuml import PlantUML


class UserInfo(rx.Base):
    name: str
    color: str
    token: str


class DocumentState(rx.SharedState):
    _code: str = """@startuml
participant User
participant "Web App" as App
participant "PlantUML Server" as Server

User -> App: Type PlantUML code
activate App
App -> App: Detect diagram type
App -> Server: Send encoded text
activate Server
Server --> App: Return SVG image
deactivate Server
App --> User: Display Diagram
deactivate App
@enduml"""
    _diagram_type: str = "Sequence"
    _visual_nodes: list[dict[str, str]] = []
    _visual_edges: list[dict[str, str]] = []
    _users: dict[str, UserInfo] = {}

    @rx.var
    def code(self) -> str:
        return self._code

    @rx.var
    def diagram_type(self) -> str:
        return self._diagram_type

    @rx.var
    def visual_nodes(self) -> list[dict[str, str]]:
        return self._visual_nodes

    @rx.var
    def visual_edges(self) -> list[dict[str, str]]:
        return self._visual_edges

    @rx.var
    def active_users(self) -> list[UserInfo]:
        return list(self._users.values())

    @rx.var
    def diagram_url(self) -> str:
        format_type = "svg"
        if "@startditaa" in self._code.lower():
            format_type = "png"
        return PlantUML.get_url(self._code, format=format_type)

    def _get_user_color(self) -> str:
        colors = [
            "bg-red-500",
            "bg-orange-500",
            "bg-amber-500",
            "bg-yellow-500",
            "bg-lime-500",
            "bg-green-500",
            "bg-emerald-500",
            "bg-teal-500",
            "bg-cyan-500",
            "bg-sky-500",
            "bg-blue-500",
            "bg-indigo-500",
            "bg-violet-500",
            "bg-purple-500",
            "bg-fuchsia-500",
            "bg-pink-500",
            "bg-rose-500",
        ]
        return random.choice(colors)

    @rx.event
    async def join_room(self):
        token = self.router.session.client_token
        if token not in self._users:
            adjectives = [
                "Swift",
                "Calm",
                "Bright",
                "Eager",
                "Merry",
                "Witty",
                "Brave",
                "Jolly",
                "Kind",
            ]
            nouns = [
                "Fox",
                "Bear",
                "Owl",
                "Cat",
                "Dog",
                "Lion",
                "Tiger",
                "Hawk",
                "Wolf",
            ]
            name = f"{random.choice(adjectives)} {random.choice(nouns)}"
            self._users[token] = UserInfo(
                name=name, color=self._get_user_color(), token=token
            )

    @rx.event
    def update_code(self, new_code: str):
        self._code = new_code
        self.detect_type(new_code)

    @rx.event
    def detect_type(self, code: str):
        code_lower = code.lower()
        if (
            "participant" in code_lower
            or "sequence" in code_lower
            or "->" in code_lower
        ):
            self._diagram_type = "Sequence"
        elif "class" in code_lower or "interface" in code_lower:
            self._diagram_type = "Class"
        elif "usecase" in code_lower or "actor" in code_lower:
            self._diagram_type = "Use Case"
        elif "activity" in code_lower or ":start" in code_lower or "fork" in code_lower:
            self._diagram_type = "Activity"
        elif "state" in code_lower or "[*]" in code_lower:
            self._diagram_type = "State"
        elif "component" in code_lower or "database" in code_lower:
            self._diagram_type = "Component"
        elif "json" in code_lower:
            self._diagram_type = "JSON"
        elif "yaml" in code_lower:
            self._diagram_type = "YAML"
        elif "mindmap" in code_lower:
            self._diagram_type = "MindMap"
        elif "gantt" in code_lower:
            self._diagram_type = "Gantt"
        else:
            self._diagram_type = "Unknown"

    @rx.event
    def handle_drop(self, item: dict):
        new_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self._visual_nodes.append(
            {
                "id": f"{item['type']}_{new_id}",
                "type": item["type"],
                "label": item["type"].title(),
            }
        )

    @rx.event
    def delete_node(self, node_id: str):
        self._visual_nodes = [n for n in self._visual_nodes if n["id"] != node_id]
        self._visual_edges = [
            e
            for e in self._visual_edges
            if e["source"] != node_id and e["target"] != node_id
        ]

    @rx.event
    def update_node_label(self, node_id: str, new_label: str):
        for node in self._visual_nodes:
            if node["id"] == node_id:
                node["label"] = new_label
                break

    @rx.event
    def add_edge(self, source: str, target: str):
        edge_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self._visual_edges.append({"id": edge_id, "source": source, "target": target})

    @rx.event
    def delete_edge(self, edge_id: str):
        self._visual_edges = [e for e in self._visual_edges if e["id"] != edge_id]