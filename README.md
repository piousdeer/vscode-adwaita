# Adwaita theme for VS Code

Dark and light themes based on GNOME 42's new Adwaita look and GNOME Builder's syntax highlighting.

<img src="assets/screenshot.png">
<font color="#777"><small><center>Fonts shown: JetBrains Mono, SF Pro Text</center></small></font>
<br>

Extra variants are included for those who prefer a colorful status bar and/or default syntax highlighting:

<img src="assets/screenshot_extra.png"><br>

## Suggested settings

Installing [adw-gtk3](https://github.com/lassekongo83/adw-gtk3) will get you a matching native title bar.

Open Command Palette and find "Open Settings (JSON)". Here are the recommended settings:

```json
"workbench.preferredDarkColorTheme": "Adwaita Dark",
"workbench.preferredLightColorTheme": "Adwaita Light",
"window.titleBarStyle": "native",
"window.menuBarVisibility": "toggle", // Menu bar will be hidden until you press Alt
"breadcrumbs.enabled": false,
"editor.renderLineHighlight": "none",
"workbench.iconTheme": null,
"workbench.tree.indent": 12,
```

## Contributing

cd into `src` and run `build.py` to build the JSON files. Open this project in VS Code and hit F5 to test out your changes.

Adwaita syntax highlighting rules are translated from a GtkSourceView style scheme. This is far from perfect, but I've tried to make sure most popular languages look good. If something seems too off, open an issue.

This project is not affiliated with GNOME Foundation.

[<img src="https://img.shields.io/badge/donate-crypto-yellow">](https://pious.dev/donate)
