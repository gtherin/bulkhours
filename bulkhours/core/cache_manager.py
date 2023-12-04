import IPython


class CacheManager:
    objects = {}

    @staticmethod
    def init(l):
        args = l.split(".")

        if len(args) > 2:
            o = f"{args[0]}.{args[1]}"
            if o not in CacheManager.objects:
                CacheManager.objects[o] = dict()
                IPython.get_ipython().run_cell(
                    f"from argparse import Namespace\n{o} = Namespace()"
                )
            v = args[2].split()[0]
            ov = args[2].replace("'", '"').split('"')
            if len(ov := args[2].replace("'", '"').split('"')) == 3:  # For string
                CacheManager.objects[o][v] = ov[1]
            elif len(ov := args[2].split("=")) == 2:  # Otherwise
                CacheManager.objects[o][v] = ov[1]
            else:  # Fuck, I don't what is going on
                CacheManager.objects[o][v] = ov
