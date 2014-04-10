import re
import os

class Configurator(object):
    """
    The `Configurator` class creates helper objects that can be used
    to easily add methods to a class to configure and query a particular setting
    on the device.

    The easiest way to understand it is by example. First, a stripped down usage example:


    .. code :: python

        class MyDevice(object):

            __metaclass__ = Configurator.ConfigurableMeta

            @Configurator.config("FOO:BAR")
            def foobar(self, val):
                return val.lower()

            @foobar.setter
            def foobar(self, val):
                return val.upper()


            @Configurator.config
            def frobbed(self, val):
                return (val == "ON")

            @frobbed.setter
            def frobbed(self, val):
                return "ON" if val else "OFF"


    And now, a more thorough example, expanded from this:

    .. code :: python

        class MyDevice(object):

            #Make sure it uses the ConfigurableMeta class as its metaclass,
            # so Configurator objects in the class definition get replaced with
            # appropriate methods.
            __metaclass__ = Configurator.ConfigurableMeta

            #Just some ordinary instance attributes, which we will be the target of
            # our setting configuring and querying.
            __foobar = "TAZ"
            __frobbed = "OFF"

            #This is where the class actually implements sending command and queries.
            # The Configurator objects will call these methods.

            def send_command(self, name, arg):
                print "~~~> %s %s" % (name, arg)
                if name == "FOO:BAR":
                    if not isinstance(arg, str):
                        raise TypeError()
                    if arg != arg.upper():
                        raise ValueError()
                    self.__foobar = arg

                elif name == "FROBBED":
                    if arg not in ("ON", "OFF"):
                        raise ValueError()
                    self.__frobbed = arg

                else:
                    raise KeyError()
                    

            def send_query(self, name):
                print "???? %s" % name
                if name == "FOO:BAR":
                    val = self.__foobar
                elif name == "FROBBED":
                    val = self.__frobbed
                else:
                    raise KeyError()
                print "    <<<< %s" % val
                return val


            #Now, define Configurators for each of our configurable settings.


            #First, for the FOO:BAR setting, which will be accessed through a
            # function called `foobar`.

            @Configurator.config("FOO:BAR")
            def foobar(self, val):
                #Translate a value returned by `send_query` into a value to return
                # to the calling code.
                return val.lower()

            @foobar.setter
            def foobar(self, val):
                #Translate a value provided by the calling code into a value that
                # will be passed to `send_command`.
                return val.upper()


            #Now, the FROBBED setting. We can use implicit named in the decorator
            # for this one.

            @Configurator.config
            def frobbed(self, val):
                '''
                +++
                Querying returns True for "ON", and False for "OFF".
                '''
                if val == "ON":
                    return True
                if val == "OFF":
                    return False
                raise ValueError(val)

            @frobbed.setter
            def frobbed(self, val):
                '''
                +++
                Valid values for configuring are True and False, or synonomously
                "ON" and "OFF".
                '''
                if val is True or val == "ON":
                    return "ON"
                elif val is False or val == "OFF":
                    return "OFF"
                raise ValueError()


    With the above code, you could then do the following:

    .. code :: pycon

        >>> dev = MyDevice()
        >>> dev.foobar()
        ???? FOO:BAR
            <<<< TAZ
        'taz'
        >>>
        >>> dev.foobar('razzle-dazzle')
        ~~~> FOO:BAR RAZZLE-DAZZLE
        >>>
        >>> dev.foobar()
        ???? FOO:BAR
            <<<< RAZZLE-DAZZLE
        'razzle-dazzle'
        >>>
        >>>
        >>> dev.frobbed()
        ???? FROBBED
            <<<< OFF
        False
        >>> dev.frobbed(True)
        ~~~> FROBBED ON
        >>> dev.frobbed()
        ???? FROBBED
            <<<< ON
        True
        >>>
        >>> dev.frobbed(False)
        ~~~> FROBBED OFF
        >>> dev.frobbed()
        ???? FROBBED
            <<<< OFF
        False
        >>>
        >>> dev.frobbed("ON")
        ~~~> FROBBED ON
        >>> dev.frobbed()
        ???? FROBBED
            <<<< ON
        True
        >>>
        >>> dev.frobbed("???")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "src\pytek\util.py", line 125, in config
            return self(device, val)
          File "src\pytek\util.py", line 116, in __call__
            self.configure(device, self.name, self.set(device, val))
          File "temp.py", line 94, in frobbed
            raise ValueError()
        ValueError
        >>>
        >>>
        >>> help(dev.foobar)
        Help on method foobar in module pytek.util:

        foobar(device, val=None) method of temp.MyDevice instance
            Configures or queries the value of the ``FOO:BAR`` setting on the device.
            If a value is given, then the setting is configured to the given value.
            If the value is `None` (the default), then the setting is queried and the value
            is returned.

        >>>
        >>> help(dev.frobbed)
        Help on method frobbed in module pytek.util:

        frobbed(device, val=None) method of temp.MyDevice instance
            Configures or queries the value of the ``FROBBED`` setting on the device.
            If a value is given, then the setting is configured to the given value.
            If the value is `None` (the default), then the setting is queried and the value
            is returned.


            Querying returns True for "ON", and False for "OFF".


            Valid values for configuring are True and False, or synonomously
            "ON" and "OFF".

        >>>
        >>>


    """

    #: A string used for default value of the `doc` attribute.
    DEFAULT_DOCTSTR = """
Configures or queries the value of the ``%(NAME)s`` setting on the device.
If a value is given, then the setting is configured to the given value.
If the value is `None` (the default), then the setting is queried and the value
is returned.
"""

    def __init__(self, name, get=None, set=None, doc=None):
        """
        :param name: Specifies the name of the setting accessed by this object.
            Should be either a `callable` object with a ``__name__`` attribute,
            or a string. Strings will be used directly, callables will be filtered
            through `func_to_name`.
        :param callable get: Optional: if given, passed to `getter`.
        :param callable set: Optional: if given, passed to `setter`.
        :param callable doc: Optional: if given, used as the value of the `doc` attribute.

        """
        if callable(name):
            self.name = self.func_to_name(name)
        else:
            self.name = str(name)

        self.doc = doc
        if doc is None:
            self.doc = self.DEFAULT_DOCTSTR % {'NAME': self.name}

        self.get = None
        if get is None:
            self.get = lambda device, val: val
        else:
            self.getter(get)

        self.set = None
        if set is None:
            self.set = lambda device, val: str(val)
        else:
            self.setter(set)


    @classmethod
    def configure(cls, device, name, val):
        """
        The final method in this object used to configure the setting, given
        the raw value to be sent to the device. This is called by the `__call__`
        method when appropriate.

        This delegates to the ``send_command`` method of the given `device`.

        :param device: The object on which the ``send_command`` will be invoked.
        :param str name: The name of the setting, usually the value of the `name` attribute.
            This is the first arguments passed to ``send_command``.
        :param str val: The raw value to configure the setting to. This is the
            second argument passed to ``send_command``.
        """
        device.send_command(name, val)

    @classmethod
    def query(cls, device, name):
        """
        The final method in this object used to query the setting, returning
        the raw value from the device. This is called by the `__call__`
        method when appropriate.

        This delegates to the ``send_query`` method of the given `device`.

        :param device: The object on which the ``send_query`` will be invoked.
        :param str name: The name of the setting, usually the value of the `name` attribute.
            This is the only arguments passed to ``send_query``.
        """
        return device.send_query(name)


    def __call__(self, device, val=None):
        """
        __call__(self, device [, val])

        The universal callback which filters values and delegates to `configure` or
        `query` as appropriate.

        If `val` is given (and not `None`), then the setting is configured. The given
        value is first filtered through the callable in the `set` attribute, and
        then passed to `configure`.

        If `val` is not given (or is `None`, the default), then the setting is queried.
        The setting's value is retrieved with `query`, then filtered through the
        callable in this object's `get` attribute before being returned.

        """
        if val is None:
            #Get it
            return self.get(device, self.query(device, self.name))
        self.configure(device, self.name, self.set(device, val))

    def create_method(self, name):
        """
        Creates a method with the given name which can be installed in a class to delegate
        to this object's `__call__` method. Sets the name of the method to `name`,
        and sets the docstr (`__doc__`) to the value of this object's `doc` attribute.

        This is used by `ConfigurableMeta` to replace Configurator instances in the classes
        dictionary with functions.
        """
        def config(device, val=None):
            return self(device, val)
        config.__name__ = name
        config.__doc__ = self.doc
        return config


    __DOC_APPEND = re.compile(r'^\s*\n(\s*)\+\+\+\s*\n', re.M)

    def update_doc(self, func):
        """
        If the given function has a docstrig (`__doc__`), then this object's
        `doc` attribute is updated with it. Otherwise, it does nothing.

        If `func`'s docstr begins with ``'+++'`` alone on a line (any amount of leading and trailing whitespace),
        then the remainder of the docstring is *appended* to the existing docstring, instead
        of replacing it.
        """
        if func.__doc__ is not None:
            match = self.__DOC_APPEND.match(func.__doc__)
            if match:
                indent = re.compile(r'^' + re.escape(match.group(1)))
                doc = self.__DOC_APPEND.sub('', func.__doc__)
                doc = os.linesep.join(indent.sub('', line) for line in doc.splitlines())
                self.doc += '\n\n' + doc
            else:
                self.doc = func.__doc__

    @classmethod
    def func_to_name(cls, func):
        """
        Derives a setting name from a function. The implementation here just
        uses the `__name__` attribute of the given `func`, and then uses
        `str.upper()` to make it all upper case.

        This is used in `__init__` if the name is a `callable` object.
        """
        return func.__name__.upper()

    @classmethod
    def config(cls, arg):
        """

        A function wrapper utility used to create a `Configurator` object and a
        function wrapper to configure its `getter`.

        There are two way to invoke this, using *implicit naming* or
        *explicit naming*.

        For **implicit naming***, simply pass a function in directly, or use
        this function directly as a decorator. For instance:

        .. code:: python

            @Configurator.config
            def foobar(self, val):
                return val

        The above code will create a new instance of `cls` (i.e., a Configurator
        object), and will pass the given function ``foobar`` in as the ``name``
        parameter to the constructor. This in turn will use `func_to_name` to
        derive a value for the instance's `name` attribute from the function, by
        default (i.e., in the base `Configurator` class), this is just the name
        of the function in all uppercase.

        The function will also be passed to the instance's `getter` method so
        that the ``foobar`` function becomes the instance's `get` filter.

        This method will then return the Configurator object itself, *not* the
        wrapped function.
        
        The alternative is **explicit naming**, in which this function is not
        used *as* a function wrapper, but invoked to *return* a function wrapper.
        This gives you some added flexibility such as explitictly giving the `name`
        to use for the Configurator object. Otherwise, the behavior is essentially
        the same.

        For instance:

        .. code:: python

            @Configurator.config('BAZ:RUFFLE')
            def foobar(self, val):
                return val

        In this case, even though the wrapped function has the same name, ``"foobar"``,
        the created Configurator object will have a ``name`` of ``"BAZ:RUFFLE"``.
        Other than that, the effects are the same.

        In either case, when code like this appears in a class definition,
        it means that class will have an attribute named ``foobar`` whose value
        is a Configurator object. If this class is using the `~Configurator.ConfigurableMeta`
        metaclass, then this attribute will be replaced by a proper method
        generated by the Configurator's `create_method` method.

        Also note that when the wrapped function is passed to the Configurator's
        `getter` method, this method will also pass it to `update_doc`, so if the
        wrapped function has a docstring, the Configurator object's `doc` attribute
        will be set accordingly. When the `~Configurator.ConfigurableMeta` gets
        a hold of it, the corresponding method it adds to the class will receive
        this docstr from the Configurator object.

        Note that for the remainder of the class definition, you can
        use the generated Configurator object. For instance, you can follow up
        either of the above examples with the following:

        .. code :: python

            @foobar.setter
            def foobar(self, val):
                if val is False:
                    return "OFF"
                return "ON"

        Since at this point the ``foobar`` symbol is actually a Configurator
        object, you can use its other decorators such as `setter` and `getter`.

        """
        c = cls(arg)
        if callable(arg):
            c.getter(arg)
            return c

        def wrapper(func):
            c.getter(func)
            return c
        return wrapper

    def setter(self, func):
        """
        A function wrapper which sets this object's `set` attribute to the given
        function and passes the function to `update_doc`, then returns `self`.

        The given function should take two arguments and return a string. The
        first argument will be the device on which the `send_command` method
        is invoked, the second argument will be the client supplied value they
        want to configure the setting to. The function should return a corresponding
        string which will actually be sent to the device.
        """
        self.set = func
        self.update_doc(func)
        return self

    def getter(self, func):
        """
        Like `setter`, but sets the object's `get` attribute, used for querying the
        setting from the device.

        This is a function wrapper which sets this object's `get` attribute to the given
        function and passes the function to `update_doc`, then returns `self`.

        The given function should take two arguments and return a string. The
        first argument will be the device on which the `send_query` method
        is invoked, the second argument will be the value returned from the device
        by `send_query`. The function should return a corresponding
        value which will be returned to the user to reflect the string returned
        by the device.
        """
        self.get = func
        self.update_doc(func)
        return self



    class ConfigurableMeta(type):
        """
        This is a meta class that can be added to classes to more easily support
        the use of `Configurator` objects as pseudo-methods.

        The meta class extends the `__new__` function to find all instances of
        `Configurator` in the class's dictionary, and replace it with a method
        created by the Configurator's `~Configurator.create_method` method.

        See the example code in the documentation for `Configurator` for an
        example.
        """

        def __new__(meta, name, bases, dct):

            for attr, val in dct.items():
                if isinstance(val, Configurator):
                    dct[attr] = val.create_method(attr)

            return super(Configurator.ConfigurableMeta, meta).__new__(meta, name, bases, dct)

