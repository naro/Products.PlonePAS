"""
$Id: groups.py,v 1.5 2005/02/04 23:23:32 k_vertigo Exp $
"""
from AccessControl import ClassSecurityInfo, Permissions
from Globals import InitializeClass

from Products.CMFPlone import ToolNames
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from Products.CMFCore.utils import getToolByName, UniqueObject
from OFS.SimpleItem import SimpleItem
from Products.PlonePAS.interfaces import group as igroup

class NotSupported(Exception): pass

class GroupsTool(UniqueObject, SimpleItem, PloneBaseTool):
    """
    for the groupie in you
    """

    id = 'portal_groups'
    meta_type = ToolNames.GroupsTool
    security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/group.gif'

    __implements__ = ( PloneBaseTool.__implements__,
                       igroup.IGroupTool )

    ##
    # basic group mgmt
    ##

    security.declareProtected(Permissions.manage_users, 'addGroup')
    def addGroup(self, id, **kw):
        group = None
        managers = self._getGroupManagers()
        if not managers:
            raise NotSupported("no plugins allow for group management")
        for mid, manager in managers:
            group =  manager.addGroup( id, **kw )
            if group is not None:
                break
        return group

    security.declareProtected(Permissions.manage_users, 'removeGroup')
    def removeGroup(self, group_id):
        managers = self._getGroupManagers()
        if not managers:
            raise NotSupported("no plugins allow for group management")
        for mid, manager in managers:
            if manager.removeGroup( group_id ):
                return True
        return False

    security.declareProtected(Permissions.manage_users, 'setRolesForGroup')
    def setRolesForGroup(self, group_id, roles=() ):
        # XXXX
        managers = self._getGroupManagers()
        if not managers:
            raise NotSupported("no plugins allow for group management")
        for mid, manager in managers:
            if manager.setRolesForGroup( group_id, roles ):
                return True



    ##
    # basic principal mgmt
    ##

    security.declareProtected(Permissions.manage_users, 'addPrincipalToGroup')
    def addPrincipalToGroup(self, principal_id, group_id):
        managers = self._getGroupManagers()
        if not managers:
            raise NotSupported("no plugins allow for group management")
        for mid, manager in managers:
            if manager.addPrincipalToGroup( principal_id, group_id):
                return True
        return False

    security.declareProtected(Permissions.manage_users, 'removePrincipalFromGroup')
    def removePrincipalFromGroup( self, principal_id, group_id):
        managers = self._getGroupManagers()
        if not managers:
            raise NotSupported("no plugins allow for group management")
        for mid, manager in managers:
            if manager.removePrincipalFromGroup( principal_id, group_id ):
                return True
        return False



    ##
    # group getters
    ##

    security.declareProtected(Permissions.manage_users, 'getGroupById')
    def getGroupById( group_id ):
        group = None
        introspecters = self._getGroupIntrospecters()
        if not introspectors:
            raise NotSupported("no plugins allow for group management")
        for iid, introspecter in introspecters:
            group = introspecters.getGroupById( group_id )
            if group is None:
                break
        return group

    security.declareProtected(Permissions.manage_users, 'searchGroups')
    def searchGroups(self, *args, **kw):
        # XXX document interface.. returns a list of dictionaries
        return self.acl_users.searchGroups( *args, **kw )

    security.declareProtected(Permissions.manage_users, 'getGroups')
    def getGroups(self):
        # potentially not all groups may be found by this interface
        # if the underlying group source doesn't support introspection
        groups = []
        introspecters = self._getGroupIntrospecters()
        for iid, introspecter in introspecters:
            groups.extend( introspecters.getGroups() )
        return groups

    security.declareProtected(Permissions.manage_users, 'getGroupIds')
    def getGroupIds(self):
        groups = []
        introspecters = self._getGroupIntrospecters()
        for iid, introspecter in introspecters:
            groups.extend( introspecters.getGroupIds() )
        return groups

    security.declareProtected(Permissions.manage_users, 'getGroupMembers')
    def getGroupMembers(self, group_id):
        members = []
        introspecters = self._getGroupIntrospecters()
        for iid, introspecter in introspecters:
            members = introspecters.getGroupMembers( group_id )
            if members:
                break
        return members

    security.declareProtected(Permissions.manage_users, 'getGroupsForPrincipal')
    def getGroupsForPrincipal( principal_id, request=None ):
        return self.acl_users._getGroupsForPrincipal( principal_id, request )

    ##
    # plugin getters
    ##

    security.declarePrivate('_getPlugins')
    def _getPlugins(self):
        return self.acl_users.plugins

    security.declarePrivate('_getGroupManagers')
    def _getGroupManagers(self):
        return self.acl_users.plugins.listPlugins(
            igroup.IGroupManagement
            )

    security.declarePrivate('_getGroupIntrospecters')
    def _getGroupIntrospecters(self):
        return self.acl_users.plugins.listPlugins(
            igroup.IGroupIntrospection
            )

    security.declarePrivate('_getGroupSpaceManagers')
    def _getGroupSpaceManagers(self):
        return self.acl_users.plugins.listPlugins(
            igroup.IGroupSpaceManagers
            )


InitializeClass(GroupsTool)
