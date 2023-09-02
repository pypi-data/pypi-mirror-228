from pyappi.encoding.url import decode_url
from pyappi.api_base import get_document_type
import json
from fastapi import Response
from functools import wraps


def verify_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs["request"]
        _session = get_user_session(request)
        if not _session:
            return Response(status_code=403)
    
        session, user = _session
        request.state.session = session
        request.state.user = user

        return await func(*args, **kwargs)

    return wrapper

def parse_session(blob):
    return json.loads(decode_url(blob).decode())

def validate_user_session(request):
    raw_session = request.query_params._list[0][0]
    session = parse_session(raw_session)
    
    with get_document_type()(f'user.{session["user"]}', session["user"], read_only=True) as doc:
        return session["challenge"] == doc.auth.challenge
    
    return False

def get_user_session(request):
    raw_session = request.query_params._list[0][0]
    session = parse_session(raw_session)
    
    try:
        with get_document_type()(f'user.{session["user"]}', session["user"], read_only=True) as doc:
            session["id"] = doc._server_id.serial
            return (session,doc) if session["challenge"] == doc.auth.challenge else None
    except Exception as _e:
        pass
    
    return None