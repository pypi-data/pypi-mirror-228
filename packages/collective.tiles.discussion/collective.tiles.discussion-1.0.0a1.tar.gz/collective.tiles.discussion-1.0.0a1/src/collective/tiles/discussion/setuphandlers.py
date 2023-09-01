from zope.interface import implementer


try:
    from plone.base.interfaces import INonInstallable
except ImportError:
    # BBB for Plone 5.2
    from Products.CMFPlone.interfaces import INonInstallable


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.tiles.discussion:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["collective.tiles.discussion.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
