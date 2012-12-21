from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI

from base import UpfrontAssessmentTestBase
from upfront.assessment.content.evaluationsheet import IEvaluationSheet

class TestEvaluationSheet(UpfrontAssessmentTestBase):
    """ Basic methods to test evaluation sheets """
    
    def test_evaluationsheet_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.assessment.content.evaluationsheet')
        self.assertNotEquals(None, fti)

    def test_evaluationsheet_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.assessment.content.evaluationsheet')
        schema = fti.lookupSchema()
        self.assertEquals(IEvaluationSheet, schema,
                                         'Evaluation Sheet schema incorrect.')

    def test_evaluationsheet_factory(self):
        fti = queryUtility(
            IDexterityFTI, name='upfront.assessment.content.evaluationsheet')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(
            IEvaluationSheet.providedBy(new_object), 
            'evaluation sheet provides wrong interface.')


