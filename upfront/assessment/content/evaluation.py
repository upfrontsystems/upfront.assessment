from five import grok
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from z3c.form.i18n import MessageFactory as _
from z3c.relationfield import Relation
from plone.directives import dexterity, form

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

class IEvaluationFieldSchema(Interface):
    """ Schema for evaluation datagrid field, stores the UID for each
        assessment item and an integer field for the rating or evaluation.
    """

    uid = schema.TextLine(title=u"UID")
    rating = schema.Int(title=u"Rating")


class IEvaluation(form.Schema):
    """ Description of Evaluation content type
    """

#    learner = Relation(
#           title=_(u"Learner"),
#        )

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
        return state.capitalize()
    

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

    def evaluationsheet_view_url(self):
        """ Return the evaluation's parent url
        """
        return self.context.aq_parent.absolute_url()

    def evaluation_view_url(self):
        """ Return the context url
        """
        return self.context.absolute_url()

    def evaluation_table(self):
        """ Return all data in the evaluation table of an evaluation object
        """
        return self.context.evaluation

