from plone.app.mosaic.widget import LayoutWidget
import logging


logger = logging.getLogger(__name__)
LayoutWidget._orig_enabled = LayoutWidget.enabled


def enabled(self):
    if "++add++" in self.request.URL:
        return False
    return self._orig_enabled


LayoutWidget.enabled = property(enabled)
logger.info("Patched plone.app.mosaic.widget.LayoutWidget: not enabled on add forms.")
