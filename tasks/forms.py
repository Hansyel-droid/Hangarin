from django import forms
from .models import Task, Note, SubTask


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the task...'}),
            'deadline':    forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status':      forms.Select(attrs={'class': 'form-control'}),
            'category':    forms.Select(attrs={'class': 'form-control'}),
            'priority':    forms.Select(attrs={'class': 'form-control'}),
        }


class NoteForm(forms.ModelForm):
    """Used inline on the task detail page (task is set in the view)."""
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a note...'}),
        }


class StandaloneNoteForm(forms.ModelForm):
    """Used on the standalone note create/edit pages (includes task selection)."""
    class Meta:
        model = Note
        fields = ['task', 'content']
        widgets = {
            'task':    forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your note...'}),
        }


class SubTaskForm(forms.ModelForm):
    """Used inline on the task detail page (parent_task is set in the view)."""
    class Meta:
        model = SubTask
        fields = ['title', 'status']
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub-task title...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class StandaloneSubTaskForm(forms.ModelForm):
    """Used on the standalone sub-task create/edit pages (includes parent task selection)."""
    class Meta:
        model = SubTask
        fields = ['parent_task', 'title', 'status']
        widgets = {
            'parent_task': forms.Select(attrs={'class': 'form-control'}),
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub-task title...'}),
            'status':      forms.Select(attrs={'class': 'form-control'}),
        }
