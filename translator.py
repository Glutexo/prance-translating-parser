class RefTranslator(object):
    def __init__(self, specs, ):
        self.specs = specs

    def translate_references(self):
        self.specs = self._translate_partial(self.specs)

    def _translate_partial(self, partial):
        changes = dict(tuple(self._translating_iterator(partial, ())))

        paths = sorted(changes.keys(), key = len)

        from prance.util.path import path_set
        for path in paths:
            value = changes[path]
            if len(path) == 0:
                partial = value
            else:
                path_set(partial, list(path), value, create = True)

        return partial

    def _translating_iterator(self, partial, path):
        from prance.util.iterators import reference_iterator
        for ref_key, refstring, item_path in reference_iterator(partial):
            ref_value = refstring
            full_path = path + item_path
            yield full_path, {ref_key: ref_value}
