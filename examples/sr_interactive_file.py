""" SemRep interactive using input file """
import argparse
import os
from skr_web_api import Submission, SEMREP_INTERACTIVE_URL

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test cas auth")
    parser.add_argument('-s', '--serviceurl',
                        default=SEMREP_INTERACTIVE_URL,
                        help='url of service')
    parser.add_argument('-e', '--email', help='Email address')
    parser.add_argument('-a', '--apikey', help='UTS api key')
    parser.add_argument('inputfile', help='inputfile')
    args = parser.parse_args()
    if args.email is None and 'EMAIL' in os.environ:
        args.email = os.environ['EMAIL']
    if args.apikey is None and 'UTS_API_KEY' in os.environ:
        args.apikey = os.environ['UTS_API_KEY']

    with open(args.inputfile) as chan:
        inputtext = chan.read()

    inst = Submission(args.email, args.apikey)
    if args.serviceurl:
        inst.set_serviceurl(args.serviceurl)
    inst.init_sr_interactive(inputtext, args='-D')
    response = inst.submit()
    print('response status: {}'.format(response.status_code))
    print('content: {}'.format(response.content.decode()))
