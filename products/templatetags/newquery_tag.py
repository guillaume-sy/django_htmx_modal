import re
from collections import OrderedDict

from django import template
from django.core.exceptions import ImproperlyConfigured
from django.template import Node, TemplateSyntaxError
from django.utils.html import escape
from django.utils.http import urlencode

register = template.Library()
kwarg_re = re.compile(r"(?:(.+)=)?(.+)")
context_processor_error_msg = (
    "Tag {%% %s %%} requires django.template.context_processors.request to be "
    "in the template configuration in "
    "settings.TEMPLATES[]OPTIONS.context_processors) in order for the included "
    "template tags to function correctly."
)


def token_kwargs(bits, parser):
    """
    Based on Django's `~django.template.defaulttags.token_kwargs`, but with a
    few changes:

    - No legacy mode.
    - Both keys and values are compiled as a filter
    """
    if not bits:
        return {}
    kwargs = OrderedDict()
    while bits:
        match = kwarg_re.match(bits[0])
        if not match or not match.group(1):
            return kwargs
        key, value = match.groups()
        del bits[:1]
        kwargs[parser.compile_filter(key)] = parser.compile_filter(value)
    return kwargs


class QuerystringNode(Node):
    def __init__(self, updates, removals, asvar=None, modal_node=None):
        super().__init__()
        self.updates = updates
        self.removals = removals
        self.asvar = asvar
        # We initalize the Node with an additional parameter modal_node
        self.modal_node = modal_node

    def render(self, context):
        if "request" not in context:
            raise ImproperlyConfigured(context_processor_error_msg % "querystring")

        params = dict(context["request"].GET)
        for key, value in self.updates.items():
            if isinstance(key, str):
                params[key] = value
                continue
            key = key.resolve(context)
            value = value.resolve(context)
            if key not in ("", None):
                params[key] = value
        for removal in self.removals:
            params.pop(removal.resolve(context), None)

        value = escape("?" + urlencode(params, doseq=True))

        # if there is a modal_node, the modal_node is added to the returned query value
        if self.modal_node:
            value = str(self.modal_node) + value

        if self.asvar:
            context[str(self.asvar)] = value
            return ""
        else:
            return value


# {% querystring_upd "name"="abc" "age"=15 as=qs %}
@register.tag
def querystring_upd(parser, token):
    """
    Creates a URL (containing only the query string [including "?"]) derived
    from the current URL's query string, by updating it with the provided
    keyword arguments.

    Example (imagine URL is ``/abc/?gender=male&name=Brad``)::

        # {% querystring "name"="abc" "age"=15 %}
        ?name=abc&gender=male&age=15
        {% querystring "name"="Ayers" "age"=20 %}
        ?name=Ayers&gender=male&age=20
        {% querystring "name"="Ayers" without "gender" %}
        ?name=Ayers

    Additional parameter : if a modal_node sub domain is added to the tag, rewrite the url with another URL query
    """

    bits = token.split_contents()

    modal_sub_domain = None
    # if there is an additonal parameter modal_node indicated in the template tag indication,
    # this will be indicated from the token and attached as modal_sub_domain on the retuning value
    if len(bits) == 3:
        modal_sub_domain = bits[1]
        bits.pop(1)

    tag = bits.pop(0)
    updates = token_kwargs(bits, parser)

    asvar_key = None
    for key in updates:
        if str(key) == "as":
            asvar_key = key

    if asvar_key is not None:
        asvar = updates[asvar_key]
        del updates[asvar_key]
    else:
        asvar = None

    # ``bits`` should now be empty of a=b pairs, it should either be empty, or
    # have ``without`` arguments.
    if bits and bits.pop(0) != "without":
        raise TemplateSyntaxError("Malformed arguments to '%s'" % tag)
    removals = [parser.compile_filter(bit) for bit in bits]

    # modal_node is added here to the custom node
    return QuerystringNode(updates, removals, asvar=asvar, modal_node=modal_sub_domain)
