..
    Copyright (C) 2020-2022 CERN.
    Copyright (C) 2020 Northwestern University.

    Invenio-Drafts-Resources is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

Version 1.0.5 (2023-08-30)

- backport new version bug fix (see invenio-app-rdm#2197) for v11 STS
- include ES/OS garbage collection timedelta
- explicitly import invenio-i18n with v11 compatible versions since flask-babelex directly used

Version 1.0.4 (2023-02-22)

- service: allow to ignore field-level permission checks in validate_draft
- files: publishing files pending download from Fetch

Version 1.0.3 (2022-12-02)

- Fix rebuild index memory usage

Version 1.0.2 (2022-11-25)

- Add i18n translations.

Version 1.0.1 (2022-11-15)

- Use bulk indexing for service `rebuild_index` method.

Version 1.0.0 (2022-11-04)

- Bump invenio-records-resources version

Version 0.2.2 (2020-08-19)

- Fix support for Elasticsearch 6 and 7

Version 0.2.1 (2020-08-18)

- Initial public release.
