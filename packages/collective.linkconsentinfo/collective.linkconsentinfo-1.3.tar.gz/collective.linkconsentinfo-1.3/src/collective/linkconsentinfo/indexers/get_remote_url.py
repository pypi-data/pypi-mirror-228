# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import ILink
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.indexer import indexer


@indexer(ILink)
def getRemoteUrl(obj):
    if getattr(obj, 'enable_consent_info'):
        return ""
    return replace_link_variables_by_paths(obj, obj.remoteUrl)
