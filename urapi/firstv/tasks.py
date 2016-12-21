from __future__ import absolute_import
from celery import shared_task,task
from firstv.tinytools.ebay_feedback import get_feedback
from firstv.dbtools.ebaydata import get_feedback_json

@task
def get_ebay_feedback():
    get_feedback()
    # print 'I am running!'

@task
def get_ebay_json(sellername):
    return get_feedback_json(sellername)