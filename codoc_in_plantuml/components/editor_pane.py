import reflex as rx
import reflex_monaco
from codoc_in_plantuml.states.editor_state import EditorState
from codoc_in_plantuml.states.document_state import DocumentState


def editor_pane() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("file_code_2", class_name="w-4 h-4 text-gray-400"),
                rx.el.span(
                    "Source Code", class_name="text-sm font-semibold text-gray-300"
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between px-4 py-3 bg-[#252526] border-b border-[#333]",
        ),
        rx.el.div(
            reflex_monaco.monaco(
                value=DocumentState.code,
                on_change=DocumentState.update_code.debounce(500),
                language="plantuml",
                theme="vs-dark",
                options={
                    "minimap": {"enabled": False},
                    "fontSize": 14,
                    "fontFamily": "'JetBrains Mono', 'Fira Code', Consolas, monospace",
                    "lineNumbers": "on",
                    "scrollBeyondLastLine": False,
                    "automaticLayout": True,
                    "padding": {"top": 16, "bottom": 16},
                },
                height="100%",
                width="100%",
            ),
            class_name="flex-1 min-h-0 bg-[#1e1e1e]",
        ),
        class_name="flex flex-col h-full w-full border-r border-[#333]",
    )