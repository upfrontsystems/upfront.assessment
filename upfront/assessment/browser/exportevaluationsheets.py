from csv import DictWriter
from cStringIO import StringIO
from DateTime import DateTime

from five import grok
from zope.component.hooks import getSite
from zope.interface import Interface
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from upfront.assessment.content.evaluation import UN_RATED, NOT_RATED
from upfront.assessment import MessageFactory as _

class ExportEvaluationSheetsView(grok.View):
    """ Export of all evaluation sheets completed between a given date range. 
        The export has following columns: 
        Assessment, Date of Assessment, Class, Learner, Activity Number, Rating
    """
    grok.context(Interface)
    grok.name('export-evaluationsheets')
    grok.require('cmf.ManagePortal')

    def evaluation_sheets_csv(self):
        """ Export of all evaluation sheets completed between a given date range
            The export has following columns: Assessment, Date of Assessment,
            Class, Learner, Activity Number, Rating
        """

        # get optional parameters off the request - in epoch format
        start_date = self.request.get('start_date', '')
        end_date = self.request.get('end_date', '')

        if start_date != '' and end_date != '':
            start = int(start_date)
            end = int(end_date)
        else:
            # if no dates given - display all evaluation sheets ever completed
            start = DateTime('2013-01-01 00:00:00')
            end = DateTime() # now

        date_range_query = { 'query':(start,end), 'range': 'min:max'}   
        evalsheets = getSite().portal_catalog(
                   portal_type = ['upfront.assessment.content.evaluationsheet'],
                   effective = date_range_query)

        csv_content = None
        evalsheet_csv = StringIO()

        if evalsheets is not None and len(evalsheets) > 0:
            writer = DictWriter(evalsheet_csv,
                                fieldnames=['assessment', 'assessment_date',
                                            'classlist','learner','learner_uid',
                                            'activity_number', 'rating',
                                            'school', 'province', 'uuid'],
                                restval='',
                                extrasaction='ignore',
                                dialect='excel'
                               )

            for brain in evalsheets:
                evalsheet = brain.getObject()
                contentFilter =\
                        {'portal_type': 'upfront.assessment.content.evaluation'}
                folder_contents = evalsheet.getFolderContents(contentFilter)
                for idx, evaluation in enumerate(folder_contents):
                    e_obj = evaluation.getObject()

                    # for each evaluation - go through all its activities
                    for activity in range(len(e_obj.evaluation)):
                        rating = e_obj.evaluation[activity]['rating']
                        if rating == NOT_RATED:
                            rating = _('Not Rated')
                        elif rating == UN_RATED:
                            rating = _('No Rating')

                        # get the user who created the data being exported
                        mt = getToolByName(self.context, 'portal_membership')
                        user = mt.getMemberById(evalsheet.Creator())

                        ldict={'assessment': evalsheet.assessment.to_object.id,
                               'assessment_date': evalsheet.assessment.\
                                    to_object.created().strftime('%d %B %Y'),
                               'classlist': evalsheet.classlist.to_object.id,
                               'learner': e_obj.learner.to_object.name,
                                # because two students of same name possible in 
                                # one class
                               'learner_uid': IUUID(e_obj.learner.to_object),
                               'activity_number': activity+1, # count from 1 on
                               'rating': rating, # a number or 'Not Rated'
                               'school': user.getProperty('school'),
                               'province': user.getProperty('province'),
                               'uuid': user.getProperty('uuid'),
                          }
                        writer.writerow(ldict)
            
            csv_content = evalsheet_csv.getvalue()
            evalsheet_csv.close()

        return csv_content

    def __call__(self):
        """ Return csv content as http response or return info IStatusMessage
        """

        csv_content = self.evaluation_sheets_csv()

        if csv_content is not None:
            now = DateTime()
            nice_filename = '%s_%s' % ('completed_evaluationsheets_',
                             now.strftime('%Y%m%d'))
            self.request.response.setHeader("Content-Disposition",
                                            "attachment; filename=%s.csv" % 
                                             nice_filename)
            self.request.response.setHeader("Content-Type", "text/csv")
            self.request.response.setHeader("Content-Length", len(csv_content))
            self.request.response.setHeader('Last-Modified',
                                            DateTime.rfc822(DateTime()))
            self.request.response.setHeader("Cache-Control", "no-store")
            self.request.response.setHeader("Pragma", "no-cache")
            self.request.response.write(csv_content)
        else:
            msg = _('No completed evaluationsheets exist')
            IStatusMessage(self.request).addStatusMessage(msg,"info")

        # redirect to show the info message
        self.request.response.redirect(
                '/'.join(self.context.getPhysicalPath()))

        return csv_content

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
