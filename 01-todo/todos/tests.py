from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Task


# ==================== MODEL TESTS ====================

class TaskModelTest(TestCase):
    """Test cases for the Task model"""

    def setUp(self):
        """Set up test data"""
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            due_date=timezone.now() + timedelta(days=1)
        )

    def test_task_creation(self):
        """Test that a task can be created with all fields"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertIsNotNone(self.task.due_date)
        self.assertFalse(self.task.is_resolved)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_task_str_method(self):
        """Test the string representation of a task"""
        self.assertEqual(str(self.task), "Test Task")

    def test_task_default_is_resolved(self):
        """Test that is_resolved defaults to False"""
        new_task = Task.objects.create(title="Another Task")
        self.assertFalse(new_task.is_resolved)

    def test_task_optional_fields(self):
        """Test that description, due_date, and reminder_date are optional"""
        task = Task.objects.create(title="Minimal Task")
        self.assertEqual(task.description, "")
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.reminder_date)

    def test_task_ordering(self):
        """Test that tasks are ordered by created_at descending"""
        # Clear existing tasks from setUp
        Task.objects.all().delete()
        
        import time
        task1 = Task.objects.create(title="First")
        time.sleep(0.01)  # Small delay to ensure different timestamps
        task2 = Task.objects.create(title="Second")
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)  # Most recent first
        self.assertEqual(tasks[1], task1)

    def test_task_with_reminder(self):
        """Test creating a task with reminder date"""
        reminder = timezone.now() + timedelta(hours=2)
        task = Task.objects.create(
            title="Task with reminder",
            reminder_date=reminder
        )
        self.assertIsNotNone(task.reminder_date)
        self.assertTrue(task.has_reminder())
        self.assertTrue(task.is_reminder_upcoming())

    def test_task_has_reminder_method(self):
        """Test has_reminder method"""
        task_with_reminder = Task.objects.create(
            title="With reminder",
            reminder_date=timezone.now() + timedelta(days=1)
        )
        task_without_reminder = Task.objects.create(title="Without reminder")
        
        self.assertTrue(task_with_reminder.has_reminder())
        self.assertFalse(task_without_reminder.has_reminder())

    def test_task_is_reminder_upcoming_method(self):
        """Test is_reminder_upcoming method"""
        future_reminder = Task.objects.create(
            title="Future reminder",
            reminder_date=timezone.now() + timedelta(days=1)
        )
        past_reminder = Task.objects.create(
            title="Past reminder",
            reminder_date=timezone.now() - timedelta(days=1)
        )
        
        self.assertTrue(future_reminder.is_reminder_upcoming())
        self.assertFalse(past_reminder.is_reminder_upcoming())


# ==================== VIEW TESTS ====================

class TaskViewTest(TestCase):
    """Test cases for Task views"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description"
        )

    def test_task_list_view(self):
        """Test the task list (home) view"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/home.html')
        self.assertContains(response, "Test Task")
        # Check that the new context variables exist
        self.assertIn('overdue_tasks', response.context)
        self.assertIn('today_tasks', response.context)
        self.assertIn('upcoming_tasks', response.context)
        self.assertIn('no_due_date_tasks', response.context)
        self.assertIn('completed_tasks', response.context)

    def test_task_list_empty(self):
        """Test task list when no tasks exist"""
        Task.objects.all().delete()
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks yet!")

    def test_task_create_get(self):
        """Test GET request to create task page"""
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/task_form.html')
        self.assertContains(response, "Create")

    def test_task_create_post(self):
        """Test POST request to create a new task"""
        initial_count = Task.objects.count()
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'due_date': '2025-12-31T23:59'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Task.objects.count(), initial_count + 1)
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.title, 'New Task')
        self.assertEqual(new_task.description, 'New Description')

    def test_task_create_post_minimal(self):
        """Test creating a task with only required field (title)"""
        response = self.client.post(reverse('task_create'), {
            'title': 'Minimal Task'
        })
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(title='Minimal Task')
        self.assertEqual(task.description, '')
        self.assertIsNone(task.due_date)

    def test_task_edit_get(self):
        """Test GET request to edit task page"""
        response = self.client.get(reverse('task_edit', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/task_form.html')
        self.assertContains(response, "Edit")
        self.assertContains(response, self.task.title)

    def test_task_edit_post(self):
        """Test POST request to update a task"""
        response = self.client.post(reverse('task_edit', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')

    def test_task_edit_nonexistent(self):
        """Test editing a non-existent task returns 404"""
        response = self.client.get(reverse('task_edit', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_task_delete_get(self):
        """Test GET request to delete confirmation page"""
        response = self.client.get(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/task_confirm_delete.html')
        self.assertContains(response, self.task.title)

    def test_task_delete_post(self):
        """Test POST request to delete a task"""
        task_id = self.task.id
        initial_count = Task.objects.count()
        response = self.client.post(reverse('task_delete', args=[task_id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), initial_count - 1)
        self.assertFalse(Task.objects.filter(id=task_id).exists())

    def test_task_toggle_resolve(self):
        """Test toggling task resolution status"""
        # Initially not resolved
        self.assertFalse(self.task.is_resolved)
        
        # Toggle to resolved
        response = self.client.post(reverse('task_toggle_resolve', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_resolved)
        
        # Toggle back to not resolved
        response = self.client.post(reverse('task_toggle_resolve', args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_resolved)

    def test_task_toggle_resolve_nonexistent(self):
        """Test toggling resolution of non-existent task returns 404"""
        response = self.client.post(reverse('task_toggle_resolve', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_task_create_with_reminder(self):
        """Test creating a task with reminder date"""
        response = self.client.post(reverse('task_create'), {
            'title': 'Task with Reminder',
            'description': 'Has a reminder',
            'reminder_date': '2025-12-25T10:00'
        })
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(title='Task with Reminder')
        self.assertIsNotNone(task.reminder_date)

    def test_task_edit_with_reminder(self):
        """Test editing a task to add/update reminder"""
        response = self.client.post(reverse('task_edit', args=[self.task.id]), {
            'title': 'Updated with Reminder',
            'description': 'Now has reminder',
            'reminder_date': '2025-12-31T12:00'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertIsNotNone(self.task.reminder_date)
        self.assertEqual(self.task.title, 'Updated with Reminder')


# ==================== URL TESTS ====================

class TaskURLTest(TestCase):
    """Test cases for URL routing"""

    def test_task_list_url_resolves(self):
        """Test that task_list URL resolves correctly"""
        url = reverse('task_list')
        self.assertEqual(url, '/')

    def test_task_create_url_resolves(self):
        """Test that task_create URL resolves correctly"""
        url = reverse('task_create')
        self.assertEqual(url, '/create/')

    def test_task_edit_url_resolves(self):
        """Test that task_edit URL resolves correctly"""
        url = reverse('task_edit', args=[1])
        self.assertEqual(url, '/edit/1/')

    def test_task_delete_url_resolves(self):
        """Test that task_delete URL resolves correctly"""
        url = reverse('task_delete', args=[1])
        self.assertEqual(url, '/delete/1/')

    def test_task_toggle_resolve_url_resolves(self):
        """Test that task_toggle_resolve URL resolves correctly"""
        url = reverse('task_toggle_resolve', args=[1])
        self.assertEqual(url, '/toggle/1/')


# ==================== INTEGRATION TESTS ====================

class TaskIntegrationTest(TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        self.client = Client()

    def test_complete_task_workflow(self):
        """Test creating, editing, resolving, and deleting a task"""
        # Create a task
        response = self.client.post(reverse('task_create'), {
            'title': 'Integration Test Task',
            'description': 'Testing complete workflow'
        })
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(title='Integration Test Task')
        
        # Edit the task
        response = self.client.post(reverse('task_edit', args=[task.id]), {
            'title': 'Updated Integration Task',
            'description': 'Updated workflow test'
        })
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Integration Task')
        
        # Mark as resolved
        self.client.post(reverse('task_toggle_resolve', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.is_resolved)
        
        # Delete the task
        self.client.post(reverse('task_delete', args=[task.id]))
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_multiple_tasks_display(self):
        """Test that multiple tasks are displayed correctly"""
        Task.objects.create(title="Task 1")
        Task.objects.create(title="Task 2")
        Task.objects.create(title="Task 3")
        
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")
        self.assertContains(response, "Task 3")
        # Count tasks in all categories
        total_tasks = (len(response.context['overdue_tasks']) + 
                      len(response.context['today_tasks']) + 
                      len(response.context['upcoming_tasks']) + 
                      len(response.context['no_due_date_tasks']) + 
                      len(response.context['completed_tasks']))
        self.assertEqual(total_tasks, 3)
