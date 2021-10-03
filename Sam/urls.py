from .views import RegisterView,LoginView, UserView,LogoutView
from django.urls import path
from Sam import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('items', views.items),
    path('itemshow',views.itemshow), 
    path('ItemEdit/<int:id>',views.ItemEdit, name="edit-item"),
    path('ItemDelete/<int:id>',views.ItemDelete, name="delete-item"),
    path('customer', views.CustomerAdd),
    path('customerview/<int:id>' ,views.CustomerView),
    path('supplier' ,views.SupplierAdd),
    path('jobadd', views.jobadd),
    path('jobshow',views.jobshow),
    path('JobEdit/<int:id>',views.JobEdit, name="edit-job"), 
    path('group', views.group),
    path('groupshow',views.groupshow), 
    path('groupEdit/<int:id>',views.groupEdit, name="edit-group"),
    path('groupDelete/<int:id>',views.ItemDelete, name="delete-group"),
    path('ledger', views.ledger),
    path('ledgershow',views.ledgershow), 
    path('ledgerEdit/<int:id>',views.ledgerEdit, name="edit-ledger"),
    path('ledgerDelete/<int:id>',views.ledgerDelete, name="delete-ledger"),
     path('EmployeeAdd', views.EmployeeAdd),
     path('employeeshow',views.employeeshow), 
    path('employeeEdit/<int:id>',views.employeeEdit, name="edit-employee"),
    path('employeeDelete/<int:id>',views.ItemDelete, name="delete-employee"),

     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

