CREATE TABLE notification_channel (
 id SERIAL PRIMARY KEY,
 clientCorrelator TEXT,
 applicationTag TEXT,
 channelType TEXT,
 channelData JSON,
 expiryDateTime TIMESTAMP WITHOUT TIME ZONE,
 callbackURL TEXT,
 resourceURL TEXT,
)

