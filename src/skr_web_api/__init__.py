import os.path
import requests
from skr_web_api.casauth import get_ticket

CAS_SERVERURL = "https://utslogin.nlm.nih.gov/cas/v1"
II_SKR_SERVERURL = 'https://ii.nlm.nih.gov/cgi-bin/II/UTS_Required'
BATCH_VALIDATION_URL = II_SKR_SERVERURL + '/API_batchValidationII.pl'
SEMREP_INTERACTIVE_URL = II_SKR_SERVERURL + "/API_SR_interactive.pl"
METAMAP_INTERACTIVE_URL = II_SKR_SERVERURL + "/API_MM_interactive.pl"
MTI_INTERACTIVE_URL = II_SKR_SERVERURL + "/API_MTI_interactive.pl"


class Submission:
    def __init__(self, email=None, apikey=None):
        self.form = {}
        self.form['COMMAND_ARGS'] = ""
        self.form['Email_Address'] = email
        self.apikey = apikey
        self.files = {}
        self.casserverurl = CAS_SERVERURL
        # ticket granting ticket server
        self.tgtserverurl = CAS_SERVERURL + "/api-key"
        # service ticket server
        self.stserverurl = CAS_SERVERURL + "/tickets"

    def set_casserverurl(self, cas_serverurl):
        """ set CAS server url"""
        self.casserverurl = cas_serverurl

    def set_stserverurl(self, cas_serverurl):
        """ set service ticket server url"""
        self.stserverurl = cas_serverurl

    def set_tgtserverurl(self, tgt_serverurl):
        """ set ticket granting ticket server url"""
        self.tgtserverurl = tgt_serverurl

    def set_serviceurl(self, serviceurl):
        """ set target service url """
        self.serviceurl = serviceurl

    def init_generic_batch(self,  command, command_args):
        self.serviceurl = BATCH_VALIDATION_URL
        self.form["Batch_Command"] = '{} {}'.format(command, command_args)
        self.form['COMMAND_ARGS'] = command_args
        self.form['RUN_PROG'] = 'GENERIC_V'
        self.form['SKR_API'] = 'true'

    def init_sr_interactive(self, inputtext, args='-D'):
        self.serviceurl = SEMREP_INTERACTIVE_URL
        self.form['APIText'] = inputtext
        self.form['COMMAND_ARGS'] = args

    def init_mm_interactive(self, inputtext, args='-N', ksource='2020AB'):
        self.serviceurl = METAMAP_INTERACTIVE_URL
        self.form['APIText'] = inputtext
        self.form['COMMAND_ARGS'] = args
        self.form['KSOURCE'] = ksource

    def init_mti_interactive(self, inputtext, args='-opt1L_DCMS'):
        self.serviceurl = MTI_INTERACTIVE_URL
        self.form['APIText'] = inputtext
        self.form['COMMAND_ARGS'] = args

    def set_mm_ksource(self, ksrelease):
        """ set UMLS Knowledge source release (e.g.: 2020AB, etc.) """
        self.form['KSOURCE'] = ksrelease

    def set_command_args(self, args):
        """set arguments for command """
        self.form["Batch_Command"] = '{} {}'.format(
            self.form["Batch_Command"], args)
        self.form['COMMAND_ARGS'] = args

    def set_batch_file(self, inputfilename, inputtext=None):
        """ set input file """
        if inputtext is None:
            with open(inputfilename) as chan:
                inputtext = chan.read()
            inputfilename = os.path.basename(inputfilename)
        self.files['UpLoad_File'] = (inputfilename, inputtext,
                                     'text/plain', {'Expires': '0'})

    def set_email(self, email):
        self.form['Email_Address'] = email

    def set_apikey(self, apikey):
        self.apikey = apikey

    def submit(self):
        serviceticket = get_ticket(self.casserverurl, self.apikey,
                                   self.serviceurl)
        params = {'ticket': serviceticket}
        headers = {'Accept': 'application/json'}
        s = requests.Session()
        response = s.post(self.serviceurl,
                          self.form, files=self.files,
                          headers=headers, params=params,
                          allow_redirects=False)
        # handle the redirect manually
        if response.status_code == 302:
            newurl = s.get_redirect_target(response)
            response = s.post(newurl,
                              self.form, files=self.files,
                              headers=headers, params=params,
                              allow_redirects=False)
        return response
