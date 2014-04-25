# -*- coding: utf-8 -*-
# Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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

from django.shortcuts import render, render_to_response

from django.core import serializers

from django.conf import settings

from django.http import *

from searchengine.search_indexes import CoreEngine

from questionnaire.models import Questionnaire

from literature.utils import dict_union

import json

# This view shows annotatted publications associated with a determined fingerprint_id,
# or a message saying there's no publications associated, in case there's none yet or 
# the questionnaire type doesn't have publications widget
def literature_database_info(request, fingerprint_id, template_name='literature_info.html'):

    c = CoreEngine()

    results = c.search_fingerprint("id:" + fingerprint_id)

    publications = []

    if(len(results) == 1):
        #getListPublications(results.docs[0])
        publications = getListPublications(results.docs[0])


    return render(request, template_name, {'request': request, 'publications': publications})

# i could presume 'Publications_t' is always the source, but its better to find out what questions 
# are of publications type, and get responses for that, 
# since nothing stops uses from having questionary types that have multiple publications widgets

def getListPublications(database):


    # first we find the questionnaire type
    qtype = None
    pubquestions = []

    qqs = Questionnaire.objects.all()
    for q in qqs:
        if q.slug == database['type_t']:
            qtype = q

    if qtype != None:
        # We get all questionset's questions with publication type
        for question in qtype.questions():
            if question.type == 'publication':
                pubquestions.append(question)
            
    # we then get the field values themselves
    publications = []
    for pubq in pubquestions:
            print pubq.slug
            string_publications = None

            try:
                string_publications = database[pubq.slug+'_t']

            except KeyError:
                pass

            # If we actually have publications defined
            if string_publications != None:
                # for some reason, json.loads returns a dict on no results
                if type(publications) == type(json.loads(string_publications)):
                    publications = publications+json.loads(string_publications)      

    return publications


# Static, old version
def getListPublicationsStatic(database):
    publications = {}
    string_publications = None

    try:
        string_publications = database['Publications_t']

    except KeyError:
        pass

    # If we actually have publications defined
    if string_publications != None:
        publications = json.loads(string_publications)

    return publications
