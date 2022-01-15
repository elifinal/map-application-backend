from django.contrib.gis.db.models import PointField
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GeoModel
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geos import GEOSGeometry, LineString, Polygon, fromstr
from django.utils.translation import gettext as _
# Create your views here.
from .serializers import GeoModelSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models.query_utils import Q


class GeoModelDet(APIView):
    def post(self, request):

        response = dict()
        print('request', request)
            # geometry_types = {
            #     'Polygon': 0
            #
            # }
        data = json.loads(request.body.decode('utf-8'))
        fields = {
            'name': data['data'].get('name'),
            'type': data['data'].get('type'),
            'desc': data['data'].get('desc'),
            'radius': data['data'].get('radius'),
            'place': data['data'].get('places'),
        }
        geometry_type = data['data'].get('type')
        print(request.body.decode('utf-8'))
        points = data['data'].get('locations')
        if geometry_type == 'rectangle' or geometry_type == 'polygon':
            locations = list()
            points = points[0]  # multipoligon için 0,1,2 diye dönücek foricinde for kullanılacak
            for point in points:
                locations.append(GEOSGeometry("POINT({} {})".format(str(point[0]), str(point[1]))))
            fields['poly'] = Polygon(locations)
        elif geometry_type == 'polyline':
            locations = list()
            for point in points:
                locations.append(GEOSGeometry("POINT({} {})".format(str(point[0]), str(point[1]))))
            fields['line'] = LineString(locations)
        elif geometry_type == 'circle' or geometry_type == 'marker':
            locations = list()
            # locations.append(GEOSGeometry("POINT({} {})".format(str(points[0]), str(points[1]))))
            fields['point'] = GEOSGeometry("POINT({} {})".format(str(points[0]), str(points[1])))
            # print('ulsss', locations[0])

        geo = GeoModel.objects.create(**fields)
        response = {
            'status': True,
            'message': _('Kayıt Oluşturuldu!')
        }
        # except Exception as e:
        #     print(str(e))
        # response['status'] = False
        return JsonResponse(response, safe=False)

    def put(self, request):
        data = json.loads(request.body.decode('utf-8'))
        param = data.get('data')
        model_id = param.get('id')
        print('id', model_id)
        element = GeoModel.objects.filter(id=model_id)
        if element.exists():
            element = element.first()
        else:
            return JsonResponse(dict(), safe=False, status=200)
        points = param.get('points')
        print('points', points)
        element.name = param.get('name')
        element.desc = param.get('desc')
        element.type = param.get('type')
        element.radius = param.get('radius', 0)
        if element.type == 'rectangle' or element.type == 'polygon':
            locations = list()
            points = points[0]
            for point in points:
                locations.append(GEOSGeometry("POINT({} {})".format(str(point[0]), str(point[1]))))
            element.poly = Polygon(locations)
        elif element.type == 'polyline':
            locations = list()
            for point in points:
                locations.append(GEOSGeometry("POINT({} {})".format(str(point[0]), str(point[1]))))
            element.line = LineString(locations)
        elif element.type == 'marker' or element.type == 'circle':
            element.point = GEOSGeometry("POINT({} {})".format(str(points[0]), str(points[1])))
        element.save()
        response = {
            'status': True
        }
        return JsonResponse(response, safe=False, status=200)

    def get(self, request):
        print('req', request.query_params)
        body = request.query_params
        page = int(body.get('page', 1))
        print('type', type(body))
        limit = int(body.get('limit', 10))
        geo_models = GeoModel.objects.filter(is_active=True)
        print(geo_models)
        serializer = list()
        for item in geo_models:
            object = {
                'name': item.name,
                'id': item.id,
                'desc': item.desc,
                'type': item.type,
                'radius': item.radius,
                'place': item.place,
            }
            if item.type == 'polyline':
                object['points'] = item.line.coords
            elif item.type == 'marker' or item.type == 'circle':
                object['points'] = item.point.coords
            elif item.type == 'polygon' or item.type == 'rectangle':
                object['points'] = item.poly.coords
            serializer.append(object)
                # object['locations'] = points.

        # serializer = GeoModelSerializer(geo_models, many=True)
        arr = serializer[((page-1)*limit):(limit*page)]
        # page = data['data'].get('page')
        # print('page', page)
        # print(serializer)
        return JsonResponse({'data': arr, 'count': len(serializer)}, safe=False)

    def delete(self, request):
        print('delete', request.query_params)
        param = request.query_params
        model_id = param.get('id')
        print('id', model_id)
        element = GeoModel.objects.get(id=model_id)
        element.is_active = False
        element.save()
        response = {
            'status': True
        }
        return JsonResponse(response, safe=False, status=200)


class ClosestAreas(APIView):
    def put(self, request):
        limit = 5
        data = json.loads(request.body.decode('utf-8'))
        # print('sata', data)
        lat = data['data'].get('lat')
        lng = data['data'].get('lng')
        radius = data['data'].get('range')
        place = data['data'].get('place')
        page = int(data['data'].get('page',1))
        # print('req', data)
        # print('req', lat)
        user_location = fromstr("POINT(%s %s)" % (lng, lat))
        # print('req', user_location)
        radius = int(radius)
        desired_radius = {'m': radius}
        # print('place', GeoModel.objects.filter(place=int(place)))
        if place == 6:
            nearby_spots = GeoModel.objects.filter(
                Q(line__distance_lte=(user_location, D(**desired_radius))) | Q(
                    poly__distance_lte=(user_location, D(**desired_radius))) | Q(
                    point__distance_lte=(user_location, D(**desired_radius))))[:limit]
            print('distance', )
        else:
            print('hello', int(place))
            nearby_spots = GeoModel.objects.filter(place=int(place)).filter(Q(line__distance_lte=(user_location, D(**desired_radius))) | Q(poly__distance_lte=(user_location, D(**desired_radius))) | Q(point__distance_lte=(user_location, D(**desired_radius))))[:limit]
        serializer = list()
        for item in nearby_spots:
            object = {
                'name': item.name,
                'id': item.id,
                'desc': item.desc,
                'type': item.type,
                'radius': item.radius,
                'place': item.get_place_display(),
            }
            if item.type == 'polyline':
                object['points'] = item.line.coords
                # nokta = item.poly.distance(user_location)
                # print('distance', nokta*81)
                # print('distance', item.line.distance(user_location))
                object['distance'] = nokta*81
            elif item.type == 'marker' or item.type == 'circle':
                object['points'] = item.point.coords
                object['distance'] = item.point.distance(user_location)*81
                # print('distance', item.point.distance(user_location)*81)
            elif item.type == 'polygon' or item.type == 'rectangle':
                object['points'] = item.poly.coords
                nokta = item.poly.distance(user_location)
                object['distance'] = nokta*81
                # print('distance', nokta*81)

            serializer.append(object)
            # print('serializer', serializer)
        # print(nearby_spots)
        # serializer = GeoModelSerializer(nearby_spots, many=True)

        return JsonResponse(serializer, safe=False, status=200)

    def get(self, request):
        # print('req', request)
        geo_models = GeoModel.objects.filter(is_active=True)
        # print('models', geo_models)
        serializer = list()
        for item in geo_models:
            object = {
                'name': item.name,
                'id': item.id,
                'desc': item.desc,
                'type': item.type,
                'radius': item.radius,
                'place': item.get_place_display(),
            }
            if item.type == 'polyline':
                object['points'] = item.line.coords
            elif item.type == 'marker' or item.type == 'circle':
                object['points'] = item.point.coords
            elif item.type == 'polygon' or item.type == 'rectangle':
                object['points'] = item.poly.coords
            serializer.append(object)
            # print('serializer', serializer)

        return JsonResponse(serializer, safe=False, status=200)

