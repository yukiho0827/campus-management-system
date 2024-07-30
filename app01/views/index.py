from app01.module_manage import *


def welcome(request):
    if request.method == 'GET':
        return render(request, 'welcome.html')
