import pytest

from ....categories.get import get_all_categories
from ....permissions.cache import MODERATORS_CACHE, PERMISSIONS_CACHE
from ....testing import assert_invalidates_cache
from ....threads.models import Post, Thread

CATEGORY_DELETE_MUTATION = """
    mutation CategoryDelete(
        $category: ID!, $moveChildrenTo: ID, $moveThreadsTo: ID
    ) {
        categoryDelete(
            category: $category,
            moveThreadsTo: $moveThreadsTo,
            moveChildrenTo: $moveChildrenTo
        ) {
            deleted
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_deletes_category_with_its_children(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids
    assert child_category.id not in categories_ids

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Sibling category
        (0, 5, 6),  # Closed category
    ]


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_deletes_category_but_moves_its_children(
    query_admin_api, category, child_category, sibling_category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveChildrenTo": str(sibling_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids
    assert child_category.id in categories_ids

    parent_from_db = await sibling_category.fetch_from_db()
    assert parent_from_db.depth == 0
    assert parent_from_db.left == 3
    assert parent_from_db.right == 6

    child_from_db = await child_category.fetch_from_db()
    assert child_from_db.depth == 1
    assert child_from_db.left == 4
    assert child_from_db.right == 5

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 6),  # Sibling category
        (1, 4, 5),  # - Child category
        (0, 7, 8),  # Closed category
    ]


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_deletes_category_and_its_threads(
    query_admin_api, category, thread, post
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.fetch_from_db()

    with pytest.raises(Post.DoesNotExist):
        await post.fetch_from_db()

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Sibling category
        (0, 5, 6),  # Closed category
    ]


@pytest.mark.asyncio
async def test_admin_category_delete_but_move_children_mutation_keeps_children_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveChildrenTo": str(sibling_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == child_category.id

    post_from_db = await post.fetch_from_db()
    assert post_from_db.category_id == child_category.id


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_deletes_children_threads(
    query_admin_api, category, child_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.fetch_from_db()

    with pytest.raises(Post.DoesNotExist):
        await post.fetch_from_db()


@pytest.mark.asyncio
async def test_admin_category_delete_but_move_threads_mutation_moves_children_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveThreadsTo": str(sibling_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == sibling_category.id

    post_from_db = await post.fetch_from_db()
    assert post_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_admin_category_delete_but_move_all_mutation_moves_category_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveChildrenTo": str(sibling_category.id),
            "moveThreadsTo": str(sibling_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == sibling_category.id

    post_from_db = await post.fetch_from_db()
    assert post_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_admin_category_delete_but_move_all_mutation_keeps_children_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveChildrenTo": str(sibling_category.id),
            "moveThreadsTo": str(sibling_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": True,
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == child_category.id

    post_from_db = await post.fetch_from_db()
    assert post_from_db.category_id == child_category.id


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_category_id_is_invalid(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": "invalid",
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "category",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_move_children_id_is_invalid(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveChildrenTo": "invalid",
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "moveChildrenTo",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_move_threads_id_is_invalid(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveThreadsTo": "invalid",
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "moveThreadsTo",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_threads_are_moved_to_deleted_category(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveThreadsTo": str(category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "moveThreadsTo",
                "type": "category_error.invalid",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_threads_are_moved_to_deleted_child(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveThreadsTo": str(child_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "moveThreadsTo",
                "type": "category_error.invalid",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_children_are_moved_to_deleted_category(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
            "moveChildrenTo": str(category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "moveChildrenTo",
                "type": "category_error.invalid",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_fails_if_children_are_moved_to_child_category(
    query_admin_api, sibling_category, child_category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(sibling_category.id),
            "moveChildrenTo": str(child_category.id),
        },
    )

    assert result["data"]["categoryDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "moveChildrenTo",
                "type": "category_error.invalid",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_invalidates_permission_caches(
    query_admin_api, category
):
    async with assert_invalidates_cache(PERMISSIONS_CACHE):
        async with assert_invalidates_cache(MODERATORS_CACHE):
            result = await query_admin_api(
                CATEGORY_DELETE_MUTATION,
                {
                    "category": str(category.id),
                },
            )

            assert result["data"]["categoryDelete"] == {
                "deleted": True,
                "errors": None,
            }


@pytest.mark.asyncio
async def test_admin_category_delete_mutation_requires_admin_auth(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION,
        {
            "category": str(category.id),
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
