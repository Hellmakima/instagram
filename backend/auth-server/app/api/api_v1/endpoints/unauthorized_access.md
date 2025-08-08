| Action           | is_deleted=True | is_deleted=False | is_blocked=True | is_blocked=False | is_verified=True | is_verified=False |
|------------------|-----------------|------------------|-----------------|------------------|------------------|-------------------|
| register         | 1               | 0                | 0               | 0                | 0                | 1                 |
| login            | 0               | 1                | 1               | 0                | 1                | 0                 |
| forgot password  | 0               | 1                | 0               | 1                | 1                | 0                 |
| recover account  | 1               | 0                | NA              | NA               | NA               | NA                |
| logout           | SHould happen automatically| -     | -               | -                | -                | -                 |
