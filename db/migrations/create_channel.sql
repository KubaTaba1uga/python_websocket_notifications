CREATE TABLE notification_channel (
 id SERIAL PRIMARY KEY,
 clientCorrelator TEXT,
 applicationTag TEXT,
 channelType TEXT,
 channelData JSON,
 channelLifeTime INT,
 callbackURL TEXT,
 resourceURL TEXT,
)

