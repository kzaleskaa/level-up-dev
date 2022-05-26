from fastapi import Depends, APIRouter, Query, Response, Header, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from _datetime import datetime
from datetime import date

router = APIRouter()
security = HTTPBasic()

router.used_paths = []


# 3.1
@router.get("/start", response_class=HTMLResponse)
def static_start_index():
    html_content = """<h1>The unix epoch started at 1970-01-01</h1>"""
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


# 3.2
@router.post("/check")
def check_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    today_date = date.today()

    try:
        birth_date = datetime.strptime(password, "%Y-%m-%d").date()
    except ValueError:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    age = today_date.year - birth_date.year - ((today_date.month, today_date.day) < (birth_date.month, birth_date.day))

    if age < 16:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    return HTMLResponse(content=f"<h1>Welcome {username}! You are {age}</h1>")


# 3.3
@router.get("/info")
def format_response(response: Response, format: str = Query(None), user_agent: str | None = Header(default=None)):
    if format == "json":
        return JSONResponse(
            content={"user_agent": user_agent},
            status_code=status.HTTP_200_OK
        )
    elif format == "html":
        html_content = f"""<input type="text" id=user-agent name=agent value="{user_agent}">"""
        return HTMLResponse(
            content=html_content,
            status_code=status.HTTP_200_OK
        )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


# 3.4
@router.put("/save/{string_path}")
def save_new_path(response: Response, string_path: str):
    if string_path not in router.used_paths:
        router.used_paths.append(string_path)
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST


@router.get("/save/{string_path}")
def redirect_new_path(response: Response, string_path: str):
    if string_path not in router.used_paths:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return RedirectResponse(
            url="/info",
            headers={"Location": "/info"},
            status_code=status.HTTP_301_MOVED_PERMANENTLY
        )


@router.delete("/save/{string_path}", status_code=status.HTTP_200_OK)
def delete_path(string_path: str):
    router.used_paths.remove(string_path)


@router.api_route("/save/{string_path}", methods=["POST", "HEAD", "OPTIONS", "TRACE", "PATCH"])
def save_no_work(response: Response):
    response.status_code = 400
