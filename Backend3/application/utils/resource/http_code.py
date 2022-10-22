class HttpCode:
    # SUCCESS
    OK = 200
    Created = 201
    Accepted = 202

    # CLIENT ERROR
    BadRequest = 400
    UnAuthorized = 401
    NotFound = 404
    PermissionDenied = 405
    UnsupportedMediaType = 415
    UnprocessableEntity = 422
    NoContent = 204

    # SERVER ERROR
    InternalError = 500
