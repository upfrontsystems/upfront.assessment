from DateTime import DateTime
from five import grok
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.component.hooks import getSite
from zc.relation.interfaces import ICatalog
from z3c.relationfield import RelationValue
from plone.uuid.interfaces import IUUID
from Products.CMFCore.WorkflowCore import WorkflowException

from upfront.assessment.content.evaluationsheet import IEvaluationSheet
from upfront.assessment.content.evaluation import IEvaluation

@grok.subscribe(IEvaluationSheet, IObjectAddedEvent)
def on_evaluationsheet_created(evaluationsheet, event):
    """ Create evaluation objects for each learner in the class list associated
        with this Evaluation Sheet. Also transition associated assessment into
        frozen (non-editable) state.
    """
    
    # if for some reason this eventhandler is called before
    # evaluationsheet is completely ready with all its fields - (in unit tests)
    if evaluationsheet.classlist is None:
        return
    if evaluationsheet.assessment is None:    
        return
    
    classlist = evaluationsheet.classlist.to_object
    assessment = evaluationsheet.assessment.to_object
    intids = getUtility(IIntIds)    

    contentFilter = { 'portal_type': 'upfront.classlist.content.learner',
                      'sort_on': 'sortable_title'}
    # create an evaluation for each learner in classlist
    for brain in classlist.getFolderContents(contentFilter):
        
        # use classlist, assessment and learner in the evaluation object's id
        evaluation_id = 'evaluation-' + classlist.id + '-'\
                        + assessment.id + '-' + brain.id;
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
            initial_rating = 0
            evaluation_dict.append({'uid': uid,
                                   'rating': initial_rating,
                                   'rating_scale': assessmentitem.rating_scale})

        new_evaluation.evaluation = evaluation_dict
        notify(ObjectModifiedEvent(new_evaluation))

    # freeze the associated assessment and classlist as they are now in use
    # with this evaluationsheet
    pw = getSite().portal_workflow
    state = pw.getStatusOf('assessment_workflow',assessment)['state']
    if state == 'editable':   
        try:
           pw.doActionFor(assessment, "set_frozen")
        except WorkflowException:    
           pass
    state = pw.getStatusOf('classlist_workflow',classlist)['state']
    if state == 'editable':   
        try:
           pw.doActionFor(classlist, "set_frozen")
        except WorkflowException:    
           pass


@grok.subscribe(IEvaluationSheet, IObjectRemovedEvent)
def on_evaluationsheet_deleted(evaluationsheet, event):
    """ Check whether the associated assessment of this deleted evaluationsheet
        is still in use by other evaluationsheets, if not, allow it to be 
        editable once more. Do the same for associated classlists.
    """

    assessment = evaluationsheet.assessment.to_object
    classlist = evaluationsheet.classlist.to_object
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result_assessment = catalog.findRelations({
        'to_id': intids.getId(assessment),
        'from_attribute': 'assessment'
        })
    result_classlist = catalog.findRelations({
        'to_id': intids.getId(classlist),
        'from_attribute': 'classlist'
        })

    try:
        rel = result_assessment.next()
    except StopIteration:
        # unfreeze the assessment
        pw = getSite().portal_workflow
        state = pw.getStatusOf('assessment_workflow',assessment)['state']
        if state == 'frozen':   
            try:
               pw.doActionFor(assessment, "set_editable")
            except WorkflowException:    
               pass
    try:
        rel = result_classlist.next()
    except StopIteration:
        # unfreeze the classlist
        pw = getSite().portal_workflow
        state = pw.getStatusOf('classlist_workflow',classlist)['state']
        if state == 'frozen':   
            try:
               pw.doActionFor(classlist, "set_editable")
            except WorkflowException:    
               pass


@grok.subscribe(IEvaluation, IObjectModifiedEvent)
def on_evaluation_modified(evaluation, event):
    """ Test if evaluation is completed and adjust workflow state appropriately
    """

    pw = getSite().portal_workflow

    # get state of object from workflow state
    state = pw.getStatusOf('evaluation_workflow',evaluation)['state']

    # test if complete state has to be reverted to in-progress
    if state == 'complete':
        transition = False
        for obj in evaluation.evaluation:
            rating = obj['rating']
            if rating == 0:
                # if one zero is found, that means that evaluation is incomplete
                transition = True
    
        if transition:
            try:
                pw.doActionFor(evaluation, "set_inprogress")
            except WorkflowException:       
                pass
        return

    # test if evaluation is complete
    if state == 'in-progress':
        transition = True        
        if len(evaluation.evaluation) == 0:
            # evaluation object with no activities 
            # (assessment had no activities) - do not transition to complete
            transition = False
        for obj in evaluation.evaluation:
            rating = obj['rating']
            if rating == 0:
                # if one zero is found, that means that evaluation is incomplete
                transition = False

        if transition:
            try:
                pw.doActionFor(evaluation, "set_complete")
                # call the eventhandler of parent evaluationsheet
                notify(ObjectModifiedEvent(evaluation.aq_parent))
            except WorkflowException:  
                pass
        return


@grok.subscribe(IEvaluationSheet, IObjectModifiedEvent)
def on_evaluationsheet_modified(evaluationsheet, event):
    """ Test if evaluation sheet is completed and adjust workflow state 
        appropriately
    """

    pw = getSite().portal_workflow
    state = pw.getStatusOf('evaluationsheet_workflow',evaluationsheet)['state']

    # test if evaluationsheet is complete
    if state == 'in-progress':
        # check all evaluation objects that in this evaluationsheet container
        contentFilter = {'portal_type': 'upfront.assessment.content.evaluation'}
        if len(evaluationsheet.getFolderContents(contentFilter)) == 0:
            # no evaluations have yet been created
            return
        for evaluation in evaluationsheet.getFolderContents(contentFilter):
            wf_state = pw.getStatusOf('evaluation_workflow',
                                      evaluation.getObject())['state']
            if wf_state == 'in-progress':
                # if one in-progress is found, it means that evaluationsheet 
                # is incomplete
                return

        try:
            pw.doActionFor(evaluationsheet, "set_complete")
            # Set effective date on the object to now
            now = DateTime()
            evaluationsheet.setEffectiveDate(now)
            # update catalog indexes
            notify(ObjectModifiedEvent(evaluationsheet))
        except WorkflowException:  
            pass
        return

