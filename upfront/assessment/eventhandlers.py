from five import grok

from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.component import createObject
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from z3c.relationfield import RelationValue

#from plone.dexterity.interfaces import IDexterityFTI

from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName

from upfront.assessment.content.evaluationsheet import IEvaluationSheet

@grok.subscribe(IEvaluationSheet, IObjectAddedEvent)
def onEvaluationSheetCreated(evaluationsheet, event):
    """ Create evaluation objects for each learner in the class list associated
        with this Evaluation Sheet
    """

    classlist = evaluationsheet.classlist.to_object
    assessment = evaluationsheet.assessment.to_object
    intids = getUtility(IIntIds)    

    contentFilter = { 'portal_type': 'upfront.classlist.content.learner'}
    # create an evaluation for each learner in classlist    
    for brain in classlist.getFolderContents(contentFilter):
        
        # use classlist, assessment and learner in the evaluation object's id
        evaluation_id = 'evaluation-' + classlist.id + '-'\
                        + assessment.id + '-learner-' + brain.id;
        evaluationsheet.invokeFactory('upfront.assessment.content.evaluation',
                                     evaluation_id,
                                     title=evaluation_id)
        new_evaluation = evaluationsheet._getOb(evaluation_id)

        learner = brain.getObject()
        learner_intid = intids.getId(learner)
        new_evaluation.learner = RelationValue(learner_intid)

        evaluation_dict = []
        # populate evaluation field
        for assessmentitem in [x.to_object for x in assessment.assessment_items]:
            uid = IUUID(assessmentitem)
            initial_rating = 0 #XXX Setting initial rating to 0 - needs review
            evaluation_dict.append({'uid': uid, 'rating': initial_rating})

        new_evaluation.evaluation = evaluation_dict
        notify(ObjectModifiedEvent(new_evaluation))

