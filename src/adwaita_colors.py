#!/usr/bin/env python3
from xml.etree.ElementTree import ElementTree, parse as parse_xml


# https://gitlab.gnome.org/GNOME/gtksourceview/-/tree/master/tests/syntax-highlighting/
# https://gitlab.gnome.org/GNOME/gtksourceview/-/blob/master/data/language-specs/
MAP = {
    'text': [''],  # default color
    # 'def:base-n-integer': [],
    'def:boolean': [
        'constant.language'
    ],
    'def:comment': [
        'comment',
        'entity.other.document.begin.yaml',  # ---
        'entity.other.document.end.yaml'  # ...
    ],
    'def:constant': [
        # 'constant', # also applies to CAPS_VARIABLES
        'support.type.property-name',
        'source.css constant keyword.other.unit',
        'support.constant.property-value.css'
    ],
    'def:decimal': [
        'constant.numeric'
    ],
    # 'def:deletion': [],
    'def:doc-comment-element': [
        'comment.block.documentation'
    ],
    'def:floating-point': [
        'constant.numeric.float'
    ],
    # gtksv is being inconstistent here, e.g. this applies to function names in definitions in
    # Python, but not in C or JS. I say less color is better than more color, so these are commented out.
    'def:function': [
        # 'meta.function entity.name.function',
        # 'meta.function.python support.function.magic.python'  # __init__, __getitem__, etc
    ],
    'def:heading': [
        'markup.heading.markdown'
    ],
    'def:keyword': [
        # most keywords (operators will be unstyled in EXTRA_RULES)
        'keyword',
        # specifically include alphabetical operators
        'keyword.operator.logical.python',  # and, or
        'source.js keyword.operator.expression',  # typeof, instanceof
        'source.ts keyword.operator.expression',
        'keyword.operator.new',  # new
        # →const← name = value;
        # →class← Class: ...
        # →def← fn(): ...
        'storage.type',
        # →static← void Main(string[] args)
        'storage.modifier',
        # key names in YAML
        'entity.name.tag.yaml'
    ],
    # 'def:link-destination': [],
    # 'def:link-text': [],
    # 'def:list-marker': [],
    # 'def:net-address': [],
    'def:number': [
        'constant.numeric'
    ],
    'def:preformatted-section': [],
    'def:preprocessor': [
        'meta.preprocessor',
        # →#include← <config.h>
        'meta.preprocessor keyword.control',
        # @decorator
        'entity.name.function.decorator',
        # @media in CSS
        'keyword.control.at-rule.media.css',
        # &amp;
        'constant.character.entity',
        # ${} in JS
        'punctuation.definition.template-expression',
        # ${} in Nix
        'punctuation.section.embedded'
    ],
    'def:shebang': [
        'comment.line.number-sign.shebang'
    ],
    'def:special-char': [
        # \n
        'constant.character.escape'
    ],
    'def:string': [
        'string'
    ],
    'def:strong-emphasis': [
        'markup.bold.markdown'
    ],
    'def:type': [
        'support.type',
        'keyword.type.cs',
        'source.go storage.type',
        # JS built-in constructors
        'support.class.builtin.js',
        'support.class.promise'
    ],
    # 'def:underlined': [],
    # 'def:warning': [],

    # 'c-sharp:format': [],
    'c-sharp:preprocessor': [
        'meta.preprocessor.cs'
    ],

    'c:printf': [
        # %s
        'string constant.other.placeholder'
    ],
    # 'c:signal-name': [],
    'c:storage-class': [
        # →const← char *var_name = ...
        'source.c storage.modifier'
    ],
    'c:type-keyword': [
        'source.c storage.type'
    ],

    'css:id-selector': [
        'entity.other.attribute-name.id.css'
    ],
    'css:property-name': [
        'support.type.property-name.css'
    ],
    'css:pseudo-selector': [
        'entity.other.attribute-name.pseudo-element.css',
        'entity.other.attribute-name.pseudo-class.css',
        'meta.selector.css punctuation.section.function'
    ],
    'css:selector-symbol': [
        # >
        'meta.selector.css keyword.operator',
        # [
        'punctuation.definition.entity.begin.bracket.square.css',
        # ]
        'punctuation.definition.entity.end.bracket.square.css'
    ],
    # 'css:type-selector': [],
    'css:vendor-specific': [
        # -webkit-property: ...
        'support.type.vendored.property-name.css'
    ],

    'diff:added-line': [
        'markup.inserted.diff'
    ],
    'diff:changed-line': [
        'markup.changed'
    ],
    'diff:diff-file': [
        'meta.diff.header'
    ],
    'diff:location': [
        'meta.diff.range'
    ],
    'diff:removed-line': [
        'markup.deleted.diff'
    ],

    # 'go:printf': [],

    'python:builtin-function': [
        'support.function.builtin.python'
    ],
    'python:class-name': [
        'entity.name.type.class.python'
    ],
    'python:module-handler': [
        'keyword.control.import.python'
    ],

    'xml:attribute-name': [
        # <property →name←="variant">...
        'meta.tag entity.other.attribute-name',
        # <property name→=←"variant">... in JSX
        'meta.tag keyword.operator.assignment',
        # <property name→=←"variant">... in HTML and alike
        'punctuation.separator.key-value.html',
        'punctuation.separator.key-value.svelte',
        # XML doesn't have a selector for =
        'text.xml meta.tag'
    ],
    'xml:attribute-value': [
        'meta.tag string'
    ],
    'xml:element-name': [
        # <→property← name="variant">...
        'entity.name.tag',
        # <→property← name="variant">... in Svelte
        'support.class.component.svelte',
        # →<←property name="variant"→>←...
        'punctuation.definition.tag'
    ],
    # 'xml:namespace': [],
    'xml:processing-instruction': [
        # <?→xml← version="1.0" encoding="UTF-8"?>
        'text.xml meta.tag.preprocessor entity.name.tag',
        # →<?←xml version="1.0" encoding="UTF-8"?→>←
        'text.xml meta.tag.preprocessor punctuation.definition.tag'
    ]
}


def gsv_get_named_colors(scheme: ElementTree):
    """Get all colors from a GtkSourceView style scheme."""
    colors = {}
    for color_elem in scheme.findall('color'):
        colors[color_elem.get('name')] = color_elem.get('value')
    return colors


def gsv_to_textmate(scheme: ElementTree):
    """Convert a GtkSourceView style scheme to a TextMate theme."""
    colors = gsv_get_named_colors(scheme)

    default_elem = scheme.find('style[@name="text"]')
    default_foreground = None

    if default_elem is not None:
        default_foreground = colors[default_elem.get('foreground')]
    if default_foreground is None:
        raise Exception('no default color defined in scheme')

    EXTRA_RULES = [
        {
            'scope': [
                'variable',
                # `${→abc←}`
                'string meta.template.expression',
                # super() calls
                'meta.function-call.python support.type.python',
                # f in f'strings'
                'storage.type.string.python',
                # Symbolic operators (most operators, alphabetical ones should be specifically
                # whitelisted in MAP['def:keyword'])
                'keyword.operator',
                'storage.type.function.arrow',  # =>
                # YAML operators
                'keyword.control.flow.block-scalar.literal.yaml',
                'keyword.control.flow.block-scalar.folded.yaml',
                'storage.modifier.chomping-indicator.yaml'
            ],
            'settings': {
                # Reset all of these to default foreground and fontStyle
                'foreground': default_foreground,
                'fontStyle': ''
            }
        }
    ]

    rules = []

    scope_paths = []
    for style_name in MAP:
        scope = MAP[style_name]
        style_elem = scheme.find(f'style[@name="{style_name}"]')

        if style_elem is None:
            print(f'warning: no {style_name} in scheme')
            continue

        settings = {}

        if style_elem.get('foreground'):
            settings['foreground'] = colors[style_elem.get('foreground')]

        font_styles = []
        for font_style in 'italic', 'bold', 'strikethorugh':
            if style_elem.get(font_style) == 'true':
                font_styles.append(font_style)
        settings['fontStyle'] = ' '.join(font_styles)

        rule = {'scope': scope, 'settings': settings}
        rules.append(rule)

    rules += EXTRA_RULES
    return rules


def get_adwaita_colors(theme_type):
    if theme_type == 'dark':
        file = 'gtksourceview_xml/Adwaita-dark.xml'
    else:
        file = 'gtksourceview_xml/Adwaita.xml'
    scheme = parse_xml(file)
    named_colors = gsv_get_named_colors(scheme)
    syntax_colors = gsv_to_textmate(scheme)
    return named_colors, syntax_colors
