t = {
    "aaa": (
        "",
        {
            "bbb": (
                "",
                {
                    "ccc": ("", None),
                    "ddd": ("()", None),
                    "eee": ("[]", {"fff": ("", None)}),
                },
            )
        },
    )
}


def handle_leaf(chain):
    print(chain)


a = tele.aaa
a = tele.aaa.bbb
a = tele.aaa.bbb.ddd
a = tele.aaa.bbb.ddd(3, k=5)
a = tele.aaa.bbb.eee[4].fff


"""
a = tele.aaa.bbb.ddd(1, k=2)
a = tele.aaa.bbb.eee[4, 6, 9].fff
a = tele.aaa.bbb.ddd[4]
"""
