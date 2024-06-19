from functools import reduce
from django.db.models import F, Q
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views import generic
# from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm, mEntryModelForm, mEntryNewModelForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, mCollection, mEntry
from django.contrib.auth.models import Group
from datetime import datetime
import operator
# from .models import Choice, Question


# class IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
#             :5
#         ]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "polls/detail.html"
#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now())


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "polls/results.html"


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'polls/signup.html'

def custom_signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(form.save())
            return redirect('login')
        else: 
            messages.warning(request, 'Error: Your passwords do not follow the rules or do not match.')
    return render(request, 'polls/signup.html')

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            if not CustomUser.objects.filter(username=username).exists():
                messages.warning(request, 'Username does not exist.')
            else:
                messages.warning(request, 'Password is incorrect.')
    return render(request, 'polls/login.html')

def index_view(request):
    return render(request, 'polls/index.html')

@login_required
def dashboard_view(request, collection=None):
    if request.method == 'POST':
        name = request.POST.get("cName", None)
        print(name)
        if name is None:
            messages.warning(request, "error")
            return redirect('dashboard')
        query = mCollection.objects.filter(cName = name)
        if query.exists():
            messages.warning(request, "Collection Already Exists")
            return redirect('dashboard')
        collection = mCollection(cName=name, created_by=request.user, cDate=datetime.now())
        collection.save()
        return redirect("mcollections:dashboard_specific", collection=name)

    # Get the list of tasks from the database
    if request.user.is_superuser:
        collections = mCollection.objects.all()
    else:
        collections = mCollection.objects.filter(created_by = request.user)

    #selectedCollectionName = request.GET.get('selection', None)
    selectedCollectionName = collection
    if selectedCollectionName is None and collections.exists():
        selectedCollectionName = collections.first().cName

    searchQuery = request.GET.get("search", None)
    selectedCollectionEntries = None
    if selectedCollectionName is not None:
        query = mCollection.objects.filter(cName = selectedCollectionName)
        if query.exists():
            selectedCollection = query.first()
            criteria = [Q(eCollection__exact = selectedCollection)]
            if searchQuery is not None:
                criteria.append(Q(eName__icontains = searchQuery)) 

            selectedCollectionEntries = mEntry.objects.filter(reduce(operator.and_, criteria))
    response = render(request, 'polls/dashboard.html', {'collections': collections, 'collection': selectedCollectionName, 
                                                        'selectedCollectionEntries': selectedCollectionEntries, 'searchQuery': searchQuery})
    return response

@login_required
def newEntryView(request, collection):
    if request.method == 'POST':
        form = mEntryNewModelForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            entry = form.save()
            messages.success(request, "Created Entry")
            return redirect("mcollections:dashboard_specific", collection=entry.eCollection.cName)
        else:
            print(form.errors.as_text())
        
        return redirect("dashboard")

    form = mEntryNewModelForm(user=request.user, collection=collection)
    return render(request, 'polls/entry.html', {'form': form})

@login_required
def modifyEntryView(request, name):
    query = mEntry.objects.filter(eName = name)
    if not query.exists():
        messages.warning(request, "Entry does not exist")
        return redirect("dashboard")

    selectedEntry = query.first()
    if selectedEntry.eCollection.created_by != request.user:
        messages.warning(request, "Unable to Edit Collection")
        return redirect("dashboard")
    
    if request.method == 'POST':
        if "shouldDelete" in request.POST:
            selectedEntry.delete()
            messages.success(request, "Deleted Entry")
            return redirect("mcollections:dashboard_specific", collection=selectedEntry.eCollection.cName)

        form = mEntryModelForm(request.POST, request.FILES, instance=selectedEntry)
        if form.is_valid():
            form.save() 
            messages.success(request, "Entry Updated")
            return redirect("mcollections:dashboard_specific", collection=selectedEntry.eCollection.cName)
        else:
            messages.warning(request, "error")
            return redirect("mcollections:entry_specific", name=selectedEntry.eName)
    
    form = mEntryModelForm(instance=selectedEntry)
    return render(request, 'polls/entry.html', {'selectedEntry': selectedEntry, 'form': form})

@login_required
def deleteCollectionView(request, collection):
    query = mCollection.objects.filter(cName = collection)
    if not query.exists():
        messages.warning(request, "Collection does not exist")
        return redirect("dashboard")
    
    collection = query.first()
    if collection.created_by != request.user:
        messages.warning(request, "You do not own collection")
        return redirect("dashboard")
    
    query = mEntry.objects.filter(eCollection = collection)
    if query.exists():
        messages.warning(request, "Collection must be empty")
        return redirect("dashboard")
    
    if request.method == 'POST':
        if "confirmDelete" in request.POST:
            collection.delete()
            messages.success(request, "Deleted Collection")
            return redirect("dashboard")
        
    return render(request, "polls/deleteCollection.html", {'collection': collection})