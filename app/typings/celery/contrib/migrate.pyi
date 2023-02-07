"""
This type stub file was generated by pyright.
"""

"""Message migration tools (Broker <-> Broker)."""
__all__ = (
    "StopFiltering",
    "State",
    "republish",
    "migrate_task",
    "migrate_tasks",
    "move",
    "task_id_eq",
    "task_id_in",
    "start_filter",
    "move_task_by_id",
    "move_by_idmap",
    "move_by_taskmap",
    "move_direct",
    "move_direct_by_id",
)
MOVING_PROGRESS_FMT = ...

class StopFiltering(Exception):
    """Semi-predicate used to signal filter stop."""

    ...

class State:
    """Migration progress state."""

    count = ...
    filtered = ...
    total_apx = ...
    @property
    def strtotal(self): ...
    def __repr__(self): ...

def republish(
    producer, message, exchange=..., routing_key=..., remove_props=...
):  # -> None:
    """Republish message."""
    ...

def migrate_task(producer, body_, message, queues=...):  # -> None:
    """Migrate single task message."""
    ...

def filter_callback(callback, tasks): ...
def migrate_tasks(source, dest, migrate=..., app=..., queues=..., **kwargs):  # -> State:
    """Migrate tasks from one broker to another."""
    ...

def move(
    predicate,
    connection=...,
    exchange=...,
    routing_key=...,
    source=...,
    app=...,
    callback=...,
    limit=...,
    transform=...,
    **kwargs
):  # -> State:
    """Find tasks by filtering them and move the tasks to a new queue.

    Arguments:
        predicate (Callable): Filter function used to decide the messages
            to move.  Must accept the standard signature of ``(body, message)``
            used by Kombu consumer callbacks.  If the predicate wants the
            message to be moved it must return either:

                1) a tuple of ``(exchange, routing_key)``, or

                2) a :class:`~kombu.entity.Queue` instance, or

                3) any other true value means the specified
                    ``exchange`` and ``routing_key`` arguments will be used.
        connection (kombu.Connection): Custom connection to use.
        source: List[Union[str, kombu.Queue]]: Optional list of source
            queues to use instead of the default (queues
            in :setting:`task_queues`).  This list can also contain
            :class:`~kombu.entity.Queue` instances.
        exchange (str, kombu.Exchange): Default destination exchange.
        routing_key (str): Default destination routing key.
        limit (int): Limit number of messages to filter.
        callback (Callable): Callback called after message moved,
            with signature ``(state, body, message)``.
        transform (Callable): Optional function to transform the return
            value (destination) of the filter function.

    Also supports the same keyword arguments as :func:`start_filter`.

    To demonstrate, the :func:`move_task_by_id` operation can be implemented
    like this:

    .. code-block:: python

        def is_wanted_task(body, message):
            if body['id'] == wanted_id:
                return Queue('foo', exchange=Exchange('foo'),
                             routing_key='foo')

        move(is_wanted_task)

    or with a transform:

    .. code-block:: python

        def transform(value):
            if isinstance(value, str):
                return Queue(value, Exchange(value), value)
            return value

        move(is_wanted_task, transform=transform)

    Note:
        The predicate may also return a tuple of ``(exchange, routing_key)``
        to specify the destination to where the task should be moved,
        or a :class:`~kombu.entity.Queue` instance.
        Any other true value means that the task will be moved to the
        default exchange/routing_key.
    """
    ...

def expand_dest(ret, exchange, routing_key): ...
def task_id_eq(task_id, body, message):
    """Return true if task id equals task_id'."""
    ...

def task_id_in(ids, body, message):  # -> bool:
    """Return true if task id is member of set ids'."""
    ...

def prepare_queues(queues): ...

class Filterer:
    def __init__(
        self,
        app,
        conn,
        filter,
        limit=...,
        timeout=...,
        ack_messages=...,
        tasks=...,
        queues=...,
        callback=...,
        forever=...,
        on_declare_queue=...,
        consume_from=...,
        state=...,
        accept=...,
        **kwargs
    ) -> None: ...
    def start(self): ...
    def update_state(self, body, message): ...
    def ack_message(self, body, message): ...
    def create_consumer(self): ...
    def prepare_consumer(self, consumer): ...
    def declare_queues(self, consumer): ...

def start_filter(
    app,
    conn,
    filter,
    limit=...,
    timeout=...,
    ack_messages=...,
    tasks=...,
    queues=...,
    callback=...,
    forever=...,
    on_declare_queue=...,
    consume_from=...,
    state=...,
    accept=...,
    **kwargs
):  # -> State:
    """Filter tasks."""
    ...

def move_task_by_id(task_id, dest, **kwargs):  # -> State:
    """Find a task by id and move it to another queue.

    Arguments:
        task_id (str): Id of task to find and move.
        dest: (str, kombu.Queue): Destination queue.
        transform (Callable): Optional function to transform the return
            value (destination) of the filter function.
        **kwargs (Any): Also supports the same keyword
            arguments as :func:`move`.
    """
    ...

def move_by_idmap(map, **kwargs):  # -> State:
    """Move tasks by matching from a ``task_id: queue`` mapping.

    Where ``queue`` is a queue to move the task to.

    Example:
        >>> move_by_idmap({
        ...     '5bee6e82-f4ac-468e-bd3d-13e8600250bc': Queue('name'),
        ...     'ada8652d-aef3-466b-abd2-becdaf1b82b3': Queue('name'),
        ...     '3a2b140d-7db1-41ba-ac90-c36a0ef4ab1f': Queue('name')},
        ...   queues=['hipri'])
    """
    ...

def move_by_taskmap(map, **kwargs):  # -> State:
    """Move tasks by matching from a ``task_name: queue`` mapping.

    ``queue`` is the queue to move the task to.

    Example:
        >>> move_by_taskmap({
        ...     'tasks.add': Queue('name'),
        ...     'tasks.mul': Queue('name'),
        ... })
    """
    ...

def filter_status(state, body, message, **kwargs): ...

move_direct = ...
move_direct_by_id = ...
move_direct_by_idmap = ...
move_direct_by_taskmap = ...