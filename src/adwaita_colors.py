#!/usr/bin/env python3
from xml.etree.ElementTree import ElementTree, parse as parse_xml


# A dictionary of GtkSourceView style names mapped to TextMate scopes.
# Use "Inspect Editor Tokens and Scopes" in VS Code to inspect TM scopes.
# Use this link to figure out what matches a style name: https://gitlab.gnome.org/GNOME/gtksourceview/-/blob/master/data/language-specs/
# Use these snippets to test how your rules look: https://gitlab.gnome.org/GNOME/gtksourceview/-/tree/master/tests/syntax-highlighting/
#
# If you wish to target all sub-scopes of a scope for a single language, you
# should use `source.<lang> parent-scope` instead of `parent.scope.*.<lang>`
# until wildcards are implemented: https://github.com/microsoft/vscode-textmate/issues/160,
MAP = {
    # Default color
    'text': [
        # Empty selector applies to everything
        '',

        # Embedded expressions (e.g. ${→something←} in a string)
        'meta.embedded',
        # Explicitly default-color variables. A workaround for nix-ide and potentially other
        # extensions. "${→abc←}" is colored like a string with nix-ide, see: https://github.com/nix-community/vscode-nix-ide/pull/222.
        'variable',
        # Embedded expression punctuation in XML attributes (e.g. <Component prop=→{←value→}←> in JSX)
        'meta.tag.attributes punctuation.section.embedded',

        # Most operators are symbolic. Make them of default color along with some symbolic keywords.
        # Alphabetical operators should be specifically whitelisted in def:keyword.
        'keyword.operator',
        'storage.type.function.arrow',  # =>
        # YAML symbolic keywords
        'keyword.control.flow.block-scalar.literal',
        'keyword.control.flow.block-scalar.folded',
        'storage.modifier.chomping-indicator',

        'storage.type.string',  # f, b, r string prefixes (in e.g. Python)
        'string.quoted.byte.raw',  # b string prefix (in e.g. Rust)

        # Rust
        'meta.macro.rules entity.name.function.macro.rust' # macro_rules! →hello_world_macro← {
    ],
    'def:base-n-integer': [
        # Whole number (in e.g. JS)
        'constant.numeric.binary',  # 0b1
        'constant.numeric.octal',  # 0o1
        'constant.numeric.hex',  # 0x1

        # Just the prefix/postfix (in e.g. C, Go)
        'keyword.other.unit.binary',  # 0b
        'keyword.other.unit.octal',  # 0o
        'keyword.other.unit.hexadecimal',  # 0x
        'keyword.other.unit.imaginary',  # 0x01→i←
        'keyword.other.unit.exponent'  # 0x01→p←2
    ],
    'def:boolean': [
        'constant.language.boolean',  # (in e.g. JS)
        'constant.language.bool'  # (in e.g. Rust)
    ],
    'def:comment': [
        'comment',
        # YAML
        'entity.other.document.begin.yaml',  # ---
        'entity.other.document.end.yaml'  # ...
    ],
    'def:constant': [
        # Note: `constant` may apply to user-defined constants, which is unwanted
        'constant.language',  # true, false

        # Character (in e.g. Rust). Note: there should probably be a separate def:character rule,
        # but the Adwaita scheme doesn't include it and gtksv falls back to def:constant.
        'string.quoted.single.char',

        'support.type.property-name',  # { →"key"←: ... } (in e.g. JSON)

        # CSS
        'support.constant.property-value.css',  # absolute, bold, etc
        'source.css keyword.other.unit'
    ],
    'def:decimal': [
        'constant.numeric',
        'constant.numeric entity.name.type.numeric'  # 1→i64← (in e.g. Rust)
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
        # Most keywords (operators are unstyled in `text`)
        'keyword',
        # Specifically include alphabetical operators and keywords
        'keyword.operator.new',  # new
        'keyword.operator.logical.python',  # and, or
        'source.js keyword.operator.expression',  # typeof, instanceof
        'source.ts keyword.operator.expression',
        'storage.modifier',  # →static← void Main(string[] args)
        'storage.type.class',  # →class← Cat
        'storage.type.function',  # →function← meow()

        # YAML key names are considered tag names. Tag names and strings are of a very similar color
        # (https://github.com/piousdeer/vscode-adwaita/issues/4), so we treat them as keywords like
        # gtksv does.
        'entity.name.tag.yaml',

        # Workarounds for extensions that incorrectly mark keywords with `storage.type`
        # (https://github.com/piousdeer/vscode-adwaita/issues/5)
        'source.js storage.type',
        'source.ts storage.type',
        'source.tsx storage.type',
        'source.rust storage.type'
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
        'meta.preprocessor keyword.control',  # →#include← <config.h> (override def:keyword)
        'punctuation.decorator',  # →@<-decorator (in e.g. TypeScript)
        'meta.decorator entity.name.function',  # @→decorator← (in e.g. TypeScript)
        'entity.name.function.decorator',  # @decorator (in e.g. Python)
        'keyword.control.at-rule.media',  # @at-rule (in e.g. CSS)
        'constant.character.entity',  # &amp;
        'punctuation.section.embedded',  # ${}
        'punctuation.definition.template-expression'  # ${} (in e.g. JS)
    ],
    'def:shebang': [
        'comment.line.number-sign.shebang'
    ],
    'def:special-char': [
        'constant.character.escape'  # \n
    ],
    'def:string': [
        'string'
    ],
    'def:strong-emphasis': [
        'markup.bold.markdown'
    ],
    'def:type': [
        # Type names
        'storage.type',  # when defining a variable of a type
        'entity.name.type',  # when referring to a type
        'entity.name.namespace',
        # C# uses this instead
        'keyword.type.cs',
        # Built-in types
        'support.type',
        # Built-in classes (in e.g. JS)
        'support.class.builtin',
        'support.class.promise'
    ],
    # 'def:underlined': [],
    # 'def:warning': [],

    # 'c-sharp:format': [],
    'c-sharp:preprocessor': [
        'meta.preprocessor.cs'
    ],

    'c:printf': [
        'constant.other.placeholder'  # %s
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
        # Intentionally different: instead of coloring [, = and ] in elem[attr="val"], color just attr
        'entity.other.attribute-name.css'
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

    'go:printf': [
        'constant.other.placeholder.go'
    ],

    'python:builtin-function': [
        'support.function.builtin.python'
    ],
    'python:class-name': [
        'entity.name.type.class.python'
    ],
    'python:module-handler': [
        'keyword.control.import.python'
    ],

    'rust:attribute': [
        'meta.attribute.rust',
        'meta.attribute.rust keyword.operator'
    ],
    'rust:lifetime': [
        'entity.name.type.lifetime.rust'
    ],
    'rust:macro': [
        'entity.name.function.macro'
    ],
    # 'rust:scope': [], # no selector

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
    '''Get all colors from a GtkSourceView style scheme.'''
    colors = {}
    for color_elem in scheme.findall('color'):
        colors[color_elem.get('name')] = color_elem.get('value')
    return colors


def gsv_to_textmate(scheme: ElementTree):
    '''Convert a GtkSourceView style scheme to a TextMate theme.'''
    colors = gsv_get_named_colors(scheme)

    default_elem = scheme.find('style[@name="text"]')
    default_foreground = None

    if default_elem is not None:
        default_foreground = colors[default_elem.get('foreground')]
    if default_foreground is None:
        raise Exception('no default color defined in scheme')

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
