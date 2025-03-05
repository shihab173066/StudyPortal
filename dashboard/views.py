from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.views import generic
from .models import Notes
from youtubesearchpython import VideosSearch
import requests

# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user, title = request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request,f"Notes from {request.user.username} Added")
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)

def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = "dashboard/notes_detail.html"

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            homeworks = Homework(
                user = request.user, 
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request, f'Homework Added from {request.user.username}')
    else:
        form = HomeworkForm()

    
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    
    context = {
        'homeworks':homework, 
        'homework_done':homework_done, 
        'form':form,
    }
    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished == False
    else:
        homework.is_finished == True
    
    homework.save()
    return redirect('homework')

    
    
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form, 
                'results':result_list, 
            }
        return render(request, "dashboard/youtube.html", context)

    else:
        form = DashboardForm()

    context = {'form':form}
    return render(request, "dashboard/youtube.html", context)


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form, 
                'results':result_list, 
            }
        return render(request, "dashboard/books.html", context)

    else:
        form = DashboardForm()

    context = {'form':form}
    return render(request, "dashboard/books.html", context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        context = {'form': form, 'input': False}  # Default context

        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context.update({'m_form': measurement_form, 'input': True})

            if 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''

                if input_value and int(input_value) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {int(input_value) * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {int(input_value) / 3} yard'

                context.update({'answer': answer})

        elif request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context.update({'m_form': measurement_form, 'input': True})

            if 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''

                if input_value and int(input_value) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'

                context.update({'answer': answer})

        return render(request, "dashboard/conversion.html", context)  # Ensure return statement

    else:
        form = ConversionForm()
        context = {'form': form, 'input': False}
    
    return render(request, "dashboard/conversion.html", context)  # Always return a response
