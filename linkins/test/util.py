import mock

class mock_call_with_name(object):
    """Like mock.call but takes the name of the call as its first
    argument. mock.call requires chained methods to define its
    name. This can be a problem, for example, if you need create
    mock.call().__enter__().__iter__().  You can optionally use
    mock._Call but you might as well use a tuple since its constructor
    requires a tuple of the form (name, args, kwargs).

    """
    def __new__(self, name, *args, **kwargs):
        return mock._Call(
            (name, args, kwargs)
            )
