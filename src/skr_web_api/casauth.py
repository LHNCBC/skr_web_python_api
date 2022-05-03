import argparse
import requests
from requests_html import HTML


def get_service_ticket(serverurl, ticket_granting_ticket, serviceurl):
    """ Obtain a Single-Use Proxy Ticket (also known as service ticket).
    Request for a Service Ticket:

        POST /cas/v1/tickets/{TGT id} HTTP/1.0

    data:
           service={form encoded parameter for the service url}

    Sucessful Response:

        200 OK

        ST-1-FFDFHDSJKHSDFJKSDHFJKRUEYREWUIFSD2132

    @param serverurl authentication server
    @param ticketGrantingTicket a Proxy Granting Ticket.
    @param serviceurl url of service with protected resources
    @return authentication ticket for service. """
    resp = requests.post("{}/{}".format(serverurl, ticket_granting_ticket),
                         {"service": serviceurl})
    if resp.status_code == 200:
        return resp.content
    return 'Error: status: {}'.format(resp.content)


def extract_tgt_ticket(htmlcontent):
    "Extract ticket granting ticket from HTML."
    # print('htmlcontent: {}'.format(htmlcontent))
    html = HTML(html=htmlcontent)
    # get form element
    elements = html.xpath("//form")
    # print('html response: {}'.format(etree.tostring(html.lxml).decode()))
    # print('action attribure: {}'.format(elements[0].attrs['action']))
    # extract ticket granting ticket out of 'action' attribute
    if elements != []:
        return elements[0].attrs['action'].split('/')[-1]
    else:
        return "form element missing from ticket granting ticket response"


def get_ticket_granting_ticket(tgtserverurl, apikey):
    """ Obtain a Proxy Granting Ticket.
    Response for a Ticket Granting Ticket Resource

      POST /cas/v1/api-key HTTP/1.0

     data:
        apikey

    Successful Response:
        201 Created

        Location: http://serviceurl/cas/v1/tickets/{TGT id}

    Parameters:
      serverurl: authentication server
      apikey: UTS profile API key

    Returns:
      a Proxy Granting Ticket.
    """
    response = requests.post(tgtserverurl, {'apikey': apikey},
                             headers={'Accept': 'test/plain'})
    return extract_tgt_ticket(response.content)


def get_ticket(cas_serverurl, apikey, serviceurl):
    """Obtain a Single-Use Proxy Ticket from Central Authentication
       Server (CAS).

      Parameters:
       stserverurl: service ticket server
       tgtserverurl: ticket granting ticket server
       apikey: UTS profile API key
       serviceurl: url of service with protected resources

      Returns:
          authentication ticket for service.

    """
    if cas_serverurl is None:
        print("cas server url must not be None")
    if apikey is None:
        print("api key must not be null")
    if serviceurl is None:
        print("service must not be null")
    # set ticket granting ticket server url
    tgtserverurl = cas_serverurl + "/api-key"
    # set service ticket server url
    stserverurl = cas_serverurl + "/tickets"
    tgt = get_ticket_granting_ticket(tgtserverurl, apikey)
    return get_service_ticket(stserverurl, tgt, serviceurl)


def get_protected_document(service_url, serviceticket):
    """ get document protected by CAS Authentication. """
    url = '%s?ticket=%s' % (service_url, serviceticket)
    params = {'ticket': serviceticket}
    s = requests.Session()
    response = s.get(url, params=params)
    # handle the redirect manually
    if response.status_code == 302:
        newurl = s.get_redirect_target(response)
        response = s.get(newurl, params=params, allow_redirects=False)
    return response


def get_document(cas_baseurl, apikey, service_url):
    """ get document protected by CAS Authentication. """
    serviceticket = get_ticket(cas_baseurl, apikey, service_url)
    return get_protected_document(service_url, serviceticket)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test cas auth")
    parser.add_argument('-s', '--serviceurl',
                        help='url of service')
    parser.add_argument('apikey', help='UTS api key')
    args = parser.parse_args()
    stserverurl = "https://utslogin.nlm.nih.gov/cas/v1/tickets"
    tgtserverurl = "https://utslogin.nlm.nih.gov/cas/v1/api-key"
    ticket = get_ticket(stserverurl, tgtserverurl,
                        args.apikey, args.serviceurl)
