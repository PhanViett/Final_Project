class HttpCode:
    # SUCCESS
    OK = 200
    Created = 201
    Accepted = 202
    NoContent = 204

    # CLIENT ERROR
    BadRequest = 400
    UnAuthorized = 401
    PermissionDenied = 403

    NotFound = 404
    UnsupportedMediaType = 415
    UnprocessableEntity = 422

    # SERVER ERROR
    InternalError = 500
