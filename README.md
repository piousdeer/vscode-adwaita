# Adwaita theme for VS Code

Dark and light themes based on GNOME's new Adwaita look and GNOME Builder's syntax highlighting.

![Screenshot of the light and dark themes](assets/screenshot.png)

Extra theme variants are included for those who prefer a colorful status bar and/or default syntax highlighting:

![Screenshot showing the dark theme with a colorful status bar and default syntax highlighting](assets/screenshot_extra.png)

## Installation

Build manually from `src/build.py` and link to `.vscode/extensions/adwaita-fork` or something.

## Suggested settings

Open the Command Palette and find "Open Settings (JSON)". Here are the recommended settings:

```jsonc
"window.titleBarStyle": "custom",
"window.commandCenter": true,
"window.autoDetectColorScheme": true,
"workbench.preferredDarkColorTheme": "Adwaita Dark",
"workbench.preferredLightColorTheme": "Adwaita Light",
"workbench.productIconTheme": "adwaita",
"editor.renderLineHighlight": "none",
"workbench.iconTheme": null,
"workbench.tree.indent": 12,
```

[Rounded Window Corners](https://extensions.gnome.org/extension/5237/rounded-window-corners/) GNOME extension can be used to get rounded corners on all windows.

## Related projects

- [wroyca/vscode-libadwaita](https://github.com/wroyca/vscode-libadwaita) contains custom CSS that brings VS Code even closer to looking like a libadwaita app:

![Screenshot of vscode-libadwaita](https://raw.githubusercontent.com/wroyca/vscode-libadwaita/main/libadwaita.png)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

This project is not affiliated with GNOME Foundation.
