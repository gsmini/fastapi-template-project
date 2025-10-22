from fastapi.responses import JSONResponse


def make_ok_resp(data=None, **kwargs):
    resp = {"code": 0, "message": "request succeed", "data": data}
    resp.update(kwargs)
    return JSONResponse(resp)
