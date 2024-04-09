import json

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from scores.models import Scores


@csrf_exempt
@login_required
def record_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('userId')
            score_value = data.get('score')

            if user_id is None or score_value is None:
                return JsonResponse({'error': 'User ID and score are required'}, status=400)

            # Assuming you have a user authentication system and the user is authenticated
            user = request.user

            # Save the score to the database
            score = Scores.objects.create(user=user, score=score_value)
            score.save()

            return JsonResponse({'message': 'Score recorded successfully'}, status=201)
        except Exception as e:
            print('Error recording score:', e)
            return JsonResponse({'error': 'Failed to record score'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def leaderboard(request):
    # Query the highest score for each user
    top_scores = Scores.objects.values('user__username').annotate(max_score=Max('score')).order_by('-max_score')[:10]
    return render(request, 'leaderboard.html', {'top_scores': top_scores})