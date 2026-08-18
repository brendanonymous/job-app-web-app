import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from src.auth import get_user_from_token


class GetUserFromTokenTests(unittest.TestCase):
    def test_get_user_from_token_returns_db_user_for_valid_cognito_claims(self):
        session = MagicMock()
        session.execute.return_value.scalar_one_or_none.return_value = {"id": 42}

        token = "fake-token"

        with patch("src.auth.jwt.PyJWKClient") as jwk_client, patch("src.auth.jwt.decode") as decode:
            signing_key = MagicMock()
            signing_key.key = "public-key"
            jwk_client.return_value.get_signing_key_from_jwt.return_value = signing_key
            decode.return_value = {"sub": "cognito-user-123"}

            user = get_user_from_token(session, token)

            self.assertEqual(user, {"id": 42})
            session.execute.assert_called_once()

    def test_get_user_from_token_raises_for_missing_user_claims(self):
        session = MagicMock()

        token = "fake-token"

        with patch("src.auth.jwt.PyJWKClient") as jwk_client, patch("src.auth.jwt.decode") as decode:
            signing_key = MagicMock()
            signing_key.key = "public-key"
            jwk_client.return_value.get_signing_key_from_jwt.return_value = signing_key
            decode.return_value = {}

            with self.assertRaises(HTTPException):
                get_user_from_token(session, token)


if __name__ == "__main__":
    unittest.main()
