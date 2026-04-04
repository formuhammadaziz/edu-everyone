import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from results.models import ExamResult


@login_required
def home(request):
    user = request.user
    recent_results = ExamResult.objects.filter(user=user).order_by('-created_at')[:5]

    # Best band score
    best = ExamResult.objects.filter(user=user).aggregate(best=Max('overall_band'))
    best_band = best['best']

    # Band score trend data
    all_results = ExamResult.objects.filter(user=user).order_by('created_at')
    chart_labels = []
    chart_overall = []
    chart_listening = []
    chart_reading = []
    for r in all_results:
        chart_labels.append(r.created_at.strftime('%b %d'))
        chart_overall.append(float(r.overall_band) if r.overall_band else 0)
        chart_listening.append(float(r.listening_score) if r.listening_score else 0)
        chart_reading.append(float(r.reading_score) if r.reading_score else 0)

    context = {
        'recent_results': recent_results,
        'best_band': best_band,
        'chart_labels': json.dumps(chart_labels),
        'chart_overall': json.dumps(chart_overall),
        'chart_listening': json.dumps(chart_listening),
        'chart_reading': json.dumps(chart_reading),
    }
    return render(request, 'dashboard/home.html', context)
