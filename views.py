from django.shortcuts import render_to_response
from pprint import pformat
from socket import gethostbyaddr, herror
from whelk import shell
from publicsuffix import PublicSuffixList
from django.conf import settings
if hasattr(settings, 'GEOIP_DATA'):
    import GeoIP
else:
    GeoIP is None

psl = PublicSuffixList()

def main(request):
    ctx = {'ip': request.META['REMOTE_ADDR']}
    try:
        ctx['hostname'] = gethostbyaddr(request.META['REMOTE_ADDR'])[0]
    except herror:
        pass
    if GeoIP:
        gi = GeoIP.open(settings.GEOIP_DATA, GeoIP.GEOIP_STANDARD)
        geo = gi.record_by_addr(request.META['REMOTE_ADDR']) or {'country_name': 'Unknown'}
        for k in geo:
            if isinstance(geo[k], str):
                geo[k] = geo[k].decode('iso-8859-1', 'replace')
        ctx['geo'] = geo
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ctx['local_ip'] = request.META['HTTP_X_FORWARDED_FOR']
    if 'HTTP_VIA' in request.META:
        ctx['proxies'] = request.META['HTTP_VIA'].split(',')
    return render_to_response('ip_info/base.html', ctx)
 
def whois_ip(request):
    ctx = {'what': request.META['REMOTE_ADDR']}
    ctx['data'] = shell.whois(request.META['REMOTE_ADDR']).stdout
    return render_to_response('ip_info/whois.html', ctx)

def whois_host(request):
    ip = request.META['REMOTE_ADDR']
    try:
        ctx = {'what': psl.get_public_suffix(gethostbyaddr(request.META['REMOTE_ADDR'])[0])}
    except herror:
        ctx = {'what': '(hostname unavailable)', 'data': "Hostname not found"}
    else:
        ctx['data'] = shell.whois(ctx['what']).stdout
    return render_to_response('ip_info/whois.html', ctx)
