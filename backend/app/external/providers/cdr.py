from backend.app.external.base_client import ExternalProviderAdapter
from backend.app.external.secure_client import secure_external_client

class CdrProvider(ExternalProviderAdapter):
    @property
    def provider_name(self) -> str:
        return "DOT_OFFICIAL_CDR_GATEWAY"

    def request_data(self, resource_id: str, case_id: str, user_badge: str, user_id: str):
        return secure_external_client.fetch_verified_external_data(
            resource_id=resource_id,
            provider_type="CDR",
            case_id=case_id,
            user_badge=user_badge,
            user_id=user_id
        )

cdr_provider = CdrProvider()
