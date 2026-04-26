from adwaita_colors import get_adwaita_colors


named_colors, _syntax_colors = get_adwaita_colors('light')


def get_adwaita_ui_colors(theme_type, colorful_status_bar=False):
    def _(name): return lambda value: named_colors[f'{name}_{value}']
    dark = theme_type == 'dark'

    ui_colors = {
        # libadwaita doesn't use shadows to indicate scrollable content.
        'scrollbar.shadow':                     '#00000000',

        'activityBar.background':               '#2d2d31' if dark else '#ebebeb',
        'titleBar.activeBackground':            '#2d2d31' if dark else '#ebebeb',
        'tab.activeBackground':                 '#2d2d31' if dark else '#ebebeb',
        'tab.inactiveBackground':               '#242428' if dark else '#e1e1e1',
        'editorGroupHeader.tabsBackground':     '#242428' if dark else '#e1e1e1',
        'breadcrumb.background':                '#242428' if dark else '#e1e1e1',
        'tab.hoverBackground':                  '#333337' if dark else '#dcdcdc',
        # 'tab.activeForeground':               '#ffffff'
        # 'tab.inactiveForeground':             '#cccccc'

        'panel.background':                     '#222226' if dark else '#fafafa',
        'sideBar.background':                   '#2d2d31' if dark else '#fafafa',
        'statusBar.background':                 '#222226' if dark else '#fafafa',
        'statusBar.noFolderBackground':         '#222226' if dark else '#fafafa',
        'statusBarItem.remoteBackground':       '#222226' if dark else '#fafafa',
        'panelSectionHeader.background':        '#00000000',
        'sideBarSectionHeader.background':      '#00000000',

        'activityBar.border':                   '#424246' if dark else '#cfcfcf',
        'editorBracketMatch.border':            '#424246' if dark else '#cfcfcf',
        'editorGroup.border':                   '#424246' if dark else '#cfcfcf',
        'editorGroupHeader.border':             '#424246' if dark else '#cfcfcf',
        'editorGroupHeader.tabsBorder':         '#424246' if dark else '#cfcfcf',
        'panel.border':                         '#424246' if dark else '#cfcfcf',
        'panelSectionHeader.border':            '#424246' if dark else '#cfcfcf',
        'sideBar.border':                       '#424246' if dark else '#cfcfcf',
        'sideBarSectionHeader.border':          '#424246' if dark else '#cfcfcf',
        'statusBar.border':                     '#424246' if dark else '#cfcfcf',
        'tab.border':                           '#424246' if dark else '#cfcfcf',
        'titleBar.border':                      '#424246' if dark else '#cfcfcf',
        'window.activeBorder':                  '#424246' if dark else '#cfcfcf',
        'tree.indentGuidesStroke':              '#42424699' if dark else '#cfcfcf99',
        'editorIndentGuide.activeBackground':   '#42424699' if dark else '#cfcfcf99',
        'editorIndentGuide.background':         '#42424680' if dark else '#cfcfcf80',
        'editorRuler.foreground':               '#42424680' if dark else '#cfcfcf80',
        'editorBracketMatch.background':        '#42424620' if dark else '#cfcfcf80',
        # A dotted outline, not a solid border, but it's the best we can get.
        # 'list.inactiveFocusOutline':            '#424246' if dark else '#cfcfcf',

        'list.hoverBackground':                 '#303034' if dark else '#ececec',
        'list.inactiveSelectionBackground':     '#37373b' if dark else '#e6e6e6',
        'input.background':                     '#37373b' if dark else '#e6e6e6',

        # #323232 is from libadwaita. For dark theme most text is #fff, but in VS Code there's way
        # more text displayed at the same time, so I find a softer color works better.
        'statusBar.foreground':                 '#cccccc' if dark else '#323232',
        'statusBar.noFolderForeground':         '#cccccc' if dark else '#323232',
        'statusBar.debuggingForeground':        '#cccccc' if dark else '#323232',
        'statusBarItem.remoteForeground':       '#cccccc' if dark else '#323232',
        'sideBar.foreground':                   '#cccccc' if dark else '#323232',
        'panelTitle.activeBorder':              '#cccccc' if dark else '#323232',
        'panelTitle.activeForeground':          '#cccccc' if dark else '#323232',

        'activityBar.activeBorder':             '#00000000',
        'activityBarBadge.background':          _('blue')(3),
        'button.background':                    _('blue')(3),
        # A border of the same color makes buttons slightly taller.
        'button.border':                        _('blue')(3),
        'list.activeSelectionBackground':       _('blue')(6 if dark else 4),
        'list.highlightForeground':             '#ffffff' if dark else '#000000',
        'list.activeSelectionForeground':       '#ffffff',
        'list.activeSelectionIconForeground':   '#ffffff',
        'list.focusHighlightForeground':        '#ffffff',


        'editorGutter.addedBackground':                     _('green')(6 if dark else 3),
        'editorGutter.deletedBackground':                   _('red')(5 if dark else 4),
        'editorGutter.modifiedBackground':                  _('blue')(5 if dark else 2),
        'gitDecoration.addedResourceForeground':            _('green')(1 if dark else 5) + 'dd',
        'gitDecoration.renamedResourceForeground':          _('green')(1 if dark else 5) + 'dd',
        'gitDecoration.untrackedResourceForeground':        _('green')(1 if dark else 5) + 'dd',
        'gitDecoration.modifiedResourceForeground':         _('orange')(1 if dark else 4) + 'dd',
        'gitDecoration.stageModifiedResourceForeground':    _('orange')(1 if dark else 4) + 'dd',
        'gitDecoration.deletedResourceForeground':          _('red')(1) + 'dd',
        'gitDecoration.stageDeletedResourceForeground':     _('red')(1) + 'dd',
        'gitDecoration.ignoredResourceForeground':          _('dark')(1),

        # Color-picked colors
        'commandCenter.background':             '#404044' if dark else '#d9d9d9',
        'commandCenter.border':                 '#00000000',
        'button.hoverBackground':               '#4990e7',
        'focusBorder':                          '#5f7999',

        # Hand-picked colors
        'activityBar.foreground':               '#ffffff' if dark else '#000000',
        'editor.background':                    '#1c1c20' if dark else '#ffffff',
        'editorLineNumber.foreground':          '#636367' if dark else '#32323280',
        'widget.shadow':                        '#00000033' if dark else '#00000022',
    }

    if colorful_status_bar:
        ui_colors |= {
            'statusBar.background':             _('blue')(4),
            'statusBar.debuggingBackground':    _('orange')(5),
            'statusBar.noFolderBackground':     _('purple')(5),
            'statusBarItem.remoteBackground':   _('green')(6),
            'statusBar.foreground':             '#ffffff',
            'statusBar.debuggingForeground':    '#ffffff',
            'statusBar.noFolderForeground':     '#ffffff',
            'statusBarItem.remoteForeground':   '#ffffff',
        }

    return ui_colors
