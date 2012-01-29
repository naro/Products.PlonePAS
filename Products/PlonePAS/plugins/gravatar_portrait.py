"""
Portraits Provider
"""
from zope.interface import implements
from Acquisition import aq_inner
from Acquisition import aq_parent

from App.class_init import InitializeClass
from App.special_dtml import DTMLFile

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PlonePAS.interfaces.plugins import IPortraitManagementPlugin
from Products.PlonePAS.interfaces.capabilities import IChangePortraitCapability
from Products.PlonePAS.plugins.portraits import VirtualImage


try:
    from hashlib import md5
    md5  # pyflakes
except ImportError:
    from md5 import md5


def manage_addGravatarPortraitProvider(self, id, title='',
                                          RESPONSE=None, **kw):
    """
    Create an instance of a portraits manager.
    """
    o = GravatarPortraitProvider(id, title, **kw)
    self._setObject(o.getId(), o)

    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')

manage_addGravatarPortraitProviderForm = DTMLFile(
    "../zmi/GravatarPortraitProviderForm", globals())


class GravatarPortraitProvider(BasePlugin):
    """Gravatar portraits plugin
    """

    meta_type = 'Gravatar Portrait Provider'

    implements(IPortraitManagementPlugin, IChangePortraitCapability)

    def __init__(self, id, title='', **kw):
        """Create Gravatar portrait provider.
        """
        self.id = id
        self.title = title

    def getPortrait(self, member_id):
        """ return member_id's portrait if you can """
        pas = aq_parent(aq_inner(self))
        member = pas.getUserById(member_id)
        if member is not None:
            email = member.getProperty('email', '')
            if email:
                # create hash
                hash_ = md5(email.lower().strip()).hexdigest()
                # images are 80x80 by default
                url = 'http://www.gravatar.com/avatar/%s.jpg' % hash_
                # create virtual image
                return VirtualImage(member_id, width=80, height=80, url=url)

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
        
InitializeClass(GravatarPortraitProvider)
