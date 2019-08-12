from xml.dom import minidom

# (1, _("TCGRanks.com Format")),
#         (2, _("Magic Tournament Software")),
#         (3, _("Yu-Gi-Oh Tournament Software")),

def handle_uploaded_file(form):
    file_format = form.cleaned_data['file_format']

    if file_format == 1: # TCGRanks.com Format
        raise NotImplementedError

    elif file_format == 2: # Magic Tournament Software
        parse_magic_tournament_software(form)

    elif file_format == 3: # Yu-Gi-Oh Tournament Software
        raise NotImplementedError

    pass


def parse_magic_tournament_software(form):
    import sys  # todo remove
    print(
        "-------------------------------Goodbye cruel world!-----------------------------------------------------------------------------------------------------------------------------",
        file=sys.stderr)

    print(f"Magic", file=sys.stderr)

    game_and_format = form.cleaned_data['game_format']
    print(f"{game_and_format}", file=sys.stderr)

    file = form.cleaned_data['file']
    print(f"{file}", file=sys.stderr)

    for chunk in file.chunks():
        print(f"{chunk}", file=sys.stderr)


def calculate_current_scores():
    pass
