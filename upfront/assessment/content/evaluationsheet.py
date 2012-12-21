from five import grok

from z3c.form.i18n import MessageFactory as _
from z3c.form.browser.select import SelectFieldWidget
from z3c.relationfield.schema import RelationChoice
from plone.directives import dexterity, form

from upfront.assessment.vocabs import availableAssessments
from upfront.assessment.vocabs import availableClassLists


class IEvaluationSheet(form.Schema):
    """ Description of Evaluation Sheet content type
    """

    form.widget(assessment=SelectFieldWidget)
    assessment = RelationChoice(
            title=_(u"Assessment"),
            source=availableAssessments,
        )

    form.widget(classlist=SelectFieldWidget)
    classlist = RelationChoice(
            title=_(u"Class List"),
            source=availableClassLists,
        )


class EvaluationSheet(dexterity.Container):
    grok.implements(IEvaluationSheet)


grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IEvaluationSheet)
    grok.require('zope2.View')
    grok.template('evaluationsheet-view')

    # XXX Add a custom view for evaluation sheet that lists all the learners
    #     and the state of their evaluation.
    # XXX Hyperlink the learner's name to their "evaluation" instance.

