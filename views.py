from django.shortcuts import render_to_response
from pprint import pformat
from socket import gethostbyaddr, herror

def main(request):
    ctx = {'ip': request.META['REMOTE_ADDR']}
    try:
        ctx['hostname'] = gethostbyaddr(request.META['REMOTE_ADDR'])[0]
    except herror:
        pass
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ctx['local_ip'] = request.META['HTTP_X_FORWARDED_FOR']
    if 'HTTP_VIA' in request.META:
        ctx['proxy'] = request.META['HTTP_VIA']
    return render_to_response('ip_info/base.html', ctx)
