from sqlalchemy import create_engine
# export DOCKER_HOST_IP=$(route -n | awk '/UG[ \t]/{print $2}')
# The ip can also be set in docker compose in this case I hard coded it but its not ideal.

db_string = "postgres+psycopg2://postgres:example@172.17.0.1:5433/mytestdb"

db = create_engine(db_string)

# Create 
db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")  
db.execute("INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")

# Read
result_set = db.execute("SELECT * FROM films")  
for r in result_set:  
    print(r)