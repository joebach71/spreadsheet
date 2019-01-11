'''
Created on Jun 9, 2017

@author: jupark
'''
from rest_framework import permissions

class IsUserAdminOrReadOnly(permissions.BasePermission):
    '''
    Custom Permission to only allow some users to add object 
    '''
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if request.user.is_superuser:
            return True
        
        return False