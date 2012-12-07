from zope.component import createObject
from zope.component import queryUtility
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
            'class list provides wrong interface.')


