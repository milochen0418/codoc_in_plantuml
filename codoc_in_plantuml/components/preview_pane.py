import reflex as rx
from codoc_in_plantuml.states.editor_state import EditorState
from codoc_in_plantuml.states.document_state import DocumentState


def preview_pane() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("image", class_name="w-4 h-4 text-gray-500"),
                rx.el.span(
                    "Live Preview", class_name="text-sm font-semibold text-gray-700"
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between px-4 py-3 bg-gray-50 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.img(
                        src=DocumentState.diagram_url,
                        class_name="max-w-none shadow-sm rounded bg-white",
                        draggable=False,
                    ),
                    class_name="inline-block p-8 min-w-full min-h-full flex items-center justify-center",
                ),
                class_name="h-full w-full flex items-center justify-center",
            ),
            class_name="flex-1 overflow-auto bg-[url('/grid-pattern.svg')] bg-gray-100 relative custom-scrollbar",
        ),
        class_name="flex flex-col h-full w-full bg-gray-50",
    )