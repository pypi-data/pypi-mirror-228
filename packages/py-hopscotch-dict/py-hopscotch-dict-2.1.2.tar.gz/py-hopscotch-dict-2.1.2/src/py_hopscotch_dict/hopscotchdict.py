################################################################################
#                              py-hopscotch-dict                               #
#    Full-featured `dict` replacement with guaranteed constant-time lookups    #
#                 (C) 2017, 2019-2020, 2022-2023  Jeremy Brown                 #
#                Released under Prosperity Public License 3.0.0                #
################################################################################

from __future__ import annotations

from array import array
from collections.abc import (
    Hashable,
    ItemsView,
    Iterator,
    KeysView,
    MutableMapping,
    ValuesView,
)
from sys import maxsize
from typing import Any, Optional, cast

from py_hopscotch_dict.views import HDItems, HDKeys, HDValues


class HopscotchDict(MutableMapping[Hashable, Any]):
    # Prevent default creation of __dict__, which should save space if
    # many instances of HopscotchDict are used at once
    __slots__ = (
        "_count",
        "_keys",
        "_indices",
        "_nbhd_size",
        "_nbhds",
        "_size",
        "_values",
    )

    # Python ints are signed, add one to get word length
    MAX_NBHD_SIZE = maxsize.bit_length() + 1

    # Only allow neighborhood sizes that match word lengths
    ALLOWED_NBHD_SIZES = {8, 16, 32, 64}

    # Sentinel value used in indices table to denote we can put value here
    FREE_ENTRY = -1

    # Maximum allowed density before resizing
    MAX_DENSITY = 0.8

    @staticmethod
    def _make_lookup_tables(table_size: int) -> tuple[array[int], array[int]]:
        """
        Make the arrays that hold the indices into _keys/_values and the
        neighborhoods for each index

        :param table_size: The number of entries of the returned table

        :return: An `array` for storing indices into _keys/_values,
                 and an `array` for storing each index's neighborhood
        """
        if table_size < 0:
            raise ValueError("Lookup table cannot have negative length")

        table_log_size = table_size.bit_length()

        if table_log_size < 8:
            index_fmt = "b"
            nbhd_fmt = "B"
        elif table_log_size < 16:
            index_fmt = "h"
            nbhd_fmt = "H"
        elif table_log_size < 32:
            index_fmt = "i"
            nbhd_fmt = "I"
        else:
            index_fmt = "l"  # pragma: no cover
            nbhd_fmt = "L"  # pragma: no cover

        lookup_table = array(index_fmt, (HopscotchDict.FREE_ENTRY,) * table_size)
        nbhd_table = array(nbhd_fmt, (0,) * table_size)

        return (lookup_table, nbhd_table)

    def clear(self) -> None:
        """
        Remove all the data from the dict and return it to its original
        size
        """
        self._indices: array[int]
        self._nbhds: array[int]

        # The maximum number of entries in the dict
        self._size = 8

        # The current number of entries in the dict
        self._count = 0

        # The maximum number of neighbors to check if a key isn't
        # in its expected index
        self._nbhd_size = 8

        # Stored values
        if hasattr(self, "_values"):
            del self._values
        self._values: list[Any] = []

        # Stored keys
        if hasattr(self, "_keys"):
            del self._keys
        self._keys: list[Hashable] = []

        # Data structure storing map from each entry's presence
        # to its location in _keys/_values
        if hasattr(self, "_indices"):
            del self._indices

        # Data structure storing location of each index's displaced neighbors
        if hasattr(self, "_nbhds"):
            del self._nbhds

        self._indices, self._nbhds = self._make_lookup_tables(self._size)

    def _free_up(self, target_idx: int) -> None:
        """
        Create an opening in the neighborhood of the given index
        by moving data from an index out to one of its neighbors

        :param target_idx: The index in _indices to find
                           a neighborhood opening for
        """
        if target_idx < 0:
            raise ValueError("Indexes cannot be negative")
        elif target_idx >= self._size:
            raise ValueError(f"Index {target_idx} outside array")

        # Attempting to free an empty index is a no-op
        if self._indices[target_idx] == self.FREE_ENTRY:
            return

        lookup_idx = target_idx
        while lookup_idx < self._size:
            lookup_data_idx = self._indices[lookup_idx]
            if lookup_data_idx != self.FREE_ENTRY:
                entry_expected_idx = abs(hash(self._keys[lookup_data_idx])) % self._size
            else:
                entry_expected_idx = None

            # It is possible the entry at target_idx in _indices is a displaced
            # neighbor of some prior index; if that's the case see if there is an
            # open neighbor of that prior index that the entry at target_idx can be
            # shifted to
            if entry_expected_idx != lookup_idx and lookup_idx == target_idx:
                entry_expected_idx = cast(int, entry_expected_idx)
                expected_nbr = self._get_open_neighbor(entry_expected_idx)

                if expected_nbr is not None:
                    data_idx = self._indices[lookup_idx]
                    exp_tgt_nbhd_idx = (lookup_idx - entry_expected_idx) % self._size
                    exp_opn_nbhd_idx = (expected_nbr - entry_expected_idx) % self._size

                    self._indices[expected_nbr] = data_idx
                    self._indices[lookup_idx] = self.FREE_ENTRY

                    # Mark the neighbor the index originally stored at lookup_idx
                    # was moved to as occupied
                    self._nbhds[entry_expected_idx] |= 1 << exp_opn_nbhd_idx

                    # Mark the neighbor originally storing the value at lookup_idx
                    # as free
                    self._nbhds[entry_expected_idx] &= ~(1 << exp_tgt_nbhd_idx)
                    return

            # Walking down the array for an empty spot and shuffling entries around
            # is the only way
            open_idx = self._get_open_neighbor(lookup_idx)

            # All of the next _nbhd_size - 1 locations in _indices are full
            if open_idx is None:
                lookup_idx += self._nbhd_size
                continue

            # Go _nbhd_size - 1 locations back in _indices from the open
            # location to find a neighbor that can be displaced into the opening
            if (open_idx - target_idx) % self._size >= self._nbhd_size:
                range_start = open_idx - self._nbhd_size + 1
                disp_range = self._nbhd_size

            elif entry_expected_idx is not None and entry_expected_idx != lookup_idx:
                range_start = open_idx - self._nbhd_size + 1
                disp_range = self._nbhd_size

            else:
                range_start = lookup_idx
                disp_range = (open_idx - lookup_idx) % self._size

            for displacement in range(disp_range):
                disp_root = (range_start + displacement) % self._size

                displaceable_nbr = None
                nbhd = self._nbhds[disp_root]
                for nbhd_idx, nbr in enumerate(bin(nbhd)[:1:-1]):
                    # There is an entry before the open location which can be
                    # shuffled into the open location
                    if nbr == "1":
                        nbr_idx = (disp_root + nbhd_idx) % self._size

                        if nbhd_idx < (open_idx - disp_root) % self._size:
                            displaceable_nbr = nbr_idx
                            break

                # There is an entry before the open location which can be
                # shuffled into the open location
                if displaceable_nbr is not None:
                    data_idx = self._indices[displaceable_nbr]
                    self._indices[open_idx] = data_idx
                    self._indices[displaceable_nbr] = self.FREE_ENTRY

                    disp_nbhd_idx = (displaceable_nbr - disp_root) % self._size
                    open_nbhd_idx = (open_idx - disp_root) % self._size

                    # Mark the displaced neighbor's new location as occupied
                    self._nbhds[disp_root] |= 1 << open_nbhd_idx

                    # Mark the displaced neighbor's original location as free
                    self._nbhds[disp_root] &= ~(1 << disp_nbhd_idx)

                    # If we must displace an entry before target_idx into a location
                    # after target_idx, don't update the index we still want to free
                    if (displaceable_nbr - target_idx) % self._size < self._nbhd_size:
                        lookup_idx = target_idx

                    elif displaceable_nbr >= target_idx:
                        lookup_idx = displaceable_nbr
                    break

                # If the last index before the open index has no displaced
                # neighbors or its closest one is after the open index, every
                # index between the given index and the open index is filled
                # with data displaced from other indices, and the invariant
                # cannot be maintained without a resize
                elif disp_root == open_idx - 1:
                    raise RuntimeError("No space available before open index")

            if self._indices[target_idx] == self.FREE_ENTRY:
                return

        # No open indices exist between the given index and the end of the array
        raise RuntimeError("Could not open index while maintaining invariant")

    def _get_open_neighbor(self, lookup_idx: int) -> Optional[int]:
        """
        Find the first neighbor of the given index that is not in use

        :param lookup_idx: _indices index to find an open neighbor
                           for

        :return: The index in _indices nearest to the given index
                 not currently in use, or None if they are all occupied
        """
        if lookup_idx < 0:
            raise ValueError("Indexes cannot be negative")
        elif lookup_idx >= self._size:
            raise ValueError(f"Index {lookup_idx} outside array")

        result = None

        for idx in range(self._nbhd_size):
            nbr = (lookup_idx + idx) % self._size
            if self._indices[nbr] == self.FREE_ENTRY:
                result = nbr
                break

        return result

    def _lookup(self, key: Hashable) -> tuple[Optional[int], Optional[int]]:
        """
        Find the indices in _indices and _keys that correspond to
        the given key

        :param key: The key to search for

        :return: The index in _indices that holds the index to
                 _keys for the given key and the index to _keys,
                 or None for both if the key has not been inserted
        """
        data_idx = None
        lookup_idx = None
        target_idx = abs(hash(key)) % self._size

        nbhd = self._nbhds[target_idx]
        for nbhd_idx, nbr in enumerate(bin(nbhd)[:1:-1]):
            if nbr == "1":
                neighbor = (target_idx + nbhd_idx) % self._size
                nbr_data_idx = self._indices[neighbor]

                if nbr_data_idx < 0:
                    raise RuntimeError(
                        (
                            "Index {} has supposed displaced neighbor that points to "
                            "free index"
                        ).format(target_idx)
                    )

                if self._keys[nbr_data_idx] == key:
                    data_idx = nbr_data_idx
                    lookup_idx = neighbor
                    break

        return (lookup_idx, data_idx)

    def _resize(self, new_size: int) -> None:
        """
        Resize the dict and relocate the current entries

        :param new_size: The desired new size of the dict
        """
        # Dict size is a power of two to make modulo operations quicker
        if new_size & new_size - 1:
            raise ValueError("New size for dict not a power of 2")

        # Neighborhoods must be at least as large as the base-2 logarithm of
        # the dict size

        # 2**k requires k+1 bits to represent, so subtract one
        resized_nbhd_size = new_size.bit_length() - 1

        if resized_nbhd_size > self._nbhd_size:
            if resized_nbhd_size > self.MAX_NBHD_SIZE:
                raise ValueError("Resizing requires too-large neighborhood")
            self._nbhd_size = min(
                s for s in self.ALLOWED_NBHD_SIZES if s >= resized_nbhd_size
            )

        self._size = new_size
        self._indices, self._nbhds = self._make_lookup_tables(new_size)

        for data_idx, key in enumerate(self._keys):
            found_nbr = False
            home_idx = abs(hash(key)) % new_size

            for offset in range(self._nbhd_size):
                nbr = (home_idx + offset) % self._size
                if self._indices[nbr] == self.FREE_ENTRY:
                    # Mark the neighbor storing the entry index as occupied
                    self._nbhds[home_idx] |= 1 << offset
                    self._indices[nbr] = data_idx
                    found_nbr = True
                    break

            if not found_nbr:
                free_up_idx = 0 if new_size - home_idx < self._nbhd_size else home_idx
                self._free_up(free_up_idx)

                for offset in range(self._nbhd_size):
                    nbr = (home_idx + offset) % self._size
                    if self._indices[nbr] == self.FREE_ENTRY:
                        # Mark the neighbor storing the entry index as occupied
                        self._nbhds[home_idx] |= 1 << offset
                        self._indices[nbr] = data_idx
                        break

    def copy(self) -> MutableMapping[Hashable, Any]:
        """
        Create a new instance with all items inserted
        """
        out = HopscotchDict()

        for key in self._keys:
            out[key] = self.__getitem__(key)

        return out

    def get(self, key: Hashable, default: Any = None) -> Any:
        """
        Retrieve the value corresponding to the specified key,
        returning the default value if not found

        :param key: The key to retrieve data from
        :param default: Value to return if the given key does not exist

        :returns: The value in the dict if the specified key exists;
                  the default value if it does not
        """
        value = default
        target_idx = abs(hash(key)) % self._size

        nbhd = self._nbhds[target_idx]
        for nbhd_idx, nbr in enumerate(bin(nbhd)[:1:-1]):
            if nbr == "1":
                neighbor = (target_idx + nbhd_idx) % self._size
                nbr_data_idx = self._indices[neighbor]

                if nbr_data_idx < 0:
                    raise RuntimeError(
                        (
                            "Index {} has supposed displaced neighbor that points to "
                            "free index"
                        ).format(target_idx)
                    )

                if self._keys[nbr_data_idx] == key:
                    value = self._values[nbr_data_idx]
                    break
        return value

    def has_key(self, key: Hashable) -> bool:
        """
        Check if the given key exists

        :param key: The key to check for existence

        :returns: True if the key exists; False if it does not
        """
        return self.__contains__(key)

    def keys(self) -> KeysView[Hashable]:
        """
        An iterator over all keys in the dict

        :returns: An iterator over self._keys
        """
        return HDKeys(self)

    def values(self) -> ValuesView[Any]:
        """
        An iterator over all values in the dict

        :returns: An iterator over self._values
        """
        return HDValues(self)

    def items(self) -> ItemsView[Hashable, Any]:
        """
        An iterator over all `(key, value)` pairs

        :returns: An iterator over the `(key, value)` pairs
        """
        return HDItems(self)

    def pop(self, key: Hashable, default: Any = None) -> Any:
        """
        Return the value associated with the given key and removes it if
        the key exists; returns the given default value if the key does
        not exist; errors if the key does not exist and no default value
        was given

        :param key: The key to search for
        :param default: Value to return if the given key does not exist

        :returns: The value associated with the key if it exists,
                  the default value if it does not
        """
        out = default
        try:
            out = self.__getitem__(key)
        except KeyError:
            if default is None:
                raise
        else:
            self.__delitem__(key)
        return out

    def popitem(self) -> tuple[Hashable, Any]:
        """
        Remove an arbitrary `(key, value)` pair if one exists,
        erroring otherwise

        :returns: An arbitrary `(key, value)` pair from the dict
                  if one exists
        """
        if not len(self):
            raise KeyError
        else:
            key = self._keys[-1]
            val = self.pop(self._keys[-1])
            return (key, val)

    def setdefault(self, key: Hashable, default: Any = None) -> Any:
        """
        Return the value associated with the given key if it exists,
        set the value associated with the given key to the default value
        if it does not

        :param key: The key to search for
        :param default: The value to insert if the key does not exist

        :returns: The value associated with the given key if it exists,
                  the default value otherwise
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            self.__setitem__(key, default)
            return default

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Create a new instance with any specified values
        """
        # Use clear function to do initial setup for new tables
        if not hasattr(self, "_size"):
            self.clear()

        self.update(*args, **kwargs)

    def __getitem__(self, key: Hashable) -> Any:
        """
        Retrieve the value associated with the given key,
        erroring if the key does not exist

        :param key: The key to search for

        :returns: The value associated with the given key
        """
        target_idx = abs(hash(key)) % self._size

        nbhd = self._nbhds[target_idx]
        for nbhd_idx, nbr in enumerate(bin(nbhd)[:1:-1]):
            if nbr == "1":
                neighbor = (target_idx + nbhd_idx) % self._size
                nbr_data_idx = self._indices[neighbor]

                if nbr_data_idx < 0:
                    raise RuntimeError(
                        (
                            "Index {} has supposed displaced neighbor that points to "
                            "free index"
                        ).format(target_idx)
                    )

                if self._keys[nbr_data_idx] == key:
                    return self._values[nbr_data_idx]

        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """
        Map the given key to the given value, overwriting any
        previously-stored value if it exists

        :param key: The key to set
        :param value: The value to map the key to
        """
        # The index key should map to in _indices if it hasn't been evicted
        expected_lookup_idx = abs(hash(key)) % self._size

        # Where to check if the key has been inserted previously
        nbhd = self._nbhds[expected_lookup_idx]

        open_neighbor = None
        already_inserted = False

        # # Note the closest open neighbor if insertion is necessary
        for offset in range(self._nbhd_size):
            nbr = (expected_lookup_idx + offset) % self._size
            data_idx = self._indices[nbr]

            if data_idx == self.FREE_ENTRY:
                open_neighbor = nbr
                break

        # Check if the key already exists in the dict;
        # overwrite with new value
        for offset, occupied in enumerate(bin(nbhd)[:1:-1]):
            if occupied == "1":
                neighbor = (expected_lookup_idx + offset) % self._size
                data_idx = self._indices[neighbor]

                if data_idx < 0:
                    raise RuntimeError(
                        (
                            "Index {} has supposed displaced neighbor that points to "
                            "free index"
                        ).format(neighbor)
                    )

                if self._keys[data_idx] == key:
                    self._values[data_idx] = value
                    already_inserted = True
                    break

        if not already_inserted:
            # Insert the item in the open neighbor found earlier
            if open_neighbor is not None:
                offset = (open_neighbor - expected_lookup_idx) % self._size
                # Mark the neighbor storing the entry index as occupied
                self._nbhds[expected_lookup_idx] |= 1 << offset
                self._indices[open_neighbor] = self._count
                self._keys.append(key)
                self._values.append(value)
                self._count += 1

            # Free up a neighbor of the expected index to accomodate the new
            # item
            else:
                try:
                    self._free_up(expected_lookup_idx)

                # No way to keep neighborhood invariant, must resize first
                except RuntimeError:
                    if self._size < 2**16:
                        self._resize(self._size * 4)
                    else:
                        self._resize(self._size * 2)

                # There should now be an available neighbor of the expected index,
                # try again
                finally:
                    self.__setitem__(key, value)
                    return

        if len(self._keys) != len(self._values):
            raise RuntimeError(
                ("Number of keys {}; " "number of values {}; ").format(
                    len(self._keys), len(self._values)
                )
            )

        if self._count / self._size >= self.MAX_DENSITY:
            if self._size < 2**16:
                self._resize(self._size * 4)
            else:
                self._resize(self._size * 2)

    def __delitem__(self, key: Hashable) -> None:
        """
        Remove the given key from the dict and its associated value

        :param key: The key to remove from the dict
        """
        # The index key should map to in _indices if it hasn't been evicted
        expected_lookup_idx = abs(hash(key)) % self._size

        # The index key actually maps to in _indices,
        # and the index its related value maps to in _values
        lookup_idx, data_idx = self._lookup(key)

        # Key not in dict
        if data_idx is None:
            raise KeyError(key)

        else:
            # If the key and its associated value aren't the last entries in
            # their respective lists, swap with the last entries to not leave a
            # hole in said lists
            lookup_idx = cast(int, lookup_idx)

            if data_idx != self._count - 1:
                tail_key = self._keys[-1]
                tail_val = self._values[-1]
                tail_lookup_idx, _ = self._lookup(tail_key)
                # Move the data to be removed to the end of each list and update
                # indices
                self._keys[data_idx] = tail_key
                self._values[data_idx] = tail_val
                self._indices[cast(int, tail_lookup_idx)] = data_idx

            # Update the neighborhood of the index the key to be removed is
            # supposed to point to, since the key to be removed must be
            # somewhere in it
            nbhd_idx = (lookup_idx - expected_lookup_idx) % self._size
            self._nbhds[expected_lookup_idx] &= ~(1 << nbhd_idx)

            # Remove the last item from the variable tables, either the actual
            # data to be removed or what was originally at the end before
            # it was copied over the data to be removed
            del self._keys[-1]
            del self._values[-1]
            self._indices[lookup_idx] = self.FREE_ENTRY
            self._count -= 1

    def __contains__(self, key: Hashable) -> bool:
        """
        Check if the given key exists

        :returns: True if the key exists, False otherwise
        """
        result = False
        home_idx = abs(hash(key)) % self._size

        nbhd = self._nbhds[home_idx]
        for nbhd_idx, nbr in enumerate(bin(nbhd)[:1:-1]):
            if nbr == "1":
                neighbor = (home_idx + nbhd_idx) % self._size
                data_idx = self._indices[neighbor]

                if data_idx < 0:
                    raise RuntimeError(
                        (
                            "Index {} has supposed displaced neighbor that points to "
                            "free index"
                        ).format(home_idx)
                    )

                if self._keys[data_idx] == key:
                    result = True
                    break

        return result

    def __eq__(self, other: Any) -> bool:
        """
        Check if the given object is equivalent to this dict

        :param other: The object to test for equality to this dict

        :returns: True if the given object is equivalent to this dict,
                  False otherwise
        """
        if not isinstance(other, MutableMapping):
            return False

        if len(self) != len(other):
            return False

        if set(self._keys) ^ set(other.keys()):
            return False

        return all(
            self[k] == other[k] and type(self[k]) == type(other[k])  # noqa
            for k in self._keys
        )

    def __iter__(self) -> Iterator[Hashable]:
        """
        Return an iterator over the keys

        :returns An iterator over the keys
        """
        return iter(self._keys)

    def __len__(self) -> int:
        """
        Return the number of items currently stored

        :returns: The number of items currently stored
        """
        return self._count

    def __ne__(self, other: Any) -> bool:
        """
        Check if the given object is not equivalent to this dict

        :param other: The object to test for equality to this dict

        :returns: True if the given object is not equivalent to this
                  dict, False otherwise
        """
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """
        Return a representation that could be used to create an
        equivalent dict using `eval()`

        :returns: A string that could be used to create an equivalent
                  representation
        """
        stringified = [
            f"{key!r}: {val!r}" for (key, val) in zip(self._keys, self._values)
        ]
        return f"HopscotchDict({{{', '.join(stringified)}}})"

    def __reversed__(self) -> Iterator[Hashable]:
        """
        Return an iterator over the keys in reverse order

        :returns: An iterator over the keys in reverse order
        """
        return reversed(self._keys)

    def __str__(self) -> str:
        """
        Return a simpler representation of the items in the dict

        :returns: A string containing all items in the dict
        """
        stringified = [
            f"{key!r}: {val!r}" for (key, val) in zip(self._keys, self._values)
        ]
        return f"{{{', '.join(stringified)}}}"
