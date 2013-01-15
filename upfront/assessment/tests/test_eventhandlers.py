from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.component.hooks import getSite
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName

from base import UpfrontAssessmentTestBase
from upfront.assessment.eventhandlers import on_evaluationsheet_created,\
                                             on_evaluation_modified

class TestEventhandlers(UpfrontAssessmentTestBase):
    """ Test event handlers """
    
    def test_on_evaluationsheet_created(self):

        cF = {'portal_type': 'upfront.assessment.content.evaluation'}
        self.evaluationsheet1.getFolderContents(cF)
        self.assertEqual(len(self.evaluationsheet2.getFolderContents(cF)),0)
        on_evaluationsheet_created(self.evaluationsheet2, None)
        evaluations = self.evaluationsheet2.getFolderContents(cF)
        self.assertEqual(len(self.evaluationsheet2.getFolderContents(cF)),3)
        self.assertEqual(evaluations[0].getObject().id,
                         'evaluation-list1-assessment1-learner1')
        self.assertEqual(evaluations[1].getObject().id,
                         'evaluation-list1-assessment1-learner2')
        self.assertEqual(evaluations[2].getObject().id,
                         'evaluation-list1-assessment1-learner3')
        self.assertEqual(evaluations[0].getObject().evaluation[0]['rating'],0)
        self.assertEqual(evaluations[0].getObject().evaluation[1]['rating'],0)
        self.assertEqual(evaluations[0].getObject().evaluation[2]['rating'],0)
        self.assertEqual(evaluations[0].getObject().evaluation[0]['uid'],
                         IUUID(self.activity1))
        self.assertEqual(evaluations[0].getObject().evaluation[1]['uid'],
                         IUUID(self.activity2))
        self.assertEqual(evaluations[0].getObject().evaluation[2]['uid'],
                         IUUID(self.activity3))    

    def test_on_evaluation_modified(self):

        pw = getSite().portal_workflow
        state = pw.getStatusOf('evaluation_workflow',self.evaluation1)['state']
        # test in-progress -> complete
        self.evaluation1.evaluation[0]['rating'] = 1
        self.evaluation1.evaluation[1]['rating'] = 1
        self.evaluation1.evaluation[2]['rating'] = 1
        on_evaluation_modified(self.evaluation1, None)
        state = pw.getStatusOf('evaluation_workflow',self.evaluation1)['state']
        self.assertEquals(state,'complete')
        # test complete -> in-progress
        self.evaluation1.evaluation[0]['rating'] = 0
        on_evaluation_modified(self.evaluation1, None)
        state = pw.getStatusOf('evaluation_workflow',self.evaluation1)['state']
        self.assertEquals(state,'in-progress')

    def test_on_evaluationsheet_modified(self):
        pw = getSite().portal_workflow
        state = pw.getStatusOf('evaluationsheet_workflow',
                                                self.evaluationsheet1)['state']
        # test in-progress -> complete
        self.assertEquals(state,'in-progress')
        # test in-progress -> complete
        self.evaluation1.evaluation[0]['rating'] = 1
        self.evaluation1.evaluation[1]['rating'] = 1
        self.evaluation1.evaluation[2]['rating'] = 1
        # call on_evaluation_modified which calls on_evaluationsheet_modified
        on_evaluation_modified(self.evaluation1, None)
        state = pw.getStatusOf('evaluation_workflow',self.evaluation1)['state']
        self.assertEquals(state,'complete')

