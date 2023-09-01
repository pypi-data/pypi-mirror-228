import pickle
import types
import contextlib

from .utils import  __VERSION__ as PAK_VERSION
import hashlib


def _hash_state(state):
    """Generate a hash of the state of a PAK object."""
    return hashlib.sha256(str(state).encode()).hexdigest()

def _sweep(pak):
    """Remove empty PAK objects from a PAK object."""
    for k, v in pak.__dict__.copy().items():
        if isinstance(v, PAK):
            _sweep(v)
            if not v:
                del pak.__dict__[k]
    return pak


# this is a requested feature from the original pak.py
# this is just a stripped down version of pak.py
# with no encryption, compression, or hashing


class PAK(types.SimpleNamespace):
    """This is the core of the PAK system. It is a recursive namespace that can be pickled and encrypted."""

    def __getattr__(self, item):
        """If the attribute does not exist, create a new PAK object."""
        return self.__dict__.setdefault(item, PAK())

    def __reduce_ex__(self, protocol):
        """Reduce the PAK object to a picklable state.
            Injects the version and hash of the state into the state itself.
        """
        state = _sweep(self).__dict__.copy()
        state.update(__hash__ = _hash_state(state), __version__ = PAK_VERSION)
        return (PAK, (), state)

    def __setstate__(self, state):
        """Restore the PAK object from a pickled state.
            Checks the version and hash of the state before restoring.
        """
        if not all(a >= b for a, b in zip(state.pop("__version__"), PAK_VERSION)):
            raise ValueError("Invalid version")
        if state.pop("__hash__") != _hash_state(state):
            raise ValueError("Invalid hash")
        self.__dict__.update(state)

    def __bytes__(self):
        """Convert the PAK object to bytes."""
        return pickle.dumps(self)

    def __new__(cls, *args, **kwargs):
        """Create a new PAK object from bytes or kwargs."""
        if args and isinstance(args[0], bytes):
            return pickle.loads(args[0])
        else:
            return super().__new__(cls)

    def __init__(self, *_, **kwargs):
        super().__init__(**kwargs)

    def __contains__(self, key):
        return key in self.__dict__

    def __bool__(self):
        return bool(self.__dict__)

    __getitem__ = __getattr__
    __setitem__ = types.SimpleNamespace.__setattr__
    __delitem__ = types.SimpleNamespace.__delattr__

def save_pak(pak, path):
    with open(path, "wb") as f:
        f.write(bytes(pak))
        
def load_pak(path):
    try:
        with open(path, "rb") as f:
            return PAK(f.read())
    except FileNotFoundError:
        return PAK()
    
@contextlib.contextmanager
def open_pak(path):
    yield (pak:= load_pak(path))
    save_pak(pak, path)
        
if __name__ == "__main__":
    with open_pak("test.pak") as pak:
        pak.a.b.c = 1
    with open_pak("test.pak") as pak:
        print(pak.a.b.c)