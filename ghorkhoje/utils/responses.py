from django.http import JsonResponse

CUSTOM_EXCEPTION_FLAG = "custom_exception: "


def custom_exception(error_message):
    error_message = f"{CUSTOM_EXCEPTION_FLAG}{error_message}"
    raise Exception(error_message)


def common_response(status_code, message, data=None, **args):
    success = True if status_code // 100 == 2 else False

    response_payload = {
        "status": None,
        "message": message,
    }

    error = None
    if args.get("error_form", None) != None:
        error_form = args.get("error_form")
        error = {field: list(errors) for field, errors in error_form.errors.items()}
    if not success and data != None:
        error = str(data)
        response_payload["message"] = error.replace(CUSTOM_EXCEPTION_FLAG, "")

    if success:
        response_payload["status"] = True
        if data != None:
            response_payload["data"] = data
    else:
        response_payload["status"] = False
        if error != None:
            response_payload["error"] = error

    return JsonResponse(response_payload, status=status_code)
