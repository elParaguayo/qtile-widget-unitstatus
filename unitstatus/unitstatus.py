import pydbus
import math

from libqtile.widget import base
from libqtile import bar


class UnitStatus(base._Widget, base.PaddingMixin, base.MarginMixin):

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("bus_name", "system", "Which bus to use. Accepts 'system' or 'session'.")
        ("font", "sans", "Default font"),
        ("fontsize", None, "Font size"),
        ("unitname", "NetworkManager.service", "Name of systemd unit."),
        ("label", "NM", "Short text to display next to indicator."),
        ("colour_active", "00ff00", "Colour for active indicator"),
        ("colour_inactive", "ffffff", "Colour for active indicator"),
        ("colour_failed", "ff0000", "Colour for active indicator"),
        ("colour_dead", "666666", "Colour for dead indicator"),
        ("indicator_size", 10, "Size of indicator (None = up to margin)"),
        ("state_map",
         {"active": ("colour_active", "colour_active"),
          "inactive": ("colour_inactive", "colour_inactive"),
          "deactivating": ("colour_inactive", "colour_active"),
          "activating": ("colour_active", "colour_inactive"),
          "failed": ("colour_failed", "colour_failed"),
          "not-found": ("colour_inactive", "colour_failed"),
          "dead": ("colour_dead", "colour_dead"),
        },
         "Map of indicator colours (border, fill)")
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.add_defaults(UnitStatus.defaults)
        self.add_defaults(base.PaddingMixin.defaults)
        self.add_defaults(base.MarginMixin.defaults)
        if self.indicator_size is not None:
            self.indicator_size = max(self.indicator_size, 1)
        self.colours = {}
        for state, cols in self.state_map.items():
            self.colours[state] = tuple(getattr(self, col) for col in cols)
        if self.bus_name == "session":
            self.bus = pydbus.SessionBus()
        else:
            self.bus = pydbus.SystemBus()

        self.systemd = self.bus.get(".systemd1")

    def find_unit(self):
        units = self.systemd.ListUnits()
        unit = [x for x in units if x[0] == self.unitname]
        if not unit:
            self.state = "not-found"
            self.unit = None

        else:
            path = unit[0][6]
            self.unit = self.bus.get(".systemd1", path)
            self.bus.subscribe(
                arg0="org.freedesktop.systemd1.Unit",
                object=path,
                signal="PropertiesChanged",
                signal_fired=self.update
            )

    def update(self, sender, object, iface, signal, params):
        props = params[1]
        self.state = props["ActiveState"]
        self.draw()

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)

        self.find_unit()

        if self.unit:
            self.state = self.unit.ActiveState

        # Work out how big the indicator should be
        max_indicator = self.bar.height - 2 * self.margin
        if self.indicator_size is None:
            self.indicator_size = max_indicator
        else:
            self.indicator_size = min(max_indicator, self.indicator_size)

        # Set fontsize
        if self.fontsize is None:
            calc = self.bar.height - self.margin * 2
            self.fontsize = max(calc, 1)

        # Create layout with basic settings (we can override these when we draw)
        self.layout = self.drawer.textlayout(
            "",
            "ffffff",
            self.font,
            self.fontsize,
            None,
            wrap=False
        )

    def text_width(self):
        width, _ = self.drawer.max_layout_size(
            [self.label],
            self.font,
            self.fontsize
        )
        return width

    def box_width(self):
        width = self.text_width()
        width = width + 3 * (self.padding_x) + self.indicator_size
        return width

    def calculate_length(self):
        return self.box_width()

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = self.margin

        self.layout.text = self.label
        self.layout.font_family = self.font
        self.layout.font_size = self.fontsize
        self.layout.colour = "ffffff"
        self.layout.width = self.text_width()

        self.layout.draw(
          (self.margin * 2 + self.indicator_size),
          int(self.bar.height / 2.0 - self.layout.height / 2.0) + 1)

        i_margin = int((self.bar.height - self.indicator_size)/2)

        self.draw_indicator(self.margin,
                            i_margin,
                            self.indicator_size,
                            self.indicator_size,
                            2,
                            self.colours[self.state])

        self.drawer.draw(offsetx=self.offset, width=self.width)

    # This is just Drawer's "_rounded_rect" but with a bigger corner radius
    def circle(self, x, y, width, height, linewidth):
        aspect = 1.0
        corner_radius = height / 3.0
        radius = corner_radius / aspect
        degrees = math.pi / 180.0

        self.drawer.ctx.new_sub_path()

        delta = radius + linewidth / 2
        self.drawer.ctx.arc(x + width - delta, y + delta, radius,
                            -90 * degrees, 0 * degrees)
        self.drawer.ctx.arc(x + width - delta, y + height - delta,
                            radius, 0 * degrees, 90 * degrees)
        self.drawer.ctx.arc(x + delta, y + height - delta, radius,
                            90 * degrees, 180 * degrees)
        self.drawer.ctx.arc(x + delta, y + delta, radius,
                            180 * degrees, 270 * degrees)

        self.drawer.ctx.close_path()

    def draw_indicator(self, x, y, width, height, linewidth, statecols):
        self.circle(x, y, width, height, linewidth)
        self.drawer.set_source_rgb(statecols[1])
        self.drawer.ctx.fill()
        self.drawer.set_source_rgb(statecols[0])
        self.circle(x, y, width, height, linewidth)
        self.drawer.ctx.stroke()
