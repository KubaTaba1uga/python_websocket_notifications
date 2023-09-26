CREATE TABLE subscription (
 id SERIAL PRIMARY KEY,
 expiry_date_time  TIMESTAMP WITHOUT TIME ZONE,
 callback_reference BYTEA,
 filter TEXT,  
 client_correlator TEXT,
 index INT,
 restart_token TEXT,
 max_events INT,
 object_attribute_names TEXT,
 inline_imdn BOOLEAN,
 user_id INT,
 CONSTRAINT fk_userId FOREIGN KEY(user_id) REFERENCES app_user(id) 

)
