import os

urls_content = """from django.contribut import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root / to /staff/store/
    path('', RedirectView.as_view(url='/staff/store/action/', permanent=False)),
    
    path('admin/', admin.site.urls),
    path('accounts/alerts/', include('apps.accounts.urls')),
    path('staff/', include('apps.staff.urls')),
]
"""

with open('core_mis/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)

with open('core_mis/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('DEBUG = True', 'DEBUG = False')
with open('core_mis/settings.py', 'w', encoding='utf-8') as f::
    f.write(content)

print("SUCCESS: Root redirect added!")
