import reflex as rx
import reflex_enterprise as rxe
from codoc_in_plantuml.components.navbar import navbar
from codoc_in_plantuml.components.editor_pane import editor_pane
from codoc_in_plantuml.components.preview_pane import preview_pane
from codoc_in_plantuml.components.help_sidebar import help_sidebar
from codoc_in_plantuml.components.visual_editor import visual_editor
from codoc_in_plantuml.states.editor_state import EditorState


def index() -> rx.Component:
    _ = visual_editor
    return rx.el.div(
        rx.el.style("""
            .custom-scrollbar::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            .custom-scrollbar::-webkit-scrollbar-track {
                background: #f1f1f1;
            }
            .custom-scrollbar::-webkit-scrollbar-thumb {
                background: #ccc;
                border-radius: 5px;
            }
            .custom-scrollbar::-webkit-scrollbar-thumb:hover {
                background: #bbb;
            }
            """),
        navbar(),
        rx.el.div(
            help_sidebar(),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        editor_pane(),
                        class_name=rx.cond(
                            EditorState.layout_mode == "maximize_preview",
                            "hidden",
                            rx.cond(
                                EditorState.layout_mode == "maximize_editor",
                                "w-full",
                                "w-1/2",
                            ),
                        )
                        + " h-full transition-all duration-300 ease-in-out",
                    ),
                    rx.el.div(
                        preview_pane(),
                        class_name=rx.cond(
                            EditorState.layout_mode == "maximize_editor",
                            "hidden",
                            rx.cond(
                                EditorState.layout_mode == "maximize_preview",
                                "w-full",
                                "w-1/2",
                            ),
                        )
                        + " h-full transition-all duration-300 ease-in-out border-l border-gray-200",
                    ),
                    class_name="flex flex-row h-full w-full overflow-hidden relative",
                ),
                class_name="w-full h-full overflow-hidden",
            ),
            class_name="flex flex-row h-[calc(100vh-64px)] w-full overflow-hidden",
        ),
        class_name="flex flex-col h-screen w-screen bg-gray-900 font-['Inter'] overflow-hidden",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
    ],
)
app.add_page(index, route="/", on_load=EditorState.on_load)
app.add_page(index, route="/doc/[share_id]", on_load=EditorState.on_load)