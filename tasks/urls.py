from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Tasks
    path('tasks/',                         views.task_list,   name='task_list'),
    path('tasks/create/',                  views.task_create, name='task_create'),
    path('tasks/<int:pk>/',                views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/',           views.task_edit,   name='task_edit'),
    path('tasks/<int:pk>/delete/',         views.task_delete, name='task_delete'),

    # Notes (inline actions from task detail)
    path('tasks/<int:task_pk>/notes/add/', views.note_add,    name='note_add'),
    path('notes/<int:pk>/delete/',         views.note_delete, name='note_delete'),

    # Notes (standalone pages in sidebar)
    path('notes/',                         views.note_list,   name='note_list'),
    path('notes/create/',                  views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/',           views.note_edit,   name='note_edit'),

    # Sub Tasks (inline actions from task detail)
    path('tasks/<int:task_pk>/subtasks/add/', views.subtask_add,    name='subtask_add'),
    path('subtasks/<int:pk>/delete/',         views.subtask_delete, name='subtask_delete'),
    path('subtasks/<int:pk>/toggle/',         views.subtask_toggle, name='subtask_toggle'),

    # Sub Tasks (standalone pages in sidebar)
    path('subtasks/',                      views.subtask_list,   name='subtask_list'),
    path('subtasks/create/',               views.subtask_create, name='subtask_create'),
    path('subtasks/<int:pk>/edit/',        views.subtask_edit,   name='subtask_edit'),

    # Categories
    path('categories/',                    views.category_list,   name='category_list'),
    path('categories/create/',             views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/',      views.category_edit,   name='category_edit'),
    path('categories/<int:pk>/delete/',    views.category_delete, name='category_delete'),

    # Priorities
    path('priorities/',                    views.priority_list,   name='priority_list'),
    path('priorities/create/',             views.priority_create, name='priority_create'),
    path('priorities/<int:pk>/edit/',      views.priority_edit,   name='priority_edit'),
    path('priorities/<int:pk>/delete/',    views.priority_delete, name='priority_delete'),
]
