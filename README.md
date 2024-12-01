# Django Demo App

This is a boilerplate template for a Django project. It includes basic configurations and three paths: home, about, and admin.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/davesheinbein/djangodemoapp.git
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Install additional packages (if needed):
   For example, to install requests:

   ```sh
   pip install requests
   pip freeze > requirements.txt
   ```

5. Run database migrations:

   ```sh
   python manage.py migrate
   ```

6. Create a superuser for the admin interface:

   ```sh
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```sh
   python manage.py runserver
   ```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the home page. Access the admin interface at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with the superuser credentials you created.

## Project Structure

- **Home**: Accessible at `/`, this path returns a simple greeting message.
- **About**: Accessible at `/about/`, this path returns a brief description message.
- **Admin**: Accessible at `/admin/`, this path provides access to the Django admin interface.
