from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Task, Note, SubTask, Category, Priority
from .forms import TaskForm, NoteForm, SubTaskForm, StandaloneSubTaskForm, StandaloneNoteForm


# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    total_tasks      = Task.objects.count()
    completed_tasks  = Task.objects.filter(status='Completed').count()
    pending_tasks    = Task.objects.filter(status='Pending').count()
    in_progress_tasks = Task.objects.filter(status='In Progress').count()
    tasks_this_year  = Task.objects.filter(created_at__year=timezone.now().year).count()
    recent_tasks     = Task.objects.select_related('category', 'priority').order_by('-created_at')[:5]

    return render(request, 'tasks/dashboard.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'tasks_this_year': tasks_this_year,
        'recent_tasks': recent_tasks,
        'page_title': 'Dashboard',
    })


# ── TASK CRUD ─────────────────────────────────────────────────────────────────

@login_required
def task_list(request):
    tasks = Task.objects.select_related('category', 'priority').all()

    query = request.GET.get('q', '')
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    status_filter   = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    priority_filter = request.GET.get('priority', '')

    if status_filter:   tasks = tasks.filter(status=status_filter)
    if category_filter: tasks = tasks.filter(category_id=category_filter)
    if priority_filter: tasks = tasks.filter(priority_id=priority_filter)

    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['title', '-title', 'created_at', '-created_at', 'deadline', '-deadline', 'status', '-status']
    tasks = tasks.order_by(sort_by if sort_by in valid_sorts else '-created_at')

    page_obj = Paginator(tasks, 10).get_page(request.GET.get('page'))

    return render(request, 'tasks/task_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'priority_filter': priority_filter,
        'sort_by': sort_by,
        'categories': Category.objects.all(),
        'priorities': Priority.objects.all(),
        'page_title': 'Tasks',
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'notes': task.notes.order_by('-created_at'),
        'subtasks': task.subtasks.order_by('created_at'),
        'note_form': NoteForm(),
        'subtask_form': SubTaskForm(),
        'page_title': task.title,
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save()
        messages.success(request, f'Task "{task.title}" created successfully!')
        return redirect('task_detail', pk=task.pk)
    return render(request, 'tasks/task_form.html', {'form': form, 'page_title': 'Create Task', 'action': 'Create'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        task = form.save()
        messages.success(request, f'Task "{task.title}" updated successfully!')
        return redirect('task_detail', pk=task.pk)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task, 'page_title': 'Edit Task', 'action': 'Update'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task, 'page_title': 'Delete Task'})


# ── NOTES (inline on task detail) ────────────────────────────────────────────

@login_required
def note_add(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.task = task
            note.save()
            messages.success(request, 'Note added successfully!')
    return redirect('task_detail', pk=task_pk)


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    task_pk = note.task.pk
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        next_url = request.POST.get('next', '')
        if next_url == 'note_list':
            return redirect('note_list')
        return redirect('task_detail', pk=task_pk)
    return redirect('task_detail', pk=task_pk)


# ── SUBTASKS (inline on task detail) ─────────────────────────────────────────

@login_required
def subtask_add(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.parent_task = task
            subtask.save()
            messages.success(request, 'Sub-task added successfully!')
    return redirect('task_detail', pk=task_pk)


@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    task_pk = subtask.parent_task.pk
    if request.method == 'POST':
        subtask.delete()
        messages.success(request, 'Sub-task deleted successfully!')
        next_url = request.POST.get('next', '')
        if next_url == 'subtask_list':
            return redirect('subtask_list')
        return redirect('task_detail', pk=task_pk)
    return redirect('task_detail', pk=task_pk)


@login_required
def subtask_toggle(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    subtask.status = 'Pending' if subtask.status == 'Completed' else 'Completed'
    subtask.save()
    next_url = request.GET.get('next', '')
    if next_url == 'subtask_list':
        return redirect('subtask_list')
    return redirect('task_detail', pk=subtask.parent_task.pk)


# ── STANDALONE SUB TASK LIST + CREATE ────────────────────────────────────────

@login_required
def subtask_list(request):
    subtasks = SubTask.objects.select_related('parent_task').all()

    query = request.GET.get('q', '')
    if query:
        subtasks = subtasks.filter(
            Q(title__icontains=query) |
            Q(parent_task__title__icontains=query)
        )

    status_filter = request.GET.get('status', '')
    if status_filter:
        subtasks = subtasks.filter(status=status_filter)

    task_filter = request.GET.get('task', '')
    if task_filter:
        subtasks = subtasks.filter(parent_task_id=task_filter)

    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['title', '-title', 'created_at', '-created_at', 'status', '-status']
    subtasks = subtasks.order_by(sort_by if sort_by in valid_sorts else '-created_at')

    page_obj = Paginator(subtasks, 10).get_page(request.GET.get('page'))

    return render(request, 'tasks/subtask_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'task_filter': task_filter,
        'sort_by': sort_by,
        'tasks': Task.objects.order_by('title'),
        'page_title': 'Sub Tasks',
    })


@login_required
def subtask_create(request):
    form = StandaloneSubTaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sub-task created successfully!')
        return redirect('subtask_list')
    return render(request, 'tasks/subtask_form.html', {'form': form, 'page_title': 'Create Sub Task', 'action': 'Create'})


@login_required
def subtask_edit(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    form = StandaloneSubTaskForm(request.POST or None, instance=subtask)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sub-task updated successfully!')
        return redirect('subtask_list')
    return render(request, 'tasks/subtask_form.html', {'form': form, 'subtask': subtask, 'page_title': 'Edit Sub Task', 'action': 'Update'})


# ── STANDALONE NOTE LIST + CREATE ────────────────────────────────────────────

@login_required
def note_list(request):
    notes = Note.objects.select_related('task').all()

    query = request.GET.get('q', '')
    if query:
        notes = notes.filter(
            Q(content__icontains=query) |
            Q(task__title__icontains=query)
        )

    task_filter = request.GET.get('task', '')
    if task_filter:
        notes = notes.filter(task_id=task_filter)

    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['created_at', '-created_at', 'task__title', '-task__title']
    notes = notes.order_by(sort_by if sort_by in valid_sorts else '-created_at')

    page_obj = Paginator(notes, 10).get_page(request.GET.get('page'))

    return render(request, 'tasks/note_list.html', {
        'page_obj': page_obj,
        'query': query,
        'task_filter': task_filter,
        'sort_by': sort_by,
        'tasks': Task.objects.order_by('title'),
        'page_title': 'Notes',
    })


@login_required
def note_create(request):
    form = StandaloneNoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Note created successfully!')
        return redirect('note_list')
    return render(request, 'tasks/note_form.html', {'form': form, 'page_title': 'Create Note', 'action': 'Create'})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = StandaloneNoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        messages.success(request, 'Note updated successfully!')
        return redirect('note_list')
    return render(request, 'tasks/note_form.html', {'form': form, 'note': note, 'page_title': 'Edit Note', 'action': 'Update'})


# ── CATEGORIES ────────────────────────────────────────────────────────────────

@login_required
def category_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    page_obj = Paginator(categories, 10).get_page(request.GET.get('page'))
    return render(request, 'tasks/category_list.html', {'page_obj': page_obj, 'query': query, 'page_title': 'Categories'})


@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Category "{name}" created!')
            return redirect('category_list')
        messages.error(request, 'Name is required.')
    return render(request, 'tasks/category_form.html', {'page_title': 'Add Category', 'action': 'Create'})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            category.name = name
            category.save()
            messages.success(request, 'Category updated!')
            return redirect('category_list')
        messages.error(request, 'Name is required.')
    return render(request, 'tasks/category_form.html', {'category': category, 'page_title': 'Edit Category', 'action': 'Update'})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted!')
        return redirect('category_list')
    return render(request, 'tasks/category_confirm_delete.html', {'category': category, 'page_title': 'Delete Category'})


# ── PRIORITIES ────────────────────────────────────────────────────────────────

@login_required
def priority_list(request):
    query = request.GET.get('q', '')
    priorities = Priority.objects.all()
    if query:
        priorities = priorities.filter(name__icontains=query)
    page_obj = Paginator(priorities, 10).get_page(request.GET.get('page'))
    return render(request, 'tasks/priority_list.html', {'page_obj': page_obj, 'query': query, 'page_title': 'Priorities'})


@login_required
def priority_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Priority.objects.create(name=name)
            messages.success(request, f'Priority "{name}" created!')
            return redirect('priority_list')
        messages.error(request, 'Name is required.')
    return render(request, 'tasks/priority_form.html', {'page_title': 'Add Priority', 'action': 'Create'})


@login_required
def priority_edit(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            priority.name = name
            priority.save()
            messages.success(request, 'Priority updated!')
            return redirect('priority_list')
        messages.error(request, 'Name is required.')
    return render(request, 'tasks/priority_form.html', {'priority': priority, 'page_title': 'Edit Priority', 'action': 'Update'})


@login_required
def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        messages.success(request, 'Priority deleted!')
        return redirect('priority_list')
    return render(request, 'tasks/priority_confirm_delete.html', {'priority': priority, 'page_title': 'Delete Priority'})
