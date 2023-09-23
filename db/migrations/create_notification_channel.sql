CREATE TABLE notification_channel (
 id SERIAL PRIMARY KEY,
 client_correlator TEXT,
 application_tag TEXT,
 channel_type TEXT,
 channel_data BYTEA,
 expiry_date_time  TIMESTAMP WITHOUT TIME ZONE,
 callback_url TEXT,
 user_id INT,
 CONSTRAINT fk_userId FOREIGN KEY(user_id) REFERENCES app_user(id) 
)
