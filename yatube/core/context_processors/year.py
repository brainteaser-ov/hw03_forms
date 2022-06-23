from datetime import datetime


def year(request):
    annum = datetime.now().year
    return{'year': annum}
