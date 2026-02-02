import reflex as rx
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
        rx.cond(
            EditorState.tutorial_open,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Examples 教學",
                            class_name="text-base font-semibold text-gray-50",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-5 h-5 text-gray-200"),
                            on_click=EditorState.close_tutorial,
                            class_name="p-1.5 rounded hover:bg-white/10 transition-colors",
                            type="button",
                        ),
                        class_name="flex items-center justify-between px-5 py-4 border-b border-white/10 bg-[#2f343b]",
                    ),
                    rx.el.iframe(
                        src=f"/examples.html#{EditorState.tutorial_anchor}",
                        class_name="w-full h-full bg-[#111827]",
                    ),
                    class_name="w-[92vw] h-[88vh] max-w-[1200px] bg-[#2b2f36] border border-white/10 rounded-2xl overflow-hidden shadow-2xl",
                    on_click=rx.stop_propagation,
                ),
                on_click=EditorState.close_tutorial,
                class_name="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center",
            ),
        ),
        class_name="flex flex-col h-screen w-screen bg-gray-900 font-['Inter'] overflow-hidden",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
    ],
)
app.add_page(index, route="/", on_load=EditorState.on_load)
app.add_page(index, route="/doc/[share_id]", on_load=EditorState.on_load)