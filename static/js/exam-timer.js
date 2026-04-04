document.addEventListener('DOMContentLoaded', function() {
    const timerDisplay = document.getElementById('timer-display');
    const timerBadge = document.getElementById('exam-timer');
    const remainingEl = document.getElementById('remaining-seconds');
    const autoSaveIndicator = document.getElementById('auto-save-indicator');
    const submitForm = document.getElementById('exam-submit-form');
    const confirmSubmitBtn = document.getElementById('confirm-submit');

    if (!remainingEl) return;

    let remaining = parseInt(remainingEl.value);
    let warningShown = false;

    function formatTime(secs) {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    }

    function updateTimer() {
        if (remaining <= 0) {
            timerDisplay.textContent = '00:00';
            if (submitForm) submitForm.submit();
            return;
        }

        remaining--;
        timerDisplay.textContent = formatTime(remaining);

        // Warning at 5 minutes
        if (remaining <= 300 && remaining > 60) {
            timerBadge.classList.add('warning');
            timerBadge.classList.remove('danger');
            if (!warningShown) {
                warningShown = true;
                try {
                    const modal = new bootstrap.Modal(document.getElementById('timeWarningModal'));
                    modal.show();
                } catch(e) {}
            }
        }

        // Danger at 1 minute
        if (remaining <= 60) {
            timerBadge.classList.remove('warning');
            timerBadge.classList.add('danger');
        }
    }

    // Start timer
    timerDisplay.textContent = formatTime(remaining);
    setInterval(updateTimer, 1000);

    // Auto-save every 60 seconds
    function autoSave() {
        const answers = collectAnswers();
        const attemptId = document.getElementById('attempt-id')?.value;
        if (!attemptId || Object.keys(answers).length === 0) return;

        if (autoSaveIndicator) {
            autoSaveIndicator.className = 'save-indicator saving';
            autoSaveIndicator.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Saving...</span>';
        }

        fetch(`/exams/${attemptId}/auto-save/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({ answers: answers })
        })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'ok' && autoSaveIndicator) {
                autoSaveIndicator.className = 'save-indicator saved';
                autoSaveIndicator.innerHTML = '<i class="fas fa-check-circle"></i> <span>Saved</span>';
            }
        })
        .catch(() => {
            if (autoSaveIndicator) {
                autoSaveIndicator.className = 'save-indicator error';
                autoSaveIndicator.innerHTML = '<i class="fas fa-exclamation-circle"></i> <span>Failed</span>';
            }
        });
    }

    setInterval(autoSave, 60000);

    // Confirm submit button
    if (confirmSubmitBtn && submitForm) {
        confirmSubmitBtn.addEventListener('click', function() {
            const answers = collectAnswers();
            for (const [qId, answer] of Object.entries(answers)) {
                let input = submitForm.querySelector(`input[name="question_${qId}"]`);
                if (!input) {
                    input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = `question_${qId}`;
                    submitForm.appendChild(input);
                }
                input.value = answer;
            }
            submitForm.submit();
        });
    }

    // Question nav dot updates
    document.querySelectorAll('.question-card input, .question-card textarea').forEach(el => {
        el.addEventListener('change', handleAnswerChange);
        el.addEventListener('input', handleAnswerChange);
    });

    function handleAnswerChange() {
        const card = this.closest('.question-card');
        if (!card) return;
        const qId = card.dataset.questionId;
        const dot = document.querySelector(`.q-dot[data-q="${qId}"]`);

        let answered = false;
        if (this.type === 'radio') {
            answered = card.querySelector('input[type="radio"]:checked') !== null;
        } else {
            answered = this.value.trim() !== '';
        }

        if (dot) dot.classList.toggle('answered', answered);
        card.classList.toggle('answered', answered);
    }
});

function collectAnswers() {
    const answers = {};
    document.querySelectorAll('[data-question-id]').forEach(el => {
        const qId = el.dataset.questionId;
        if (el.type === 'radio') {
            if (el.checked) answers[qId] = el.value;
        } else if (el.value && el.value.trim()) {
            answers[qId] = el.value;
        }
    });
    return answers;
}

function getCsrfToken() {
    const meta = document.querySelector('[name=csrfmiddlewaretoken]');
    if (meta) return meta.value;
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}
