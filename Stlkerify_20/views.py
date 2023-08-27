from django.shortcuts import render
from . import spotipy_model


def index(request):
    return render(request, 'index.html')


def post_from_index(request):
    if request.method == 'POST':
        option = request.POST.get('option')
        if option == 'name-artist':
            return search_by_name(request)
        elif option == 'track-url':
            search_result = search_by_track_url(request)
            if search_result is None:
                return render(request, '404.html')
            return render_result_site(request, search_result)
        else:
            return render(request, '404.html', {'text': 'undefined error'})
    else:
        return render(request, 'index.html')


def found(request, text):
    return render(request, 'found.html', {'text': text})


def search_by_track_url(request):
    user_input = request.POST.get('user-p-link')
    user_id = spotipy_model.parse_user_url(user_input)
    if user_id is None:
        return None
    track_id = spotipy_model.parse_track_url(request.POST.get('song-url'))
    if track_id is None:
        return None
    result = spotipy_model.search_by_track_id(user_id, track_id)
    if result is None:
        return None
    return result


def search_by_name(request):
    user_input = request.POST.get('user-p-link')
    user_id = spotipy_model.parse_user_url(user_input)
    if user_id is None:
        return render(request, '404.html')
    artist_name = request.POST.get('song-artist')
    track_name = request.POST.get('song-name')
    search_results = spotipy_model.search_tracks_by_name_artist(track_name, artist_name)
    if search_results:
        return render(request, 'choose_track.html', {'results': search_results, 'user_id': user_id})
    else:
        return render(request, 'index.html', {'text': 'Sorry but I cant find this track, Please try again...'})


def render_result_site(request, results):
    user_id = results[4]
    user_name = spotipy_model.get_user_name(user_id)
    if user_name is None:
        return render(request, '404.html')
    if results[0]:
        return render(request, 'found.html', {
            'playlist_name': results[1],
            'track_name': results[2],
            'artist_name': results[3],
            'user_name': user_name,
        })
    else:
        return render(request, 'not_found.html', {
            'track_name': results[2],
            'artist_name': results[3],
            'user_name': user_name,
        })


def render_choose_result_site(request):
    user_id = request.POST.get('user-p-link')
    track_id = request.POST.get('track-id')
    if track_id:
        search_result = spotipy_model.search_by_track_id(user_id, track_id)
        if search_result is None:
            return render(request, '404.html')
        return render_result_site(request, search_result)
    else:
        return render(request, '404.html', {'text': 'undefined error'})
