from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from django.conf import settings
from .models import Tenant

class TenantMiddleware(MiddlewareMixin):

    HEADER_NAME="HTTP_X_TENANT_ID"   # Django exposes X-Tenant-ID as HTTP_X_TENANT_ID
    HOST_HEADER="HTTP_HOST"

    def process_request(self,request):
        tenant=None

         # 1) Header-based (development-friendly). Only used when allowed in settings.
        allow_header = getattr(settings,"TENANT_ALLOW_HEADER",True)
        if allow_header:
            tenant_id=request.META.get(self.HEADER_NAME)
            if tenant_id:
                tenant=Tenant.objects.filter(id=tenant_id).first()
                # if header provided but not found, return 404 to avoid ambiguous routing
                if tenant is None:
                    raise Http404("Tenant not found")
                request.tenant=tenant
                return
            
        # Host/subdomain parsing
        host=request.META.get(self.HOST_HEADER,"")
        if host:
            host_only=host.split(":")[0]
            parts=host_only.split(".")
            # Example: acme.localhost or acme.example.com
            if len(parts) >=3 or (len(parts) == 2 and "localhost" in host_only):
                subdomain = parts[0]
                tenant= Tenant.objects.filter(slug=subdomain).first()
                if tenant:
                    request.tenant=tenant
                    return
                
         # 3) Fallback to authenticated user's tenant (if User has tenant FK)
        if getattr(request, "user", None) and request.user.is_authenticated:
            request.tenant = getattr(request.user, "tenant", None)
        else:
            request.tenant = None