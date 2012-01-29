"""
Portraits Provider
"""
from zope.interface import implements

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from App.special_dtml import DTMLFile
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PlonePAS.interfaces.plugins import IPortraitManagementPlugin
from Products.PlonePAS.interfaces.capabilities import IChangePortraitCapability
from OFS.Image import Image
from Products.PlonePAS.utils import scale_image


class VirtualImage(object):

    meta_type = 'VirtualImage'

    def __init__(self, id, width=None, height=None, title='', url=''):
        self.id = id
        self.url = url
        self.width = width
        self.title = title
        self.height = height

    def getId(self):
        return self.id

    def absolute_url(self):
        return self.url


def manage_addZODBPortraitProvider(self, id, title='',
                                          RESPONSE=None, **kw):
    """
    Create an instance of a portraits manager.
    """
    o = ZODBPortraitProvider(id, title, **kw)
    self._setObject(o.getId(), o)

    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')

manage_addZODBPortraitProviderForm = DTMLFile(
    "../zmi/PortraitProviderForm", globals())


class ZODBPortraitProvider(BasePlugin):
    """Storage for portraits in the ZODB.
    """

    meta_type = 'ZODB Portrait Provider'

    implements(IPortraitManagementPlugin,
               IChangePortraitCapability)
    security = ClassSecurityInfo()

    manage_options = (BasePlugin.manage_options +
                      ( { 'label' : 'Migrate portraits'
                     , 'action' : 'manage_migrate_portraits'
                     },))

    security.declareProtected(ManagePortal, 'manage_migrate_portraits')
    manage_migrate_portraits = DTMLFile('../zmi/migrate_portraits', globals())

    def __init__(self, id, title='', **kw):
        """Create in-ZODB portrait provider.
        """
        self.id = id
        self.title = title
        self.portraits=BTreeFolder2(id='portraits')

    def getPortrait(self, member_id):
        """ return member_id's portrait if you can """
        return self.portraits.get(member_id, None)
        
    def setPortrait(self, portrait, member_id):
        """ store portrait for particular member.
            portrait must be file-like object"""
        if member_id in self.portraits:
            self.portraits._delObject(member_id)
        
        # ignore VirtualImage portraits
        if isinstance(portrait, VirtualImage):
            return False

        if portrait and portrait.filename:
            scaled, mimetype = scale_image(portrait)
            portrait = Image(id=safe_id, file=scaled, title='')
            self.portraits._setObject(id= member_id, object=portrait)
        return True
        
    def deletePortrait(self, member_id):
        """ remove member_id's portrait """
        if member_id in self.portraits:
            self.portraits._delObject(member_id)
        return True

    security.declareProtected(ManagePortal, 'migratePortraits' )
    def migratePortraits(self):
        """ migrate portraits from MemberDataTool._portraits """
        md = getToolByName(self, 'portal_memberdata')
        storage = getattr(md, 'portraits', None)
        count = removed = 0
        if storage is not None:
            for member_id, portrait in storage.items():
                if self.getPortrait(member_id) is None:
                    self.portraits._setObject(id= member_id, object=portrait)
                    count += 1
                del storage[member_id]
                removed += 1
        return count, removed
                    
    def portraitInfo(self):
        md = getToolByName(self, 'portal_memberdata')
        result = {'md': 0, 'plugin': len(self.portraits)}
        storage = getattr(md, 'portraits', None)
        if storage is not None:
            result['md'] = len(storage)
        return result

    # IChangePortraitCapability 
    def allowModifyPortrait(self, member_id):
        return True
        
InitializeClass(ZODBPortraitProvider)

def manage_addPortalMemberdataPortraitProvider(self, id, title='',
                                          RESPONSE=None, **kw):
    """
    Create an instance of a portraits manager.
    """
    o = PortalMemberdataPortraitProvider(id, title, **kw)
    self._setObject(o.getId(), o)

    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')

manage_addPortalMemberdataPortraitProviderForm = DTMLFile(
    "../zmi/PortalMemberdataPortraitProviderForm", globals())
    
class PortalMemberdataPortraitProvider(BasePlugin):
    """Reuse portal_memberdata portraits storage
    """

    meta_type = 'PortalMemberdata Portrait Provider'

    implements(IPortraitManagementPlugin,
               IChangePortraitCapability)

    def __init__(self, id, title='', **kw):
        """Create portrait provider.
        """
        self.id = id
        self.title = title

    def getPortrait(self, member_id):
        """ return member_id's portrait if you can """
        mds = getattr(getToolByName(self, 'portal_memberdata'), 'portraits', None)
        if mds is not None:
            return mds.get(member_id, None)
        
    def setPortrait(self, portrait, member_id):
        """ store portrait for particular member.
            portrait must be OFS.Image.Image """
        # ignore VirtualImage portraits
        if isinstance(portrait, VirtualImage):
            return False

        mds = getattr(getToolByName(self, 'portal_memberdata'), 'portraits', None)
        if mds is not None:
            if member_id in mds:
                mds._delObject(member_id)
            mds._setObject(id= member_id, object=portrait)
            return True
        
    def deletePortrait(self, member_id):
        """ remove member_id's portrait """
        mds = getattr(getToolByName(self, 'portal_memberdata'), 'portraits', None)
        if mds is not None:
            if member_id in mds:
                mds._delObject(member_id)
            return True

    # IChangePortraitCapability 
    def allowModifyPortrait(self, member_id):
        return True

InitializeClass(PortalMemberdataPortraitProvider)
