from base import UpfrontAssessmentTestBase
from upfront.assessment.vocabs import availableAssessments
from upfront.assessment.vocabs import availableClassLists

class TestAssessmentVocabs(UpfrontAssessmentTestBase):
    """ Basic methods to test vocabs """

    def test_availableAssessments(self):
        self.assertEquals(True,True)
        self.assertEqual(len(availableAssessments(self.portal)), 2)
        assessment = availableAssessments(self.portal).__iter__()
        self.assertEqual(assessment.next().title,'Assessment1')
        self.assertEqual(assessment.next().title,'Assessment2')

    def test_availableClassLists(self):
        self.assertEquals(True,True)
        self.assertEqual(len(availableClassLists(self.portal)), 2)
        classlist = availableClassLists(self.portal).__iter__()
        self.assertEqual(classlist.next().title,'Classlist1')
        self.assertEqual(classlist.next().title,'Classlist2')

