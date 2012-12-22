from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI

from base import UpfrontAssessmentTestBase
from upfront.assessment.content.evaluation import IEvaluation

class TestEvaluation(UpfrontAssessmentTestBase):
    """ Basic methods to test evaluations """
    
    def test_evaluation_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.assessment.content.evaluation')
        self.assertNotEquals(None, fti)

    def test_evaluation_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.assessment.content.evaluation')
        schema = fti.lookupSchema()
        self.assertEquals(IEvaluation, schema,
                                         'Evaluation Sheet schema incorrect.')

    def test_evaluation_factory(self):
        fti = queryUtility(
            IDexterityFTI, name='upfront.assessment.content.evaluation')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(
            IEvaluation.providedBy(new_object), 
            'evaluation provides wrong interface.')
