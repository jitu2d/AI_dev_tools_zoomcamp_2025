# Django TODO Application

A fully functional TODO application built with Django that allows you to manage your tasks efficiently.

## Features

- ✅ **Create TODOs** - Add new tasks with title, description, and due dates
- ✏️ **Edit TODOs** - Update existing tasks
- 🗑️ **Delete TODOs** - Remove tasks you no longer need
- 📅 **Assign Due Dates** - Set deadlines for your tasks
- 🔔 **Set Reminders** - Get notified about important tasks
- ✔️ **Mark as Resolved** - Toggle task completion status
- 🎨 **Beautiful UI** - Clean and modern interface with gradient backgrounds

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Start the Development Server

```bash
python manage.py runserver
```

### 4. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## Usage

### Create a TODO
1. Click the **"+ Add New Task"** button
2. Fill in the title (required)
3. Optionally add a description and due date
4. Click **"Create Task"**

### Edit a TODO
1. Click the **"Edit"** button next to any task
2. Modify the fields you want to change
3. Click **"Edit Task"** to save

### Delete a TODO
1. Click the **"Delete"** button next to any task
2. Confirm the deletion

### Mark as Resolved
- Click the **"Mark Resolved"** button to mark a task as complete
- Click **"✓ Resolved"** to unmark it

## Project Structure

```
01-todo/
├── todoproject/         # Django project settings
│   ├── settings.py     # Project configuration
│   └── urls.py         # Main URL routing
├── todos/              # TODO app
│   ├── models.py       # Task model definition
│   ├── views.py        # View functions (CRUD operations)
│   ├── urls.py         # App URL routing
│   └── templates/      # HTML templates
│       └── todos/
│           ├── base.html              # Base template with styling
│           ├── task_list.html         # List all tasks
│           ├── task_form.html         # Create/Edit form
│           └── task_confirm_delete.html # Delete confirmation
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Model Schema

### Task Model
- `title` (CharField) - Task title (max 200 characters)
- `description` (TextField) - Optional task description
- `due_date` (DateTimeField) - Optional due date
- `reminder_date` (DateTimeField) - Optional reminder date to get notified
- `is_resolved` (BooleanField) - Completion status (default: False)
- `created_at` (DateTimeField) - Auto-generated creation timestamp
- `updated_at` (DateTimeField) - Auto-updated modification timestamp

### Model Methods
- `has_reminder()` - Check if task has a reminder set
- `is_reminder_upcoming()` - Check if reminder is in the future

## Technologies Used

- **Django 3.2.25** - Python web framework
- **SQLite** - Database (default Django database)
- **HTML/CSS** - Frontend templates with embedded styling

## Testing

The application includes comprehensive test coverage:

### Running Tests

```bash
python manage.py test todos
```

### Test Coverage

**29 tests covering:**

1. **Model Tests (10 tests)**
   - Task creation with all fields
   - String representation
   - Default values
   - Optional fields (description, due_date, reminder_date)
   - Ordering by creation date
   - Reminder functionality (has_reminder, is_reminder_upcoming)

2. **View Tests (15 tests)**
   - Task list view (home page)
   - Empty task list
   - Create task (GET and POST)
   - Create task with reminder
   - Edit task (GET and POST)
   - Edit task with reminder
   - Delete task (GET and POST)
   - Toggle resolution status
   - Error handling (404 for non-existent tasks)

3. **URL Tests (5 tests)**
   - All URL patterns resolve correctly

4. **Integration Tests (2 tests)**
   - Complete workflow (create → edit → resolve → delete)
   - Multiple tasks display

### Run Tests with Verbose Output

```bash
python manage.py test todos --verbosity=2
```

## Admin Panel (Optional)

To use the Django admin panel:

1. Create a superuser:
```bash
python manage.py createsuperuser
```

2. Access the admin panel at:
```
http://127.0.0.1:8000/admin/
```

## License

This project is open source and available for educational purposes.
