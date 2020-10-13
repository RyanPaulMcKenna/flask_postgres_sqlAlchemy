FROM postgres:10

RUN echo "host  all  postgres  app  md5" > /var/lib/postgresql/data/pg_hba.conf

ADD create.sql /docker-entrypoint-initdb.d
