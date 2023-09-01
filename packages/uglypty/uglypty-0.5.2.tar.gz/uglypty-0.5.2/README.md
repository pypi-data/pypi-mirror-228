# UglyPTY

UglyPTY is an extensible graphical terminal emulator built with Python and PyQt6. It provides a user-friendly interface for managing and establishing SSH connections, with some great productivity of features. This is the base product of many Network Engineering automation tools currently in development. A plugin based system for adding features to the application is included in this release, along with some basic plugin examples. The best network automation tools are in python ...

### Python needed a native SSH GUI Terminal
This application does NOT wrap a backend web server like Webssh. It DOES use xterm.js for terminal emulation.

> **Note**: This is a VERY beta release with a lot of functionality.

## Features

- **Session Manager**: Leverage the sessions you use in your Terminal environment in your automation scripts (examples included).
  - Create, edit, or delete sessions with specific settings.
  - Supports password and key based authentication.
  
- **Credentials Manager**: Safely manage your user credentials.
  - Passwords are encrypted.
  - Fetch all credentials or a specific credential by ID from a SQLite database (`settings.sqlite`).
  
- **Themed Views**: Multiple theme modes - light, dark, light-dark, and dark-light.
  
- **Tab Management**: Handle multiple SSH connections across different tabs.

- **Plugin System**: Plugins are PIP wheel based add-ons to UglyPTY. They can be anything represented by a PyQt6 Widget. Sample plugin's available include "UglyAce" a PyQt6 Webengine and Ace.js based editor with syntax highlighting, and "UglyTerminal for Windows" a fully functional tabbed Terminal application that can open embeded cmd.exe, powershell.exe and wsl.exe based sessions. Terminal is also based on the webengine and Xterm.js, so it supports full terminal emulation. Soon to be released plugins will include a CLI collector that leverages UglyPTY's session information to collect and store device output, Parser UI's to simplify network automation development tasks - including Jinja2 Template and TTP Parser template creation and testing. See the Plugins section below for more information...


## Installation

1. Tested with Python 3.9.13 for Windows in venv, and Ubuntu 22.04 with Python 3.10. Other versions might work.
2. Use PyPi unless you want to contribute.
3. Use `pip` with an activated venv:

    ```bash
    pip install uglypty
    ```

To start the application, navigate to the activated virtual directory, local keys, your session database, and log files will be here:

    python or pythonw -m uglypty

## UglyPTY Plugins
To use a plugin, download its `.whl` file and save it in a `./wheels` directory where your UglyPTY application is installed. You will have to create this folder.

## Download More Plugins

You can find more about UglyPTY's wheel based plugins from [github](https://github.com/scottpeterman/UglyPTY-Plugins).
You can download more `.whl` plugins from [wheels](https://github.com/scottpeterman/UglyPTY-Plugins/tree/main/wheels).

### `catalog.yaml` Explained

Only 2 example plugins are pre-entered in the pluging catalog. The `catalog.yaml` file contains metadata for all available plugins. UglyPTY's Plugin Manager reads this file, so if you download additional plugins, you will have to edit this file to get them installed and registered with the application. Each plugin has its entry defined by the following keys:

- `name`: The human-readable name of the plugin.
- `package_name`: The name used to register the plugin as a Python package. This is the name you would use if you were to install the plugin using pip.
- `description`: A brief description of what the plugin does.
- `import_name`: The Python import statement that would be used to load the plugin's main class or function.
- `version`: The version number of the plugin.
- `source_type`: The type of installation source, currently only supports "wheel".
- `wheel_url`: The path to the `.whl` file for the plugin, relative to the `./wheels` directory.

Example entry:

```yaml
- name: "Ugly Ace Editor"
  package_name: "ugly_ace_editor"
  description: "An Ace based editor with some unique features."
  import_name: "uglyplugin_ace.ugly_ace.QtAceWidget"
  version: "0.1.0"
  source_type: "wheel"
  wheel_url: "./wheels/uglyplugin_ace-0.1.0-py3-none-any.whl"
```

## Plugin Manager

When you start UglyPTY, go to Options/Plugin Manager. Here you can install and uninstall plugins:

<div align="center">
  <img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/pluginmanager.png" alt="UglyPTY Dark" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/pluginmanager_install.png" alt="UglyPTY Dark" width="400px">
</div>

## A special thanks to those whose efforts this tool is built on (shoulders of giants and all that)
- Qt   https://www.qt.io/
- PyQt6    https://www.riverbankcomputing.com/software/pyqt/   Yes I could have used PySide6, and maybe will add that. I've used PyQt to fix my own problems for years, and I just love it!
- Netmiko  Kirk - you are awesome! (Network Engineers - his classes are awesome as well)
- Paramiko  Most don't know just how much automation has been enabled by this project (Ansible, looking at you over the years)
- TTP  Very few outside the network automation space know of this, but it transformed the ability to automate legacy network equipment, much of which still wont do a simple "show blah | json". I have literally worked with it since ver 0.0.1 - this guy is amazing: https://github.com/dmulyalin/ttp


## Screenshots

Here are some snapshots of UglyPTY in action:

<div align="center">
  <img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/uglydark.PNG" alt="UglyPTY Dark" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/uglylight.png" alt="UglyPTY Light Splash" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/darklight.png" alt="UglyPTY darklight" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/lightdark.png" alt="UglyPTY Lightdark" width="400px">
</div>

---

## Here are some snapshots of UglyPTY-Plugins in action:

<div align="center">
  <img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/UglyConsole.png" alt="UglyPTY Console" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/UglyCollector.png" alt="UglyPTY Light Splash" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/UglyParser.png" alt="UglyPTY darklight" width="400px">
  
</div>

---

**Enjoy using UglyPTY!**


## Package Distribution

```python
# Create a source distribution and a wheel
python setup.py sdist bdist_wheel

# Set up a new virtual environment
python -m venv test_env

# Activate the virtual environment
source test_env/bin/activate  # On Linux/Mac
test_env\Scripts\activate     # On Windows

# Install the wheel
pip install dist/uglypty-0.1-py3-none-any.whl

# Test your script
python or pythonw -m uglypty
