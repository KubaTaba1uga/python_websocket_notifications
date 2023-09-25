CREATE TABLE subscription (
 id SERIAL PRIMARY KEY,
 expiry_date_time  TIMESTAMP WITHOUT TIME ZONE,
 callback_reference BYTEA,
 filter TEXT,  
 client_correlator TEXT,
 index INT,
 restart_token TEXT,
 max_events INT,
 objectAttributeNames TEXT,
 inlineImdn BOOLEAN
)
