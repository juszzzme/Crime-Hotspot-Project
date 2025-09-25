# Crime Hotspot Project - Running Guide

This guide will help you set up and run the Crime Hotspot Project on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)
- PostgreSQL (for the database)
- Node.js and npm (for frontend dependencies if any)

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Crime-Hotspot-Project.git
cd Crime-Hotspot-Project
```

## 2. Set Up a Virtual Environment (Recommended)

### Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
 
### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Set Up Environment Variables

1. Create a `.env` file in the project root directory
2. Add the following variables (modify as needed):

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost/crime_hotspot
```

## 5. Set Up the Database

1. Make sure PostgreSQL is running
2. Create a new database:
   ```bash
   createdb crime_hotspot
   ```
3. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## 6. Import Data (if applicable)

If you have initial data to import, you can use the provided scripts in the `scripts/` directory or use the following command:

```bash
python import_data.py  # Replace with your actual import script
```

## 7. Run the Application

### Development Mode:
```bash
python run.py
```

Or using Flask's built-in server:
```bash
export FLASK_APP=run.py  # On Windows: set FLASK_APP=run.py
flask run
```

The application should now be running at `http://localhost:5000`

## 8. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 9. Available Endpoints

- Home: `/`
- API Documentation: `/api/docs` (if Swagger/OpenAPI is configured)
- Admin Dashboard: `/admin` (if admin interface is set up)

## 10. Running Tests

```bash
pytest
```

## 11. Stopping the Application

Press `Ctrl+C` in the terminal where the application is running to stop the server.

## Troubleshooting

1. **Port already in use**:
   - Find the process using the port: `lsof -i :5000` (macOS/Linux) or `netstat -ano | findstr :5000` (Windows)
   - Kill the process: `kill <PID>` or `taskkill /PID <PID> /F` (Windows)

2. **Database connection issues**:
   - Verify PostgreSQL is running
   - Check the `DATABASE_URL` in your `.env` file
   - Ensure the database and user credentials are correct

3. **Missing dependencies**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - If using a virtual environment, ensure it's activated

## Production Deployment

For production deployment, consider using:
- Gunicorn or uWSGI as the WSGI server
- Nginx or Apache as a reverse proxy
- Environment variables for sensitive configuration
- Proper logging and monitoring

## Support

For additional help, please refer to the project's documentation or open an issue on the GitHub repository.
