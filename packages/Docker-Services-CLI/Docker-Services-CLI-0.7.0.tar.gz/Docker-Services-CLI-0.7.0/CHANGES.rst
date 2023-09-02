..
    Copyright (C) 2020-2023 CERN.

    Docker-Services-CLI is free software; you can redistribute it and/or modify
    it under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 0.7.0 (released 2023-09-02)

- Upgrades Postgres and MySQL versions

Version 0.6.1 (released 2023-03-20)

- Adds back support for Python 3.6

Version 0.6.0 (released 2022-10-03)

- Adds OpenSearch v2

Version 0.5.0 (released 2022-08-30)

- Adds OpenSearch v1
- Removes Elasticsearch 6

Version 0.4.2 (released 2022-08-17)

- Upgrades Redis and MQ to latest version
- Supports min version of Python to 3.7
- Formats code with Black

Version 0.4.1 (released 2022-02-23)

- Removes upper bound on Click which causes projects where docker-services-cli
  is installed to limit Celery to v5.1.x because Celery v5.2 requires Click 8+.

Version 0.4.0 (released 2022-02-15)

- Changes default version of Postgres to v12.
- Adds Postgres v14 and upgrades other versions.

Version 0.3.1 (released 2021-08-04)

- Fixes an issue where created volumes were not removed again.
