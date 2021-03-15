import prance.util.url as _url


class RefTranslator(object):
    def __init__(self, specs, url):
        import copy
        self.specs = copy.deepcopy(specs)

        self.__strict = True
        self.__reference_cache = {}
        self.__collected_references = {}

        if url:
            self.url = _url.absurl(url)
            url_key = (_url.urlresource(self.url), self.__strict)

            # If we have a url, we want to add ourselves to the reference cache
            # - that creates a reference loop, but prevents child resolvers from
            # creating a new resolver for this url.
            self.__reference_cache[url_key] = self.specs
        else:
            self.url = None

    def translate_references(self):
        self.specs = self._translate_partial(self.url, self.specs)

        # Add collected references to the root document.
        if self.__collected_references:
          if 'components' not in self.specs:
            self.specs['components'] = {}
          if 'schemas' not in self.specs['components']:
            self.specs['components'].update({'schemas': {}})

          self.specs['components']['schemas'].update(self.__collected_references)

    def _dereference(self, ref_url, obj_path):
        """
        Dereference the URL and object path.

        Returns the dereferenced object.

        :param mixed ref_url: The URL at which the reference is located.
        :param list obj_path: The object path within the URL resource.
        :param tuple recursions: A recursion stack for resolving references.
        :return: A copy of the dereferenced value, with all internal references
            resolved.
        """
        # In order to start dereferencing anything in the referenced URL, we have
        # to read and parse it, of course.
        contents = _url.fetch_url(ref_url, self.__reference_cache, strict=self.__strict)

        # In this inner parser's specification, we can now look for the referenced
        # object.
        value = contents
        if len(obj_path) != 0:
            from prance.util.path import path_get
            try:
                value = path_get(value, obj_path)
            except (KeyError, IndexError, TypeError) as ex:
                raise _url.ResolutionError('Cannot resolve reference "%s": %s'
                                           % (ref_url.geturl(), str(ex)))

        # Deep copy value; we don't want to create recursive structures
        import copy
        value = copy.deepcopy(value)

        # Now resolve partial specs
        # value = self._resolve_partial(ref_url, value)

        # That's it!
        return value

    def _translate_partial(self, base_url, partial):
        changes = dict(tuple(self._translating_iterator(base_url, partial, ())))

        paths = sorted(changes.keys(), key = len)

        from prance.util.path import path_set
        for path in paths:
            value = changes[path]
            if len(path) == 0:
                partial = value
            else:
                path_set(partial, list(path), value, create = True)

        return partial

    def _translating_iterator(self, base_url, partial, path):
        from prance.util.iterators import reference_iterator
        for _, ref_string, item_path in reference_iterator(partial):
            ref_url, obj_path = _url.split_url_reference(base_url, ref_string)
            full_path = path + item_path
            ref_value = self._dereference(ref_url, obj_path)

            if ref_url.path == self.url.path:
                # Reference to the root document. Keeping intact.
                yield full_path, ref_value
            else:
                # Reference to a non-root document. Translating.
                ref_key = self._collect_reference(ref_url, obj_path, ref_value)
                translated_url = '#/components/schemas/' + ref_key
                yield full_path, {'$ref': translated_url}

    def _collect_reference(self, ref_url, item_path, value):
        """
        Return a portion of the dereferenced URL.

        format - ref-url_obj-path
        """
        ref_key = ref_url.path.split('/')[-1] + '_' + '_'.join(item_path[1:])
        self.__collected_references[ref_key] = value
        return ref_key
