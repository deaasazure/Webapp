FROM postgres:13.1
COPY init.sql /docker-entrypoint-initdb.d/
# COPY postgresql.conf /tmp/postgresql.conf
# COPY updateconfig.sh /docker-entrypoint-initdb.d/updateconfig.sh


RUN chmod -R 755 /docker-entrypoint-initdb.d/init.sql
#ENV POSTGRES_PASSWORD postgres
#EXPOSE 5432
# CMD ["postgres", "-c", "config-file=/tmp/postgresql.conf"]