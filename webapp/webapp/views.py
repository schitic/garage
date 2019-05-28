from django.http import HttpResponseBadRequest, HttpResponse
import json
import os
import inspect
from django.shortcuts import render
from GarageDeamon.Loader import ActorLoader, SensorLoader
from django.contrib.sites.shortcuts import get_current_site


def index(request):
    params = {
        'sensors': [],
        'actors': []
    }
    sensors = SensorLoader.get_modules()
    for sensor in sorted(sensors.keys()):
        params['sensors'].append(sensors[sensor].html_hook())
    actors = ActorLoader.get_modules()
    for actor in sorted(actors.keys()):
        params['actors'].append(actor)
    return render(request, 'index.html', context=params)


def logs(request):
    logs = os.environ.get("GARAGE_LOG")
    lines = []
    if logs:
        with open(logs, 'r') as f:
            lines = f.readlines()
    lines.reverse()
    return render(request, 'logs.html', context={'lines': lines[0:1000]})


def rest_sensor(request, sensor_name=None):
    if sensor_name:
        sensor_name = sensor_name.upper()
    sensors = SensorLoader.get_modules()
    results = []
    for sensor in sensors.keys():
        if sensor_name and sensor.upper() != sensor_name:
            continue
        results.append({
            'sensor_name': sensor,
            'value': sensors[sensor].get_db_state()
        })

    return HttpResponse(json.dumps(results),
                        content_type='application/json')


def rest_actor(request, actor_name):
    actor_name = actor_name.upper()
    actors = ActorLoader.get_modules()
    for actor in actors.keys():
        if actor.upper() != actor_name:
            continue
        try:
            actors[actor].run()
            return HttpResponse()
        except Exception as e:
            return HttpResponseBadRequest(str(e))


def rest_list(request):
    sensors = SensorLoader.get_modules()
    results = []
    url_base = request.build_absolute_uri()
    url_base = url_base.replace('/rest/list/', '')
    for sensor in sensors.keys():
        results.append({
            'sensor_name': sensor,
            'type': 'sensor',
            'config': _get_config(sensors[sensor]),
            'url': '%s/rest/sensors/%s/' % (url_base, sensor)
        })
    actors = ActorLoader.get_modules()
    for actor in actors.keys():
        results.append({
            'sensor_name': actor,
            'type': 'actor',
            'config': _get_config(actors[actor]),
            'url': '%s/rest/actor/%s/' % (url_base, actor)

        })
    return HttpResponse(json.dumps(results),
                        content_type='application/json')


def _get_config(device):
    module_info = {}
    for tmp in dir(device):
        if tmp.startswith('_'):
            continue
        if inspect.ismethod(getattr(type(device), tmp, None)):
            continue
        if tmp in ['log', 'current_state', 'sensor_name', 'actor_name']:
            continue
        module_info[tmp] = getattr(device, tmp)
    return module_info
