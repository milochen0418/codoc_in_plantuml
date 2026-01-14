import reflex as rx
from codoc_in_plantuml.states.editor_state import EditorState
from codoc_in_plantuml.states.document_state import DocumentState


def palette_item(label: str, icon: str, type_id: str, color: str) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 {color}"),
            rx.el.span(label, class_name="text-sm font-medium text-gray-700"),
            class_name="flex items-center gap-3",
        ),
        on_click=lambda: EditorState.add_node(type_id),
        class_name="w-full text-left p-3 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md cursor-pointer transition-all hover:border-indigo-300",
        type="button",
    )


@rx.memo
def node_card(node: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("grip-vertical", class_name="w-4 h-4 text-gray-400 mr-2"),
            rx.el.span(
                node["type"],
                class_name="text-[10px] uppercase tracking-wider font-bold text-gray-400 select-none",
            ),
            rx.el.button(
                rx.icon("x", class_name="w-3 h-3"),
                on_click=lambda: EditorState.delete_node(node["id"]),
                class_name="ml-auto text-gray-400 hover:text-red-500 p-1 rounded hover:bg-red-50 transition-colors",
            ),
            class_name="flex items-center w-full mb-2",
        ),
        rx.el.input(
            default_value=node["label"],
            on_blur=lambda v: EditorState.update_node_label(node["id"], v),
            class_name="w-full text-sm font-semibold bg-transparent border-b border-transparent hover:border-gray-300 focus:border-indigo-500 focus:outline-none px-1 py-0.5 transition-colors",
        ),
        rx.el.div(
            rx.cond(
                EditorState.linking_source_id == node["id"],
                rx.el.button(
                    "Cancel Link",
                    on_click=EditorState.start_linking(node["id"]),
                    class_name="text-xs w-full mt-3 py-1.5 px-2 bg-red-100 text-red-600 rounded hover:bg-red-200 transition-colors font-medium",
                ),
                rx.cond(
                    EditorState.linking_source_id != "",
                    rx.el.button(
                        "Link Here",
                        on_click=EditorState.complete_linking(node["id"]),
                        class_name="text-xs w-full mt-3 py-1.5 px-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors font-medium shadow-sm",
                    ),
                    rx.el.button(
                        "Connect",
                        on_click=EditorState.start_linking(node["id"]),
                        class_name="text-xs w-full mt-3 py-1.5 px-2 bg-gray-100 text-gray-600 rounded hover:bg-gray-200 transition-colors font-medium",
                    ),
                ),
            )
        ),
        class_name=rx.cond(
            EditorState.linking_source_id == node["id"],
            "ring-2 ring-indigo-500 ring-offset-2",
            "hover:border-indigo-300",
        )
        + " flex flex-col p-3 bg-white rounded-xl border border-gray-200 shadow-sm w-48 transition-all duration-200 animate-in zoom-in-95",
    )


def edge_item(edge: dict) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            edge["source"].split("_")[-1],
            class_name="text-xs font-mono text-gray-500 bg-gray-100 px-1 rounded",
        ),
        rx.icon("arrow-right", class_name="w-3 h-3 text-gray-400"),
        rx.el.span(
            edge["target"].split("_")[-1],
            class_name="text-xs font-mono text-gray-500 bg-gray-100 px-1 rounded",
        ),
        rx.el.button(
            rx.icon("trash-2", class_name="w-3 h-3"),
            on_click=lambda: EditorState.delete_edge(edge["id"]),
            class_name="ml-auto text-gray-400 hover:text-red-500 p-1 rounded hover:bg-red-50",
        ),
        class_name="flex items-center gap-2 p-2 bg-white border border-gray-100 rounded-lg text-sm",
    )


def visual_editor() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Elements",
                class_name="text-xs font-bold text-gray-400 uppercase mb-4 tracking-wider",
            ),
            rx.el.div(
                palette_item("Class", "box", "class", "text-orange-500"),
                palette_item("Interface", "circle", "interface", "text-purple-500"),
                palette_item("Actor", "user", "actor", "text-blue-500"),
                palette_item("Component", "package", "component", "text-emerald-500"),
                palette_item("Use Case", "circle", "usecase", "text-yellow-500"),
                palette_item("Database", "database", "database", "text-indigo-500"),
                palette_item("State", "circle-dot", "state", "text-red-500"),
                class_name="flex flex-col gap-2",
            ),
            rx.el.div(
                rx.el.h2(
                    "Connections",
                    class_name="text-xs font-bold text-gray-400 uppercase mt-8 mb-4 tracking-wider",
                ),
                rx.el.div(
                    rx.foreach(DocumentState.visual_edges, edge_item),
                    class_name="flex flex-col gap-2 overflow-y-auto max-h-[300px] custom-scrollbar",
                ),
                class_name="flex flex-col",
            ),
            class_name="w-64 bg-gray-50 border-r border-gray-200 p-4 flex flex-col h-full overflow-y-auto",
        ),
        rx.el.div(
            rx.cond(
                DocumentState.visual_nodes.length() == 0,
                rx.el.div(
                    rx.icon(
                        "mouse-pointer-click",
                        class_name="w-12 h-12 text-gray-300 mb-4",
                    ),
                    rx.el.p(
                        "Click an element on the left to add it here",
                        class_name="text-gray-400 font-medium",
                    ),
                    class_name="flex flex-col items-center justify-center h-full border-2 border-dashed border-gray-200 rounded-xl m-8",
                ),
                rx.el.div(
                    rx.foreach(
                        DocumentState.visual_nodes,
                        lambda node: node_card(node=node, key=node["id"]),
                    ),
                    class_name="flex flex-wrap content-start gap-4 p-8 w-full h-full align-start",
                ),
            ),
            class_name="bg-white w-full h-full transition-all duration-200",
        ),
        class_name="flex flex-row w-full h-full bg-white",
    )