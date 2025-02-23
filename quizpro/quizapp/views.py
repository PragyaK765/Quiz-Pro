from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, UserQuizAttempt, Answer
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                selected_answer_id = form.cleaned_data[f'question_{question.id}']
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1

            UserQuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)
            return redirect('quiz_result', quiz_id=quiz.id)
    else:
        form = QuizForm(questions=questions)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})

    
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).last()
    return render(request, 'quiz_result.html', {'quiz': quiz, 'attempt': attempt})
