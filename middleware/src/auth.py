from fastapi import Request, HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

# Define the security schemes
bearer_scheme = HTTPBearer(auto_error=False)
header_scheme_anthropic = APIKeyHeader(name="x-api-key", auto_error=False)
header_scheme_azure = APIKeyHeader(name="api-key", auto_error=False)

async def get_api_key(
    request: Request,
    bearer: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
    x_api_key: Optional[str] = Security(header_scheme_anthropic),
    api_key: Optional[str] = Security(header_scheme_azure),
) -> str:
    """
    Protocol 2.2: Authentication Architectures.
    Supports Bearer Token (OpenAI), x-api-key (Anthropic), and api-key (Azure).
    """
    token = None
    
    # 1. Check Bearer Token
    if bearer:
        token = bearer.credentials
    
    # 2. Check x-api-key (Anthropic)
    elif x_api_key:
        token = x_api_key
        
    # 3. Check api-key (Azure)
    elif api_key:
        token = api_key
        
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication. Provide 'Authorization: Bearer <key>', 'x-api-key', or 'api-key'."
        )
    
    # TODO: Validate against a database or hash.
    # For now, we enforce that a key is present.
    return token
