
#nohup sh -c "chmod +x PostgreSQL_install.sh && ./PostgreSQL_install.sh"> $OPENSHIFT_LOG_DIR/PostgreSQL_install.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/PostgreSQL_install.log

POSTGRESQL_VERSION="9.1.4"

# Installing DB (one-time)

cd $OPENSHIFT_DATA_DIR

wget http://ftp.postgresql.org/pub/source/v${POSTGRESQL_VERSION}/postgresql-${POSTGRESQL_VERSION}.tar.gz

tar xf postgresql-${POSTGRESQL_VERSION}.tar.gz
rm postgresql-${POSTGRESQL_VERSION}.tar.gz

cd postgresql-${POSTGRESQL_VERSION}

./configure --prefix=${OPENSHIFT_DATA_DIR}postgres --enable-nls="cs" --with-python --with-openssl --with-libxml
make
make install

cd ..

rm -rf postgresql-${POSTGRESQL_VERSION}

# Setup DB (one-time)

${OPENSHIFT_DATA_DIR}postgres/bin/initdb -D ${OPENSHIFT_DATA_DIR}postgres/data

# Starting DB

if [ -f ${OPENSHIFT_DATA_DIR}postgres/data/postmaster.pid ]; then
  kill -0 `head -1 ${OPENSHIFT_DATA_DIR}postgres/data/postmaster.pid`
else
  false
fi

if [ $? = 0 ]; then
  echo "PostgreSQL is running."
else
  ${OPENSHIFT_DATA_DIR}postgres/bin/postgres -D ${OPENSHIFT_DATA_DIR}postgres/data > ${OPENSHIFT_LOG_DIR}postgres 2>&1 &
fi

# Stopping DB

kill -INT `head -1 ${OPENSHIFT_DATA_DIR}postgres/data/postmaster.pid`

# Foreman to keep PostgreSQL running (setup)

export GEM_PATH=${OPENSHIFT_DATA_DIR}gems
export GEM_HOME=${OPENSHIFT_DATA_DIR}gems
gem install foreman --no-ri --no-rdoc

cat <<EOF > ${OPENSHIFT_DATA_DIR}postgresql
if [ -f \${OPENSHIFT_DATA_DIR}postgres/data/postmaster.pid ]; then
  kill -0 \`head -1 \${OPENSHIFT_DATA_DIR}postgres/data/postmaster.pid\`
else
  false
fi

if [ \$? = 0 ]; then
  echo "PostgreSQL is running."
else
  \${OPENSHIFT_DATA_DIR}postgres/bin/postgres -D \${OPENSHIFT_DATA_DIR}postgres/data > \${OPENSHIFT_LOG_DIR}postgres 2>&1
fi
EOF

chmod +x ${OPENSHIFT_DATA_DIR}postgresql

cat <<EOF > ${OPENSHIFT_DATA_DIR}Procfile
pgsql: \${OPENSHIFT_DATA_DIR}postgresql
EOF

# Foreman to keep PostgreSQL running (start & ensure)

export GEM_PATH=${OPENSHIFT_DATA_DIR}gems
export GEM_HOME=${OPENSHIFT_DATA_DIR}gems
${OPENSHIFT_DATA_DIR}gems/bin/foreman start

# Installing PostGIS

GDAL_VERSION="1.9.1"
GEOS_VERSION="3.3.5"
PROJ_VERSION="4.8.0"
POSTGIS_VERSION="2.0.1"

cd $OPENSHIFT_DATA_DIR

wget http://download.osgeo.org/gdal/gdal-${GDAL_VERSION}.tar.gz

tar xf gdal-${GDAL_VERSION}.tar.gz
rm gdal-${GDAL_VERSION}.tar.gz
cd gdal-${GDAL_VERSION}

./configure --prefix=${OPENSHIFT_DATA_DIR}postgres
make
make install

cd ..

rm -rf gdal-${GDAL_VERSION}

wget http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2

tar xf geos-${GEOS_VERSION}.tar.bz2
rm geos-${GEOS_VERSION}.tar.bz2
cd geos-${GEOS_VERSION}

./configure --prefix=${OPENSHIFT_DATA_DIR}postgres
make
make install

cd ..

rm -rf geos-${GEOS_VERSION}

wget http://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz

tar xf proj-${PROJ_VERSION}.tar.gz
rm proj-${PROJ_VERSION}.tar.gz

cd proj-${PROJ_VERSION}

./configure --prefix=${OPENSHIFT_DATA_DIR}postgres
make
make install

cd ..
rm -rf proj-${PROJ_VERSION}

wget http://postgis.refractions.net/download/postgis-${POSTGIS_VERSION}.tar.gz

tar xf postgis-${POSTGIS_VERSION}.tar.gz
rm postgis-${POSTGIS_VERSION}.tar.gz

cd postgis-${POSTGIS_VERSION}

./configure --with-pgconfig=${OPENSHIFT_DATA_DIR}postgres/bin/pg_config --with-geosconfig=${OPENSHIFT_DATA_DIR}postgres/bin/geos-config --with-gdalconfig=${OPENSHIFT_DATA_DIR}postgres/bin/gdal-config --with-projdir=${OPENSHIFT_DATA_DIR}postgres
make
make install

cd ..

rm -rf postgis-${POSTGIS_VERSION}

# Setting up PostGIS

${OPENSHIFT_DATA_DIR}postgres/bin/createdb db
${OPENSHIFT_DATA_DIR}postgres/bin/psql -d db -c "CREATE EXTENSION postgis;"

#nohup sh -c "PostgreSQL_install.sh"> $OPENSHIFT_LOG_DIR/PostgreSQL_install.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/PostgreSQL_install.log