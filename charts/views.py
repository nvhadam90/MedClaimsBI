from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count, F, Sum, Avg
from .models import Editors
from .models import Claims

# Create your views here.
class EditorChartView(TemplateView):
    template_name = 'editors/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Editors.objects.all()
        return context

def dashboard_view(request):
    # Claim Summary Table
    totalclaims = Claims.objects.all().count()
    totalbilled = Claims.objects.all().aggregate(Sum('billed_amount')).get('billed_amount__sum')
    totaldiscount = Claims.objects.all().aggregate(Sum('savings_amount')).get('savings_amount__sum')
    commondx = Claims.objects.values('primary_dx').annotate(mc=Count('primary_dx')).order_by('-mc')[0].get('primary_dx')
    commonprovider = Claims.objects.values('billing_provider_name').annotate(mc=Count('billing_provider_name')).order_by('-mc')[0].get('billing_provider_name')
    
    return render(request, 'dashboard/dashboard.html', {
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