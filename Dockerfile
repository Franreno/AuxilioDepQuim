FROM postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB Auxilios
COPY esquema.sql /docker-entrypoint-initdb.d/
EXPOSE 5433