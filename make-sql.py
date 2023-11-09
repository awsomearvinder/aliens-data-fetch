print("""
      DROP DATABASE aliens;
      CREATE DATABASE aliens;
      USE aliens;

      CREATE TABLE LOCATION (
          location_id INTEGER PRIMARY KEY AUTO_INCREMENT,
          country VARCHAR(255) NOT NULL,
          state VARCHAR(255) NOT NULL,
          city VARCHAR(255) NOT NULL,
          UNIQUE unique_loc(city, state, country)
      );
      CREATE TABLE USER (
          username VARCHAR(255) PRIMARY KEY,
          password VARCHAR(255) NOT NULL
      );
      CREATE TABLE EVENT (
          event_id INTEGER PRIMARY KEY AUTO_INCREMENT,
          reporting_user VARCHAR(255) NOT NULL,
          occurence_time datetime NOT NULL,
          reporting_time datetime NOT NULL,
          description TEXT,
          image int,
          location_id int NOT NULL,
          FOREIGN KEY(reporting_user) REFERENCES USER(username),
          FOREIGN KEY(location_id) REFERENCES LOCATION(location_id)
      );
      CREATE TABLE AGENT (
          username VARCHAR(255),
          PRIMARY KEY(username),
          FOREIGN KEY(username) REFERENCES USER(username)
      );
      CREATE TABLE InvestigatedBy (
          username VARCHAR(255) NOT NULL,
          event_id INTEGER NOT NULL,
          notes multilinestring,
          PRIMARY KEY (username, event_id),
          FOREIGN KEY (username) REFERENCES AGENT(username),
          FOREIGN KEY (event_id) REFERENCES EVENT(event_id)
      );
      INSERT INTO USER VALUES ("NUFORC_IMPORT", "gjewogiwjgewoigjwiogjwioghjwiohjwoijhiowhjoiwj");
""")

import json
import re
from MySQLdb import _mysql
with open("data-no-empties-with-description.json.partial") as f:
    for line in f:
        event = json.loads(line)
        desc = ""
        for line in event['desc'].splitlines():
            if "" == line.strip():
                continue
            desc += line + '\n'

        if event['desc'] is None:
            continue

        for i in event:
            if event[i] is not None:
                event[i] = _mysql.escape_string(event[i])
            else:
                event[i] = "null"
        desc = _mysql.escape_string(desc)
        print((
              f"INSERT IGNORE INTO LOCATION (city, state, country) VALUES ({event['city']}, {event['state']}, {event['country']});\n"
              f"INSERT INTO EVENT (reporting_user, occurence_time, reporting_time, description, image, location_id) SELECT 'NUFORC_IMPORT', STR_TO_DATE({event['occurence']}, '%m/%d/%Y %k:%i'), STR_TO_DATE({event['reported']}, '%m/%d/%Y'), {desc}, NULL, "
              f"      location_id FROM LOCATION WHERE city={event['city']} AND state={event['state']} AND country={event['country']}"
              ";"
        ))
