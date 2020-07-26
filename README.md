# UnitStatus widget

UnitStatus is a basic widget for Qtile which shows the current status of systemd units.

It may not be particular useful for you and was primarily written as an exercise to familiarise myself with writing Qtile widgets and interacting with d-bus.

## About

The widget is incredibly basic. It subscribes to the systemd d-bus interface, finds the relevant service and displays an icon based on the current status. The widget listens for announced changes to the service and updates the icon accordingly.

## Demo

Here is a screenshot from my HTPC showing multiple instances of the widget. Green icons are active services and the white is inactive.

![Screenshot](images/widget-unitstatus-screenshot.png?raw=true)

## Installation

You can clone the repository and run:

```
python setup.py install
```
or, for Arch users, just copy the PKGBUILD file to your machine and build.

## Configuration

Add the widget to your config (`~/.config/qtile/config.py`):

```python
from unitstatus import UnitStatus
...
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                UnitStatus(label="Avahi",unitname="avahi-daemon.service"),
                UnitStatus(), # NetworkManager.service is default
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.QuickExit(),
            ],
            24,
        ),
    ),
]
```

## Customising

The widget can be customised with the following arguments:

<table>
    <tr>
            <td>font</td>
            <td>Default font</td>
    </tr>
    <tr>
            <td>fontsize</td>
            <td>Font size</td>
    </tr>
    <tr>
            <td>unitname</td>
            <td>Name of systemd unit.</td>
    </tr>
    <tr>
            <td>label</td>
            <td>Short text to display next to indicator.</td>
    </tr>
    <tr>
            <td>colour_active</td>
            <td>Colour for active indicator</td>
    </tr>
    <tr>
            <td>colour_inactive</td>
            <td>Colour for active indicator</td>
    </tr>
    <tr>
            <td>colour_failed</td>
            <td>Colour for active indicator</td>
    </tr>
    <tr>
            <td>colour_dead</td>
            <td>Colour for dead indicator</td>
    </tr>
    <tr>
            <td>indicator_size</td>
            <td>Size of indicator (None = up to margin)</td>
    </tr>
    <tr>
            <td>state_map</td>
            <td>Map of indicator colours (state: (border, fill))<br />
            {"active": ("colour_active", "colour_active"),
             "inactive": ("colour_inactive", "colour_inactive"),
             "deactivating": ("colour_inactive", "colour_active"),
             "activating": ("colour_active", "colour_inactive"),
             "failed": ("colour_failed", "colour_failed"),
             "not-found": ("colour_inactive", "colour_failed"),
             "dead": ("colour_dead", "colour_dead"),
           }</td>
    </tr>
</table>

## Contributing

If you've used this (great, and thank you) you will find bugs so please [file an issue](https://github.com/elParaguayo/qtile-widget-unitstatus/issues/new).
