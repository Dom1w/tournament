

def handle_uploaded_file(request):
    f = request.FILES['file']

    import sys  # todo remove
    print(
        "-------------------------------Goodbye cruel world!-----------------------------------------------------------------------------------------------------------------------------",
        file=sys.stderr)
    print(f"{request}", file=sys.stderr)

    pass

