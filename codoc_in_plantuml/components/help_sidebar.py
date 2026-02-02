import reflex as rx
from codoc_in_plantuml.states.editor_state import EditorState, Category, Snippet, SubCategory
from codoc_in_plantuml.states.document_state import DocumentState


def snippet_button(snippet: Snippet, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.el.span(
                    snippet.label, class_name="text-xs font-semibold text-gray-200"
                ),
                rx.el.span(
                    snippet.description,
                    class_name="text-[10px] text-gray-500 truncate w-full text-left",
                ),
                class_name="flex flex-col items-start gap-0.5 overflow-hidden",
            ),
            rx.icon(
                "play",
                class_name=f"w-3 h-3 {color_class} opacity-0 group-hover:opacity-100 transition-opacity absolute right-2 top-1/2 -translate-y-1/2",
            ),
            on_click=DocumentState.update_code(snippet.code),
            class_name="group relative w-full p-2 rounded bg-[#252526] hover:bg-[#2a2d2e] border border-[#333] hover:border-gray-600 transition-all duration-200 text-left",
            type="button",
        ),
        rx.el.div(
            rx.el.button(
                "?",
                on_click=EditorState.open_tutorial(snippet.anchor),
                class_name="inline-flex items-center justify-center w-5 h-5 text-[11px] font-bold text-gray-300 bg-[#2a2d2e] border border-[#3a3a3a] rounded-full hover:text-white hover:border-gray-500 transition-colors",
                aria_label="Usage help",
                type="button",
            ),
            rx.el.div(
                rx.el.p(
                    snippet.description,
                    class_name="text-xs text-gray-200 mb-2",
                ),
                class_name="absolute right-full top-1/2 -translate-y-1/2 mr-3 z-50 opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity duration-200 [transition-delay:100ms] group-hover:[transition-delay:0ms] bg-[#1f1f1f] border border-[#333] rounded-lg p-3 shadow-lg max-w-[220px]",
            ),
            class_name="relative group",
        ),
        class_name="flex items-center gap-2",
    )


def subcategory_section(subcategory: SubCategory, parent_color: str) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.el.span(
                    subcategory.name,
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.icon(
                "chevron-down",
                class_name=rx.cond(
                    EditorState.expanded_categories.contains(subcategory.name),
                    "w-3 h-3 text-gray-600 transition-transform duration-200",
                    "w-3 h-3 text-gray-600 -rotate-90 transition-transform duration-200",
                ),
            ),
            on_click=lambda: EditorState.toggle_category(subcategory.name),
            class_name="flex items-center justify-between w-full mt-2 mb-1 px-2 py-1 hover:bg-[#2a2d2e] rounded transition-colors cursor-pointer",
        ),
        rx.cond(
            EditorState.expanded_categories.contains(subcategory.name),
            rx.el.div(
                rx.foreach(
                    subcategory.snippets, lambda s: snippet_button(s, parent_color)
                ),
                class_name="grid grid-cols-1 gap-1.5 pl-3 border-l border-[#333] ml-1 animate-in slide-in-from-top-1 duration-150",
            ),
        ),
        class_name="flex flex-col",
    )


def category_section(category: Category) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon(category.icon, class_name=f"w-4 h-4 {category.color}"),
                rx.el.span(
                    category.name, class_name="text-sm font-medium text-gray-300"
                ),
                class_name="flex items-center gap-2",
            ),
            rx.icon(
                "chevron-down",
                class_name=rx.cond(
                    EditorState.expanded_categories.contains(category.name),
                    "w-4 h-4 text-gray-500 transition-transform duration-200",
                    "w-4 h-4 text-gray-500 -rotate-90 transition-transform duration-200",
                ),
            ),
            on_click=lambda: EditorState.toggle_category(category.name),
            class_name="flex items-center justify-between w-full mb-1 px-1 hover:bg-[#2a2d2e] p-1.5 rounded transition-colors cursor-pointer",
        ),
        rx.cond(
            EditorState.expanded_categories.contains(category.name),
            rx.el.div(
                rx.foreach(
                    category.snippets, lambda s: snippet_button(s, category.color)
                ),
                rx.foreach(
                    category.subcategories,
                    lambda sc: subcategory_section(sc, category.color),
                ),
                class_name="flex flex-col gap-1.5 pl-2 animate-in slide-in-from-top-2 duration-200",
            ),
        ),
        class_name="flex flex-col mb-4",
    )


def help_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.span("Examples & Help", class_name="font-semibold text-gray-100"),
                rx.el.button(
                    rx.icon("x", class_name="w-4 h-4 text-gray-400 hover:text-white"),
                    on_click=EditorState.toggle_sidebar,
                    class_name="p-1 rounded hover:bg-[#333] transition-colors",
                ),
                class_name="flex items-center justify-between p-4 border-b border-[#333] bg-[#1e1e1e] sticky top-0 z-10",
            ),
            rx.el.div(
                rx.foreach(EditorState.snippet_categories, category_section),
                class_name="p-4 overflow-y-auto custom-scrollbar flex-1",
            ),
            class_name="flex flex-col h-full w-full",
        ),
        class_name=rx.cond(
            EditorState.show_sidebar,
            "w-72 border-r border-[#333] bg-[#1e1e1e] flex flex-col h-full shrink-0 transition-all duration-300 ease-in-out",
            "w-0 overflow-hidden border-0 bg-[#1e1e1e] flex flex-col h-full shrink-0 transition-all duration-300 ease-in-out",
        ),
    )