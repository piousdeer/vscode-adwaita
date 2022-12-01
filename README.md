# Adwaita theme for VS Code

Dark and light themes based on GNOME's new Adwaita look and GNOME Builder's syntax highlighting.

![Screenshot of the light and dark themes](assets/screenshot.png)

Extra theme variants are included for those who prefer a colorful status bar and/or default syntax highlighting:

![Screenshot showing the dark theme with a colorful status bar and default syntax highlighting](assets/screenshot_extra.png)<br>
<small><center>Fonts shown: JetBrains Mono, SF Pro Text.</center></small>

## Installation

Get it on [VS Marketplace](https://marketplace.visualstudio.com/items?itemName=piousdeer.adwaita-theme) or [Open VSX](https://open-vsx.org/extension/piousdeer/adwaita-theme).

## Suggested settings

Open the Command Palette and find "Open Settings (JSON)". Here are the recommended settings:

```jsonc
"workbench.preferredDarkColorTheme": "Adwaita Dark",
"workbench.preferredLightColorTheme": "Adwaita Light",
"window.titleBarStyle": "native",
"window.menuBarVisibility": "toggle", // Menu bar will be hidden until you press Alt
"window.autoDetectColorScheme": true,
"window.title": "${rootPath}${separator}Code",
"breadcrumbs.enabled": false,
"editor.renderLineHighlight": "none",
"workbench.iconTheme": null,
"workbench.tree.indent": 12,
```

Installing [adw-gtk3](https://github.com/lassekongo83/adw-gtk3) will get you a matching native title bar.

[Rounded Window Corners](https://extensions.gnome.org/extension/5237/rounded-window-corners/) GNOME extension can be used to get rounded corners on all windows.

## Related projects

- [wroyca/vscode-gnome](https://github.com/wroyca/vscode-gnome) contains custom CSS that brings VS Code even closer to looking like a libadwaita app.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

<hr>

This project is not affiliated with GNOME Foundation.

[<img src="https://img.shields.io/badge/donate-crypto-yellow">](https://pious.dev/donate)
