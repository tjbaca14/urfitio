docker run -d \
  --name urfitio_dbcontainer \
  -e POSTGRES_USER="data_admin" \
  -e POSTGRES_PASSWORD="3rdHbaELbYoPuUDWRmSUiw="\
  -e POSTGRES_DB=urfitio \
  -p 5434:5434 \
  postgres:16
# 3rdHbaELbYoPuUDWRmSUiw== admin
# 1R58HPPyWiFxiT9DCUIC7g== api rw

export DATABASE='urfitio'
export USER='data_admin'
export PASSWORD='3rdHbaELbYoPuUDWRmSUiw=='
export HOST='localhost'
export PORT='5434'

# Export the password to use it with psql
export PGPASSWORD="$PASSWORD"

# Execute the psql command to connect to the database
docker run urfitio_dbcontainer 
psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DATABASE"