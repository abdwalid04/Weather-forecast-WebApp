from email import message
import json
import stat
from unicodedata import name
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from matplotlib.pyplot import vlines
from scipy.fftpack import idct
from sklearn.preprocessing import scale
from .models import *
from .forms import *
import pandas as pd
from json import dumps
from datetime import datetime, timedelta
from .apps import PredictionConfig
import pickle as pk
from django.templatetags.static import static
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import user_passes_test



def check_admin(user):
   return user.is_superuser


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')   
    date = max(list(pd.DataFrame(observation.objects.all().values('date'))['date']))
    obs = pd.DataFrame(observation.objects.filter(date__lte=date, date__gt=date-timedelta(days=30)).values())
    # min/max Temperature chart
    data_tmax = obs[(obs['ech']==18)]
    data_tmin = obs[(obs['ech']==6)]
    data_tmax = data_tmax[['nom','date','tx']]
    data_tmin = data_tmin[['nom','date','tn']]
    data_tminmax = pd.DataFrame(data_tmax.merge(data_tmin).groupby(['date'])['tx','tn'].mean())
    data_tminmax.reset_index(level=0,inplace=True)
    context['tminmax'] = data_tminmax.itertuples(index=False)
    # perc/temp chart
    data_t = obs[(obs['ech']<=24) & (obs['ech']>=0)][['nom','ech','date','t2m']]
    data_t = pd.DataFrame(data_t.groupby(['date'])['t2m'].mean())
    data_t.reset_index(level=0,inplace=True)
    context['data_t'] = data_t.itertuples(index=False)
    data_p = obs[(obs['ech']<=24) & (obs['ech']>=0)][['nom','ech','date','rr']]
    data_p = pd.DataFrame(data_p.groupby(['date'])['rr'].mean())
    data_p.reset_index(level=0,inplace=True)
    data_p['rr'] = data_p['rr']*100
    context['data_p'] = data_p.itertuples(index=False)
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")    
def model(request):
    context = {'segment': 'MLmodel'}
    html_template = loader.get_template('home/model.html')
    model = PredictionConfig.model
    context['parms'] = model['xgb'].get_xgb_params()
    metric = PredictionConfig.metrics
    context['metric'] = metric.to_dict('records')[0]
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def table(request):
    context = {'segment': 'table'}
    html_template = loader.get_template('home/table.html')
    date = max(list(pd.DataFrame(observation.objects.all().values('date'))['date']))
    obs = pd.DataFrame(observation.objects.filter(date=date).values())
    prev = pd.DataFrame(prevision.objects.filter(observation__in=list(obs['observation_id'].unique())).values())
    data = obs.merge(prev)
    neb =  pd.DataFrame(nebulosite.objects.all().values())
    table_data = data.merge(neb)
    table_data['date'] = pd.to_datetime(table_data['date'], format="%Y-%m-%d").dt.strftime('%Y-%m-%d')
    context['data'] = table_data.itertuples(index=False) 
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def tablevalide(request):
    context = {'segment': 'tablevalide'}
    html_template = loader.get_template('home/table.html')
    date = max(list(pd.DataFrame(observation.objects.all().values('date'))['date']))
    obs = pd.DataFrame(observation.objects.filter(date=date).values())
    prev = pd.DataFrame(prevision.objects.filter(observation__in=list(obs['observation_id'].unique())).values())
    data = obs.merge(prev)
    neb =  pd.DataFrame(nebulosite.objects.all().values())
    table_data = data.merge(neb)
    table_data['date'] = pd.to_datetime(table_data['date'], format="%Y-%m-%d").dt.strftime('%Y-%m-%d')
    context['data'] = table_data.itertuples(index=False)
    context['neb'] = neb.itertuples(index=False)

    if request.method == 'POST':
        for row in json.loads(request.POST.get('valide')):
            if validation.objects.filter(prevision_id=int(row['id'])).exists():
                validation.objects.filter(prevision_id=int(row['id'])).update(nebulosite_id=int(row['nebulosite_id']),valideur=request.user)
            else:
                validation.objects.create(prevision_id=int(row['id']),nebulosite_id=int(row['nebulosite_id']),valideur=request.user)
        return HttpResponse(json.dumps(request.POST.get('csrfmiddlewaretoken')))
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def Viewvalide(request):
    context = {'segment': 'validation'}
    html_template = loader.get_template('home/validation.html')
    date = max(list(pd.DataFrame(observation.objects.all().values('date'))['date']))
    obs = pd.DataFrame(observation.objects.filter(date=date).values())
    obs_ids = list(obs['observation_id'].unique())
    prev = pd.DataFrame(prevision.objects.filter(observation__in=obs_ids).values())
    prev_ids = list(prev['observation_id'].unique())
    val = pd.DataFrame(validation.objects.filter(valideur=request.user).filter(prevision__in=prev_ids).values())
    if(not val.empty):
        val.drop(columns=['valideur_id'], inplace=True)
        neb =  pd.DataFrame(nebulosite.objects.all().values())
        table_prev = prev.merge(neb)
        table_val = val.merge(neb)
        
        table_prev.rename(columns = {'nebulosite_id':'prev_neb_id','nebulosite':'prev_nebulosite'}, inplace = True)
        table_val.rename(columns = {'prevision_id':'observation_id','nebulosite_id':'val_neb_id','nebulosite':'val_nebulosite'}, inplace = True)
        
        table_data = obs.merge(table_prev,on='observation_id').merge(table_val,on='observation_id')

        table_data['date'] = pd.to_datetime(table_data['date'], format="%Y-%m-%d").dt.strftime('%Y-%m-%d')
        context['data'] = table_data.itertuples(index=False) 
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
@user_passes_test(check_admin)
def upload(request):
    context = {'segment': 'upload'}
    html_template = loader.get_template('home/upload.html')
    ########################################################################################
    # obs = observation.objects.filter(date='2020-09-10')
    # obs_id = pd.DataFrame(obs.values())['observation_id'].unique()
    # prevision.objects.filter(observation__in=obs_id).delete()
    # obs.delete()
    ########################################################################################

    if request.method == 'POST':
        if request.FILES.get("csv_file", False):
            data = pd.read_csv(request.FILES["csv_file"],sep=';').fillna(0)
            context['data'] = data.itertuples(index=False)
        elif request.POST.get("message",False):
            if request.POST.get("message") == 'save':
                df = pd.DataFrame(json.loads(request.POST.get('savedata')))
                df.rename(columns = {'ville':'nom'}, inplace = True)
                model = PredictionConfig.model
                label_encoder = PredictionConfig.LabelEncoder
                
                ptrt_data = df.copy()
                ptrt_data["date"] = pd.to_datetime(ptrt_data["date"], format = "%Y-%m-%d", errors = "coerce")
                ptrt_data.insert(loc=4, column="month", value=ptrt_data["date"].dt.month)
                ptrt_data.insert(loc=5, column="day", value=ptrt_data["date"].dt.day)
                ptrt_data.drop(columns=["date"],inplace=True)
                ptrt_data.rename(columns = {'id_ville':'id'}, inplace = True)
                ptrt_data = ptrt_data[['id', 'ech', 't2m', 'month', 'day','hu2m', 'hu10m', 'hu1000hpa', 'hu925hpa', 'hu850hpa', 'hu700hpa',
                        'hu500hpa', 'hu300hpa','u10ff', 'u10dd', 'u10ddd', 'u20ff', 'u20dd','u20ddd', 'u50ff', 'u50dd','u50ddd', 
                        'u100ff', 'u100dd','u100ddd','cape', 'psol', 'ch', 'cm', 'cl', 'rr', 'rr_gn', 'rr_cv', 'rr_sn','vcty']]
                for i in [10,20,50,100]:
                    ptrt_data["u"+str(i)+"ddd"] = label_encoder.transform(ptrt_data["u"+str(i)+"ddd"].str.strip())
                
                label_pred = model.predict(ptrt_data)
                df['nebulosite_id'] = label_pred
                
                observation.objects.bulk_create(
                    observation(**vals) for vals in df.drop(columns=['nebulosite_id']).to_dict('records')
                )
                obs = pd.DataFrame(observation.objects.filter(date=list(df['date'].unique())[0]).values())
                prevision.objects.bulk_create(
                    prevision(**{'observation_id':int(obs.loc[(obs['id_ville']==int(row['id_ville'])) & (obs['ech']==int(row['ech']))]['observation_id']), 'nebulosite_id':row['nebulosite_id']}) for row in df.to_dict('records')
                )
                
                return HttpResponse(json.dumps(request.POST.get('csrfmiddlewaretoken')))
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def map(request):
    context = {'segment': 'map'}
    html_template = loader.get_template('home/map.html')
    date = max(list(pd.DataFrame(observation.objects.all().values('date'))['date']))
    obs = pd.DataFrame(observation.objects.filter(date=date).values())
    prev = pd.DataFrame(prevision.objects.filter(observation__in=list(obs['observation_id'].unique())).values())
    data = obs.merge(prev)
    neb =  pd.DataFrame(nebulosite.objects.all().values())
    map_data = data.merge(neb)
    map_data = map_data[['nom','date','ech','lat','lon','t2m','u10ff','u10ddd','nebulosite_id','nebulosite']] 
    
    context['data'] = map_data.itertuples(index=False) 
    context['date'] = str(date)
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
