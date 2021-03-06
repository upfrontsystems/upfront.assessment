import json
import unicodedata
from five import grok

from zope.interface import Interface
from zope.component.hooks import getSite
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from upfront.assessment import MessageFactory as _
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

    def is_editable(self): 
        """ Check whether the assessment can be edited 
            ie. it is not in use by evaluationsheets.
        """
        pw = getSite().portal_workflow
        state = pw.getStatusOf('assessment_workflow',self)['state']
        if state == 'editable':
            return True
        return False


grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.context(IAssessment)
    grok.require('zope2.View')
    grok.template('assessment-view')

    def assessment(self):
        """ Return the currently selected assessment
        """
        return self.context.title

    def add_activities_url(self):
        """ url to activities view """
        return '%s/activities' % getSite().absolute_url()

    def topics(self):
        """ Return all the topics in the activities that this assessment 
            references
        """
        activities = [x.to_object for x in self.context.assessment_items]
        topic_list = []
        for activity in activities:
            if hasattr(activity,'topics'):
                topics = activity.topics
                for topic in topics:
                    if topic.to_object.title not in topic_list:
                        # convert to string from unicode if necessary
                        if isinstance(topic.to_object.title, unicode):    
                            topic_string = unicodedata.normalize('NFKD',
                                topic.to_object.title).encode('ascii','ignore')
                            topic_list.append(topic_string)
                        else:
                            topic_list.append(topic.to_object.title)

        topic_list.sort(key=str.lower)
        return topic_list

    def activities(self):
        """ Return all the activities that this assessment references
        """
        return [x.to_object for x in self.context.assessment_items]

    def first_activity(self):
        """ Return first activity
        """
        return self.context.assessment_items[0].to_object

    def last_activity(self):
        """ Return last activity
        """        
        last_index = len(self.context.assessment_items)-1
        return self.context.assessment_items[last_index].to_object



class RemoveAssessmentItemView(grok.View):
    """ Removes the selected assessmentitem from an assessment
    """
    grok.context(IAssessment)
    grok.name('remove-assessmentitem')
    grok.require('zope2.View')

    def __call__(self):
        """ Removes the selected assessmentitem from an assessment """

        remove_id = self.request.get('remove_id', '')

        assessment = self.context
        assessment_items = []
        # remove assessment item from assessment_items relation list
        for item in assessment.assessment_items:
            if item.to_object.id != remove_id:
                assessment_items.append(item)

        assessment.assessment_items = assessment_items
        notify(ObjectModifiedEvent(assessment))

        # success
        msg = _("Activity removed")
        return json.dumps({'status'    : 'info',
                           'msg'       : msg,
                           'remove_id' : remove_id })

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class MoveUpAssessmentItemView(grok.View):
    """ Moves the selected assessmentitem up in the assessment
    """
    grok.context(IAssessment)
    grok.name('move-up-assessmentitem')
    grok.require('zope2.View')

    def __call__(self):
        """ Moves the selected assessmentitem up in the assessment """

        move_id = self.request.get('id', '')

        assessment = self.context
        assessment_items = assessment.assessment_items

        # find the position of the item with the id
        id_list = [x.to_object.id for x in assessment_items]
        index = id_list.index(move_id)
        item_to_move = assessment_items[index]

        # implement move up
        del assessment_items[index]
        assessment_items.insert(index-1,item_to_move)

        # reindex
        assessment.assessment_items = assessment_items
        notify(ObjectModifiedEvent(assessment))

        # success
        msg = _("Activity moved up")
        # move up and move down are sometimes dynamically inserted by ajax
        # these strings are provided so that they are correctly translated.
        move_up_str = self.context.translate(_("Move up"))
        move_down_str = self.context.translate(_("Move down"))
        return json.dumps({'status'        : 'info',
                           'msg'           : msg,
                           'id'            : move_id,
                           'move_up_str'   : move_up_str,
                           'move_down_str' : move_down_str })

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class MoveDownAssessmentItemView(grok.View):
    """ Moves the selected assessmentitem down in the assessment
    """
    grok.context(IAssessment)
    grok.name('move-down-assessmentitem')
    grok.require('zope2.View')

    def __call__(self):
        """ Moves the selected assessmentitem down in the assessment """

        move_id = self.request.get('id', '')

        assessment = self.context
        assessment_items = assessment.assessment_items

        # find the position of the item with the id
        id_list = [x.to_object.id for x in assessment_items]
        index = id_list.index(move_id)
        item_to_move = assessment_items[index]

        # implement move down
        del assessment_items[index]
        assessment_items.insert(index+1,item_to_move)

        # reindex
        assessment.assessment_items = assessment_items
        notify(ObjectModifiedEvent(assessment))

        # success
        msg = _("Activity moved down")
        # move up and move down are sometimes dynamically inserted by ajax
        # these strings are provided so that they are correctly translated.
        move_up_str = self.context.translate(_("Move up"))
        move_down_str = self.context.translate(_("Move down"))
        return json.dumps({'status'        : 'info',
                           'msg'           : msg,
                           'id'            : move_id,
                           'move_up_str'   : move_up_str,
                           'move_down_str' : move_down_str })

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
