from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CollectionForm, PictureForm, UserForm
from .models import Collection, Picture

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_collection(request):
    if not request.user.is_authenticated():
        return render(request, 'gallery/login.html')
    else:
        form = CollectionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.collection_logo = request.FILES['collection_logo']
            file_type = collection.collection_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'collection': collection,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'gallery/create_collection.html', context)
            collection.save()
            return render(request, 'gallery/detail.html', {'collection': collection})
        context = {
            "form": form,
        }
        return render(request, 'gallery/create_collection.html', context)


def create_picture(request, collection_id):
    form = PictureForm(request.POST or None, request.FILES or None)
    collection = get_object_or_404(Collection, pk=collection_id)
    if form.is_valid():
        collections_pictures = collection.picture_set.all()
        for s in collections_pictures:
            if s.picture_title == form.cleaned_data.get("picture_title"):
                context = {
                    'collection': collection,
                    'form': form,
                    'error_message': 'You already added that picture',
                }
                return render(request, 'gallery/create_picture.html', context)
        picture = form.save(commit=False)
        picture.collection = collection
        picture.picture_file = request.FILES['picture_file']
        file_type = picture.picture_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'collection': collection,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'gallery/create_picture.html', context)

        picture.save()
        return render(request, 'gallery/detail.html', {'collection': collection})
    context = {
        'collection': collection,
        'form': form,
    }
    return render(request, 'gallery/create_picture.html', context)


def delete_collection(request, collection_id):
    collection = Collection.objects.get(pk=collection_id)
    collection.delete()
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'gallery/index.html', {'collections': collections})


def delete_picture(request, collection_id, picture_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    picture = Picture.objects.get(pk=picture_id)
    picture.delete()
    return render(request, 'gallery/detail.html', {'collection': collection})


def detail(request, collection_id):
    if not request.user.is_authenticated():
        return render(request, 'gallery/login.html')
    else:
        user = request.user
        collection = get_object_or_404(Collection, pk=collection_id)
        return render(request, 'gallery/detail.html', {'college': collection, 'user': user})


def favorite(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    try:
        if picture.is_favorite:
            picture.is_favorite = False
        else:
            picture.is_favorite = True
        picture.save()
    except (KeyError, Picture.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    try:
        if collection.is_favorite:
            collection.is_favorite = False
        else:
            collection.is_favorite = True
        collection.save()
    except (KeyError, Collection.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'gallery/login.html')
    else:
        collections = Collection.objects.filter(user=request.user)
        picture_results = Picture.objects.all()
        query = request.GET.get("q")
        if query:
            collections = collections.filter(
                Q(collection_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            picture_results = picture_results.filter(
                Q(picture_title__icontains=query)
            ).distinct()
            return render(request, 'gallery/index.html', {
                'collections': collections,
                'pictures': picture_results,
            })
        else:
            return render(request, 'gallery/index.html', {'collections': collections})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'gallery/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                collections = Collection.objects.filter(user=request.user)
                return render(request, 'gallery/index.html', {'collections': collections})
            else:
                return render(request, 'gallery/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'gallery/login.html', {'error_message': 'Invalid login'})
    return render(request, 'gallery/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                collections = Collection.objects.filter(user=request.user)
                return render(request, 'gallery/index.html', {'collections': collections})
    context = {
        "form": form,
    }
    return render(request, 'gallery/register.html', context)


def pictures(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'gallery/login.html')
    else:
        try:
            picture_ids = []
            for collection in Collection.objects.filter(user=request.user):
                for picture in collection.picture_set.all():
                    picture_ids.append(picture.pk)
            users_pictures = Picture.objects.filter(pk__in=picture_ids)
            if filter_by == 'favorites':
                users_pictures = users_pictures.filter(is_favorite=True)
        except Collection.DoesNotExist:
            users_pictures = []
        return render(request, 'gallery/pictures.html', {
            'picture_list': users_pictures,
            'filter_by': filter_by,
        })
