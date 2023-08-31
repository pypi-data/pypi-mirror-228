from datetime import timedelta
from typing import Optional, Union, Sequence, List
from pydantic import BaseModel, field_validator, StrictBool, StrictInt, StrictStr


class LoadConfig(BaseModel):
    authjwt_token_location: set[StrictStr] | None = {"headers"}
    authjwt_secret_key: StrictStr | None = None
    authjwt_public_key: StrictStr | None = None
    authjwt_private_key: StrictStr | None = None
    authjwt_algorithm: StrictStr | None = "HS256"
    authjwt_decode_algorithms: list[StrictStr] | None = None
    authjwt_decode_leeway: StrictInt | timedelta | None = 0
    authjwt_encode_issuer: StrictStr | None = None
    authjwt_decode_issuer: StrictStr | None = None
    authjwt_decode_audience: StrictStr | set[StrictStr] | None = None
    authjwt_denylist_enabled: StrictBool | None = False
    authjwt_denylist_token_checks: set[StrictStr] | None = {"access", "refresh"}
    authjwt_header_name: StrictStr | None = "Authorization"
    authjwt_header_type: StrictStr | None = "Bearer"
    authjwt_access_token_expires: StrictBool | StrictInt | timedelta | None = timedelta(
        minutes=15
    )
    authjwt_refresh_token_expires: StrictBool | StrictInt | timedelta | None = (
        timedelta(days=30)
    )
    # option for create cookies
    authjwt_access_cookie_key: StrictStr | None = "access_token_cookie"
    authjwt_refresh_cookie_key: StrictStr | None = "refresh_token_cookie"
    authjwt_access_cookie_path: StrictStr | None = "/"
    authjwt_refresh_cookie_path: StrictStr | None = "/"
    authjwt_cookie_max_age: StrictInt | None = None
    authjwt_cookie_domain: StrictStr | None = None
    authjwt_cookie_secure: StrictBool | None = False
    authjwt_cookie_samesite: StrictStr | None = None
    # option for double submit csrf protection
    authjwt_cookie_csrf_protect: StrictBool | None = True
    authjwt_access_csrf_cookie_key: StrictStr | None = "csrf_access_token"
    authjwt_refresh_csrf_cookie_key: StrictStr | None = "csrf_refresh_token"
    authjwt_access_csrf_cookie_path: StrictStr | None = "/"
    authjwt_refresh_csrf_cookie_path: StrictStr | None = "/"
    authjwt_access_csrf_header_name: StrictStr | None = "X-CSRF-Token"
    authjwt_refresh_csrf_header_name: StrictStr | None = "X-CSRF-Token"
    authjwt_csrf_methods: set[StrictStr] | None = {"POST", "PUT", "PATCH", "DELETE"}

    @field_validator("authjwt_access_token_expires")
    def validate_access_token_expires(cls, v):
        if v is True:
            raise ValueError(
                "The 'authjwt_access_token_expires' only accept value False (bool)"
            )
        return v

    @field_validator("authjwt_refresh_token_expires")
    def validate_refresh_token_expires(cls, v):
        if v is True:
            raise ValueError(
                "The 'authjwt_refresh_token_expires' only accept value False (bool)"
            )
        return v

    @field_validator("authjwt_denylist_token_checks")
    def validate_denylist_token_checks(cls, v):
        for i in v:
            if i not in ["access", "refresh"]:
                raise ValueError(
                    "The 'authjwt_denylist_token_checks' must be between 'access' or 'refresh'"
                )
        return v

    @field_validator("authjwt_token_location")
    def validate_token_location(cls, v):
        for i in v:
            if i not in ["headers", "cookies"]:
                raise ValueError(
                    "The 'authjwt_token_location' must be between 'headers' or 'cookies'"
                )
        return v

    @field_validator("authjwt_cookie_samesite")
    def validate_cookie_samesite(cls, v):
        if v not in ["strict", "lax", "none"]:
            raise ValueError(
                "The 'authjwt_cookie_samesite' must be between 'strict', 'lax', 'none'"
            )
        return v

    @field_validator("authjwt_csrf_methods")
    def validate_csrf_methods(cls, v):
        response: set[StrictStr] = set()
        for i in v:
            if i.upper() not in {"GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"}:
                raise ValueError(
                    "The 'authjwt_csrf_methods' must be between http request methods"
                )
            response.add(i.upper())
        return response

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
