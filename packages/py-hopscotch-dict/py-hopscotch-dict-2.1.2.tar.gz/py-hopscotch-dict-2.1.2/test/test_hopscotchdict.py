################################################################################
#                              py-hopscotch-dict                               #
#    Full-featured `dict` replacement with guaranteed constant-time lookups    #
#                 (C) 2017, 2019-2020, 2022-2023  Jeremy Brown                 #
#                Released under Prosperity Public License 3.0.0                #
################################################################################

from operator import itemgetter
from test import dict_keys, dict_values, max_dict_entries, sample_dict

import pytest

from hypothesis import example, given, seed, settings
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule
from hypothesis.strategies import integers

from py_hopscotch_dict import HopscotchDict


def get_displaced_neighbors(hd, lookup_idx):
    result = []

    nbhd = hd._nbhds[lookup_idx]
    for nbhd_idx, neighbor in enumerate(bin(nbhd)[:1:-1]):
        if neighbor == "1":
            result.append((lookup_idx + nbhd_idx) % hd._size)

    return result


@given(sample_dict, integers())
def test_get_open_neighbor(gen_dict, lookup_idx):
    hd = HopscotchDict(gen_dict)

    if lookup_idx < 0 or lookup_idx >= hd._size:
        with pytest.raises(ValueError):
            hd._get_open_neighbor(lookup_idx)
    else:
        open_idx = hd._get_open_neighbor(lookup_idx)

        if open_idx is None:
            open_idx_dist = hd._nbhd_size
        else:
            open_idx_dist = (open_idx - lookup_idx) % hd._size

        for idx in range(open_idx_dist):
            assert hd._indices[(lookup_idx + idx) % hd._size] != hd.FREE_ENTRY


@given(integers(max_value=max_dict_entries))
def test_make_lookup_tables(tbl_size):
    if tbl_size < 0:
        with pytest.raises(ValueError):
            HopscotchDict._make_lookup_tables(tbl_size)
    else:
        indices, nbhds = HopscotchDict._make_lookup_tables(tbl_size)

        if tbl_size.bit_length() < 8:
            index_type = "b"
            nbhd_type = "B"
        elif tbl_size.bit_length() < 16:
            index_type = "h"
            nbhd_type = "H"
        elif tbl_size.bit_length() < 32:
            index_type = "i"
            nbhd_type = "I"
        else:
            index_type = "l"
            nbhd_type = "L"

        assert indices.typecode == index_type
        assert nbhds.typecode == nbhd_type
        assert len(indices) == len(nbhds) == tbl_size


def test_valid_free_up():
    hd = HopscotchDict()
    hd._resize(16)

    for i in range(5, 13):
        hd[i] = f"test_valid_free_up_{i}"

    # Free up already-empty index
    hd._free_up(0)

    # Nothing was stored at the index, so nothing to do
    assert hd._indices[0] == hd.FREE_ENTRY
    assert get_displaced_neighbors(hd, 0) == []

    # Free up index with open neighbor
    hd._free_up(7)

    # Entry originally in index 7 moved to index 13
    assert hd._indices[7] == hd.FREE_ENTRY
    assert hd._indices[13] == 2
    assert get_displaced_neighbors(hd, 7) == [13]

    hd[23] = "test_valid_free_up_23"

    # Free up index with full neighborhood
    hd._free_up(5)

    # Entry originally in index 7 moved to index 14
    assert hd._indices[7] == 0
    assert hd._indices[14] == 8
    assert get_displaced_neighbors(hd, 7) == [13, 14]

    # Entry originally in index 5 moved to index 7
    assert hd._indices[5] == hd.FREE_ENTRY
    assert get_displaced_neighbors(hd, 5) == [7]

    # Free up index with displaced neighbor at end of its neighborhood,
    # Have to move some entry out to do so
    hd._free_up(14)

    # Entry originally in index 14 moved to index 8
    assert hd._indices[14] == hd.FREE_ENTRY
    assert hd._indices[8] == 8
    assert get_displaced_neighbors(hd, 7) == [8, 13]
    assert get_displaced_neighbors(hd, 8) == [15]

    # Free up index with displaced neighbor
    hd._free_up(7)

    # Entry in index 7 originally from index 5,
    # should be back there now
    assert hd._indices[7] == hd.FREE_ENTRY
    assert hd._indices[5] == 0
    assert get_displaced_neighbors(hd, 5) == [5]

    assert hd._size == 16

    hd.clear()
    hd._resize(16)

    for i in range(6):
        hd[i] = f"test_valid_free_up_{i}"

    hd[15] = 15

    # Free up index with neighborhood that wraps around _lookup_tables
    hd._free_up(15)

    # Entry originally in index 15 moved to index 6
    assert hd._indices[15] == hd.FREE_ENTRY
    assert get_displaced_neighbors(hd, 15) == [6]


def test_invalid_free_up():
    hd = HopscotchDict()

    with pytest.raises(ValueError):
        hd._free_up(-1)

    with pytest.raises(ValueError):
        hd._free_up(100)

    for i in range(1, 257, 32):
        hd[i] = f"test_invalid_free_up_{i}"

    with pytest.raises(RuntimeError):
        hd._free_up(1)

    hd.clear()

    hd._resize(16)
    for i in range(12, 125, 16):
        hd[i] = f"test_invalid_free_up_{i}"

    with pytest.raises(RuntimeError):
        hd._free_up(12)

    hd.clear()

    hd._resize(32)

    hd[8] = "test_invalid_free_up_8"
    hd[9] = "test_invalid_free_up_9"
    hd[40] = "test_invalid_free_up_40"

    del hd[40]
    del hd[9]

    for i in range(1, 257, 32):
        hd[i] = f"test_invalid_free_up_{i}"

    with pytest.raises(RuntimeError):
        hd._free_up(1)


@given(dict_keys)
def test_lookup(key):
    hd = HopscotchDict()

    hd[7] = "test_lookup_7"
    hd[15] = "test_lookup_15"

    assert hd._lookup(7) == (7, 0)
    assert hd._lookup(15) == (0, 1)

    del hd[7]
    del hd[15]

    lookup_idx = abs(hash(key)) % hd._size
    hd[key] = True
    assert hd._lookup(key)[0] == lookup_idx


@pytest.mark.parametrize(
    "scenario", ["missing", "free"], ids=["missing-key", "neighbor-previously-freed"]
)
def test_lookup_fails(scenario):
    hd = HopscotchDict()

    if scenario == "missing":
        assert hd._lookup("test_lookup") == (None, None)

    elif scenario == "free":
        hd[4] = "test_lookup"
        hd._indices[4] = hd.FREE_ENTRY

        with pytest.raises(RuntimeError):
            hd._lookup(4)


def test_resize():
    hd = HopscotchDict()

    with pytest.raises(ValueError):
        hd._resize(25)

    with pytest.raises(ValueError):
        hd._resize(2**65)

    for i in range(16):
        hd[i] = i

    hd[132] = 132
    hd._resize(128)
    assert get_displaced_neighbors(hd, 4) == [4, 9]

    hd._resize(512)

    assert hd._nbhd_size == 16

    for i in range(16):
        assert hd[i] == i

    hd.clear()

    for i in range(26, 32):
        hd[i] = i

    for i in range(1, 7):
        hd[i] = i

    hd[7] = 7
    hd[25] = 25
    hd[57] = 57
    hd[0] = 0
    del hd[7]
    hd._resize(32)

    assert get_displaced_neighbors(hd, 25) == [25, 0]
    assert get_displaced_neighbors(hd, 0) == [7]


def test_clear():
    hd = HopscotchDict()

    for i in range(256):
        hd[f"test_clear_{i}"] = i

    hd.clear()

    assert hd._count == 0
    assert hd._size == 8
    assert hd._nbhd_size == 8

    assert len(hd._keys) == 0
    assert len(hd._values) == 0

    for lookup_idx in range(hd._size):
        assert hd._indices[lookup_idx] == hd.FREE_ENTRY
        assert get_displaced_neighbors(hd, lookup_idx) == []


def test_bare_init():
    hd = HopscotchDict()
    assert len(hd) == 0


@given(sample_dict)
def test_list_init(gen_dict):
    items = list(gen_dict.items())
    size = len(gen_dict)
    hd = HopscotchDict(items)
    assert len(hd) == size


@given(sample_dict)
def test_dict_init(gen_dict):
    hd = HopscotchDict(gen_dict)
    assert len(hd) == len(gen_dict)


@pytest.mark.parametrize(
    "scenario",
    ["good-key", "bad-key", "prev-free"],
    ids=["valid-key", "invalid-key", "neighbor-previously-freed"],
)
def test_getitem(scenario):
    hd = HopscotchDict()

    if scenario == "good-key":
        hd["test_getitem"] = True
        assert hd["test_getitem"]

    elif scenario == "bad-key":
        with pytest.raises(KeyError):
            assert hd["test_getitem"]

    elif scenario == "prev-free":
        hd[1] = True
        hd._indices[1] = hd.FREE_ENTRY

        with pytest.raises(RuntimeError):
            assert hd[1]


@given(sample_dict)
def test_setitem_happy_path(gen_dict):
    hd = HopscotchDict()

    for k, v in gen_dict.items():
        hd[k] = v

    assert len(hd) == len(gen_dict)

    for key in gen_dict:
        assert hd[key] == gen_dict[key]
        expected_lookup_idx = abs(hash(key)) % hd._size
        neighbors = get_displaced_neighbors(hd, expected_lookup_idx)
        lookup_idx, _ = hd._lookup(key)
        assert lookup_idx in neighbors


@pytest.mark.parametrize(
    "scenario",
    [
        "overwrite",
        "density_resize",
        "snr",
        "bnr",
        "ovw_err",
        "ins_err",
        "key_coll",
        "free",
    ],
    ids=[
        "overwrite",
        "density-resize",
        "small-nbhd-resize",
        "big-nbhd-resize",
        "overwrite-error",
        "insert-error",
        "degenerate-key-collision",
        "invalid-free-neighbor",
    ],
)
def test_setitem_special_cases(scenario):
    hd = HopscotchDict()

    if scenario == "overwrite":
        hd["test_setitem"] = False
        hd["test_setitem"] = True
        assert len(hd) == 1
        assert hd["test_setitem"]

    elif scenario == "density_resize":
        hd._resize(2**16)

        for i in range(55000):
            hd[i] = i

        assert hd._size == 2**17
        assert len(hd) == 55000
        for i in range(55000):
            assert hd[i] == i

    elif scenario == "free":
        hd[4] = "test_setitem_special_cases"
        hd._indices[4] = hd.FREE_ENTRY

        with pytest.raises(RuntimeError):
            hd[4] = None

    elif scenario == "ovw_err" or scenario == "ins_err":
        if scenario == "ovw_err":
            hd["test_setitem"] = False
        hd["test"] = True
        hd._values.pop()

        with pytest.raises(RuntimeError):
            hd["test_setitem"] = True

    elif scenario == "snr":
        for i in range(10, 17):
            hd[i] = f"test_setitem_{i}"

        assert hd._size == 32

        for i in range(1, 257, 32):
            hd[i] = f"test_setitem_{i}"

        hd[257] = "test_setitem_257"

        assert len(hd) == 16
        assert hd._size == 128

        for i in hd._keys:
            assert hd[i] == f"test_setitem_{i}"

    elif scenario == "bnr":
        for i in range(26250):
            hd[i] = f"test_setitem_{i}"

        assert hd._size == 2**17

        for i in range(30001, 30001 + 32 * 2**17, 2**17):
            hd[i] = f"test_setitem_{i}"

        assert len(hd) == 26282

        hd[4224305] = "test_setitem_4224305"

        assert len(hd) == 26283
        assert hd._size == 2**18

        for i in hd._keys:
            assert hd[i] == f"test_setitem_{i}"

    elif scenario == "key_coll":
        small_key = -1 % 2**33
        large_key = -1 % 2**34

        hd[small_key] = "test_setitem_key_coll_small"
        hd[large_key] = "test_setitem_key_coll_large"

        assert hd._size == 8
        assert hd[small_key] == "test_setitem_key_coll_small"
        assert hd[large_key] == "test_setitem_key_coll_large"


def test_delitem():
    hd = HopscotchDict()

    for i in range(1, 7):
        hd[i] = f"test_delitem_{i}"

    for key in hd._keys:
        _, data_idx = hd._lookup(key)
        assert data_idx == key - 1

    key_struct = [[6, 2, 3, 4, 5], [6, 5, 3, 4], [6, 5, 4], [6, 5], [6], []]

    for i in range(1, 7):
        del hd[i]
        assert hd._keys == key_struct[i - 1]

    for i in range(hd._size):
        assert hd._indices[i] == hd.FREE_ENTRY
        assert get_displaced_neighbors(hd, i) == []

    with pytest.raises(KeyError):
        del hd["test_delitem"]


@given(sample_dict)
@seed(262902792531650980708949300196033766230)
def test_contains_and_has_key(gen_dict):
    hd = HopscotchDict(gen_dict)
    for key in hd._keys:
        assert key in hd

    assert "test_contains" not in hd
    assert not hd.has_key("test_contains")  # noqa

    hd.clear()
    hd[4] = "test_setitem_special_cases"
    hd._indices[4] = hd.FREE_ENTRY

    with pytest.raises(RuntimeError):
        4 in hd


@given(sample_dict)
def test_iter_and_len(gen_dict):
    hd = HopscotchDict(gen_dict)

    count = 0

    for key in hd:
        count += 1

    assert count == len(hd) == len(gen_dict)


@given(sample_dict)
def test_repr(gen_dict):
    hd = HopscotchDict(gen_dict)

    assert eval(repr(hd)) == hd


@pytest.mark.parametrize(
    "scenario",
    ["eq", "bad_type", "bad_len", "bad_keys", "bad_vals"],
    ids=["equal", "type-mismatch", "length-mismatch", "key-mismatch", "value-mismatch"],
)
def test_eq_and_neq(scenario):
    hd = HopscotchDict()
    dc = {}

    for i in range(5):
        hd[f"test_eq_and_neq_{i}"] = i
        dc[f"test_eq_and_neq_{i}"] = i

    if scenario == "bad_len" or scenario == "bad_keys":
        dc.pop("test_eq_and_neq_4")

    if scenario == "bad_keys":
        dc["test_eq_and_neq_5"] = 4

    if scenario == "bad_vals":
        dc["test_eq_and_neq_0"] = False

    if scenario == "bad_type":
        assert hd != dc.items()

    elif scenario != "eq":
        assert hd != dc

    else:
        assert hd == dc


@given(sample_dict)
def test_reversed(gen_dict):
    hd = HopscotchDict(gen_dict)

    keys = hd.keys()
    if not isinstance(keys, list):
        keys = list(keys)

    rev_keys = list(reversed(hd))

    assert len(keys) == len(rev_keys)
    for i in range(len(keys)):
        assert keys[i] == rev_keys[len(keys) - i - 1]


@pytest.mark.parametrize(
    "scenario",
    ["valid-key", "invalid-key", "prev-free"],
    ids=["stored-value", "default-value", "neighbor-previously-freed"],
)
def test_get(scenario):
    hd = HopscotchDict()

    if scenario == "valid-key":
        hd["test_get"] = 1337
        assert hd.get("test_get", 1017) == 1337

    elif scenario == "invalid-key":
        assert hd.get("test_get", 1017) == 1017

    elif scenario == "prev-free":
        idx = abs(hash("test_get")) % hd._size
        hd["test_get"] = False
        hd._indices[idx] = hd.FREE_ENTRY

        with pytest.raises(RuntimeError):
            assert hd.get("test_get", 420)


@pytest.mark.parametrize(
    "scenario",
    ["valid_key", "invalid_key", "default"],
    ids=["valid-key", "invalid-key", "default-value"],
)
def test_pop(scenario):
    hd = HopscotchDict()
    val = None

    if scenario == "valid_key":
        hd["test_pop"] = val = 1337
    else:
        val = 0

    if scenario != "invalid_key":
        assert hd.pop("test_pop", 0) == val
    else:
        with pytest.raises(KeyError):
            hd.pop("test_pop")


@given(sample_dict)
@example({})
def test_popitem(gen_dict):
    hd = HopscotchDict()

    if not gen_dict:
        with pytest.raises(KeyError):
            hd.popitem()
    else:
        hd.update(gen_dict)

        key = hd._keys[-1]
        val = hd._values[-1]

        cur_len = len(hd)
        assert (key, val) == hd.popitem()
        assert len(hd) == cur_len - 1
        assert key not in hd


@pytest.mark.parametrize(
    "existing_key", [True, False], ids=["no-use-default", "use-default"]
)
def test_setdefault(existing_key):
    hd = HopscotchDict()
    val = None

    if existing_key:
        hd["test_setdefault"] = val = 1337
    else:
        val = 1017

    assert hd.setdefault("test_setdefault", 1017) == val


@given(sample_dict)
def test_copy(gen_dict):
    hd = HopscotchDict(gen_dict)

    hdc = hd.copy()

    for key in hd._keys:
        assert id(hd[key]) == id(hdc[key])


@given(sample_dict)
def test_str(gen_dict):
    hd = HopscotchDict(gen_dict)

    assert str(hd) == str(gen_dict)


class HopscotchStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.d = HopscotchDict()

    def teardown(self):
        keys = list(self.d.keys())

        for key in keys:
            del self.d[key]

    @invariant()
    def no_missing_data(self):
        assert len(self.d._keys) == len(self.d._values) == self.d._count

    @invariant()
    def no_duplicate_keys(self):
        assert len(self.d._keys) == len(set(self.d._keys))

    @invariant()
    def valid_indices(self):
        assert len([i for i in self.d._indices if i != -1]) == len(self.d._keys)

    @invariant()
    def valid_neighborhoods(self):
        for idx, nbhd in filter(itemgetter(1), enumerate(self.d._nbhds)):
            for nbhd_idx, neighbor in enumerate(bin(nbhd)[:1:-1]):
                nbr_idx = (idx + nbhd_idx) % self.d._size
                data_idx = self.d._indices[nbr_idx]

                if data_idx != self.d.FREE_ENTRY:
                    nbr_expected_idx = abs(hash(self.d._keys[data_idx])) % self.d._size
                else:
                    nbr_expected_idx = None

                if neighbor == "1":
                    assert nbr_expected_idx == idx

                elif nbr_expected_idx is not None:
                    assert nbr_expected_idx != idx

    @invariant()
    def bounded_density(self):
        if self.d._count > 0:
            assert self.d._count / self.d._size <= self.d.MAX_DENSITY

    @rule(k=dict_keys, v=dict_values)
    def add_entry(self, k, v):
        self.d[k] = v

    @rule(k=dict_keys)
    def remove_entry(self, k):
        if k not in self.d._keys:
            with pytest.raises(KeyError):
                del self.d[k]
        else:
            del self.d[k]


HopscotchStateMachine.TestCase.settings = settings(max_examples=50, deadline=None)
test_hopscotch_dict = HopscotchStateMachine.TestCase
