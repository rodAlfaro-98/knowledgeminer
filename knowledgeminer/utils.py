from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict, fileName):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        # Force pdf download
        response = HttpResponse(result.getvalue(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="'+str(fileName)+'.pdf"'
            
        return response
        # view pdf in browser
#        return http.HttpResponse(result.getvalue(), mimetype='application/pdf', content_type='application/force-download')
        
    return HttpResponse('We had some errors')
