from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from .forms import ProfileForm


@login_required
def profile_view(request):
    from results.models import ExamResult

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    recent_results = ExamResult.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_exams = ExamResult.objects.filter(user=request.user).count()
    best = ExamResult.objects.filter(user=request.user).aggregate(best=Max('overall_band'))

    context = {
        'form': form,
        'recent_results': recent_results,
        'total_exams': total_exams,
        'best_band': best['best'],
    }
    return render(request, 'accounts/profile.html', context)
