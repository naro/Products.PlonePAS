# Define certain interfaces that a plugin must meet if it is to allow
# certain operations to be done by the Plone UI.

from Products.PluggableAuthService.interfaces.plugins import Interface

class IDeleteCapability(Interface):
    """Interface for plugin to say if it allows for deletion of a user.
    Expected to be found on IUserManagement plugins.
    For Plone UI.
    """

    def allowDeletePrincipal(self, id):
        """True iff this plugin can delete a certain user/group."""

class IPasswordSetCapability(Interface):
    """Interface for plugin to say if it allows for setting the password of a user.
    Expected to be found on IUserManagement plugins.
    For Plone UI.
    """

    def allowPasswordSet(self, id):
        """True iff this plugin can set the password of a certain user."""


class IGroupCapability(Interface):
    """Interface for plugin to say if it allows for deletion of a user.
    For Plone UI.
    """

    def allowGroupAdd(self, principal_id, group_id):
        """True iff this plugin will allow adding a certain principal to a certain group."""

    def allowGroupRemove(self, principal_id, group_id):
        """True iff this plugin will allow removing a certain principal from a certain group."""


class IAssignRoleCapability(Interface):
    """Interface for plugin to say if it allows for deletion of a user.
    For Plone UI.
    """

    def allowRoleAssign(self, id, role):
        """True iff this plugin will allow assigning a certain principal a certain role."""


class IManageCapabilities(Interface):
    """Interface for MemberData/GroupData to provide information as to whether or not
    the member can be deleted, reset password, modify a property.
    """

    def canDelete(self):
        """True iff user can be removed from the Plone UI."""

    def canPasswordSet(self):
        """True iff user can change password."""

    def passwordInClear(self):
        """True iff password can be retrieved in the clear (not hashed.)"""

    def canWriteProperty(self, prop_name):
        """True iff the member/group property named in 'prop_name'
        can be changed.
        """

    def canAddToGroup(self, group_id):
        """True iff member can be added to group."""

    def canRemoveFromGroup(self, group_id):
        """True iff member can be removed from group."""

    def canAssignRole(self, role):
        """True iff member can be assigned role."""

class IChangePortraitCapability(Interface):
    """Interface for plugin to say if it allows for change user portraits.
    """

    def allowModifyPortrait(self, member_id):
        """True if this plugin will allow to set or remove member's portrait"""

