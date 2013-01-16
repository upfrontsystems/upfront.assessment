from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
import unittest2 as unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.testing import z2

from zope.component.hooks import getSite
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from plone.app.controlpanel.security import ISecuritySchema

from upfront.classlist.vocabs import availableLanguages
from upfront.assessment.eventhandlers import on_evaluationsheet_created

PROJECTNAME = "upfront.assessment"

class TestCase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.topictree
        import upfront.assessment
        import upfront.classlist
        import upfront.assessmentitem
        self.loadZCML(package=collective.topictree)
        self.loadZCML(package=upfront.assessment)
        self.loadZCML(package=upfront.classlist)
        self.loadZCML(package=upfront.assessmentitem)
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="fixture:Integration")


class UpfrontAssessmentTestBase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.intids = getUtility(IIntIds)

        # create members folder
        self.portal.invokeFactory(type_name='Folder', id='Members',
                                     title='Members')

        self.portal.invokeFactory(type_name='Folder', id='topictrees',
                                  title='Topic Trees')
        folder = self.portal._getOb('topictrees')

        self.topictrees = self.portal.topictrees
        self.topictrees.invokeFactory('collective.topictree.topictree',
                                      'language', title='Language')
        topictree = self.topictrees._getOb('language')

        topictree.invokeFactory('collective.topictree.topic',
                                'afrikaans', title='Afrikaans')
        self.topic1 = topictree._getOb('afrikaans')
        topictree.invokeFactory('collective.topictree.topic',
                                'english', title='English')
        self.topic2 = topictree._getOb('english')
        topictree.invokeFactory('collective.topictree.topic',
                                'xhosa', title='Xhosa')
        self.topic3 = topictree._getOb('xhosa')

        self.topictree = topictree

        # allow member folders to be created
        security_adapter =  ISecuritySchema(self.portal)
        security_adapter.set_enable_user_folders(True)
        # enable self-registration of users
        security_adapter.set_enable_self_reg(True)

        pm = getSite().portal_membership
        # create members folder
        pm.createMemberArea()
        members_folder = pm.getHomeFolder()

        # create classlists folder in members folder
        members_folder.invokeFactory(type_name='Folder', id='classlists',
                                     title='Class Lists')
        self.classlists = members_folder._getOb('classlists')

        # create assessments folder in members folder
        members_folder.invokeFactory(type_name='Folder', id='assessments',
                                     title='Assessments')
        self.assessments = members_folder._getOb('assessments')
    
        # create evaluation folder in members folder
        members_folder.invokeFactory(type_name='Folder', id='evaluation',
                                     title='Evaluation')
        self.evaluationsheets = members_folder._getOb('evaluation')

        # create classlists
        self.classlists.invokeFactory('upfront.classlist.content.classlist',
                                      'list1', title='Classlist1')
        self.classlist1 = self.classlists._getOb('list1')
        self.classlists.invokeFactory('upfront.classlist.content.classlist',
                                      'list2', title='Classlist2')
        self.classlist2 = self.classlists._getOb('list2')

        # add 3 learners to classlist1
        self.classlist1.invokeFactory('upfront.classlist.content.learner',
                                      'learner1', title='Learner1')
        self.learner1 = self.classlist1._getOb('learner1')
        self.classlist1.invokeFactory('upfront.classlist.content.learner',
                                      'learner2', title='Learner2')
        self.learner2 = self.classlist1._getOb('learner2')
        self.classlist1.invokeFactory('upfront.classlist.content.learner',
                                      'learner3', title='Learner3')
        self.learner3 = self.classlist1._getOb('learner3')

        # some details for learner1
        self.learner1.code = '1'
        self.learner1.name = 'John'
        self.learner1.gender = 'Male'

        # some details for learner2
        self.learner2.code = '2'
        self.learner2.name = 'Jennie'
        self.learner2.gender = 'Female'

        # some details for learner3
        self.learner3.code = '3'
        self.learner3.name = 'Nomsa'
        self.learner3.gender = 'Female'

        language_vocab = availableLanguages(self.classlist1).__iter__()
        #associate each language with a learner
        lang = language_vocab.next()
        self.learner1.home_language = RelationValue(lang.value)
        lang = language_vocab.next()
        self.learner2.home_language = RelationValue(lang.value)
        lang = language_vocab.next()
        self.learner3.home_language = RelationValue(lang.value)

        notify(ObjectModifiedEvent(self.learner1))
        notify(ObjectModifiedEvent(self.learner2))
        notify(ObjectModifiedEvent(self.learner3))


        # create assessments
        self.assessments.invokeFactory('upfront.assessment.content.assessment',
                                      'assessment1', title='Assessment1')
        self.assessment1 = self.assessments._getOb('assessment1')
        self.assessments.invokeFactory('upfront.assessment.content.assessment',
                                      'assessment2', title='Assessment2')
        self.assessment2 = self.assessments._getOb('assessment2')


        self.portal.invokeFactory(type_name='Folder', id='activities',
                                  title='Activities')
        self.activities = self.portal._getOb('activities')

        # create activities
        self.activities.invokeFactory('upfront.assessmentitem.content.assessmentitem',
                                      'assessmentitem1', title='Activity1')
        self.activity1 = self.activities._getOb('assessmentitem1')
        self.activities.invokeFactory('upfront.assessmentitem.content.assessmentitem',
                                      'assessmentitem2', title='Activity2')
        self.activity2 = self.activities._getOb('assessmentitem2')
        self.activities.invokeFactory('upfront.assessmentitem.content.assessmentitem',
                                      'assessmentitem3', title='Activity3')
        self.activity3 = self.activities._getOb('assessmentitem3')

        #create 2 extra topics
        topictree.invokeFactory('collective.topictree.topic',
                                'maths', title='Maths')
        self.topic4 = topictree._getOb('maths')
        topictree.invokeFactory('collective.topictree.topic',
                                'science', title='Science')
        self.topic5 = topictree._getOb('science')

        #associate activity1 with topic4
        self.activity1.topics = [RelationValue(self.intids.getId(self.topic4))]
        #associate activity2 with topic5
        self.activity2.topics = [RelationValue(self.intids.getId(self.topic5))]
        notify(ObjectModifiedEvent(self.activity1))
        notify(ObjectModifiedEvent(self.activity2))

        # add activities to assessment1
        self.assessment1.assessment_items = [
                            RelationValue(self.intids.getId(self.activity1)),
                            RelationValue(self.intids.getId(self.activity2)),
                            RelationValue(self.intids.getId(self.activity3)),
                            ]
        notify(ObjectModifiedEvent(self.assessment1))


        # create evaluationsheets
        eval_factory = 'upfront.assessment.content.evaluationsheet'
        self.evaluationsheets.invokeFactory(eval_factory,
                                      'evalsheet1', title='EvalSheet1')
        self.evaluationsheet1 = self.evaluationsheets._getOb('evalsheet1')
        self.evaluationsheets.invokeFactory(eval_factory,
                                      'evalsheet2', title='EvalSheet2')
        self.evaluationsheet2 = self.evaluationsheets._getOb('evalsheet2')

        classlist1_intid = self.intids.getId(self.classlist1)
        self.evaluationsheet1.classlist = RelationValue(classlist1_intid)
        self.evaluationsheet2.classlist = RelationValue(classlist1_intid)

        assessment1_intid = self.intids.getId(self.assessment1)
        self.evaluationsheet1.assessment = RelationValue(assessment1_intid)
        self.evaluationsheet2.assessment = RelationValue(assessment1_intid)

        notify(ObjectModifiedEvent(self.evaluationsheet1))
        # do not notify(ObjectModifiedEvent(self.evaluationsheet2)) as
        # it will be used to specifically to test eventhandlers

        # manually call eventhandlers to create evaluation objects
        # (they were called but all fields were not ready)
        on_evaluationsheet_created(self.evaluationsheet1,None)

        self.evaluation1 = self.evaluationsheet1.getFolderContents()[0].getObject()
        self.evaluation1.evaluation[0]['rating'] = 0
        self.evaluation1.evaluation[1]['rating'] = 0
        self.evaluation1.evaluation[2]['rating'] = 0
        notify(ObjectModifiedEvent(self.evaluation1))

        self.evaluation2 = self.evaluationsheet1.getFolderContents()[1].getObject()
        self.evaluation2.evaluation[0]['rating'] = 0
        self.evaluation2.evaluation[1]['rating'] = 0
        self.evaluation2.evaluation[2]['rating'] = 0
        notify(ObjectModifiedEvent(self.evaluation2))

        self.evaluation3 = self.evaluationsheet1.getFolderContents()[2].getObject()
        self.evaluation3.evaluation[0]['rating'] = 0
        self.evaluation3.evaluation[1]['rating'] = 0
        self.evaluation3.evaluation[2]['rating'] = 0
        notify(ObjectModifiedEvent(self.evaluation3))







