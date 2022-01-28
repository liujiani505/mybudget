from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="incomeapp"),
    path('add-income', views.add_income, name="add-incomes"),
    path('edit-income/<int:id>', views.edit_income, name="edit-incomes"),
    path('delete-income/<int:id>', views.delete_income, name="delete-incomes"),    
]
