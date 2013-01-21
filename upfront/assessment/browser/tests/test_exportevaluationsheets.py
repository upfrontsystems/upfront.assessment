import datetime
from time import time
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from z3c.form.i18n import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from upfront.assessment.tests.base import UpfrontAssessmentTestBase
#from upfront.assessment.eventhandlers import on_evaluation_modified

class TestExportEvaluationSheetsView(UpfrontAssessmentTestBase):
    """ Test ExportEvaluationSheetsView view """

    def test_evaluation_sheets_csv(self):

        view = self.portal.restrictedTraverse('@@export-evaluationsheets')
        test_out = view()
        self.assertEqual(test_out,None)

        # create a completed evaluationsheet (complete existing incomplete one)
        self.evaluation1.evaluation[0]['rating'] = 1
        self.evaluation1.evaluation[1]['rating'] = 1
        self.evaluation1.evaluation[2]['rating'] = 1
        notify(ObjectModifiedEvent(self.evaluation1))
        self.evaluation2.evaluation[0]['rating'] = 3
        self.evaluation2.evaluation[1]['rating'] = 3
        self.evaluation2.evaluation[2]['rating'] = 3
        notify(ObjectModifiedEvent(self.evaluation2))
        self.evaluation3.evaluation[0]['rating'] = 4
        self.evaluation3.evaluation[1]['rating'] = 4
        self.evaluation3.evaluation[2]['rating'] = 4
        notify(ObjectModifiedEvent(self.evaluation3))

        view = self.portal.restrictedTraverse('@@export-evaluationsheets')
        test_out = view()

        now = datetime.datetime.now()
        datetime_str = now.strftime('%d %B %Y')

        csv_ref = 'assessment1,' + datetime_str +',list1,John,1,1\r\n' +\
                  'assessment1,' + datetime_str +',list1,John,2,1\r\n' +\
                  'assessment1,' + datetime_str +',list1,John,3,1\r\n' +\
                  'assessment1,' + datetime_str +',list1,Jennie,1,3\r\n' +\
                  'assessment1,' + datetime_str +',list1,Jennie,2,3\r\n' +\
                  'assessment1,' + datetime_str +',list1,Jennie,3,3\r\n' +\
                  'assessment1,' + datetime_str +',list1,Nomsa,1,4\r\n' +\
                  'assessment1,' + datetime_str +',list1,Nomsa,2,4\r\n' +\
                  'assessment1,' + datetime_str +',list1,Nomsa,3,4\r\n'

        self.assertEqual(test_out,csv_ref)

        start = str(int(time())-500)
        end = str(int(time()))

        # test with some date paramenters on the request
        self.request.set('start_date',start)
        self.request.set('end_date',end)
        view = self.portal.restrictedTraverse('@@export-evaluationsheets')
        test_out = view()
        self.assertEqual(test_out,csv_ref)

    def test__call__(self):

        view = self.portal.restrictedTraverse('@@export-evaluationsheets')
        test_out = view()
        self.assertEqual(test_out,None)
        test = IStatusMessage(self.request).show()
        self.assertEqual(test[0].type,'info')
        self.assertEqual(test[0].message,'No completed evaluationsheets exist')

        # create a completed evaluationsheet (complete existing incomplete one)
        self.evaluation1.evaluation[0]['rating'] = 1
        self.evaluation1.evaluation[1]['rating'] = 1
        self.evaluation1.evaluation[2]['rating'] = 1
        notify(ObjectModifiedEvent(self.evaluation1))
        self.evaluation2.evaluation[0]['rating'] = 3
        self.evaluation2.evaluation[1]['rating'] = 3
        self.evaluation2.evaluation[2]['rating'] = 3
        notify(ObjectModifiedEvent(self.evaluation2))
        self.evaluation3.evaluation[0]['rating'] = 4
        self.evaluation3.evaluation[1]['rating'] = 4
        self.evaluation3.evaluation[2]['rating'] = 4
        notify(ObjectModifiedEvent(self.evaluation3))

        view = self.portal.restrictedTraverse('@@export-evaluationsheets')
        test_out = view()
        now = datetime.datetime.now()
        datetime_str = now.strftime('%d %B %Y')

        csv_ref = 'assessment1,' + datetime_str +',list1,John,1,1\r\n' +\
                  'assessment1,' + datetime_str +',list1,John,2,1\r\n' +\
                  'assessment1,' + datetime_str +',list1,John,3,1\r\n' +\
                  'assessment1,' + datetime_str +',list1,Jennie,1,3\r\n' +\
                  'assessment1,' + datetime_str +',list1,Jennie,2,3\r\n' +\
                  'assessment1,' + datetime_str +',list1,Jennie,3,3\r\n' +\
                  'assessment1,' + datetime_str +',list1,Nomsa,1,4\r\n' +\
                  'assessment1,' + datetime_str +',list1,Nomsa,2,4\r\n' +\
                  'assessment1,' + datetime_str +',list1,Nomsa,3,4\r\n'

        self.assertEqual(test_out,csv_ref)
        ct = self.request.response.getHeader("Content-Type")
        self.assertEqual(ct,"text/csv")

        start = str(int(time())-500)
        end = str(int(time()))

        # test with some date paramenters on the request
        self.request.set('start_date',start)
        self.request.set('end_date',end)
        view = self.portal.restrictedTraverse('@@export-evaluationsheets')
        test_out = view()
        self.assertEqual(test_out,csv_ref)
        ct = self.request.response.getHeader("Content-Type")
        self.assertEqual(ct,"text/csv")

