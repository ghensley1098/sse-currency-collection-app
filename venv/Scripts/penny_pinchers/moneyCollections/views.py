from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import mCollection, mEntry
from django.template import RequestContext

def index(request):
    latest_collection_list = mCollection.objects.order_by("-cDate")[:5]
    context = {
        "latest_collection_list": latest_collection_list,
    }
    return render(request, "moneycollections/index.html", context)

def detail(request, collection_id):
    mcollection = get_object_or_404(mCollection, pk=collection_id)
    return render(request, "moneycollections\detail.html", {"collection": mcollection})

