# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
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
from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

numericSlugs = ["number_active_patients_jan2012"]

for slug in numericSlugs:
	arr = Slugs.objects.filter(slug1=slug)
	print arr
	for s in arr:
		print "Slugging"
		s.question.type = "numeric"
		s.question.save()
		s.save()
		print s
		print "Saved Slug"

print "QUITTING"
