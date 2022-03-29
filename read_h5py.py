import h5py
data  = h5py.File('Sample.h5')
print(data.keys())

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os


credentials_dict = {
  "type": "service_account",
  "project_id": "bigdata-assignment-340502",
  "private_key_id": "766cad4a3cbfd9f36a7cae4b4b8ce1f874f6a4a3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcOZ+i5OT4eQXg\nVRL7nqdy70v8rwqjh5zz9mlgU3ynqz8ZT5H+qBdCbkxicBrS+3OE7R8NTFNTU+qz\nT0RtO1yzYlLG8c4e+MSp3E+FiLHG+fa7wDnmEDHmOzoJMkb0Kpw4QCtocg/GywZw\nyJZ6zrQaxyelESYtzlKX6HQ3YQIgVHHVAEEj/nT5P8UaaCNmEvyOalPmgrOTEiW7\n0b5C9SBdPrAxRgxZlWt4LHlXlKNykR9f1EAixHz8Ju4YUf9+aTsG35svrq2jHhSN\noDlRziWj9rkEaKB3Rmi+q8e5k2IKUwI/VfhTd6YJMcSZmGqmTGGltlmS6ImUzpJT\nA9rd9mQvAgMBAAECggEAR9SDvR3rkR/oSsN07Z1SAKsMnd56Gdyh1PEKbeDNR+MT\nMa5CcE1jSMexImpuVWKuyyyMdEnw47z7UIEKUJaMJfZsCXfVQ0Tg4IZ7aZKsaboe\nQB7yw5eErxOiWl2Lxxge3DoR7n9FphGSiDbk3imNlS5gP/bX/RjO1716KpX5m5FU\nWzc3dM5z7UY0dtxy8kgPTevEHE+OlHlVKLMShZb/o7ReWJHqB977psgSMbinApRR\ngf86Gye+5OTcoH0ikSjliNVdYzxFnk4C7QtpdamqrejFv8DFzuy3i3yYMwaEJMcX\n9+USy4+37/dJ6pAp4y4I7BSUL/l5OLrS8tv5YZtsAQKBgQD9AjM/r8RrLIZnxORm\nTAFcxOAkv6Mx18sNwv30bmCAQAmMgekQUpFeRjZLR7MWiVfjP9GPT0hgMAcnpoX3\nzZ8rAKPf6fEfDyxhng85G5S8MlJCpwddagmrZrUik0BrCy+Cb7S1grb0sdFruyKf\n3hzRudzKPSJbSqpV56aaxvN/cwKBgQDe1DH0qc8C8+JZiW6LGuUmbBb/iL7NLicr\nfhgPqrGwRflUlX3pUsnCAymeCmLJhN9RUaFlZXmASWWBZf3QVXFDjG0YGoLQ8TfQ\n4yGX9ZyqT69XOILrfIlPENL10y2DghHo1EOfvfG0aTS7Vnutzswo5uXR9pGRVD+w\nYBJfi0PhVQKBgFDb8CcNdJfP/hCR83DiH5lXbk8wU+atEb8PL3x7/ileze5y4lqO\nGNlpVRbQDmNId6cwEThc3UOoddDtPmmI9LKYnMcGDEKh5cw46KKWtv1Ck9mragYn\nynlV9NPc/bx4MbHdI4LTCMfBQK3Oe+1d3hYE8ZRM33sPrMqRo0RaCx4TAoGATsFa\nwql9tAJ0vsaXHm0sDm9nlXtETIqCZ5nScT8YPEAPBnkrnlqXWo35mJT9I1JmB3y9\neXPrBI9sY9ajZY29UW2BZWKBV83Zt2d/iRDTBVLSmxYrF4XVle9RUHcKAA/puovD\nNuNQWT5R1+CSJ/UOLWqmUZY/DsljFThvZft3y10CgYEAmgBofrdmJQ5PBGWuYXuH\n2gC97aV9ABinXObM0dXh2hxqInyPOHE2Oeh/Tf6EJUY0ysMrWF9Pe00JrHjn0a77\nhKUjXbREatbIQb7Z9YOej/BJb+voUZp0lw4SYBbPSyaDxG9Dn8UsjnY5xucdSGa2\nunsNYP3IYuEpQdxu2BZ/rNw=\n-----END PRIVATE KEY-----\n",
  "client_email": "accessvildata@bigdata-assignment-340502.iam.gserviceaccount.com",
  "client_id": "113255129406006569368",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/accessvildata%40bigdata-assignment-340502.iam.gserviceaccount.com"
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
client = storage.Client(credentials=credentials, project='bigdata-assignment-340502')
print(client)
bucket = client.get_bucket('nowcast_api_data')
blob = bucket.blob('myfile1.h5')
blob.upload_from_filename('Sample.h5')
