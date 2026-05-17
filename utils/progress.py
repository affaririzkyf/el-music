def create_progress_bar(

    progress,

    total,

    length=12
):

    filled = int(

        length * progress // total
    )

    bar = (

        "━" * filled +

        "🔘" +

        "─" * (length - filled)
    )

    return bar