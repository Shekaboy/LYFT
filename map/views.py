from django.shortcuts import render, reverse
from django.views import generic
from map.models import Nodes, Edges, Event
from django.core import serializers
from django.http import JsonResponse
from .djikshtra import *
from django.contrib.auth import get_user_model
from django.views import View
from .forms import EventForm
from .models import Event, Trip
from login.models import Beaver
from django.http import HttpResponseRedirect
import json
# Create your views here.

def home(request):
    return render(request, 'map/home.html')

def home2(request):
    return render(request, 'map/home2.html')

class HomeView(View):
    template_name = "map/homepage.html"

    def get(self, request):
        if request.user.is_authenticated:
            events = Event.objects.all()
            kwargs = {"user" : request.user, "events" : events}
            return render(request, self.template_name, kwargs)
        else:
            return HttpResponseRedirect(reverse("login:index"))

class AddView(View):
    template_name = "map/addevent.html"
    form_class = EventForm

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
    
    def post(self, request):
        addeventform = self.form_class(request.POST, request.FILES)
        if(addeventform.addevent((request))):
            return HttpResponseRedirect(reverse("map:home"))
        else:
            kwargs = {"form" : addeventform}
            return render(request, self.template_name, kwargs)


class EventView(View):
    template_name = "map/event.html"

    def get(self, request, id):
        if request.user.is_authenticated:
            event = Event.objects.get(pk=id)
            beaver = Beaver.objects.get(user=request.user)
            try:
                trips = Trip.objects.all()
                related_trips = Trip.objects.filter(event=event)
                trips = trips | related_trips
            except Trip.DoesNotExist:
                trips = None
            print(trips)
            count = trips.count()
            source = beaver.address
            destination = event.desc
            nodes = {}
            a = Nodes.objects.values('id', 'node')
            print(a.count)
            graph = Graph(a.count())
            for i in range(15):
                id = a[i]['id'] - 64
                node = a[i]['node']
                nodes[node] = id
            b = Edges.objects.values('node1', 'node2', 'distance')
            for i in range(b.count()):
                node1 = b[i]['node1'] - 64
                node2 = b[i]['node2'] - 64
                distance = b[i]['distance']
                graph.addEdge(node1, node2, distance)
            source = nodes[source]
            print(source)
            destination = nodes[destination]
            print(destination)
            dji1 = graph.dijkstra(source, destination)
            path = printingpath(source, destination, dji1[1])
            for i in range(len(path) - 1):
                c = b.filter(node1=(path[i] + 64), node2 = (path[i+1] + 64)).values('edge')
                path[i] = c[0]['edge']
            del path[-1]
            print("Distance is ", dji1[0][destination])
            print("Path is ", path)
            path2 = json.dumps(path)
            kwargs = {"event" : event, "beaver" : beaver, "distance" : dji1[0][destination], "path" : path2, "trips" : trips, "count" : count}
            return render(request, self.template_name, kwargs)
     
    def post(self, request, id):
        if request.user.is_authenticated:
            beaver = Beaver.objects.get(user = request.user)
            event = Event.objects.get(pk = id)
            trip = Trip(user=beaver, event=event)
            trip.save()
            return HttpResponseRedirect(reverse("map:home"))
    

def getit(request):

    if request.is_ajax and request.method == "GET":
        source = request.GET.get("source", None)
        destination = request.GET.get("destination", None)
        print(source)
        print(type(source))
        print(destination)
        print(type(destination))
        nodes = {}
        a = Nodes.objects.values('id', 'node')
        graph = Graph(a.count())
        for i in range(15):
            id = a[i]['id'] - 49
            node = a[i]['node']
            nodes[node] = id
        b = Edges.objects.values('node1', 'node2', 'distance')
        for i in range(b.count()):
            node1 = b[i]['node1'] - 49
            node2 = b[i]['node2'] - 49
            distance = b[i]['distance']
            graph.addEdge(node1, node2, distance)
        source = nodes[source]
        print(source)
        destination = nodes[destination]
        print(destination)
        dji1 = graph.dijkstra(source, destination)
        path = printingpath(source, destination, dji1[1])
        for i in range(len(path) - 1):
            c = b.filter(node1=(path[i] + 49), node2 = (path[i+1] + 49)).values('edge')
            path[i] = c[0]['edge']
        del path[-1]
        return JsonResponse({"distance" : dji1[0][destination], "path" : path}, status = 200)


def getit2(request):
    if request.is_ajax and request.method == 'GET':
        source1 = request.GET.get("source1", None)
        source2 = request.GET.get("source2", None)
        destination = request.GET.get("desc", None)
        nodes = {}
        a = Nodes.objects.values('id', 'node')
        graph = Graph(a.count())
        for i in range(15):
            id = a[i]['id'] - 64
            node = a[i]['node']
            nodes[node] = id
        graph = Graph(a.count())
        b = Edges.objects.values('node1', 'node2', 'distance')
        for i in range(b.count()):
            node1 = b[i]['node1'] - 64
            node2 = b[i]['node2'] - 64
            distance = b[i]['distance']
            graph.addEdge(node1, node2, distance)
        source1 = nodes[source1]
        source2 = nodes[source2]
        destination = nodes[destination]
        paths = graph.dijkstrafortwo(source1, source2, destination)
        for i in range(len(paths[0]) - 1):
            c = b.filter(node1=(paths[0][i] + 64), node2 = (paths[0][i+1] + 64)).values('edge')
            paths[0][i] = c[0]['edge']
        del paths[0][-1]

        for i in range(len(paths[1]) - 1):
            c = b.filter(node1=(paths[1][i] + 64), node2 = (paths[1][i+1] + 64)).values('edge')
            paths[1][i] = c[0]['edge']
        del paths[1][-1]
        return JsonResponse({"path1" : paths[0], "path2" : paths[1], "boolean" : paths[2]}, status = 200)