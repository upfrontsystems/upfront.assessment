from five import grok
from zope import schema
from zope.interface import Interface
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
        # XXX get state of object from workflow state
        return 'Temp message'
    

grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IEvaluation)
    grok.require('zope2.View')
    grok.template('evaluation-view')

    def evaluation_table(self):
        """ Return all data in the evaluation table of an evaluation object
        """
        return self.context.evaluation



