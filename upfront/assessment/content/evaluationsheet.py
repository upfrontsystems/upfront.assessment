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

    def getTitle(self):
        return '%s %s' % (self.assessment.to_object.title,
                          self.classlist.to_object.title)

    def setTitle(self, value):
        pass

    title = property(getTitle, setTitle)

grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IEvaluationSheet)
    grok.require('zope2.View')
    grok.template('evaluationsheet-view')

    def evaluations(self):
        """ Return all evaluations in the current folder
        """
        contentFilter = {
            'portal_type': 'upfront.assessment.content.evaluation'}
        return self.context.getFolderContents(contentFilter)

    def evaluationsheet(self):
        """ Return the current evaluationsheet
        """
        return self.context
