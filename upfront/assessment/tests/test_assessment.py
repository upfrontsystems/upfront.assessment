import json
from zope.component import createObject
from zope.component import queryUtility
from zope.component.hooks import getSite
from plone.dexterity.interfaces import IDexterityFTI
 
from base import UpfrontAssessmentTestBase
from upfront.assessment.content.assessment import IAssessment


class TestAssessment(UpfrontAssessmentTestBase):
    """ Basic methods to test assessments """
    
    def test_assessment_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.assessment.content.assessment')
        self.assertNotEquals(None, fti)

    def test_assessment_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.assessment.content.assessment')
        schema = fti.lookupSchema()
        self.assertEquals(IAssessment, schema, 'Assessment schema incorrect.')

    def test_assessment_factory(self):
        fti = queryUtility(
            IDexterityFTI, name='upfront.assessment.content.assessment')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(
            IAssessment.providedBy(new_object), 
            'assessment provides wrong interface.')

    def test_assessment(self):
        view = self.assessment1.restrictedTraverse('@@view')
        self.assertEqual(view.assessment(),self.assessment1.title)

    def test_add_activities_url(self):
        view = self.assessment1.restrictedTraverse('@@view')
        self.assertEqual(view.add_activities_url(),
                         '%s/activities' % getSite().absolute_url())

    def test_topics(self):
        view = self.assessment1.restrictedTraverse('@@view')
        self.assertEquals(view.topics(),['Maths', 'Science'])

    def test_activities(self):
        view = self.assessment1.restrictedTraverse('@@view')
        self.assertEquals([self.activity1,self.activity2,self.activity3],
                          view.activities())

    def test_first_activity(self):
        view = self.assessment1.restrictedTraverse('@@view')
        self.assertEquals(self.activity1,view.first_activity())

    def test_last_activity(self):
        view = self.assessment1.restrictedTraverse('@@view')
        self.assertEquals(self.activity3,view.last_activity())


class TestRemoveAssessmentItemView(UpfrontAssessmentTestBase):
    """ Test RemoveAssessmentItem browser view """

    def test__call__(self):
        view = self.assessment1.restrictedTraverse('@@remove-assessmentitem')

        self.assertEqual(len(self.assessment1.assessment_items),3)
        self.request.set('remove_id','assessmentitem1')
        test = json.dumps({'status'   : 'info',
                            'msg' :"Activity removed",
                            'remove_id' : 'assessmentitem1'})
        self.assertEqual(view(),test)
        self.assertEqual(len(self.assessment1.assessment_items),2)


class TestMoveUpAssessmentItemView(UpfrontAssessmentTestBase):
    """ Test MoveUpAssessmentItem browser view """

    def test__call__(self):
        view = self.assessment1.restrictedTraverse('@@move-up-assessmentitem')

        self.assertEqual(len(self.assessment1.assessment_items),3)

        item1 = self.assessment1.assessment_items[0]
        item2 = self.assessment1.assessment_items[1]
        item3 = self.assessment1.assessment_items[2]

        self.request.set('id','assessmentitem3')
        test = json.dumps({'status'   : 'info',
                            'msg' :"Activity moved up",
                            'id' : 'assessmentitem3'})
        self.assertEqual(view(),test)
        self.assertEqual(len(self.assessment1.assessment_items),3)
        self.assertEqual([item1,item3,item2],self.assessment1.assessment_items)


class TestMoveDownAssessmentItemView(UpfrontAssessmentTestBase):
    """ Test MoveUpAssessmentItem browser view """

    def test__call__(self):
        view = self.assessment1.restrictedTraverse('@@move-down-assessmentitem')

        self.assertEqual(len(self.assessment1.assessment_items),3)

        item1 = self.assessment1.assessment_items[0]
        item2 = self.assessment1.assessment_items[1]
        item3 = self.assessment1.assessment_items[2]

        self.request.set('id','assessmentitem1')
        test = json.dumps({'status'   : 'info',
                            'msg' :"Activity moved down",
                            'id' : 'assessmentitem1'})
        self.assertEqual(view(),test)
        self.assertEqual(len(self.assessment1.assessment_items),3)
        self.assertEqual([item2,item1,item3],self.assessment1.assessment_items)

