from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DiscussionStatesVocabulary:
    """
    A simple vocab to translate the discussion states
    """

    def __call__(self, context):
        wf_tool = api.portal.get_tool("portal_workflow")
        wf_id = wf_tool.getChainForPortalType("Discussion Item")[-1]
        workflow = wf_tool.getWorkflowById(wf_id)
        if workflow is None:
            return SimpleVocabulary.fromItems([])
        request = getRequest()
        items = []
        for state in workflow.states.values():
            title = translate(state.title_or_id, domain="plone", context=request)
            items.append((title, state.getId()))
        return SimpleVocabulary.fromItems(items)


DiscussionStatesVocabularyFactory = DiscussionStatesVocabulary()
