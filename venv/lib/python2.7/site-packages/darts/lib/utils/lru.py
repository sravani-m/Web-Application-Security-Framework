# -*- coding: utf-8 -*-
#
#  Deterministic Arts Utilities
#  Copyright (c) 2011 Dirk Esser
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

"""Trivial LRU-Dictionary implementation
"""

from __future__ import with_statement

import sys
from threading import RLock, Lock, Condition, Thread

__all__ = (
    'LRUDict', 'AutoLRUCache', 'CacheLoadError', 'CacheAbandonedError',
    'CachingError', 'SynchronizedLRUDict', 'DecayingLRUCache',
)

def log():
    from logging import getLogger
    return getLogger(__name__)

log = log()


class CachingError(Exception):

    """Base class for caching-related errors
    """


class CacheLoadError(CachingError):

    """Exception raised, when loading a key fails

    This exception is raised by an `AutoLRUCache` instance, if loading
    the value associated with some key fails. The `key` property
    of the exception instance provides the key being looked up
    and the `exc_info` property contains a tuple, which provides
    information about the actual exception caught while loading.
    """

    def __init__(self, key=None, exc_info=None):
        super(CacheLoadError, self).__init__()
        self.key = key
        self.exc_info = exc_info


class CacheAbandonedError(CachingError):

    """A loading operation has been discarded

    This exception is raised to indicate, that the result of
    a load operation had to be discarded, because the cache has
    been reset.
    """

    def __init__(self, key=None, value=None, exc_info=None):
        super(CacheAbandonedError, self).__init__()
        self.key = key
        self.value = value
        self.exc_info = exc_info


class LRUItem(object):

    """Element of an LRUDict

    Instances of this class are used internally to hold the entries
    of `LRUDict` instances. The entries form a doubly-linked list,
    and are also interned in a dictionary for fast look-up.
    """

    __slots__ = (
        '_previous',
        '_next',
        '_key',
        '_value',
    )

    def __init__(self, key, value):
        super(LRUItem, self).__init__()
        self._key = key
        self._value = value
        self._previous = None
        self._next = None

    def __str__(self):
        return "<LRUItem %r: %r>" % (self._key, self._value)

    def __repr__(self):
        return "LRUItem(%r, %r)" % (self._key, self._value)



# Internal tag value used to mark optional arguments, for
# which no value has been supplied by the caller.

missing = object()


class LRUDict(object):

    """Dictionary with LRU behaviour

    This class implements a dictionary, whose size is limited to a
    pre-defined capacity. Adding new elements to a full LRU dictionary
    will cause \"old\" elements to be evicted from the dictionary in
    order to make room for new elements.

    Instances of this class are not thread-safe; if an instance is
    to be shared across multiple concurrently running threads, the
    client application is responsible for providing proper synchronization.
    In particular, be aware, that even read-only operations on instances
    of this class might internally modify data structures, and thus,
    concurrent read-only access has to be synchronized as well.
    """

    __slots__ = (
        '__weakref__',
        '_LRUDict__index',
        '_LRUDict__first',
        '_LRUDict__last',
        '_LRUDict__capacity',
    )
    
    def __init__(self, capacity=1024):
        super(LRUDict, self).__init__()
        self.__index = dict()
        self.__first = None
        self.__last = None
        self.__capacity = self.__check_capacity(capacity)

    def __set_capacity(self, value):
        value = self.__check_capacity(value)
        if value > self.__capacity:
            self.__capacity = value
        else:
            if value < self.__capacity:
                self.__capacity = value
                self.__ensure_room(0)

    def capacity():
        def getter(self): 
            return self.__capacity
        def setter(self, value):
            self.__set_capacity(value)
        return property(getter, setter, doc="""Capacity

            This property holds an integer number, which defines the
            capacity of this dictionary (i.e., the maximum number of 
            elements it may hold at any time). Setting this property
            to a new value may cause elements to be evicted from the
            dictionary.""")

    capacity = capacity()

    def __check_capacity(self, value):
        if value < 1:
            raise ValueError("%r is not a valid capacity" % (value,))
        return value

    def clear(self):

        """Removes all entries
        """

        first = self.__first

        self.__index.clear()
        self.__first = self.__last = None

        # XXX: This code should be reconsidered. We clean up the
        # doubly-linked list primarily for the sake of CPython and
        # its reference-counting based memory management. However,
        # maybe we should just forget about this and rely on the 
        # GC to clean up the cycles here. There should not be any
        # __del__ methods involved here anyway (at least not in the
        # objects we are responsible for, i.e., the LRUItems)

        while first is not None:
            next = first._next
            first._key = first._value = None
            first._previous = first._next = None
            first = next

    def __len__(self):

        """Answers the current number of elements in this dictionary
        """

        return len(self.__index)
    
    def __contains__(self, key):

        """Tests, whether a key is contained

        This method returns true, if there is an entry with the
        given `key` in this dictionary. If so, the entry's priority
        will be boosted by the call, making it more unlikely, that
        the entry will be evicted when the dictionary needs to make
        room for new entries.
        """

        item = self.__index.get(key)
        if item is None:
            return False
        else:
            self.__make_first(item)
            return True

    def __iter__(self):

        """Iterator for all keys of this dictionary

        See `iterkeys`.
        """

        return self.__index.iterkeys()

    def iterkeys(self):

        """Iterator for all keys of this dictionary

        This method returns a generator, which yields all keys
        currently present in this dictionary. Note, that iterating
        over the elements of an LRU dictionary does not change
        the priorities of individual entries. Also note, that the
        order, in which entries are generated, is undefined. In
        particular, the order does usually *not* reflect the LRU 
        priority in any way.
        """

        return self.__index.iterkeys()

    def itervalues(self):

        """Iterator for all values of this dictionary

        This method returns a generator, which yields all values
        currently present in this dictionary. Note, that iterating
        over the elements of an LRU dictionary does not change
        the priorities of individual entries. Also note, that the
        order, in which entries are generated, is undefined. In
        particular, the order does usually *not* reflect the LRU 
        priority in any way.
        """

        for item in self.__index.itervalues():
            yield item._value

    def iteritems(self):

        """Iterator for all entries of this dictionary

        This method returns a generator, which yields all keys and
        values currently present in this dictionary as tuples of
        `key, value`. Note, that iterating over the elements of an 
        LRU dictionary does not change the priorities of individual 
        entries. Also note, that the order, in which entries are 
        generated, is undefined. In particular, the order does usually 
        *not* reflect the LRU priority in any way.
        """

        for key, item in self.__index.iteritems():
            yield key, item._value

    def __delitem__(self, key):

        """Removes an entry from this dictionary

        This method removes the entry identified by the given
        `key` from this dictionary. If no matching entry exists,
        this method raises a `KeyError` exception.

        This method does not affect the priorities of entries
        remaining in the dictionary.
        """

        item = self.__index.pop(key)
        self.__unlink(item)

    def pop(self, key, default=missing):

        """Removes an entry from this dictionary

        This method removes the entry identified by the given
        `key` from this dictionary, returning its associated
        value. If no matching entry exists, this method returns
        the value supplied as `default` or raises a `KeyError` 
        exception, if no default value was supplied.

        This method does not affect the priorities of entries
        remaining in the dictionary.
        """

        item = self.__index.pop(key, None)
        if item is None:
            if default is not missing:
                return default
            else:
                raise KeyError(key)
        else:
            self.__unlink(item)
            return item._value

    def get(self, key, default=None):
        
        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        returns the value of `default` instead.

        If a matching entry is found, this method will boost that
        entry's priority, making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry.
        """

        item = self.__index.get(key)
        if item is None:
            return default
        else:
            self.__make_first(item)
            return item._value

    def peek(self, key, default=None):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        returns the value of `default` instead.

        This method differs from `get` in that it does not alter the
        priority of a matching entry, i.e., the likelyhood of the 
        entry being evicted the next time, the dict needs to make 
        room, is not affected by calls to this method.
        """

        item = self.__index.get(key)
        if item is None:
            return default
        else:
            return item._value

    def __getitem__(self, key):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        raises a `KeyError` instead.

        If a matching entry is found, this method will boost that
        entry's priority, making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry.
        """

        item = self.__index.get(key)
        if item is None:
            raise KeyError(key)
        else:
            self.__make_first(item)
            return item._value

    def __setitem__(self, key, value):

        """Adds or modifies an entry

        This method sets the value associated with `key` in this
        dictionary to `value`. If there is no present entry for
        `key` in this dictionary, this method may need to evict
        entries from the dictionary in order to make room for the
        new entry.

        This method boosts the priority of the entry associated
        with `key` making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry. 
        """

        present = self.__index.get(key)
        if present is not None:
            present._value = value
            self.__make_first(present)
        else:
            self.__ensure_room(1)
            item = LRUItem(key, value)
            item._previous = None
            item._next = self.__first
            if self.__first is None:
                self.__last = item
            else:
                self.__first._previous = item
            self.__index[key] = item
            self.__first = item

    def __ensure_room(self, size):
        
        """(internal)

        This method makes sure, that there is room for `size` 
        new elements in this dictionary, potentially evicting
        old elements.
        """
        
        index = self.__index
        capacity = self.__capacity
        if size > capacity:
            raise ValueError(size)
        else:
            while len(index) + size > capacity:
                last = self.__last
                del index[last._key]
                self.__unlink(last)
            return self

    def __unlink(self, item):

        """(internal)

        Unlink `item` from the doubly-linked list of LRU items
        maintained by this dictionary. Makes sure, that the 
        dictionary's `__first` and `__last` pointers are properly
        updated, if the item happens to be the first/last in
        the list.
        """

        p, n = item._previous, item._next
        if p is None:
            self.__first = n
        else:
            p._next = n
        if n is None:
            self.__last = p
        else:
            n._previous = p
        item._previous = None
        item._next = None
        return item

    def __make_first(self, item):

        """(internal)

        Boosts `item`'s priority by making it the first item of
        the doubly linked list of all items. Since the eviction
        process removes elements from the end of the list, the
        items closer to the head are more unlikely to be removed
        if we need to make room for new elements.
        """

        p, n = item._previous, item._next
        if p is None:
            assert item is self.__first, "no previous entry in %r, but first is %r" % (item, self.__first,)
            return item
        else:
            p._next = n
            if n is None:
                self.__last = p
            else:
                n._previous = p
            item._previous = None
            item._next = self.__first
            self.__first._previous = item
            self.__first = item
            return item


class SynchronizedLRUDict(object):

    """Thread-safe LRU Dictionary

    This class acts as a thread-safe wrapper around a regular
    LRU dictionary. The primary interface is that of a standard
    `LRUDict`, but all methods are internally synchronized.

    Note, that there is nothing fancy going on this class; all
    methods simply ensure, that the lock is held around calls
    to the underlying plain `LRUDict` instance, which does the
    actual work.
    """

    __slots__ = (
        '__weakref__', 
        '_SynchronizedLRUDict__dict', 
        '_SynchronizedLRUDict__lock',
    )

    def __init__(self, capacity=1024, lock=None):
        
        """Initialize a new instance

        This method initializes a new instance, providing an
        initial capacity of `capacity` elements. If `lock` is
        provided, it must be a `threading.Lock` or `threading.RLock`
        instance. The lock will be used to synchronize all 
        access to the underyling `LRUDict`. If no lock is 
        provided, the method will create a new one.
        """

        super(SynchronizedLRUDict, self).__init__()
        self.__dict = LRUDict(capacity)
        self.__lock = RLock() if lock is None else lock

    def capacity():
        def getter(self):
            with self.__lock:
                return self.__dict.capacity
        def setter(self, value):
            with self.__lock:
                self.__dict.capacity = value
        return property(getter, setter, doc="""Capacity

            This property holds an integer number, which defines the
            capacity of this dictionary (i.e., the maximum number of 
            elements it may hold at any time). Setting this property
            to a new value may cause elements to be evicted from the
            dictionary.""")

    capacity = capacity()

    def clear(self):
        
        """Removes all entries
        """
        
        with self.__lock:
            self.__dict.clear()

    def get(self, key, default=None):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        returns the value of `default` instead.

        If a matching entry is found, this method will boost that
        entry's priority, making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry.
        """

        with self.__lock:
            return self.__dict.get(key, None)

    def peek(self, key, default=None):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        returns the value of `default` instead.

        This method differs from `get` in that it does not alter the
        priority of a matching entry, i.e., the likelyhood of the 
        entry being evicted the next time, the dict needs to make 
        room, is not affected by calls to this method.
        """

        with self.__lock:
            return self.__dict.peek(key, None)

    def pop(self, key, default=missing):

        """Removes an entry from this dictionary

        This method removes the entry identified by the given
        `key` from this dictionary, returning its associated
        value. If no matching entry exists, this method returns
        the value supplied as `default` or raises a `KeyError` 
        exception, if no default value was supplied.

        This method does not affect the priorities of entries
        remaining in the dictionary.
        """

        with self.__lock:
            return self.__dict.pop(key, default)
        
    def __len__(self):

        """Answers the current number of elements in this dictionary
        """

        with self.__lock:
            return self.__dict.__len__()

    def __contains__(self, key):

        """Tests, whether a key is contained

        This method returns true, if there is an entry with the
        given `key` in this dictionary. If so, the entry's priority
        will be boosted by the call, making it more unlikely, that
        the entry will be evicted when the dictionary needs to make
        room for new entries.
        """

        with self.__lock:
            return self.__dict.__contains__(key)

    def __iter__(self):

        """Iterator for all keys of this dictionary

        See `iterkeys`.
        """

        return self.iterkeys()

    def iterkeys(self):

        """Iterator for all keys of this dictionary

        This method returns a generator, which yields all keys
        currently present in this dictionary. Note, that iterating
        over the elements of an LRU dictionary does not change
        the priorities of individual entries. Also note, that the
        order, in which entries are generated, is undefined. In
        particular, the order does usually *not* reflect the LRU 
        priority in any way.

        Note, that the resulting generator actually traverses
        a snapshot copy of the key set taken, when the `iterkeys`
        method was called.
        """

        with self.__lock:
            return iter(tuple(self.__dict.iterkeys()))

    def itervalues(self):
        """Iterator for all values of this dictionary

        This method returns a generator, which yields all values
        currently present in this dictionary. Note, that iterating
        over the elements of an LRU dictionary does not change
        the priorities of individual entries. Also note, that the
        order, in which entries are generated, is undefined. In
        particular, the order does usually *not* reflect the LRU 
        priority in any way.

        Note, that the resulting generator actually traverses
        a snapshot copy of the value collection taken, when the 
        `itervalues` method was called.
        """

        with self.__lock:
            return iter(tuple(self.__dict.itervalues()))

    def iteritems(self):

        """Iterator for all entries of this dictionary

        This method returns a generator, which yields all keys and
        values currently present in this dictionary as tuples of
        `key, value`. Note, that iterating over the elements of an 
        LRU dictionary does not change the priorities of individual 
        entries. Also note, that the order, in which entries are 
        generated, is undefined. In particular, the order does usually 
        *not* reflect the LRU priority in any way.

        Note, that the resulting generator actually traverses
        a snapshot copy of the items collection taken, when the 
        `iteritems` method was called.
        """

        with self.__lock:
            return iter(tuple(self.__dict.iteritems()))

    def __getitem__(self, key):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        raises a `KeyError` instead.

        If a matching entry is found, this method will boost that
        entry's priority, making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry.
        """

        with self.__lock:
            return self.__dict.__getitem__(key)

    def __setitem__(self, key, value):

        """Adds or modifies an entry

        This method sets the value associated with `key` in this
        dictionary to `value`. If there is no present entry for
        `key` in this dictionary, this method may need to evict
        entries from the dictionary in order to make room for the
        new entry.

        This method boosts the priority of the entry associated
        with `key` making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry. 
        """

        with self.__lock:
            self.__dict.__setitem__(key, value)

    def __delitem__(self, key):

        """Removes an entry from this dictionary

        This method removes the entry identified by the given
        `key` from this dictionary. If no matching entry exists,
        this method raises a `KeyError` exception.

        This method does not affect the priorities of entries
        remaining in the dictionary.
        """

        with self.__lock:
            self.__dict.__delitem__(key)



loading = object()
available = object()
failed = object()
discarded = object()

class Placeholder(object):

    """Placeholder for a value-yet-to-come

    The `condition` property holds a condition variable, which
    is synchronized using the creating cache's lock. In order
    to wait for a load to finish, wait on this condition variable.

    The state property indicates, what's the current state of
    the load operation, which this object represent:

    - `loading` the operation is still in progress. Wait on
      the placeholder's `condition` for updates

    - `available` the operation has successfully been performed
      and the value is available in the `value` property

    - `failed` the loader raised an exception. The `value`
      property contains the `exc_info` tuple of the exception.

    - `discarded` the cache has been reset with the `discard_loads`
      option. When seen, a `CacheAbandonedError` should be raised
    """

    def __init__(self, lock):
        super(Placeholder, self).__init__()
        self._condition = Condition(lock)
        self._state = loading
        self._value = None



class AutoLRUCache(object):

    """Auto-loading LRU cache

    Instances of this class provide simple caches, which support
    automatic loading of resources, when cache look-up fails. 
    Loading of resources is accomplished by providing a `loader`
    function to the cache's constructor. The function must have
    the signature

        lambda key: ...

    It may return `None` to indicate, that the resource has not
    been found. Any other value is taken to be the resource value
    associated with the given `key`. Note, that `None` is never
    a valid resource value and will always be taken to mean, that
    no value is available. If the loader raises an exception, the 
    cache will wrap the exception in a `CacheLoadError` and propagate 
    the information by raising that one.

    This class carefully tries to ensure, that only a single
    thread attempts to actually load a given key value (though
    multiple threads may be busy concurrently loading resources 
    for different key values at the same time). If the value for
    a key `K` is currently being loaded by a thread `A`, and 
    another thread `B` requests the value of `K` from the same
    cache, then `B` will block until `A` has loaded the value
    (or bailed out due to an exception).

    Thread-safety. Instances of this class are fully thread safe,
    using an internal locking discipline. Note, though, that the
    load function is called unsynchronized, and needs to provide
    its own locking discipline.
    """

    __slots__ = (
        '__weakref__',
        '_AutoLRUCache__lock',
        '_AutoLRUCache__cache',
        '_AutoLRUCache__loader',
        '_AutoLRUCache__loading',
    )

    def __init__(self, loader, capacity=1024):
        super(AutoLRUCache, self).__init__()
        self.__lock = Lock()
        self.__cache = LRUDict(capacity)
        self.__loader = loader
        self.__loading = dict()

    def clear(self, discard_loads=False):
        
        """Remove all cached values

        This method removes all values from this cache. If
        `discard_loads`, then the method also forces all currently
        running load operations to fail with a `CacheAbandonedError`.
        Note, that this method has no way of interrupting load
        operations, so all pending operations will have to complete 
        before the discard condition can be detected.
        """

        with self.__lock:
            self.__cache.clear()
            if discard_loads:
                conditions = list()
                keys = tuple(self.__loading.iterkeys())
                for k in keys:
                    placeholder = self.__loading.pop(k)
                    if placeholder._state is loading:
                        placeholder._state = discarded
                        conditions.append(placeholder._condition)
                while conditions:
                    conditions.pop().notifyAll()
                        
    def load(self, key, default=None):

        """Load a value 

        This method returns the value associated with `key`,
        possibly loading it, if it is not already available
        in the cache. If no matching value can be found, the
        method returns the value supplied as `default`.
        """

        # TODO: I'd really like to have a timeout parameter
        # on this method. This would be trivial to implement
        # for threads, which can piggy back on load operations
        # performed by other threads (since `Condition.wait`
        # already supports a timeout parameter). However, it
        # will be hard to do, when the current thread is the
        # actual loading one. The only way I can think of right
        # now is to always move the load operations to a fresh
        # thread, and make the triggering thread block like a
        # piggy-backing one.

        with self.__lock:
            item = self.__cache.get(key, missing)
            if item is not missing:
                if item is None:
                    return default
                else:
                    return item
            else:
                placeholder = self.__loading.get(key)
                if placeholder is not None:
                    while placeholder._state is loading:
                        placeholder._condition.wait()
                    if placeholder._state is failed:
                        raise CacheLoadError(key, placeholder._value)
                    else:
                        if placeholder._state is available:
                            value = placeholder._value
                            if value is None:
                                return default
                            else:
                                return value
                        else:
                            assert placeholder._state is discarded
                            raise CacheAbandonedError(key=key)
                    assert False, "this line should never be reached"
                else:
                    placeholder = Placeholder(self.__lock)
                    self.__loading[key] = placeholder
                    # The previous line was the point of no return.
                    # Reaching this point means, that we are the thread
                    # which has to do the actual loading. It also means,
                    # that we must never leave this method without properly
                    # cleaning up behind us.

        try:
            value = self.__loader(key)
        except:
            with self.__lock:
                if placeholder._state is loading:
                    # We are still responsible for the placeholder.
                    del self.__loading[key]
                    placeholder._value = sys.exc_info()
                    placeholder._state = failed
                    placeholder._condition.notifyAll()
                    raise CacheLoadError(key, placeholder._value)
                else:
                    # Do not notify the condition variable, since
                    # that should already have been done by whoever
                    # changed the placeholder's state
                    raise CacheAbandonedError(key=key, exc_info=sys.exc_info())
        else:
            with self.__lock:
                if placeholder._state is loading:
                    # We are still responsible for the placeholder.
                    del self.__loading[key]
                    placeholder._value = value
                    placeholder._state = available
                    self.__cache[key] = value
                    placeholder._condition.notifyAll()
                else:
                    # Do not notify the condition variable, since
                    # that should already have been done by whoever
                    # changed the placeholder's state
                    raise CacheAbandonedError(key=key, value=value)
            if value is None:
                return default
            else:
                return value


def identity(value):
    return value

def good(value):
    return True


class DecayingLRUCache(object):

    """Auto-LRU cache with support for stale entry detection

    This class implements a variant of `AutoLRUCache`, which
    also supports the detection of entries, that are too old
    and need to be reloaded even if they are are present.

    The client application needs to provide the following
    parameters:

    - `loader`
      A callable, which is applied to a key value in order
      to load the associated object. This must be a function
      with the signature `lambda key: ...`

    - `tester`
      Is applied to a cached element before that is handed
      out to the caller; if this function returns false, the
      cached element is considered "too old" and dropped from
      the cache. 

    - `key`
      A callable, which is applied to a key value in order 
      to produce a properly hashable value from it. The 
      default key extraction function is `identity`, i.e.,
      we use the supplied key value unchanged.

    - `capacity`
      Maximum number of elements in kept in the LRU cache. The
      cache starts evicting elements, which have not been
      recently accessed, if the number of preserved elements
      reaches this limit.

      Note, that eviction is *not* in any way controlled by
      the `tester` function, but by access order only!

    Note, that unlike `AutoLRUCache`, this class does not
    consider a `None` result from the `loader` function to be
    special in any way. It is up to the `tester` function to
    decide, whether the entry is "good" (i.e., should be 
    reported back to the application) or not (i.e., must be
    reloaded upon access).
    """

    __slots__ = (
        '__weakref__',
        '_DecayingLRUCache__lock',
        '_DecayingLRUCache__cache',
        '_DecayingLRUCache__loader',
        '_DecayingLRUCache__loading',
        '_DecayingLRUCache__tester',
        '_DecayingLRUCache__key',
    )

    def __init__(self, loader, tester=good, key=identity, capacity=1024):

        """Initialize a new instance
        """

        super(DecayingLRUCache, self).__init__()
        self.__lock = Lock()
        self.__cache = LRUDict(capacity)
        self.__loader = loader
        self.__loading = dict()
        self.__tester = tester
        self.__key = key

    def clear(self, discard_loads=False):
        
        """Remove all cached values

        This method removes all values from this cache. If
        `discard_loads`, then the method also forces all currently
        running load operations to fail with a `CacheAbandonedError`.
        Note, that this method has no way of interrupting load
        operations, so all pending operations will have to complete 
        before the discard condition can be detected.
        """

        with self.__lock:
            self.__cache.clear()
            if discard_loads:
                conditions = list()
                keys = tuple(self.__loading.iterkeys())
                for k in keys:
                    placeholder = self.__loading.pop(k)
                    if placeholder._state is loading:
                        placeholder._state = discarded
                        conditions.append(placeholder._condition)
                while conditions:
                    conditions.pop().notifyAll()
                        
    def load(self, key):

        """Load a value 

        Returns the value associated with `key`. If no
        matching value is currently present in this cache,
        or if the value present is considered "too old"
        by the `tester` function, then a value is loaded via 
        the cache's `loader` function.
        """

        loader, tester, keyfn = self.__loader, self.__tester, self.__key
        kref = keyfn(key)

        with self.__lock:
            item = self.__cache.get(kref, missing)
            if item is not missing:
                if tester(item):
                    return item
                else:
                    del self.__cache[kref]
            placeholder = self.__loading.get(kref)
            if placeholder is not None:
                while placeholder._state is loading:
                    placeholder._condition.wait()
                if placeholder._state is failed:
                    raise CacheLoadError(key, placeholder._value)
                else:
                    if placeholder._state is available:
                        return placeholder._value
                    else:
                        assert placeholder._state is discarded
                        raise CacheAbandonedError(key=key)
                assert False, "this line should never be reached"
            else:
                placeholder = Placeholder(self.__lock)
                self.__loading[kref] = placeholder
                # The previous line was the point of no return.
                # Reaching this point means, that we are the thread
                # which has to do the actual loading. It also means,
                # that we must never leave this method without properly
                # cleaning up behind us.
        try:
            value = loader(key)
        except:
            with self.__lock:
                if placeholder._state is loading:
                    # We are still responsible for the placeholder.
                    del self.__loading[kref]
                    placeholder._value = sys.exc_info()
                    placeholder._state = failed
                    placeholder._condition.notifyAll()
                    raise CacheLoadError(key, placeholder._value)
                else:
                    # Do not notify the condition variable, since
                    # that should already have been done by whoever
                    # changed the placeholder's state
                    raise CacheAbandonedError(key=key, exc_info=sys.exc_info())
        else:
            with self.__lock:
                if placeholder._state is loading:
                    # We are still responsible for the placeholder.
                    del self.__loading[kref]
                    placeholder._value = value
                    placeholder._state = available
                    self.__cache[kref] = value
                    placeholder._condition.notifyAll()
                else:
                    # Do not notify the condition variable, since
                    # that should already have been done by whoever
                    # changed the placeholder's state
                    raise CacheAbandonedError(key=key, value=value)
            return value
