source env/bin/activate

export FLASK_APP=application.py
export DATABASE_URL=postgres://ulpdbhlgoztmgl:a18d8e4746db57b4bdcd0e85d37ef6384ad8ab82cd96e0c9071270b90a33015d@ec2-50-16-196-57.compute-1.amazonaws.com:5432/d1lfc84243tvuk
export FLASK_DEBUG=1

flask run
