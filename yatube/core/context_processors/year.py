from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    annum = datetime.now().year
    return  {
       'year': annum
    }
