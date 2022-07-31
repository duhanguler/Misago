# Querying database

## Table of contents

- [Querying models](#querying-models)
- [Select](#select)
- [Insert](#insert)
- [Update](#update)
- [Delete](#delete)
- [Lookups](#lookups)
- [Transactions](#transactions)
- [Executing raw queries](#executing-raw-queries)


## Querying models

Every model extending `misago.database.models.Model` and registered with `misago.database.models.register_model` has `query` attribute containing instance of query builder class that can be used to construct and execute queries against it's table:

```python
from misago.users.models import User


async def get_user_by_id(id: int):
    await User.query.one(id=id)
```

In addition to `query` attribute, models also have `table` attribute that can be used to construct SQL Alchemy expressions:

```python
from misago.database import database
from misago.users.models import User, UserGroup


async def run_complex_query():
    users_table = User.table
    groups_table = UserGroup.table

    query = User.table.select([users_table.c.id, users_table.c.name]).where(
        users_table.c.group_id=groups_table.select().where(groups_table.c.is_admin=True)
    )
    await database.fetch_all(query=query)
```


## Select

### Selecting single object

To retrieve single object matching query, use `one()` method:

```python
from misago.users.models import User

user = await User.query.one()
```

If query returns more than one result it will raise `misago.database.models.MultipleObjectsReturned` exception. If no results are found, `misago.database.models.DoesNotExist` will be raised.

`one()` accepts kwargs as filters:

```python
from misago.users.models import User

# Select user with id 100
user = await User.query.one(id=100)

# Select user with id 500 but only if they are admin
admin = await User.query.one(id=500, is_admin=True)
```

`one()` can also be used on queries that were already filtered with `filter` and `exclude`.


### Selecting some values of single object

To retrieve some values of single object matching query, use `one()` with names of columns passed to it:

```python
from misago.users.models import User

user_id, user_name, user_email = await User.query.one("id", "name", "email")
```

By default the result is returned as a tuple, but you can request named tuple instead by using `named=True` option:

```python
from misago.users.models import User

user = await User.query.one("id", "name", named=True)  # <Result(id=1, name="User")>
```

### Selecting single value

To retrieve single value of single object matching query, use `one_flat()` with name of column:

```python
from misago.users.models import User

user_name = await User.query.one_flat("name")
```


### Selecting list of all results

To retrieve all results matching query, use `all()` method:

```python
from misago.users.models import User

all_users = await User.query.all()
```


### Selecting list of all results limited to selected columns

To retrieve only some of columns for all results matching query, pass those columns names to `all()`:

```python
from misago.users.models import User

all_users = await User.query.all("id", "name", "email")
for id, name, email in all_users:
    ...
```

By default results are returned as a tuple, but you can request named tuple instead by using `named=True` option:

```python
from misago.users.models import User

all_users = await User.query.all("id", "name", "email", named=True)
for user in all_users:
    await do_something(user.id, user.name, user.email)
```


### Selecting flat list of values of single column

To retrieve values from single column as flat list use `all_flat()`:

```python
from misago.users.models import User

users_ids = await User.query.all_flat("id")  # [1, 3, 4, 5...]
```


### Making results distinct

Combine `all()` with `distinct()` to make results distinct:

```python
from misago.threads.models import Thread

categories_with_threads = await Thread.query.distinct().all_flat("category_id")
```


### Ordering results

To make select query ordered, call `order_by` on query with one or more column names:

```python
from misago.users.models import User

users_sorted_by_name = await User.query.order_by("name").all()
```

To reverse the order, prefix column name with minus:

```python
from misago.users.models import User

users_sorted_by_name = await User.query.order_by("-name").all()
```

To order by multiple columns, specify them one after another:

```python
from misago.threads.models import Thread

threads_sorted_by_title = await Thread.query.order_by("title", "id").all()
```


### Limiting results

To limit number of query results, call `limit` with `int` as only argument:

```python
from misago.users.models import User

five_oldest_users = await User.query.order_by("id").limit(5).all()
```

To remove limit from query, call `limit` without arguments:

```python
from misago.users.models import User

all_oldest_users = await User.query.order_by("id").limit(5).limit().all()
```

This is useful in utilities transforming queries.


### Offset results

To offset results (eg. for offset pagination), call `offset` with `int` as only argument:

```python
from misago.users.models import User

next_oldest_users = await User.query.order_by("id").offset(5).all()
```

To remove offset from query, call `offset` without arguments:

```python
from misago.users.models import User

all_oldest_users = await User.query.order_by("id").offset(5).offset().all()
```

This is useful in utilities transforming queries.


## Insert

To insert new data into database, use `insert` on unfiltered query:

```python
from misago.threads.models import Thread

new_thread = await Thread.query.insert(title="Thread title!", slug="thread-title")
```

`insert()` returns new model instance with attributes having values from `insert` arguments. This instance will also have its `id` attribute set to value returned by the database.

To bulk insert values pass list of dicts to `insert_bulk`:

```python
from misago.threads.models import Thread

Thread.query.insert_bulk(
    [
        {"title": "Thread A", "slug": "thread-a"},
        {"title": "Thread B", "slug": "thread-b"},
        {"title": "Thread C", "slug": "thread-c"},
    ]
)
```

`insert_bulk()` has no return value.


## Update

To update all objects run `update_all` on unfiltered query:

```python
from misago.threads.models import Thread

await Thread.query.update_all(is_closed=False)
```

To update only some objects in database run `update`:

```python
from misago.threads.models import Thread

await Thread.query.filter(id=2137).update(is_closed=False)
```

Both `update_all` and `update` take values to save to database as kwargs. Those values can be basic Python values (like `int` or `str`) or SQL Alchemy expressions:

```python
from misago.threads.models import Thread

await Thread.query.filter(id=2137).update(replies=Thread.table.c.replies + 1)
```


## Delete

To delete all objects run `delete_all` on unfiltered query:

```python
from misago.threads.models import Thread

await Thread.query.delete_all()
```

To delete only some objects in database run `delete`:

```python
from misago.threads.models import Thread

await Thread.query.filter(id=2137).delete()
```


## Lookups


## Transactions

To run database queries within transaction use `database.transaction` asynchronous context manager:

```python
from misago.database import database

async with database.transaction():
    post = await Post.create(thread_id=thread.id, content="Hello world!")
    await thread.update(last_post_id=post.id)
```

You can also use it as decorator:

```python
from misago.database import database


@database.transaction()
async def create_post(thread: Thread, content: str):
    post = await Post.create(thread_id=thread.id, content=content)
    await thread.update(last_post_id=post.id)
    return post
```

If you need manual control on commit or rollback, use `transaction()` return value:

```python
transaction = await database.transaction()
try:
    ...
except:
    await transaction.rollback()
else:
    await transaction.commit()
```

For more examples see ["databases" documentation](https://www.encode.io/databases/connections_and_transactions/#transactions).


## Executing raw queries

To run raw query against the database, use `database` instance from `misago.database`:

```python
from misago.database import database

# Run query
await database.execute(
    query="UPDATE misago_settings SET value = 'Test Forum ' WHERE name = 'forum_name'"
)

# Run select
cache_versions = await database.fetch_all(query="SELECT * FROM misago_cache_versions")
```

See "databases" library [documentation](https://www.encode.io/databases/database_queries/) for more examples.