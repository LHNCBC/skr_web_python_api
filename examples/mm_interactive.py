""" MetaMap interactive using embedded string """
import argparse
from skr_web_api import Submission, METAMAP_INTERACTIVE_URL

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test cas auth")
    parser.add_argument('-s', '--serviceurl',
                        default=METAMAP_INTERACTIVE_URL,
                        help='url of service')
    parser.add_argument('-e', '--email', help='Email address')
    parser.add_argument('-a', '--apikey', help='UTS api key')
    args = parser.parse_args()
    inputtext = "A spinal tap was performed and oligoclonal bands were \
detected in the cerebrospinal fluid.\n"
    inst = Submission(args.email, args.apikey)
    if args.serviceurl:
        inst.set_serviceurl(args.serviceurl)
    inst.init_mm_interactive(inputtext, args='-N')
    response = inst.submit()
    print('response status: {}'.format(response.status_code))
    print('content: {}'.format(response.content.decode()))
