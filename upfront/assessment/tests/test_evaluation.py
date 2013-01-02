from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI
from zope.component.hooks import getSite

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

    def test_getState(self):
        pw = getSite().portal_workflow
        state = pw.getStatusOf('evaluation_workflow',self.evaluation1)['state']
        self.assertEquals(state.capitalize(),self.evaluation1.getState())

    def test_update(self):
        view = self.evaluation1.restrictedTraverse('@@view')
        self.request.form['buttons.update.evaluation.submit'] = 'aplaceholder'
        act1 = 'activity_' + self.evaluation1.evaluation[0]['uid']
        act2 = 'activity_' + self.evaluation1.evaluation[1]['uid']
        act3 = 'activity_' + self.evaluation1.evaluation[2]['uid']
        self.request.form[act1] = '1'
        self.request.form[act2] = '2'
        self.request.form[act3] = '3'
        url = view.update()
        self.assertEquals(self.evaluation1.aq_parent.absolute_url(),url)
        self.assertEquals(self.evaluation1.evaluation[0]['rating'],1)
        self.assertEquals(self.evaluation1.evaluation[1]['rating'],2)
        self.assertEquals(self.evaluation1.evaluation[2]['rating'],3)

    def test_evaluation_view_url(self):
        view = self.evaluation1.restrictedTraverse('@@view')
        self.assertEquals(view.evaluation_view_url(),
                          self.evaluation1.absolute_url())

    def test_evaluation_table(self):
        view = self.evaluation1.restrictedTraverse('@@view')
        self.assertEquals(view.evaluation_table(),self.evaluation1.evaluation)

