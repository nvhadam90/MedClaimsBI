from itertools import count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from .models import Editors, Providers
from .models import Claims

# Create your views here.
class EditorChartView(TemplateView):
    template_name = 'editors/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Editors.objects.all()
        return context

def home_view(request):
    return render(request, 'home.html', {
        'header': 'Home Page'
    })

def dashboard_view(request):
    # Claim Summary Table
    totalclaims = Claims.objects.all().count()
    totalbilled = Claims.objects.all().aggregate(Sum('billed_amount')).get('billed_amount__sum')
    totaldiscount = Claims.objects.all().aggregate(Sum('savings_amount')).get('savings_amount__sum')
    commondx = Claims.objects.values('primary_dx').annotate(mc=Count('primary_dx')).order_by('-mc')[0].get('primary_dx')
    commonprovider = Claims.objects.values('billing_provider_name').annotate(mc=Count('billing_provider_name')).order_by('-mc')[0].get('billing_provider_name')
    
    return render(request, 'dashboard/dashboard.html', {
        'header': "My Dashboard",
        'totalclaims': totalclaims,
        'totalbilled': totalbilled,
        'totaldiscount': totaldiscount,
        'commondx': commondx,
        'commonprovider': commonprovider,
    })


def get_claimtype_chart(request):
    total_inst = Claims.objects.filter(claim_type="Institutional").count()
    total_prof = Claims.objects.filter(claim_type="Professional").count()
    bardatamax = max(total_inst, total_prof)
    bardata = [total_inst, total_prof]
    labels = ['Institutional', 'Professional']
    return JsonResponse(data={
        'labels': labels,
        'data': bardata,
        'datamax': bardatamax
    })

def get_totalbilled_chart(request):
    total_billed_inst = Claims.objects.filter(claim_type="Institutional").aggregate(Sum('billed_amount'))
    total_billed_prof = Claims.objects.filter(claim_type="Professional").aggregate(Sum('billed_amount'))
    inst_sum = total_billed_inst.get('billed_amount__sum') 
    prof_sum = total_billed_prof.get('billed_amount__sum')
    bardatamax = max(inst_sum, prof_sum)
    bardata = [inst_sum, prof_sum]
    labels = ['Institutional', 'Professional']
    return JsonResponse(data={
        'labels': labels,
        'data': bardata,
        'datamax': bardatamax
    })

def get_provider_data(request, providerID):
    if providerID < 0:
        providerID = 1
    else:
        providerID = int(providerID)
    all_providers = Providers.objects.all()
    provider_selected = Providers.objects.filter(provider_id = providerID).values('provider_name')
    print(provider_selected)
    return render(request, 'provider/providerdetails.html', {'allproviders': all_providers,
    'header': "Provider Data",
    'providerID': providerID,
    'provider_selected': provider_selected[0]['provider_name'] })

def get_provider_chart(request, providerID):
    
    total_inst = Claims.objects.filter(billing_provider_ID = providerID, claim_type="Institutional").count()
    total_prof = Claims.objects.filter(billing_provider_ID = providerID, claim_type="Professional").count()
    piedata = [total_inst, total_prof]
    labels = ['Institutional', 'Professional']
    return JsonResponse(data={
        'labels': labels,
        'data': piedata
        
    })

def get_provider_bar(request, providerID):
    
    total_billed = Claims.objects.filter(billing_provider_ID = providerID).aggregate(Sum('billed_amount'))
    total_allowed = Claims.objects.filter(billing_provider_ID = providerID).aggregate(Sum('allowed_amount'))
    avg_billed = Claims.objects.filter(billing_provider_ID = providerID).aggregate(Avg('billed_amount'))
    avg_discount = Claims.objects.filter(billing_provider_ID = providerID).aggregate(Avg('savings_amount'))
    billed_sum = total_billed.get('billed_amount__sum') 
    allowed_sum = total_allowed.get('allowed_amount__sum')
    billed_per_claim = avg_billed.get('billed_amount__avg')
    discount_per_claim = avg_discount.get('savings_amount__avg')
    bardata = [billed_sum, allowed_sum]
    avgbardata = [billed_per_claim, discount_per_claim]
    labels = ['Billed Amount', 'Allowed Amount']
    avglabels = ['Average Billed Amount', 'Avg Discount Per Claim']
    bardatamax = max(billed_sum, allowed_sum)
    avgbardatamax = max(billed_per_claim, discount_per_claim)
    return JsonResponse(data={
        'labels': labels,
        'data': bardata,
        'bardatamax': bardatamax,
        'avglabels': avglabels,
        'avgdata': avgbardata,
        'avgbardatamax': avgbardatamax
    })

def get_claim_volume(request):
    claims_years = Claims.objects.order_by().values('received_date__year').distinct()
    
    years_dict = []
    for year in claims_years:
        years_dict.append(year['received_date__year'])

    
    return render(request, 'claimvolume/claimvolume.html', {
    'header': "Claim Volume",
    'yearslisted': years_dict
    })

def get_claim_volume_data(request, year):
    
    print(year)

    months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
        ]
    
    year_dict = dict()
    for month in months:
        year_dict[month] = 0
    
    claims_for_year = Claims.objects.filter(received_date__year=year)

    grouped_claims_billed = claims_for_year.annotate(claimamount=F('billed_amount')).annotate(month=ExtractMonth('received_date'))\
        .values('month').annotate(sum=Sum('billed_amount')).values('month', 'sum').order_by('month')

    claim_dict = year_dict

    for group in grouped_claims_billed:
        claim_dict[months[group['month']-1]] = round(group['sum'], 2)

    labels = list(claim_dict.keys())

    linedata = list(claim_dict.values())

    grouped_claims_number = claims_for_year.annotate(month=ExtractMonth('received_date'))\
        .values('month').annotate(count=Count('id')).values('month', 'count').order_by('month')

    claim_count_dict = year_dict

    for group in grouped_claims_number:
        claim_count_dict[months[group['month']-1]] = round(group['count'], 2)

    countlabels = list(claim_dict.keys())

    countlinedata = list(claim_dict.values())

    return JsonResponse(data={
        'labels': labels,
        'data': linedata,
        'countlabels':countlabels,
        'countdata': countlinedata
        
    })