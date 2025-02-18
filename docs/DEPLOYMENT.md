# Deployment Guide

This guide covers deployment instructions for different platforms.

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yuan-accounting.git
cd yuan-accounting
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start development server:
```bash
python manage.py runserver
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t yuan-accounting .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e DATABASE_URL=your_db_url yuan-accounting
```

Or using docker-compose:
```bash
docker-compose up -d
```

## Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

4. Deploy:
```bash
git push heroku main
```

5. Run migrations:
```bash
heroku run python manage.py migrate
```

## AWS Elastic Beanstalk Deployment

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB application:
```bash
eb init -p python-3.9 yuan-accounting
```

3. Create environment:
```bash
eb create yuan-accounting-env
```

4. Set environment variables:
```bash
eb setenv SECRET_KEY=your_secret_key DEBUG=False
```

5. Deploy:
```bash
eb deploy
```

## Production Considerations

### Security
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Enable HTTPS
- Set up proper CORS settings

### Performance
- Use Redis for caching
- Configure database connection pooling
- Set up static file serving with CDN
- Enable database query optimization

### Monitoring
- Set up logging
- Configure error tracking (e.g., Sentry)
- Set up performance monitoring
- Enable health checks

### Backup
- Configure database backups
- Set up file storage backups
- Implement disaster recovery plan
