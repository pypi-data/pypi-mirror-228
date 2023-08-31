# This file is part of project py-tailwind-utils
#
# Copyright (c) [2023] by Monallabs.in.
# This file is released under the MIT License.
#
# Author(s): Kabira K. (webworks.monallabs.in).
# MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""wrapper over dpath.util to 
"""
import logging
import os

if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


from dpath import (
    get as dpath_get,
    new as dpath_new,
    delete as dpath_delete,
)
from addict_tracking_changes import Dict
from collections import UserList


def dget(dictobj, dpath):
    dictval = dictobj
    if not dpath:
        return dictval
    if dpath == "/":
        return dictval
    for key in dpath.split("/")[1:]:
        if type(dictval) == list or isinstance(dictval, UserList):
            dictval = dictval[int(key)]
            pass
        else:
            dictval = dictval[key]

    return dictval


# def dget(dictobj, dpath):
#     return dpath_get(dictobj, dpath)


# def dnew(dictobj, dpath, value):
#     if '[' in dpath and ']' in dpath:
#         raise ValueError(f"cannot process array in {dpath}")

#     dpath_new(dictobj, dpath, value)

# def dnew(dictobj, dpath, value):
#     """
#     needs to work with dicts and arrays
#     """
#     keyidxs = dpath.split("/")[1:]
#     nextidx = keyidxs[1:]

#     dictval = dictobj
#     for_next_round = None
#     for keyidx, next_keyidx in zip(keyidxs, nextidx):
#         keyidx_is_idx = False
#         next_keyidx_is_idx = False
#         try:
#             key_int = int(keyidx)
#             keyidx_is_idx = True
#         except:
#             pass

#         try:
#             key_int = int(next_keyidx)
#             next_keyidx_is_idx = True
#         except:
#             pass


#         match keyidx_is_idx, next_keyidx_is_idx:
#             case False, False:
#                 if  for_next_round is None:
#                     for_next_round= (dictval, keyidx)
#                     dictval = dictval[keyidx]
#                 else:
#                     dictval = for_next_round[0]


#                 pass
#             case False, True:
#                 if keyidx in dictval:
#                     assert isinstance(dictval[keyidx], UserList) or isinstance(dictval[keyidx], list)
#                     assert len(dictval[keyidx]) > int(next_keyidx)
#                     for_next_round = (dictval, keyidx)
#                     dictval = dictval[keyidx]

#                 else:
#                     dictval[keyidx] = [Stub(None)] * (int(next_keyidx) +1) #[None] * (int(next_keyidx) +1)
#                     for_next_round= (dictval, keyidx)
#                     dictval = dictval[keyidx]

#                 pass

#             case True, False:
#                 for_next_round = (dictval, int(keyidx))
#                 dictval = dictval[int(keyidx)]

#                 pass

#             case True, True:
#                 for_next_round = (dictval, int(keyidx))
#                 dictval = dictval[int(keyidx)]
#                 raise ValueError("Array within array not allowed")
#                 pass

#     # ===================== finally set the value ====================
#     keyidx_is_idx = False
#     keyidx = keyidxs[-1]
#     try:
#         keyidx = int(keyidx)
#         keyidx_is_idx = True
#     except:
#         pass

#     dictval[keyidx] = value


def dsearch(tdict, dpath):
    """
    Only first matching path is returned.
    what works and not works:
    straightforward search "/a/b/c/d" should work
    search path with * willl work /*/a/b/*/c"
    list index should work as well /a/b/0/

    """

    def dsearch_recurse(dlobj, steps):
        curr_keyidx = steps[0]
        curr_keyidx_is_idx = False
        try:
            curr_keyidx = int(curr_keyidx)
            curr_keyidx_is_idx = True
        except:
            pass

        if curr_keyidx_is_idx:
            assert isinstance(dlobj, list) or isinstance(dlobj, UserList)
            if len(dlobj) > curr_keyidx:
                # steps.pop(0)
                if steps:
                    yield from dsearch_recurse(dlobj[curr_keyidx], steps[1:])
                else:
                    yield dlobj[curr_keyidx]
            else:
                return None
        else:
            if isinstance(dlobj, list) or isinstance(dlobj, UserList):
                return None

            if curr_keyidx in dlobj:
                if len(steps) > 1:
                    yield from dsearch_recurse(dlobj[curr_keyidx], steps[1:])
                else:
                    yield dlobj[curr_keyidx]
            elif curr_keyidx == "*":
                if len(steps) > 1:
                    for key in dlobj.keys():
                        yield from dsearch_recurse(dlobj[key], steps[1:])
                else:
                    assert False
            else:
                return None

    keyidxs = dpath.split("/")[1:]
    return dsearch_recurse(tdict, keyidxs)


def dnew(tdict, dpath, value):
    def dnew_recurse(dlobj, keyidx_pair_seq):
        # print ("start dnew_recurse----------------------------> ")
        curr_keyidx, next_keyidx = keyidx_pair_seq[0]
        curr_keyidx_is_idx = False
        try:
            curr_keyidx = int(curr_keyidx)
            curr_keyidx_is_idx = True
        except:
            pass

        next_keyidx_is_idx = False
        try:
            next_keyidx = int(next_keyidx)
            next_keyidx_is_idx = True
        except:
            pass

        match curr_keyidx_is_idx, next_keyidx_is_idx:
            case False, False:
                # value is a dict
                childobj = dlobj[curr_keyidx]
                pass
            case False, True:
                if curr_keyidx in dlobj:
                    assert isinstance(dlobj[curr_keyidx], list) or isinstance(
                        dlobj[curr_keyidx], UserList
                    )
                    assert len(dlobj[curr_keyidx]) > next_keyidx
                    childobj = dlobj[curr_keyidx]
                else:
                    dlobj[curr_keyidx] = [None] * (int(next_keyidx) + 1)
                    childobj = dlobj[curr_keyidx]
            case True, False:
                assert isinstance(dlobj, list) or isinstance(dlobj, UserList)
                if dlobj[curr_keyidx]:
                    childobj = dlobj[curr_keyidx]
                    assert (childobj, dict)
                else:
                    # We are not sure if we want to turn on tracking changes by default
                    dlobj[curr_keyidx] = Dict(track_changes=True)
                    childobj = dlobj[curr_keyidx]
            case True, True:
                assert isinstance(dlobj, list)
                if dlobj[curr_keyidx]:
                    childobj = dlobj[curr_keyidx]
                    assert isinstance(childobj, list) or isinstance(childobj, UserList)
                else:
                    dlobj[curr_keyidx] = [None] * (int(next_keyidx) + 1)
                    childobj = dlobj[curr_keyidx]

            case _:
                raise ValueError("Not implemented yet")
        keyidx_pair_seq.pop(0)
        # print ("end dnew_recurse----------------------------> ")
        if keyidx_pair_seq:
            return dnew_recurse(childobj, keyidx_pair_seq)
        else:
            return childobj

    keyidxs = dpath.split("/")[1:]
    nextidx = keyidxs[1:]
    curr_next_pairs = [_ for _ in zip(keyidxs, nextidx)]
    if curr_next_pairs:
        terminal_obj = dnew_recurse(tdict, curr_next_pairs)

    else:
        terminal_obj = tdict

    keyidx = keyidxs[-1]
    keyidx_is_idx = False
    try:
        keyidx = int(keyidx)
        keyidx_is_idx = True
        assert isinstance(terminal_obj, list)
    except:
        pass

    terminal_obj[keyidx] = value


# def dpop(addict, dpath):
#     assert(dpath[-1] != '/')
#     pk = dpath.split("/")
#     ppath = "/".join(pk[:-1])
#     pkey = pk[-1]
#     pnode = addict
#     if ppath != "":
#         pnode = dget(addict, ppath)
#     pnode.pop(pkey, None)


def dpop(dictobj, dpath):
    if "[" in dpath and "]" in dpath:
        raise ValueError(f"cannot process array in {dpath}")

    dpath_delete(dictobj, dpath)


def list_walker(alist, ppath="", guards=None, internal=False):
    """
    to be used in conjuction with walker; navigates the list
    part of the dict.
    todo; make guards over list part
    """
    if internal:
        yield (f"{ppath}/__arr", len(alist))
    for i, value in enumerate(alist):
        if isinstance(value, dict):
            yield from walker(value, ppath + f"/{i}", guards=guards, internal=internal)
        elif isinstance(value, list):
            yield from list_walker(
                value, ppath + f"/{i}", guards=guards, internal=internal
            )


def walker(adict, ppath="", guards=None, internal=False):
    """
    if internal is True; __arr path will be exposed

    """
    for key, value in adict.items():
        try:
            if guards:
                if f"{ppath}/{key}" in guards:
                    logger.debug(f"stoping at guard for {key}")
                    yield (f"{ppath}/{key}", value)
                    continue  # stop at the guard
            if isinstance(value, dict):
                yield from walker(
                    value, ppath + f"/{key}", guards=guards, internal=internal
                )
            elif isinstance(value, list):
                yield from list_walker(
                    value, ppath + f"/{key}", guards=guards, internal=internal
                )

            else:
                yield (f"{ppath}/{key}", value)
                pass

        except Exception as e:
            print(f"in walker exception {ppath} {key} {e}")
            raise e


def stitch_from_dictiter(from_iter):
    """create/stitch a dictionary back from paths obtained from from_dictwalker after applying
    filter
    """
    res_dict = Dict()
    # arr_kpaths = {}
    for kpath, val in from_iter:
        if "__arr" in kpath:
            # TODO: not the best approach; use list constructor
            logger.debug(f"arr_create {kpath[:-6]}")
            dnew(res_dict, kpath[:-6], [Dict() for _ in range(val)])
            # arr_kpaths[kpath] = dget(res_dict, kpath)
            logger.debug(f"saw __arr in {kpath}")
        else:
            if val is not None:
                # if kpath in arr_kpaths:
                #     ppath, idx = get_path_idx(kpath)
                #     arr_kpaths[ppath].apppend(val)
                dnew(res_dict, kpath, val)
    return res_dict


def dupdate(addict, path, value):
    # TODO : think carefully about this
    # print("change history = ", [_ for _ in addict.get_changed_history()])
    dnew(addict, path, value)
    # print("change history = ", [_ for _ in addict.get_changed_history()])


#     # skip if path not already present
#     print (f"dupdate: updating {path} with {value}")
#     try:
#         dpop(addict, path)

#     except Exception as e:
#         logger.debug(f"path {path} not present..skipping")
#         #raise e
#     dnew(addict, path, value)
