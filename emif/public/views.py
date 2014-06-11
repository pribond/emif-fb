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

from django.shortcuts import render, render_to_response, redirect
from django.db.models import Q

from django.core import serializers
from django.conf import settings
from django.http import *

from public.models import *
from fingerprint.models import Answer
from fingerprint.services import findName
from public.services import createFingerprintShare, deleteFingerprintShare

def fingerprint_list(request, template_name='fingerprints.html', added=False):

    alink = request.session.get('created_public_link')
    dlink = request.session.get('deleted_public_link')
    try:
        del request.session['created_public_link']
        del request.session['deleted_public_link']
    except:
        pass

    links_query  = PublicFingerprintShare.objects.filter(user=request.user)

    own_dbs      = Fingerprint.objects.filter(owner=request.user)
    shared_dbs   = Fingerprint.objects.filter(shared=request.user)

    links = []
    linkedfingerprints = []
    # This is a bother, must find names since they are not readily available anywhere... I reiterate i think the name
    # should be linked somehow to the fingerprint object directly...
    for link in links_query:
        this_fingerprint = link.fingerprint

        linkedfingerprints.append(this_fingerprint.id)

        name = findName(this_fingerprint)

        links.append({'name': name, 'share': link})

    intersection = own_dbs | shared_dbs 
    intersection_clean = intersection.filter(~Q(id__in=linkedfingerprints))

    intersection_wnames = []

    for o in intersection_clean:
        name = findName(o)

        intersection_wnames.append({'name': name, 'fingerprint': o})

    return render(request, template_name, {'request': request, 'links': links, 'create_public': True, 
        'own_dbs': intersection_wnames, 'hide_add': True, 'breadcrumb': True, 'added': alink, 'deleted': dlink})

def fingerprint(request, fingerprint_id, template_name='fingerprint_summary.html'):

    return render(request, template_name, {'request': request})

def fingerprint_create(request, fingerprint_id):

    createFingerprintShare(fingerprint_id, request.user)

    request.session['created_public_link'] = True
    return redirect('public.views.fingerprint_list')

def fingerprint_delete(request, share_id):

    deleteFingerprintShare(share_id)

    request.session['deleted_public_link'] = True
    return redirect('public.views.fingerprint_list')
