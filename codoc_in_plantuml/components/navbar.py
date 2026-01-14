import reflex as rx
from codoc_in_plantuml.states.editor_state import EditorState
from codoc_in_plantuml.states.document_state import DocumentState, UserInfo


def user_avatar(user: UserInfo) -> rx.Component:
    return rx.tooltip(
        rx.el.div(
            rx.el.span(
                user.name.split(" ")[0][0] + user.name.split(" ")[1][0],
                class_name="text-[10px] font-bold text-white leading-none",
            ),
            class_name=f"w-7 h-7 rounded-full flex items-center justify-center {user.color} border-2 border-[#1e1e1e] ring-1 ring-white/10",
        ),
        content=user.name,
    )


def layout_toggle_button(icon: str, mode: str, tooltip: str) -> rx.Component:
    return rx.el.button(
        rx.tooltip(rx.icon(icon, class_name="w-4 h-4"), content=tooltip),
        on_click=lambda: EditorState.set_layout(mode),
        class_name=rx.cond(
            EditorState.layout_mode == mode,
            "p-2 rounded-md bg-emerald-500/20 text-emerald-400",
            "p-2 rounded-md text-gray-400 hover:text-white hover:bg-[#333]",
        )
        + " transition-colors",
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("panel-left-open", class_name="w-5 h-5 text-gray-400"),
                    on_click=EditorState.toggle_sidebar,
                    class_name=rx.cond(
                        EditorState.show_sidebar,
                        "p-2 mr-2 rounded-md bg-[#333] text-white hover:bg-[#444]",
                        "p-2 mr-2 rounded-md text-gray-400 hover:text-white hover:bg-[#333]",
                    )
                    + " transition-colors",
                ),
                rx.icon("flower-2", class_name="w-6 h-6 text-emerald-400"),
                rx.el.h1("PlantUML", class_name="text-lg font-bold text-gray-100"),
                rx.el.span(
                    "Live Editor", class_name="text-lg font-light text-gray-400 ml-1"
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.div(
                    layout_toggle_button(
                        "panel-left", "maximize_editor", "Focus Editor"
                    ),
                    layout_toggle_button("columns-2", "split", "Split View"),
                    layout_toggle_button(
                        "panel-right", "maximize_preview", "Focus Preview"
                    ),
                    class_name="flex items-center gap-1 bg-[#252526] border border-[#333] rounded-lg p-0.5",
                ),
                rx.el.div(
                    rx.el.span(
                        rx.icon("file-code", class_name="w-4 h-4 mr-1.5"),
                        DocumentState.diagram_type,
                        class_name="flex items-center text-xs font-semibold tracking-wide uppercase whitespace-nowrap",
                    ),
                    class_name=rx.cond(
                        DocumentState.diagram_type == "Sequence",
                        "bg-blue-500/20 text-blue-300 border-blue-500/30",
                        rx.cond(
                            DocumentState.diagram_type == "Class",
                            "bg-orange-500/20 text-orange-300 border-orange-500/30",
                            rx.cond(
                                DocumentState.diagram_type == "State",
                                "bg-purple-500/20 text-purple-300 border-purple-500/30",
                                rx.cond(
                                    DocumentState.diagram_type == "Activity",
                                    "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
                                    "bg-gray-700/20 text-gray-300 border-gray-600/30",
                                ),
                            ),
                        ),
                    )
                    + " px-3 py-1.5 rounded-lg border backdrop-blur-sm transition-all duration-300 w-fit",
                ),
                class_name="flex items-center flex-row gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(DocumentState.active_users, user_avatar),
                    class_name="flex items-center -space-x-2 mr-4",
                ),
                rx.el.button(
                    rx.icon("share-2", class_name="w-4 h-4 mr-2"),
                    "Share",
                    on_click=EditorState.copy_link,
                    class_name="flex items-center px-3 py-1.5 text-xs font-medium bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors",
                ),
                rx.el.div(class_name="w-px h-6 bg-[#333] mx-4"),
                rx.el.a(
                    rx.icon(
                        "github",
                        class_name="w-5 h-5 text-gray-400 hover:text-white transition-colors",
                    ),
                    href="https://github.com/plantuml/plantuml",
                    target="_blank",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between w-full max-w-[1920px] mx-auto",
        ),
        class_name="w-full bg-[#1e1e1e] border-b border-[#333] px-6 py-3 select-none",
    )