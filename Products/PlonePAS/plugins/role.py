##############################################################################
#
# PlonePAS - Adapt PluggableAuthService for use in Plone
# Copyright (C) 2005 Enfold Systems, Kapil Thangavelu, et al
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this
# distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
group aware role manager, returns roles assigned to group a principal
is a member of, in addition to the explicit roles assigned directly
to the principal.

$Id: role.py,v 1.8 2005/06/29 17:27:45 jccooper Exp $
"""

from AccessControl import ClassSecurityInfo
from Globals import DTMLFile, InitializeClass

from Products.PluggableAuthService.plugins.ZODBRoleManager \
     import ZODBRoleManager

from Products.PlonePAS.utils import unique
from Products.PlonePAS.interfaces.capabilities import IAssignRoleCapability

from Products.PluggableAuthService.permissions import ManageUsers


def manage_addGroupAwareRoleManager( self, id, title='', RESPONSE=None):
    """
    this is a doc string
    """
    garm = GroupAwareRoleManager( id, title )
    self._setObject( garm.getId(), garm)

    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')

manage_addGroupAwareRoleManagerForm = DTMLFile(
    '../zmi/GroupAwareRoleManagerForm', globals())

class GroupAwareRoleManager( ZODBRoleManager ):

    meta_type = "Group Aware Role Manager"
    __implements__ = ZODBRoleManager.__implements__ + (IAssignRoleCapability,)

    security = ClassSecurityInfo()

    security.declareProtected( ManageUsers, 'assignRolesToPrincipal' )
    def assignRolesToPrincipal( self, roles, principal_id ):
        """ Assign a specific set of roles, and only those roles, to a principal.

        o no return value

        o Raise KeyError if a role_id is unknown.
        """
        for role_id in roles:
            if role_id not in ('Authenticated','Anonymous','Owner'):
                role_info = self._roles[ role_id ] # raise KeyError if unknown!

        self._principal_roles[ principal_id ] = tuple(roles)


    security.declarePrivate( 'getRolesForPrincipal' )
    def getRolesForPrincipal( self, principal, request=None ):
        """ See IRolesPlugin.
        """
        roles = []
        principal_ids = [principal.getId()]
        principal_ids.extend( principal.getGroups() )
        for pid in principal_ids:
            roles.extend( self._principal_roles.get( pid, () ) )
        return tuple( unique( roles ) )


    ## implement IAssignRoleCapability

    def getRoleInfo(self, role_id):
        """Over-ride parent to not explode when getting role info by role_id."""
        return self._roles.get(role_id,None)

    def allowRoleAssign(self, user_id, role_id):
        """True iff this plugin will allow assigning a certain user a certain role."""
        present = self.getRoleInfo(role_id)
        if present: return 1   # if we have a role, we can assign it
                               # slightly naive, but should be okay. 
        return 0

InitializeClass( GroupAwareRoleManager )
