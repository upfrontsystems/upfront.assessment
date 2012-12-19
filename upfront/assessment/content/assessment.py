from five import grok

from zope.component.hooks import getSite
from z3c.form.i18n import MessageFactory as _
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.directives import dexterity, form
from plone.formwidget.contenttree import ObjPathSourceBinder

from upfront.assessmentitem.content.assessmentitem import IAssessmentItem

class IAssessment(form.Schema):
    """ Description of Assessment content type
    """

    form.omitted('assessment_items')
    assessment_items = RelationList(
            title=u"Assessment Items",
            default=[],
            value_type=RelationChoice(title=_(u"Related"),
    source=ObjPathSourceBinder(object_provides=IAssessmentItem.__identifier__)),
            required=False,
        )

class Assessment(dexterity.Container):
    grok.implements(IAssessment)


grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IAssessment)
    grok.require('zope2.View')
    grok.template('assessment-view')

    def add_activities_url(self):
        """ url to activities view """
        return '%s/activities' % getSite().absolute_url()

    def activities(self):
        """ Return all the activities that this assessment references
        """
        return [x.to_object for x in self.context.assessment_items]


