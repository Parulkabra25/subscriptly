from rest_framework.permissions import BasePermission
from .models import Membership

class IsTenantAdmin(BasePermission):
    # Allow access only to tenant owner or admin

    def has_permission(self,request,view):
        user=request.user
        tenant=getattr(request,"tenant",None)

        #Must be logged in 
        if not user or not user.is_authenticated:
            return False
        
        # Tenant must be resolved
        if tenant is None:
            return False
        
        # Fatch membership
        membership=Membership.objects.filter(
            tenant=tenant,
            user=user
        ).first()

        if membership is None:
            return False
        
        # Allow only owner or admin
        return membership.role in[
            Membership.ROLE_OWNER,
            Membership.ROLE_ADMIN
        ]
    
