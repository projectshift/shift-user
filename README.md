# shift-user
Extensible user registration and [authentication](https://flask-login.readthedocs.io/en/latest/) including [OAuth](https://pythonhosted.org/Flask-OAuth/) support for facebook, google and vk, instagram and linkedin.
Provides support RBAC and access control with [Principal](http://pythonhosted.org/Flask-Principal/)


**Important note:** although the codebase is pretty mature it is currently in
the process of being migrated to a separate project (this one). Use with caution.


# Installation

### get the package

You can install the package wrom PyPI:

```
pip install shiftuser
```

### enabling users feature
To enable the feature run the code below at bootstrap time passing it an instance
of you flask application

```python
from shiftuser.feature import users_feature
users_feature(app)
```

There is a lot to users feature - it provides facilities to create and manage user profiles, authenticate with username, passwords and oauth, manage user profiles, reset passwords, confirm and activate accounts and a handy set of console commands for your cli to perform admin tasks.

### users cli
To connect user commands to your project CLI edit cli file in your project root and mount the commands:

```python
from shiftuser.cli import users_cli
cli.add_command(users_cli, name='user')
```

### migrations
If you are using Alembic migrations, make sure to import user models in `migrations/env.py`:

```python
# using boiler users?
from shiftuser import models
```


# Configuration