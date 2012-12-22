from five import grok
from zope import schema
from zope.interface import Interface
from z3c.form.i18n import MessageFactory as _
from z3c.relationfield.schema import Relation
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

    learner = Relation(
           title=_(u"Learner")
        )

    form.widget(evaluation=DataGridFieldFactory)
    evaluation = schema.List(
            title=u"Evaluation",
            value_type=DictRow(title=u"tablerow", schema=IEvaluationFieldSchema)
        )


class Evaluation(dexterity.Item):
    grok.implements(IEvaluation)


grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IEvaluation)
    grok.require('zope2.View')
    grok.template('evaluation-view')

    # XXX Add a custom view for evaluation similar to FullMarks marks sheet
    # (Go to Tests -> Marks and add a mark sheet).


