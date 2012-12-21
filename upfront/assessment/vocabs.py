from five import grok
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder

from Products.CMFCore.utils import getToolByName

@grok.provider(IContextSourceBinder)
def availableAssessments(context):
    terms = []

    # get all the assessments from the member's assessments folder
    pm = getToolByName(context, 'portal_membership')
    members_folder = pm.getHomeFolder()
    assessments_folder = members_folder._getOb('assessments')
    contentFilter = { 'portal_type': 'upfront.assessment.content.assessment'}
    
    for brain in assessments_folder.getFolderContents(contentFilter):
        assessment = brain.getObject()
        intids = getUtility(IIntIds)
        assessment_intid = intids.getId(assessment)
        terms.append(SimpleVocabulary.createTerm(assessment_intid,
                                                 assessment_intid,
                                                 brain.Title))
    return SimpleVocabulary(terms)

@grok.provider(IContextSourceBinder)
def availableClassLists(context):
    terms = []

    # get all the classlists from the member's classlists folder
    pm = getToolByName(context, 'portal_membership')
    members_folder = pm.getHomeFolder()
    classlists_folder = members_folder._getOb('classlists')
    contentFilter = { 'portal_type': 'upfront.classlist.content.classlist'}

    for brain in classlists_folder.getFolderContents(contentFilter):
        classlist = brain.getObject()
        intids = getUtility(IIntIds)
        classlist_intid = intids.getId(classlist)
        terms.append(SimpleVocabulary.createTerm(classlist_intid,
                                                 classlist_intid,
                                                 brain.Title))
    return SimpleVocabulary(terms)
