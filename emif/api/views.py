# -*- coding: utf-8 -*-
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from django.http import HttpResponse

from django.contrib.auth.models import User
from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.views import *
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils import simplejson
# import json
import md5
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny, IsAuthenticated

# Import Search Engine 

from searchengine.search_indexes import CoreEngine


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(('GET', 'POST', 'PUT', 'OPTIONS', 'HEAD'))
def api_root(request, format=None):
    return Response({
        'search': reverse('search', request=request),
        'metadata': reverse('metadata', request=request),
        'stats': reverse('stats', request=request),
        'validate': reverse('validate', request=request),

    })


class SearchView(APIView):
    """
    Class to search and return fingerprint details, like Name, ID and structure
    """
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kw):

        # If authenticated
        if request.auth:
            user = request.user
            result = {'status': 'authenticated', 'method': 'GET', 'user': str(user)}
         #if query!=None:

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        # response['Access-Control-Allow-Origin'] = "*"
        # response['Access-Control-Allow-Headers'] = "Authorization"
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


class AdvancedSearchView(APIView):
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        return response


class MetaDataView(APIView):
    """
    Class to insert or update data values of one fingerprint

    Method POST: to insert a new field and value
    Method PUT: to update a value that already exists

    Note: both methods check if field value already exists and, if exists, it is updated,
    otherwise the field is created and the value added
    """
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes((JSONParser,))

    def post(self, request, *args, **kw):


        # If authenticated
        if request.auth:
            user = request.user
            result = {'status': 'authenticated', 'method': 'POST', 'user': str(user)}

            # objs = json.loads(request.POST)
            # Iterate through the stuff in the list
            # for o in objs:
            #     print o

            # print request.content_type
            print request.DATA['fingerprintID']

            # for i in request.DATA:
            #     print i
            #     json_data = simplejson.loads(i)
            #     print json_data

            # json_data = simplejson.loads(request.body)
            # print json_data
            # try:
            #   data = json_data['data']
            # except KeyError:
            #     print "ERROR"

            # for t in request.POST:
            #     print t
            # print request.POST.items()
            # jsonstr = request.POST["foo"]
            # print jsonstr

                # data = JSONParser().parse(i[0])
                # print data
                # json_test = json.loads(str(i[0]))
                # print json_test
            # data = JSONParser().parse(request)
            # print data
            #
            # #c = CoreEngine()
            # print request.content_type

            #
            # #c.index_fingerprint_as_json(json.loads(request.POST.get('_content')))
        else:
            result = {'status': 'NOT authenticated', 'method': 'POST'}
        # result = {'myValue': 'lol', 'myValue2': 'lol'}
        response = Response(result, status=status.HTTP_200_OK)
        # response['Access-Control-Allow-Origin'] = "192.168.1.2"
        response['Access-Control-Allow-Origin'] = "http://localhost"
        response['Access-Control-Allow-Headers'] = "authorization"

        return response

    def put(self, request, *args, **kw):

        # If authenticated
        if request.auth:
            user = request.user
            result = {'status': 'authenticated', 'method': 'PUT', 'user': str(user)}
        else:
            result = {'status': 'NOT authenticated', 'method': 'PUT'}
        # If modified
        response = Response(result, status=status.HTTP_200_OK)
        # If created
        # response = Response(result, status=status.HTTP_201_CREATED)
        # response['Access-Control-Allow-Origin'] = "*"
        # response['Access-Control-Allow-Headers'] = "Authorization"

        return response


class ValidateView(APIView):
    def get(self, request, *args, **kw):

        database_name = request.GET['name']
        c = CoreEngine()
        results = c.search_fingerprint("database_name_t:" + database_name)
        result = {'contains': len(results) != 0}

        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kw):
        try:

            print request.POST.items()
            for i in request.POST.items():
                print i[0]
                json_test = json.loads(i[0])
                print json_test

            #database_name = request.POST['database_name']
            # c = CoreEngine()
            #results = c.search_fingerprint("database_name_t:"+database_name)
            #result = {'contains': len(results)==0}
            result = {'test': 'teste2'}
            response = Response(result, status=status.HTTP_200_OK)
        except:
            print("fuck")
            raise
        return response


class StatsView(APIView):
    """
    Class that returns json values of answers to create stats (charts)
    """

    def get(self, request, *args, **kw):
        """
        Method to return values on format json
        :param request:
        :param args:
        :param kw:
        """

        try:
            results = dict()

            # GET Values
            questionnaire_id = int(request.GET['q_id'])
            question_set = int(request.GET['qs_id'])
            slug = request.GET['slug']

            question = Question.objects.filter(questionset_id=question_set, slug=slug, stats='1',
                                               questionset__questionnaire=questionnaire_id).order_by('number')

            results = self.getResults(question)

            if results:
                #Dump json file
                result = json.dumps(results)
            else:
                result = []
                # print(result)

            response = Response(result, status=status.HTTP_200_OK)
        except:
            print("fuck")
            raise
        return response

    def getResults(self, question):
        """
        Method that returns values to use in charts
        :param question:
        """

        from emif.statistics import Statistic

        results = dict()
        graphs = []
        for q in question:
            try:
                s = Statistic(q)

                graph = s.get_percentage()
                # print graph
                if not graph:
                    # results["values"] = "No"
                    #Return NULL if graph is empty
                    return results
                else:
                    # results["values"] = "Yes"
                    for g in graph:
                        # print g
                        for i in g:
                            graphs_aux = dict()
                            # print i, g[i]
                            graphs_aux['name'] = i
                            graphs_aux['score'] = g[i]
                            graphs.append(graphs_aux)
            except:
                raise

        results["attr1"] = "name"
        results["attr2"] = "score"
        results['charts'] = graphs

        return results