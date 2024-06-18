# to start working as dev
docker-compose -f docker-compose.prod.yml up -d --build
python3 manage.py runserver

# to deploy in stg
docker compose -f docker-compose.stg.yml up -d --build

# to deploy in prod
docker compose -f docker-compose.prod.yml up -d --build

# to deploy in dev 
docker compose -f docker-compose.dev.yml up -d --build

go to praxsa_manager folder

pip install -r requirements-3.8.10.txt

go to proforma folder

npm i

## run praxsa server
python manage.py runserver
## run proforma
npm run dev:ssr


# create admin user
python manage.py createsuperuser --username=joe --email=joe@example.com

# to run migration
python manage.py migrate 

# to create static file
python manage.py collectstatic

# chage static file owenership
chown -R app:app /praxsa_manager