import datetime
import os
from pathlib import Path

import pandas as pd
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from AdClassificationPackage.Main import run

from .models import History


def index(request) -> render:
    history = History.objects.all()
    return render(request, 'home_page.html', {'history': history})


def recognition(request) -> HttpResponseRedirect:
    if request.method == 'POST':
        history = History()
        ad = request.POST.get('ad')
        path = str(Path(os.path.dirname(__file__)).joinpath('resources'))
        output = run(ad, path)
        history.datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
        history.input_string = ad
        history.output = output
        history.save()
        return HttpResponseRedirect("/")


def download_logs_exel(request) -> FileResponse:
    if request.method == 'GET':

        path = Path(os.path.dirname(__file__)).joinpath('logs')
        for file_path in path.rglob("*.xlsx"):
            try:
                os.remove(file_path)
            except Exception as e:
                pass
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M')
        name = f'log_report_{date}.xlsx'
        logs_df = pd.DataFrame(columns=['datatime', 'input', 'output'])

        history = History.objects.all()
        for records in history:
            logs_df.loc[len(logs_df.index)] = [records.datetime, records.input_string, records.output]

        logs_df.to_excel(f'{path}/{name}', sheet_name="Sheet1", index=False)
        response = FileResponse(open(f'{path}/{name}', "rb"))
        response['Content-Disposition'] = 'attachment; filename=' + name
        response['X-Sendfile'] = name

        return response
