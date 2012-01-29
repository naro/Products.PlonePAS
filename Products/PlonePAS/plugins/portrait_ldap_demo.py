"""
Portraits Provider
"""
from zope.interface import implements, Interface

from App.class_init import InitializeClass
from App.special_dtml import DTMLFile

from Products.Five import BrowserView
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PlonePAS.interfaces.plugins import IPortraitManagementPlugin
from Products.PlonePAS.interfaces.capabilities import IChangePortraitCapability
from Products.PlonePAS.plugins.portraits import VirtualImage

def manage_addLDAPPortraitProvider(self, id, title='',
                                          RESPONSE=None, **kw):
    """
    Create an instance of a portraits manager.
    """
    o = LDAPPortraitProvider(id, title, **kw)
    self._setObject(o.getId(), o)

    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')

manage_addLDAPPortraitProviderForm = DTMLFile(
    "../zmi/LDAPPortraitProviderForm", globals())

class ILDAPPortraitProvider(Interface):
    """ Marker interface """
    
class PortraitView(BrowserView):
    
    def portrait(self, member_id=''):
        """ This is really DEMO! 
            Real function should return content of jpegPhoto member attribute,
            if exist.
        """
        from Products.PlonePAS import config
        import os
        pas_path = os.path.dirname(config.__file__)
        path = os.path.join(pas_path, 'tests', 'images')
        raw_data = open(os.path.join(path, 'test.jpg'), 'rb').read()
        self.request.response.setHeader('Content-Type', 'image/jpeg')
        return raw_data
    
class LDAPPortraitProvider(BasePlugin):
    """LDAP portraits plugin demo
       This demo does not contact ldap server for data but uses raw image data
       as example of jpegPhoto attribute contents
    """

    meta_type = 'LDAP Portrait Provider'

    implements(ILDAPPortraitProvider, 
               IPortraitManagementPlugin, 
               IChangePortraitCapability)

    def __init__(self, id, title='', **kw):
        """Create LDAP portrait provider.
        """
        self.id = id
        self.title = title

    def getPortrait(self, member_id):
        """ Return URL of traversable Image
        """
        # Check if member exist in LDAP and if there is jpegPhoto attribute 
        # if not, return None, otherwise return similar URL:
        return VirtualImage(member_id, url=self.absolute_url() + '/@@portrait?member_id=' + member_id)

    def setPortrait(self, portrait, member_id):
        """ store portrait for particular member.
            portrait must be OFS.Image.Image """
        # not supported
        return False
        
    def deletePortrait(self, member_id):
        """ remove member_id's portrait """
        # not supported
        return False

    # IChangePortraitCapability 
    def allowModifyPortrait(self, member_id):
        return False
        
InitializeClass(LDAPPortraitProvider)

