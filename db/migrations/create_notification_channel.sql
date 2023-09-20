CREATE TABLE notification_channel (
 id SERIAL PRIMARY KEY,
 client_correlator TEXT,
 application_tag TEXT,
 channel_type TEXT,
 channel_data BYTEA,
 channel_life_time INT,
 callback_url TEXT,
 user_id INT,
 CONSTRAINT fk_userId FOREIGN KEY(user_id) REFERENCES app_user(id) 
)
