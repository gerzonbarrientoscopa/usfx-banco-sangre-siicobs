DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'siicobs_prod',
        'USER': 'sa',
        'PASSWORD': 'B4nc0Sangr3',
        'HOST': '127.0.0.1',
        'PORT': '1433',
    }
}
DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost', '172.16.1.195', 'sucre-siicobs.herokuapp.com', 'sucre-siicobs-assets.s3.amazonaws.com']
CSRF_TRUSTED_ORIGINS = ['http://universitarios1.usfx.bo']


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'siicobs_prod',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
DEBUG = False
ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost', '201.131.45.30', '172.16.1.195', 'universitarios1.usfx.bo', 'sucre-siicobs.herokuapp.com', 'sucre-siicobs-assets.s3.amazonaws.com']
'''