import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from exams.models import ExamAttempt, StudentResponse
from .models import ExamResult


@login_required
def result_detail(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    result = get_object_or_404(ExamResult, attempt=attempt)

    # Get all responses grouped by section
    responses = StudentResponse.objects.filter(attempt=attempt).select_related('question', 'question__section')

    sections_data = {}
    question_type_stats = {}
    for resp in responses:
        st = resp.question.section.section_type
        if st not in sections_data:
            sections_data[st] = []
        sections_data[st].append(resp)

        # Track question type performance
        qt = resp.question.get_question_type_display()
        if qt not in question_type_stats:
            question_type_stats[qt] = {'correct': 0, 'total': 0}
        question_type_stats[qt]['total'] += 1
        if resp.is_correct:
            question_type_stats[qt]['correct'] += 1

    # Find weakest question types
    weakest = []
    for qt, stats in question_type_stats.items():
        if stats['total'] > 0:
            pct = stats['correct'] / stats['total'] * 100
            weakest.append({'type': qt, 'correct': stats['correct'], 'total': stats['total'], 'percentage': round(pct)})
    weakest.sort(key=lambda x: x['percentage'])

    # Previous attempts for comparison
    previous_results = ExamResult.objects.filter(user=request.user).exclude(id=result.id).order_by('-created_at')[:5]

    # Band score history for chart
    all_results = ExamResult.objects.filter(user=request.user).order_by('created_at')
    chart_labels = []
    chart_data = []
    for r in all_results:
        chart_labels.append(r.created_at.strftime('%b %d'))
        chart_data.append(float(r.overall_band) if r.overall_band else 0)

    context = {
        'attempt': attempt,
        'result': result,
        'sections_data': sections_data,
        'weakest': weakest[:5],
        'previous_results': previous_results,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'results/detail.html', context)


@login_required
def result_list(request):
    results = ExamResult.objects.filter(user=request.user)
    return render(request, 'results/list.html', {'results': results})
