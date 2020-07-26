from django.shortcuts import render
from .models import Notice, Attachment

# Create your views here.
def allNotices(request):
    template = 'notices/all_notices.html'
    context = {
        'title'     : 'Notices',
        'notices'   : Notice.objects.all(),
        'page_name' : 'notice',
        }
    return render(request, template, context)

def view_notice(request, notice_id):
    template = 'notices/view_notice.html'
    notice = Notice.objects.get(id=notice_id)
    context = {
        'title'         : 'Notice',
        'notice'        : notice,
        'attachments'   : Attachment.objects.filter(notice=notice),
        'page_name'     : 'notice',
        }
    return render(request, template, context)