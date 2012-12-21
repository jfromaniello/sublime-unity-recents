import os
import json
import sublime_plugin

package_path = os.getcwdu()
sessions_path = os.path.join(package_path, '../../Settings/Auto Save Session.sublime_session')
shortcut_path = os.path.expanduser('~/.local/share/applications/sublime-text-2.desktop')

TEMPLATE = """#!/usr/bin/env xdg-open

[Desktop Entry]
Name=Sublime Text 2
GenericName=Text Editor
Comment=Sophisticated text editor for code, html and prose
Exec=/usr/bin/sublime-text-2 %%F
Terminal=false
Type=Application
MimeType=text/plain;text/x-chdr;text/x-csrc;text/x-c++hdr;text/x-c++src;text/x-java;text/x-dsrc;text/x-pascal;text/x-perl;text/x-python;application/x-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/xml;text/html;text/css;text/x-sql;text/x-diff;x-directory/normal;inode/directory;
Icon=sublime-text-2
Categories=TextEditor;Development;Utility;
Name[en_US]=Sublime Text 2
X-Ayatana-Desktop-Shortcuts=NewWindow;%s

[NewWindow Shortcut Group]
Name=Open a New Window
Exec=/usr/bin/sublime-text-2 --new-window
TargetEnvironment=Unity

%s
"""

TEMPLATE_SHORTCUT = """
[SublimeFolder%s Shortcut Group]
Name=%s
Exec=/usr/bin/sublime-text-2 %s
TargetEnvironment=Unity
"""


class UnityRecentCommand(sublime_plugin.EventListener):
    def on_close(self, view):
        print sessions_path
        json_string = open(sessions_path, 'r') \
                                .read() \
                                .replace('\r', '') \
                                .replace('\n', '') \
                                .replace('\t', '')

        recents = json.loads(json_string)

        items = recents['folder_history'][0:10]

        if len(items) == 0:
            return

        shortcuts_names = ';'.join(['SublimeFolder' + str(x) for x in range(0, len(items))])
        shortcuts_details = '\n'.join([TEMPLATE_SHORTCUT % (items.index(x), x, x) for x in items])

        new_shortcut_file_content = TEMPLATE % (shortcuts_names, shortcuts_details)

        f = open(shortcut_path, 'w')
        f.write(new_shortcut_file_content)
        f.close()
