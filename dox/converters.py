class ShortUUIDConverter:
    regex = '[0-9A-Z]{32}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%s' % value
