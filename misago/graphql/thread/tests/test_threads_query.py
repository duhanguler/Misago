import pytest

THREADS_QUERY = """
    query GetThreads($category: ID, $user: ID) {
        threads(category: $category, user: $user, first: 10) {
            edges {
                node {
                    id
                }
                cursor
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_threads_query_resolves_to_empty_list(query_public_api, db):
    result = await query_public_api(THREADS_QUERY)
    assert result["data"]["threads"] == {
        "edges": [],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_threads_list(query_public_api, thread):
    result = await query_public_api(THREADS_QUERY)
    assert result["data"]["threads"] == {
        "edges": [
            {
                "node": {
                    "id": str(thread.id),
                },
                "cursor": str(thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_empty_list_for_negative_cursor(
    query_public_api, thread
):
    result = await query_public_api(THREADS_QUERY, {"cursor": "-1"})
    assert result["data"]["threads"] == {
        "edges": [
            {
                "node": {
                    "id": str(thread.id),
                },
                "cursor": str(thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_category_threads_list(
    query_public_api, category, thread, closed_category_thread
):
    result = await query_public_api(THREADS_QUERY, {"category": str(category.id)})
    assert result["data"]["threads"] == {
        "edges": [
            {
                "node": {
                    "id": str(thread.id),
                },
                "cursor": str(thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_none_for_nonexistant_category(
    query_public_api, category, thread
):
    result = await query_public_api(THREADS_QUERY, {"category": str(category.id * 100)})
    assert result["data"]["threads"] == {
        "edges": [],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_none_for_invalid_category(
    query_public_api, category, thread
):
    result = await query_public_api(THREADS_QUERY, {"category": "invalid"})
    assert result["data"]["threads"] is None


@pytest.mark.asyncio
async def test_threads_query_resolves_to_user_threads_list(
    query_public_api, thread, user_thread, user
):
    result = await query_public_api(THREADS_QUERY, {"user": str(user.id)})
    assert result["data"]["threads"] == {
        "edges": [
            {
                "node": {
                    "id": str(user_thread.id),
                },
                "cursor": str(user_thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_empty_list_for_nonexistant_user(
    query_public_api, thread, user_thread, user
):
    result = await query_public_api(THREADS_QUERY, {"user": str(user.id * 100)})
    assert result["data"]["threads"] == {
        "edges": [],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_none_list_for_invalid_user(
    query_public_api, thread, user_thread, user
):
    result = await query_public_api(THREADS_QUERY, {"user": "invalid"})
    assert result["data"]["threads"] is None
