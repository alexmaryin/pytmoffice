def hide_widget(widget):
    widget.saved_attrs = widget.height, widget.size_hint_y, widget.opacity, widget.disabled
    widget.height, widget.size_hint_y, widget.opacity, widget.disabled = 0, None, 0, True


def show_widget(widget):
    if hasattr(widget, 'saved_attrs'):
        widget.height, widget.size_hint_y, widget.opacity, widget.disabled = widget.saved_attrs
        del widget.saved_attrs
