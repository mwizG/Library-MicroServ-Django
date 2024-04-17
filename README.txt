(0.000) SELECT "users_customuser"."id", "users_customuser"."password", "users_customuser"."last_login", "users_customuser"."is_superuser", "users_customuser"."is_admin", "users_customuser"."email", "users_customuser"."username", "users_customuser"."membership_status", "users_customuser"."is_active", "users_customuser"."is_staff", "users_customuser"."date_joined" FROM "users_customuser" WHERE "users_customuser"."username" = 'mwiza' LIMIT 21; args=('mwiza',); alias=default
here are the token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMjQ5MTAyMSwiaWF0IjoxNzEyNDA0NjIxLCJqdGkiOiI5ZjQyZWU5YWJkODk0Y2E1OWI4MjQ3YzU2NjBiOGMyMyIsInVzZXJfaWQiOjF9.7rTxHi-fyrrRTk6T6aP2PGrHe8LGpJdzYwG9mE5_Jbk
HERE ARE THE response <Response [401]>
HEREs the header {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNDA0OTIxLCJpYXQiOjE3MTI0MDQ2MjEsImp0aSI6IjRhZDE1OWViMDkwMTQ5MmRiZjFhMTNmYTQ4ZDUwNTY2IiwidXNlcl9pZCI6MX0.XPVDt6JfBmL8YlXR-Id3Rfs5dyn2aQL5pPf7PnEsX3Y', 'Content-Type': 'application/json'}
Internal Server Error: /users/login/
[06/Apr/2024 11:57:01] "POST /users/login/ HTTP/1.1" 500 54
