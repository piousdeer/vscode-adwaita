#!/usr/bin/env python3
import json
import re
import itertools
from adwaita_colors import get_adwaita_colors
from adwaita_ui_colors import get_adwaita_ui_colors


def load_jsonc(path):
    """Read JSON with comments."""
    original = open(path).read()
    stripped = re.sub(r'[^:]//.+$', '', original, flags=re.MULTILINE)
    return json.loads(stripped)


def get_default_syntax_colors(theme_type):
    return load_jsonc(f'default_themes/{theme_type}.jsonc')['tokenColors']


extra_syntax_colors = [
    {
        'scope': ['markup.italic.markdown'],
        'settings': {
            'fontStyle': 'italic'
        }
    },
    {
        'scope': ['markup.strikethrough.markdown'],
        'settings': {
            'fontStyle': 'strikethrough'
        }
    }
]

package_json_entry = {
    "contributes": {
        "themes": []
    }
}

for (
    theme_type,
    syntax_colors_type,
    colorful_status_bar
) in itertools.product(
    ('dark', 'light'),
    ('adwaita', 'default'),
    (False, True)
):
    name = f'Adwaita {theme_type.capitalize()}'
    ui_colors = get_adwaita_ui_colors(theme_type, colorful_status_bar)

    if syntax_colors_type == 'adwaita':
        _named_colors, syntax_colors = get_adwaita_colors(theme_type)
        syntax_colors += extra_syntax_colors
    else:
        syntax_colors = get_default_syntax_colors(theme_type)
        name += ' & default syntax highlighting'

    if colorful_status_bar:
        name += ' & colorful status bar'

    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": name,
        "type": "light",
        "colors": ui_colors,
        "tokenColors": syntax_colors
    }

    file_name = f'{name.lower().replace(" ", "-").replace("-&-", "-")}.json'
    json.dump(theme, open(f'../themes/{file_name}', 'w'), indent=2)

    package_json_entry['contributes']['themes'].append({
        "label": name,
        "uiTheme": "vs-dark" if theme_type == 'dark' else "vs",
        "path": f"./themes/{file_name}"
    })

print('Suggested package.json entry:')
print(json.dumps(package_json_entry, indent=2)[2:-2])
