def check_qrcode_time(func):
    def inner(request, place):
        result = False
        if request.session.get('post_qrcode'):
            result = True

        ret = func(request, place, result)
        return ret

    return inner


