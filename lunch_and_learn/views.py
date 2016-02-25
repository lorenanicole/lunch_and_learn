from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from twitter import get_home_timeline, analyze_sources, post_tweet
from django.http import JsonResponse
import json

__author__ = 'lorenamesa'

@require_http_methods(["GET"])
def timeline(request):

    count = request.GET.get('count')

    # Get home timeline
    if not count:
        timeline = get_home_timeline()  # Default grabs 10 tweets
    else:
        timeline = get_home_timeline(count=count)

    try:
        sources = json.loads(request.GET.get('sources'))
    except TypeError as e:
        return JsonResponse({'errors': 'missing parameter sources'}, status=400)

    # Keep only what want to return :-)
    trimmed_timeline = map(lambda t: {'created_at': t.get('created_at'),
                                      'screen_name': t.get('user').get('screen_name'),
                                      'id': t.get('id'),
                                      'url': 'https://twitter.com/{0}/status/{1}'.format(t.get('user').get('id'), t.get('id')),
                                      'text': t.get('text')}, timeline)

    # Find sources from home timeline
    if sources:
        tweet_sources = analyze_sources(timeline)

        # Return it as JSON
        return JsonResponse({'tweets': trimmed_timeline, 'sources': tweet_sources}, status=200)

    return JsonResponse({'tweets': trimmed_timeline}, status=200)

@require_http_methods(["POST"])
@csrf_exempt
def post_status(request):

    # Get the text for the tweet status
    text = request.POST.get('text') #request.POST.get('text')

    # Whoops, we didn't provide it! Let's tell the user.
    if not text:
        return JsonResponse({'errors': 'no text provided'}, status=400)

    # Do the posting thing :-)
    tweet = post_tweet(text)

    # Did it work? =(>.<)=
    if tweet.get('errors'):
        return JsonResponse({'errors': 'Couldn\'t post to Twitter: {0}'.format(tweet.get('errors')[0].get('message'))},
                            status=400)
    else:
        return JsonResponse({'url': 'https://twitter.com/{0}/status/{1}'.format(tweet.get('user').get('id'), tweet.get('id')),
                             'created_at': tweet.get('created_at'),
                             'screen_name': tweet.get('user').get('screen_name')},
                            status=200)



