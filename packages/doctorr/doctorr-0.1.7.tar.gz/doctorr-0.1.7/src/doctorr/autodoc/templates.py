import contextvars
from functools import singledispatch

from doctorr.autodoc.docstring import (
    ProcessedClass,
    ProcessedFunction,
    ProcessedMethod,
    ProcessedPage,
    ProcessedProperty,
)

page_context_var = contextvars.ContextVar('page')

@singledispatch
def _render_element(processed_element, template_renderer) -> str:
    raise ValueError(f"Unsupported ProcessedElement type: {type(processed_element)}")


def format_user_import_path(user_import_path):
    if user_import_path:
        user_import_path += "."
    return user_import_path


def element_to_template_dict(processed_element):
    _page_context = page_context_var.get()
    user_import_path = format_user_import_path(
        _page_context.user_import_path 
    )
    return {
        "name": processed_element.name,
        "signature": getattr(processed_element, "signature", ""),
        "docstring": processed_element.docstring,
        "user_import_path": user_import_path,
    }


@_render_element.register(ProcessedClass)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "class.jinja2"
    rendered_members = [
        _render_element(member, renderer) for member in processed_element.members
    ]
    context["rendered_members"] = "".join(rendered_members)
    return renderer.render(template_name, context)


@_render_element.register(ProcessedFunction)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "function.jinja2"
    return renderer.render(template_name, context)


@_render_element.register(ProcessedMethod)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "method.jinja2"
    return renderer.render(template_name, context)


@_render_element.register(ProcessedProperty)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "property.jinja2"
    return renderer.render(template_name, context)


@_render_element.register(ProcessedPage)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "page.jinja2"
    rendered_content = [
        _render_element(piece_of_content, renderer)
        for piece_of_content in processed_element.content
    ]
    context["rendered_content"] = "".join(rendered_content)
    return renderer.render(template_name, context)


def render_page(page: ProcessedPage, renderer):
    page_context_var.set(page)
    return _render_element(page, renderer)
