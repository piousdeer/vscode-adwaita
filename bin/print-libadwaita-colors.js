#!/usr/bin/env gjs
//@ts-check

/*
 * This program prints a JSON object containing libadwaita named colors as seen by a libadwaita app:
 * unless ran with `--ignore-customizations`, it respects the `GTK_THEME` environment variable and
 * settings in `XDG_CONFIG_HOME/gtk-4.0/gtk.css`.
 *
 * REFERENCES
 *
 * How libadwaita applies its stylesheets
 * https://gitlab.gnome.org/GNOME/libadwaita/-/blob/065eeb9c4e4f797641e60c75005cf7bcfddf06c6/src/adw-style-manager.c#L255-269
 *
 * How GTK applies its built-in stylesheets and gtk.css
 * https://gitlab.gnome.org/GNOME/gtk/-/blob/913e3680f377e6dfb03c9b87248b7dbcec6d4267/gtk/gtksettings.c#L1138-1162
 *
 * Resource paths for GTK's built-in stylesheets (unused)
 * https://gitlab.gnome.org/GNOME/gtk/-/blob/913e3680f377e6dfb03c9b87248b7dbcec6d4267/gtk/gtkcssprovider.c#L1347-1350
 */

imports.gi.versions.Gtk = "4.0";
const System = imports.system;
const GLib = imports.gi.GLib;
/** @type {import("@gi-types/adw1")} */
const Adw = imports.gi.Adw;
/** @type {import("@gi-types/gtk4")} */
const Gtk = imports.gi.Gtk;

const environ = GLib.get_environ();

/** Exit if a color resolving failure occurs */
const exitOnError = checkFlag("--exit-on-error");
/** Ignore `GTK_THEME` and `gtk.css` */
const ignoreCustomizations = checkFlag("--ignore-customizations");

const shouldApplyAdwStyle = !GLib.environ_getenv(environ, "GTK_THEME") || ignoreCustomizations;

const app = new Gtk.Application();

app.connect("activate", () => {
  try {
    printLibadwaitaColors();
  } finally {
    app.quit();
  }
});

app.run([]);

function printLibadwaitaColors() {
  Adw.init(); // so we can load from /org/gnome/Adwaita/

  const output = {
    versions: {
      Gtk: getVersion(Gtk),
      Adw: getVersion(Adw),
    },
    colors: {},
  };

  const window = new Gtk.ApplicationWindow({ application: app });
  const settings = window.get_settings();
  const context = window.get_style_context();

  if (shouldApplyAdwStyle) {
    settings.gtk_theme_name = "Adwaita-empty";
  }

  for (const highContrastSuffix of ["", "-hc"]) {
    const baseProvider = setupProvider(`base${highContrastSuffix}`, context);
    for (const scheme of ["dark", "light"]) {
      const schemeProvider = setupProvider(`defaults-${scheme}`, context);
      const colorNames = new Set([
        ...getColorNames(baseProvider),
        ...getColorNames(schemeProvider),
      ]);
      output.colors[scheme + highContrastSuffix] = getColorValues(context, colorNames);
      context.remove_provider(schemeProvider);
    }
    context.remove_provider(baseProvider);
  }

  // Why not just create an AdwApplication, AdwApplicationWindow and use its StyleContext's
  // lookup_color method? First, we don't know the color names. GtkCssProvider doesn't expose its
  // color table nor its CSS parser, so we have to resort to an absolute bummer of a workaround:
  // parsing stylesheets with regex. Second, libadwaita doesn't allow apps to override high contrast
  // mode by design.

  print(JSON.stringify(output, null, 2));
}

/**
 * @param {string} path
 * @param {import("@gi-types/gtk4").StyleContext} context
 */
function setupProvider(path, context) {
  const provider = new Gtk.CssProvider();
  provider.load_from_resource(`/org/gnome/Adwaita/styles/${path}.css`);
  if (shouldApplyAdwStyle) {
    const priority = ignoreCustomizations
      ? Gtk.STYLE_PROVIDER_PRIORITY_USER
      : Gtk.STYLE_PROVIDER_PRIORITY_THEME;
    context.add_provider(provider, priority);
  }
  return provider;
}

/**
 * @param {import("@gi-types/gtk4").CssProvider} provider
 */
function getColorNames(provider) {
  const css = provider.to_string();
  return new Set(
    Array.from(css.matchAll(/(?:^|{.+})\s*@define-color\s+(?<name>\S+)\s+(?<value>.+);/gm)).map(
      ([_, name]) => name
    )
  );
}

/**
 * @param {import("@gi-types/gtk4").StyleContext} context
 * @param {Iterable<string>} names
 */
function getColorValues(context, names) {
  const values = {};
  for (const name of names) {
    const [success, rgba] = context.lookup_color(name);

    if (!success && exitOnError) {
      throw new Error(`Failed to resolve color ${name}`);
    }

    values[name] = success ? rgba.to_string() : null;
  }
  return values;
}

function checkFlag(flag) {
  return System.programArgs.includes(flag);
}

function getVersion(lib) {
  return `${lib.MAJOR_VERSION}.${lib.MINOR_VERSION}.${lib.MICRO_VERSION}`;
}
