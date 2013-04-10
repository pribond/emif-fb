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


"""A module for Python index

.. moduleauthor:: Luís A. Bastião Silva <bastiao@ua.pt>

"""

from __future__ import print_function
import pysolr

from questionnaire.models import RunInfoHistory
#from questionnaire.models import Answer, Question

from django.db.models.signals import post_save
from django.dispatch import receiver

import logging


"""
Convert a answer from questionarie to a JSON document to be indexed by SOLR
"""
def convert_answer_to_json(question_id,answers):
	# Get the questions

	response = dict()

	# for answer in answers:
	# 	question_key = answer.question.text
	# 	question_value = answer.answer 
	# 	response[question_key] = question_value

	# # Convert to JSON
	# response_json =  JSONEncoder().encode(response)

	# return response_json


"""It is responsible for index the documents and search over them
It also connects to SOLR
"""
class CoreEngine:
	CONNECTION_TIMEOUT_DEFAULT = 10
	def __init__(self, timeout=CONNECTION_TIMEOUT_DEFAULT):
		# Setup a Solr instance. The timeout is optional.
		self.solr = pysolr.Solr('http://localhost:8983/solr', timeout=timeout)

	def index_fingerprint(self, doc):
		"""Index fingerprint 
		"""
		# index document
		self.index_fingerprint_as_json(convert_answer_to_json(doc))
	
	def index_fingerprint_as_json(self, d):
		"""Index fingerprint as json
		"""
		# index document
		
		xlm_answer = self.solr.add([d])
		print(xlm_answer)
		self.optimize()

	def optimize(self):
		"""This function optimize the index. It improvement the search and retrieve documents subprocess.
		However, it is a hard tasks, and call it for every index document might not be a good idea.
		"""
		self.solr.optimize()

	def update(self, doc):
		"""Update the document
		"""
		# Search  and identify the document id

		# Delete 
		self.solr.delete(id='doc_1')

		# Index the new document
		self.index(doc)

	def search_fingerprint(self, query):
		"""search the fingerprint
		"""
		# Later, searching is easy. In the simple case, just a plain Lucene-style
		# query is fine.
		results = self.solr.search(query)

		return results

	def more_like_this(self, id_doc):
		similar = self.solr.more_like_this(q='id:doc_2', mltfl='text')
		return similar



from django.db.models.signals import post_save
from django.dispatch import receiver
from searchengine.search_indexes import CoreEngine
from questionnaire.models import *
from searchengine.models import Slugs


def convert_text_to_slug(text):
	#TODO: optimize
	return text.replace(' ', '_').replace('?','').replace('.', '').replace(',','')

def clean_answer(answer):
	#TODO: optimize
	return answer


def convert_answers_to_solr(runinfo):
    c = CoreEngine()
    
    runid = runinfo.runid
    answers = Answer.objects.filter(runid=runid)

    print(answers)
    d = {}
    for a in answers:
    	logging.debug("Answer text: " + a.answer)
    	logging.debug("Q: " + a.question.text)
    	logging.debug("Slug:" + a.question.slug)
    	slug = a.question.slug	
    	
    	slug_aux = ""
    	if len(slug)>2:
    		slug = a.question.slug
    		logging.debug("Slug@"+slug)
    		logging.debug("Slug@len"+str(len(slug)))
    	else:
    		slug = convert_text_to_slug(a.question.text)
    		logging.debug("Slug@@"+slug)
    	slug_final = slug+"_t"

    	results = Slugs.objects.filter(description=a.question.text)
    	print("Slugs:")
    	print(results)
    	if results==None or len(results)==0:
    		slugs = Slugs()
    		slugs.slug1 = slug_final
    		slugs.description = a.question.text
    		slugs.question = a.question
    		slugs.save()

    	d[slug_final] = a.answer	
    print(d)
    d['id']=runid
    c.index_fingerprint_as_json(d)


@receiver(post_save, sender=RunInfoHistory)
def my_handler(sender, **kwargs):
	# Check if it is advanced search or not.
	# If it is advanced search, it is not necessary to index
	# Otherwise the index will be necessary

    print("#### Indexing now ###############")
    logging.debug(sender)
    for key in kwargs:
        logging.debug("another keyword arg: %s: %s" % (key, kwargs[key]))
    runinfo = kwargs["instance"]
    
    logging.debug(runinfo.questionnaire.questionsets())
    logging.debug(runinfo.subject)
    logging.debug(runinfo.skipped)
    logging.debug(runinfo.tags)
    logging.debug(runinfo.completed)
    logging.debug(runinfo.runid)
    convert_answers_to_solr(runinfo)

def main():

	c = CoreEngine()
	_m = {'id':'Luis', 'title': 'dam', 'my_stat_t': 'lol'}
	import json
	_mm=json.dumps(_m)
	print(_mm)
	c.index_fingerprint_as_json(_m)
	results = c.search_fingerprint("my_stat_t:locals()")
	print(results)
	for r in results:
		print(r)

if __name__=="__main__":
	main()
