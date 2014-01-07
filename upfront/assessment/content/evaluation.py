from five import grok
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from upfront.assessment import MessageFactory as _
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import dexterity, form
from plone.indexer import indexer

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from upfront.classlist.content.learner import ILearner

UN_RATED  = -1 # This represents entries that the user has not rated yet
NOT_RATED = -2 # This represents explicitly NOT-RATED (user set as NOT-RATED)

class IEvaluationFieldSchema(Interface):
    """ Schema for evaluation datagrid field, stores the UID for each
        assessment item and an integer field for the rating or evaluation.
    """

    uid = schema.TextLine(title=u"UID")
    rating = schema.Int(title=u"Rating")

@indexer(IEvaluationFieldSchema)
def activity_id_indexer(obj):
    pc = getToolByName(obj, 'portal_catalog')
    activity = pc(UID = obj.uid)
    return activity.id
grok.global_adapter(activity_id_indexer, name="activity_id")

class IEvaluation(form.Schema):
    """ Description of Evaluation content type
    """

    form.omitted('learner')
    learner = RelationChoice(
            title=_(u"Learner"),            
            source=ObjPathSourceBinder(object_provides=ILearner.__identifier__),
            required=False,
        )

    form.widget(evaluation=DataGridFieldFactory)
    evaluation = schema.List(
            title=u"Evaluation",
            value_type=DictRow(title=u"tablerow", schema=IEvaluationFieldSchema)
        )


class Evaluation(dexterity.Item):
    grok.implements(IEvaluation)

    def getState(self):
        pw = getSite().portal_workflow
        # get state of object from workflow state
        state = pw.getStatusOf('evaluation_workflow',self)['state']
        if state == 'complete':
            msg = _('Complete')
        else: 
            msg = _('In-Progress')
        return msg
    

grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IEvaluation)
    grok.require('zope2.View')
    grok.template('evaluation-view')

    #  __call__ calls update before generating the template
    def update(self, **kwargs):

        # check if form has been submitted
        if self.request.form.has_key('buttons.update.evaluation.submit'):

            new_rating_list = []
            for evaluation in self.context.evaluation:
                uid = evaluation['uid']
                activity = 'activity_' + uid
                rating_value = self.request.form[activity]
                new_rating_list.append(rating_value)

            # update rating values
            for i in range(len(new_rating_list)):
                self.context.evaluation[i]['rating'] = int(new_rating_list[i])
            notify(ObjectModifiedEvent(self.context))

            parent_url = self.context.aq_parent.absolute_url()
            return self.request.RESPONSE.redirect(parent_url)

    def evaluation_view_url(self):
        """ Return the context url
        """
        return self.context.absolute_url()

    def evaluation_table(self):
        """ Return all data in the evaluation table of an evaluation object
        """
        return self.context.evaluation

    def learner_name(self):
        """ Return the learner that is associated with evaluation object
        """
        return self.context.learner.to_object.name

    def not_rated(self):
        """ Return the explicitly not_rated constant """
        return NOT_RATED

