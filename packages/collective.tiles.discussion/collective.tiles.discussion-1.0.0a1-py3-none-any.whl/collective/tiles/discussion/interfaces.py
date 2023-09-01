from . import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveTilesDiscussionLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IDiscussionTileData(model.Schema):
    title = schema.TextLine(
        title=_("Title"),
        required=False,
    )

    discussion_states = schema.List(
        title=_("Review states"),
        description=_(
            "Select the review state of the discussions. Leave empty to show all the discussions."
        ),
        required=False,
        value_type=schema.Choice(
            vocabulary="collective.tile.discussion.DiscussionStatesVocabulary",
        ),
    )

    discussion_folder = schema.Choice(
        title=_("Discussions folder"),
        description=_(
            "Insert the folder where you want to search the discussions. "
            "Leave empty to search in all the portal."
        ),
        required=False,
        vocabulary="plone.app.vocabularies.Catalog",
    )
    directives.widget(
        "discussion_folder",
        RelatedItemsFieldWidget,
        pattern_options={"is_folderish": True},
    )

    number_of_discussions = schema.Int(
        title=_("Number of discussions"),
        required=False,
        default=5,
        description=_("Specify how many discussions will be shown in the tile."),
    )
