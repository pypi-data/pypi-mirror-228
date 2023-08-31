"""
This module adds new classes of threads, including one for deamonic threads, but also fallen threads and useful multithreading tools.
"""


import atexit
from concurrent.futures import ThreadPoolExecutor
from threading import Event, RLock, Thread
from typing import Any, Callable, Generic, Iterable, Mapping, ParamSpec, Set, TypeVar

__all__ = ["Future", "DaemonThread", "FallPriority", "FallenThread", "DeamonPoolExecutor", "exclusive", "critical", "ExclusionGroup"]





T = TypeVar("T")

class Future(Event, Generic[T]):
    
    """
    A Future represents an eventual value. This value might get defined at some point.
    It can also be set to raise an exception.
    You can wait for it like an event.
    """

    def __init__(self) -> None:
        from threading import Lock, Event
        super().__init__()
        self.__value : "T" | None = None
        self.__exception : BaseException | None = None
        self.__lock = Lock()
        self.__waiting : int = 0
        self.__collapsed = Event()
        self.__collapsed.set()

    def set(self, value : T) -> None:
        """
        Sets the value of the Future.
        """
        with self.__lock:
            self.__value = value
            if self.__waiting:
                self.__collapsed.clear()
            return super().set()
    
    def set_exception(self, exc : BaseException) -> None:
        """
        Makes the Future raise an exception.
        """
        if not isinstance(exc, BaseException):
            raise TypeError("Expected BaseException, got " + repr(type(exc).__name__))
        with self.__lock:
            self.__exception = exc
            if self.__waiting:
                self.__collapsed.clear()
            return super().set()
    
    def clear(self) -> None:
        """
        Clears the Future. Removes the associated value and exception.
        """
        if not self.__collapsed.is_set():
            self.__collapsed.wait()
        with self.__lock:
            if not self.is_set():
                return
            if not self.__waiting:
                self.__value = None     # Do not hold references to unknown objects
                self.__exception = None
                return super().clear()
    
    def wait(self, timeout : float = float("inf")) -> bool:
        try:
            timeout = float(timeout)
        except:
            pass
        if not isinstance(timeout, float):
            raise TypeError("Expected float for timeout, got " + repr(type(timeout).__name__))
        if timeout < 0 or timeout == float("nan"):
            raise ValueError("Expected positive timeout, got " + repr(timeout))
        try:
            with self.__lock:
                self.__waiting += 1
            return super().wait(timeout if timeout != float("inf") else None)
        finally:
            with self.__lock:
                self.__waiting -= 1
                if not self.__waiting:
                    self.__collapsed.set()
    
    def result(self, timeout : float = float("inf")) -> T:
        """
        Waits for the Future to be resolved and returns the associated value.
        Raises TimeoutError if the future has not been resolved before timeout has been reached.
        """
        try:
            timeout = float(timeout)
        except:
            pass
        if not isinstance(timeout, float):
            raise TypeError("Expected float for timeout, got " + repr(type(timeout).__name__))
        if timeout < 0 or timeout == float("nan"):
            raise ValueError("Expected positive timeout, got " + repr(timeout))
        self.__collapsed.wait()
        try:
            with self.__lock:
                self.__waiting += 1
            ok = self.wait(timeout)
            if not ok:
                raise TimeoutError("Future has not been resolved yet")
            if not self.__exception:
                return self.__value
            else:
                raise self.__exception from None
        finally:
            with self.__lock:
                self.__waiting -= 1
                if not self.__waiting:
                    self.__collapsed.set()





class DaemonThread(Thread):

    """
    Just a separate class for deamonic threads.
    """

    def __init__(self, group: None = None, target: Callable[..., Any] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=True)

    def start(self) -> None:
        self.daemon = True
        return super().start()
    
    @property
    def daemon(self):
        assert self._initialized, "Thread.__init__() not called"
        return True

    @daemon.setter
    def daemon(self, daemonic):
        if daemonic != True:
            raise ValueError("This is a thread of type DeamonThread. You cannot make it not deamonic.")
        if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
        if self._started.is_set():
            raise RuntimeError("cannot set daemon status of active thread")
        
        self._daemonic = True






class FallPriority:

    """
    Just a placeholder for priorities
    """

    EXTREME = 100
    HIGH = 80
    MEDIUM = 60
    LOW = 40
    VERY_LOW = 20

class FallenThread(DaemonThread):

    """
    This subclass of deamonic threads will be alerted upon interpreter shutdown and will be given time to finish their tasks if necessary.
    This is done through the finalization_callback function.
    The FallenThread will be judged disposable when its finalization completes.
    """


    def __init__(self, finalizing_callback : Callable[[], None], group: None = None, target: Callable[..., Any] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = None, priority : int | float = FallPriority.MEDIUM) -> None:
        
        if not isinstance(priority, int | float):
            raise TypeError("Expected int or float, got " + repr(type(priority).__name__))
        if priority < 0 or priority == float("nan"):
            raise ValueError("Expected positive number for priority, got " + repr(priority))

        if not callable(finalizing_callback):
                raise TypeError("Expected callable for finalizing_callback, got " + repr(finalizing_callback.__class__.__name__))
        
        super().__init__(group, target, name, args, kwargs)

        self.__priority = priority
        self.__finalizing_callback = finalizing_callback



    


@atexit.register
def save_fallen_threads():
    """
    This function is responsible for calling the finalization process. For each priority level (descending), it will:
        - Start a new DeamonThread for each finalization callback
        - Wait for the completion of all finalizations
    """

    from threading import enumerate

    finalized = set()

    def finalize(t : FallenThread):
        try:
            t._FallenThread__finalizing_callback()
        finally:
            finalized.add(t)

    while True:

        remaining_fallen = {t for t in enumerate() if isinstance(t, FallenThread) and t not in finalized}
        if not remaining_fallen:
            break
        current_level = max(t._FallenThread__priority for t in remaining_fallen)
        batch = {t for t in remaining_fallen if t._FallenThread__priority == current_level}

        active_finalizers : set[DaemonThread] = set()

        for t in batch:
            
            d = DaemonThread(target = finalize, args = (t, ), name = "Finalizer of thread " + repr(t.name))
            active_finalizers.add(d)
            d.start()
        
        for d in active_finalizers:
            d.join()

    




class DeamonPoolExecutor(ThreadPoolExecutor):

    def _adjust_thread_count(self) -> None:

        from concurrent.futures.thread import _worker, _threads_queues
        import weakref
        # if idle threads are available, don't spin new threads
        if self._idle_semaphore.acquire(timeout=0):
            return

        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                     num_threads)
            t = DaemonThread(name=thread_name, target=_worker,
                                 args=(weakref.ref(self, weakref_cb),
                                       self._work_queue,
                                       self._initializer,
                                       self._initargs))
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue





P = ParamSpec("P")
T = TypeVar("T")

class ExclusionGroup:

    """
    This is used to create a mutual exclusion group. It is like using a RLock but that can be used as a decorator to make a function mutually exclusive in regards to anyone using this same function.
    """

    def __call__(self, f : Callable[P, T]) -> Callable[P, T]:
        from Viper.meta.utils import signature_def, signature_call
        from functools import wraps

        sig = "@wraps(old_target)\n"

        sig_def, env = signature_def(f, init_env = {"old_target" : f, "wraps" : wraps, "__lock" : self})
        
        code = sig + sig_def
        
        code += "\n\twith __lock:\n\t\t"

        code += "return old_target("

        sig_call = signature_call(f, decorate = False)

        code += sig_call + ")"

        exec(code, env)

        return env[f.__name__]





def exclusive(f : Callable):

    return ExclusionGroup()(f)
    
critical = exclusive



    

del save_fallen_threads, Any, Callable, Iterable, Mapping, Set, Event, RLock, Thread, atexit, ThreadPoolExecutor, TypeVar, T


