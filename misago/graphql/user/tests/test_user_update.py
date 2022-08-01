import pytest

ADMIN_USER_UPDATE_MUTATION = """
    mutation UserUpdate($id: ID!, $input: UserUpdateInput!) {
        userUpdate(user: $id, input: $input) {
            updated
            user {
                id
                name
                slug
                fullName
                email
                isActive
                isAdmin
                isModerator
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_id_is_invalid(query_admin_api):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": "invalid",
            "input": {},
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": None,
        "errors": [
            {
                "location": "user",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_doesnt_exist(
    query_admin_api, admin
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(admin.id + 1),
            "input": {},
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": None,
        "errors": [
            {
                "location": "user",
                "type": "user_error.not_found",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_user_name(query_admin_api, user):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "UpdatedUser",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "UpdatedUser",
            "slug": "updateduser",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.name == "UpdatedUser"
    assert user_from_db.slug == "updateduser"


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_name_is_invalid(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "!!!!",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "name",
                "type": "value_error.username",
            },
        ],
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.name == user.name
    assert user_from_db.slug == user.slug


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_name_is_not_available(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "Admin",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "name",
                "type": "value_error.username.not_available",
            },
        ],
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.name == user.name
    assert user_from_db.slug == user.slug


@pytest.mark.asyncio
async def test_admin_user_update_mutation_skips_update_if_new_name_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "User",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.name == user.name
    assert user_from_db.slug == user.slug


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_user_email(query_admin_api, user):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": "new@email.com",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "new@email.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.email == "new@email.com"


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_email_is_invalid(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": "invalid",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "email",
                "type": "value_error.email",
            },
        ],
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_email_is_not_available(
    query_admin_api, admin, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": admin.email,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "email",
                "type": "value_error.email.not_available",
            },
        ],
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_admin_user_update_mutation_skips_update_if_new_email_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": user.email,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_user_password(query_admin_api, user):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "password": "n3wp5ssword  ",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert await user_from_db.check_password("n3wp5ssword  ")


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_password_is_invalid(
    query_admin_api, user, user_password
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "password": "a",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "password",
                "type": "value_error.any_str.min_length",
            },
        ],
    }

    user_from_db = await user.fetch_from_db()
    assert await user_from_db.check_password(user_password)


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_user_full_name(query_admin_api, user):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "Bob Bobertson",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": "Bob Bobertson",
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.full_name == "Bob Bobertson"


@pytest.mark.asyncio
async def test_admin_user_update_mutation_clears_user_full_name(query_admin_api, user):
    user = await user.update(full_name="Bob Bobertson")

    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.full_name is None


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_full_name_is_too_long(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "Bob Bobertson" * 20,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "fullName",
                "type": "value_error.any_str.max_length",
            },
        ],
    }

    user_from_db = await user.fetch_from_db()
    assert not user_from_db.full_name


@pytest.mark.asyncio
async def test_admin_user_update_mutation_skips_update_if_new_full_name_is_same(
    query_admin_api, user
):
    user = await user.update(full_name="Bob Bobertson")

    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "Bob Bobertson",
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": "Bob Bobertson",
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.full_name == "Bob Bobertson"


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_admin_status_to_true(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isAdmin": True,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": True,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_admin_status_to_false(
    query_admin_api, user
):
    user = await user.update(is_admin=True)

    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isAdmin": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert not user_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_update_mutation_skips_update_if_admin_status_is_same(
    query_admin_api, admin
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(admin.id),
            "input": {
                "isAdmin": True,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(admin.id),
            "name": "Admin",
            "slug": "admin",
            "fullName": None,
            "email": "admin@example.com",
            "isActive": True,
            "isAdmin": True,
            "isModerator": False,
        },
        "errors": None,
    }

    admin_from_db = await admin.fetch_from_db()
    assert admin_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_user_update_mutation_skips_update_if_admin_status_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isAdmin": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert not user_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_update_mutation_fails_if_admin_tries_to_remove_own_status(
    query_admin_api, admin
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(admin.id),
            "input": {
                "isAdmin": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(admin.id),
            "name": "Admin",
            "slug": "admin",
            "fullName": None,
            "email": "admin@example.com",
            "isActive": True,
            "isAdmin": True,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "isAdmin",
                "type": "user_error.remove_own_admin",
            },
        ],
    }

    admin_from_db = await admin.fetch_from_db()
    assert admin_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_moderator_status_to_true(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isModerator": True,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": True,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.is_moderator


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_moderator_status_to_false(
    query_admin_api, moderator
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(moderator.id),
            "input": {
                "isModerator": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(moderator.id),
            "name": "Moderator",
            "slug": "moderator",
            "fullName": None,
            "email": "moderator@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    moderator_from_db = await moderator.fetch_from_db()
    assert not moderator_from_db.is_moderator


@pytest.mark.asyncio
async def test_moderator_update_mutation_skips_update_if_moderator_status_is_same(
    query_admin_api, moderator
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(moderator.id),
            "input": {
                "isModerator": True,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(moderator.id),
            "name": "Moderator",
            "slug": "moderator",
            "fullName": None,
            "email": "moderator@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": True,
        },
        "errors": None,
    }

    moderator_from_db = await moderator.fetch_from_db()
    assert moderator_from_db.is_moderator


@pytest.mark.asyncio
async def test_admin_user_update_mutation_skips_update_if_moderator_status_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isModerator": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert not user_from_db.is_moderator


@pytest.mark.asyncio
async def test_inactive_user_update_mutation_updates_active_status_to_true(
    query_admin_api, inactive_user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(inactive_user.id),
            "input": {
                "isActive": True,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(inactive_user.id),
            "name": "InactiveUser",
            "slug": "inactiveuser",
            "fullName": None,
            "email": "inactive@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    inactive_user_from_db = await inactive_user.fetch_from_db()
    assert inactive_user_from_db.is_active


@pytest.mark.asyncio
async def test_admin_user_update_mutation_updates_active_status_to_false(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isActive": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": True,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": False,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert not user_from_db.is_active


@pytest.mark.asyncio
async def test_admin_user_update_mutation_fails_if_user_deactivates_themselves(
    query_admin_api, admin
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(admin.id),
            "input": {
                "isActive": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(admin.id),
            "name": "Admin",
            "slug": "admin",
            "fullName": None,
            "email": "admin@example.com",
            "isActive": True,
            "isAdmin": True,
            "isModerator": False,
        },
        "errors": [
            {
                "location": "isActive",
                "type": "user_error.deactivate_self",
            },
        ],
    }

    admin_from_db = await admin.fetch_from_db()
    assert admin_from_db.is_active


@pytest.mark.asyncio
async def test_inactive_user_update_mutation_skips_update_if_active_status_is_same(
    query_admin_api, inactive_user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(inactive_user.id),
            "input": {
                "isActive": False,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(inactive_user.id),
            "name": "InactiveUser",
            "slug": "inactiveuser",
            "fullName": None,
            "email": "inactive@example.com",
            "isActive": False,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isActive"]

    inactive_user_from_db = await inactive_user.fetch_from_db()
    assert not inactive_user_from_db.is_active


@pytest.mark.asyncio
async def test_admin_user_update_mutation_skips_update_if_active_status_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isActive": True,
            },
        },
    )

    assert result["data"]["userUpdate"] == {
        "updated": False,
        "user": {
            "id": str(user.id),
            "name": "User",
            "slug": "user",
            "fullName": None,
            "email": "user@example.com",
            "isActive": True,
            "isAdmin": False,
            "isModerator": False,
        },
        "errors": None,
    }

    user_from_db = await user.fetch_from_db()
    assert user_from_db.is_active


@pytest.mark.asyncio
async def test_admin_user_update_mutation_requires_admin_auth(query_admin_api, user):
    result = await query_admin_api(
        ADMIN_USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isActive": True,
            },
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
