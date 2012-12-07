from five import grok

from z3c.form.i18n import MessageFactory as _
from plone.directives import dexterity, form

class IAssessment(form.Schema):
    """ Description of Assessment content type
    """


class Assessment(dexterity.Container):
    grok.implements(IAssessment)



