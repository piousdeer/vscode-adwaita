# Contributing

## Color themes

Requirements: Python 3, npm

Run `npm run build:color-themes`. Alternatively, `cd` into `src` and run `build.py`. Open this project in VS Code and hit F5 to test out your changes.

Adwaita syntax highlighting rules are translated from a GtkSourceView style scheme. This is far from perfect, but I've tried to make sure most popular languages look good. If something seems too off, open an issue.

## Product icons

Requirements: Python 3, npm, [nanoemoji](https://github.com/googlefonts/nanoemoji)

### Adding a new icon

1. Obtain an .svg icon in the [Icon Library](https://flathub.org/apps/details/org.gnome.design.IconLibrary) app
2. Put it into [product-icons/scalable/](product-icons/scalable/), incrementing the name in hexadecimal
3. Open it with a text editor, replace the hardcoded color with `currentColor` and apply `style="transform:scale(0.8)translate(2,2)"` as the icons are too big by default for some reason
4. Edit the icon if needed
5. Add it to [adwaita.json](icons/adwaita.json)
6. Build the .ttf file with `npm run build:product-icons`

This process should be automated in the future.

List of icons edited in step 4:

- All window controls got a background circle with opacity 0.1
- [`layout`](product-icons/scalable/ea0b.svg) is `grid-symbolic` modified in Inkscape

The menu bar icon must have the code point of U+EB94. It's [!important](https://github.com/microsoft/vscode/blob/2a16bdb4677649893126816d2e22fce76288eeb7/src/vs/base/browser/ui/menu/menubar.css#L102) for some reason.
