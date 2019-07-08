# coding=utf8

import os


default_mode = {
    'bind': '0.0.0.0:34567',
    'workers': 4,
    'worker_class': 'gevent',
    'max_requests': 10000,
    'timeout': 30,
    'config': '',
}

args_mapping = {

    # TODO complete this mapping dict items and descriptions

    'config': {
        'option': '-c',
        'value': None,
        'type': 'string(file)',
        'default': '',
        'desc': """\
                The Gunicorn config file.

                A string of the form ``PATH``, ``file:PATH``, or ``python:MODULE_NAME``.

                Only has an effect when specified on the command line or as part of an
                application specific configuration.

                .. versionchanged:: 19.4
                   Loading the config from a Python module requires the ``python:``
                   prefix.
                """,
        'desc_cn': u'指定加载的配置文件，尽量使用绝对路径。若工作目录与配置文件目录相同，可以直接指定文件名',
        'example': 'e.g: "/home/root/.../config.py"、 "config.py"、 "config.conf"'
    },
    'bind': {
        'option': '-b',
        'value': None,
        'type': 'string(socket)',
        'default': '0.0.0.0:34567',
        'desc': """\
                The socket to bind.

                A string of the form: ``HOST``, ``HOST:PORT``, ``unix:PATH``. An IP is
                a valid ``HOST``.

                Multiple addresses can be bound. ex.::

                    $ gunicorn -b 127.0.0.1:8000 -b [::1]:8000 test:app

                will bind the `test:app` application on localhost both on ipv6
                and ipv4 interfaces.
                """,
        'desc_cn': u'绑定的地址，支持ip：port、ip模式，只设置ip默认监听8000端口',
        'example': 'e.g: "0.0.0.0:22222"、 "14.24.53.160"'
    },
    'workers': {
        'option': '-w',
        'value': None,
        'type': 'int',
        'default': 4,
        'desc': """\
                The number of worker processes for handling requests.

                A positive integer generally in the ``2-4 x $(NUM_CORES)`` range.
                You'll want to vary this a bit to find the best for your particular
                application's work load.

                By default, the value of the ``WEB_CONCURRENCY`` environment variable.
                If it is not defined, the default is ``1``.
                """,
        'desc_cn': u'启动的工作进程数量，通常设置为cpu核数的2-4倍，默认值为4',
        'example': 'e.g: 4'
    },
    'worker_class': {
        'option': '-k',
        'value': None,
        'type': 'string',
        'default': 'gevent',
        'desc': """\
                The type of workers to use.

                The default class (``sync``) should handle most "normal" types of
                workloads. You'll want to read :doc:`design` for information on when
                you might want to choose one of the other worker classes.

                A string referring to one of the following bundled classes:

                * ``sync``
                * ``eventlet`` - Requires eventlet >= 0.9.7
                * ``gevent``   - Requires gevent >= 0.13
                * ``tornado``  - Requires tornado >= 0.2
                * ``gthread``  - Python 2 requires the futures package to be installed
                * ``gaiohttp`` - Requires Python 3.4 and aiohttp >= 0.21.5

                Optionally, you can provide your own worker by giving Gunicorn a
                Python path to a subclass of ``gunicorn.workers.base.Worker``.
                This alternative syntax will load the gevent class:
                ``gunicorn.workers.ggevent.GeventWorker``.
                """,
        'desc_cn': u'工作进程模式，支持：同步、eventlet、gevent、tornado、gthread、gaiohttp几种模式。默认以gevent模式工作',
        'example': 'e.g："sync"、"eventlet"、"gevent"、"tornado"、"gthread"、"gaiohttp"'
    },
    'max_requests': {
        'option': '--max-requests',
        'value': None,
        'type': 'int',
        'default': 10000,
        'desc': """\
                The maximum number of requests a worker will process before restarting.

                Any value greater than zero will limit the number of requests a work
                will process before automatically restarting. This is a simple method
                to help limit the damage of memory leaks.

                If this is set to zero (the default) then the automatic worker
                restarts are disabled.
                """,
        'desc_cn': u'每一个工作进程（worker）处理请求的最大数量，处理完该数量的请求后，worker自动重启，一般这种模式用于防止内存泄漏，设置为 0 时，永远不会自动重启',
        'example': 'e.g：10000'
    },
    'timeout': {
        'option': '-t',
        'value': None,
        'type': 'int',
        'default': '30',
        'desc': """\
                Workers silent for more than this many seconds are killed and restarted.

                Generally set to thirty seconds. Only set this noticeably higher if
                you're sure of the repercussions for sync workers. For the non sync
                workers it just means that the worker process is still communicating and
                is not tied to the length of time required to handle a single request.
                """,
        'desc_cn': u'超时时间，当超过这个时间后worker会被强制杀死并重新启动。默认为30s。如果需要长时间同步处理，适当调大该值',
        'example': 'e.g：30'
    },
    'backlog': {
        'option': '--backlog',
        'value': None,
        'type': 'int',
        'default': 2048,
        'desc': """\
                The maximum number of pending connections.

                This refers to the number of clients that can be waiting to be served.
                Exceeding this number results in the client getting an error when
                attempting to connect. It should only affect servers under significant
                load.

                Must be a positive integer. Generally set in the 64-2048 range.
                """,
        'desc_cn': u'可以接受的最大连接数，该数量指所有工作进程接受客户端连接的总数。超过这个数量的请求会返回错误。通常设置为64-2048。默认为2048',
        'example': 'e.g: 2048'
    },
    'threads': {
        'option': '--threads',
        'value': None,
        'type': 'int',
        'default': 1,
        'desc': """\
                The number of worker threads for handling requests.

                Run each worker with the specified number of threads.

                A positive integer generally in the ``2-4 x $(NUM_CORES)`` range.
                You'll want to vary this a bit to find the best for your particular
                application's work load.

                If it is not defined, the default is ``1``.

                This setting only affects the Gthread worker type.
                """,
        'desc_cn': u'一个worker启动的线程数量。这个参数只有在gthread模式下生效。默认为1',
        'example': 'e.g: 1'
    },
    'worker_connections': {
        'option': '--worker-connections',
        'value': None,
        'type': 'int',
        'default': 1000,
        'desc': """\
                The maximum number of simultaneous clients.

                This setting only affects the Eventlet and Gevent worker types.
                """,
        'desc_cn': u'单个worker同时接受的最大请求数，这个参数只在eventlet和gevent两种模式下生效。默认为1000',
        'example': 'e.g: 1000'
    },
    'max_requests_jitter': {
        'option': '--max-requests-jitter',
        'value': None,
        'type': 'int',
        'default': 0,
        'desc': """\
                The maximum jitter to add to the *max_requests* setting.

                The jitter causes the restart per worker to be randomized by
                ``randint(0, max_requests_jitter)``. This is intended to stagger worker
                restarts to avoid all workers restarting at the same time.

                .. versionadded:: 19.2
                """,
        'desc_cn': u'worker接受最大请求随机数的上限，worker会从1到该值随机一个数量，当处理的请求达到这个数量后，worker自动重启。设置为0不会生效，默认为0',
        'example': 'e.g: 0'
    },
    'graceful_timeout': {
        'option': '--graceful-timeout',
        'value': None,
        'type': 'int',
        'default': 30,
        'desc': """\
                Timeout for graceful workers restart.

                After receiving a restart signal, workers have this much time to finish
                serving requests. Workers still alive after the timeout (starting from
                the receipt of the restart signal) are force killed.
                """,
        'desc_cn': u'当接收到重新启动worker的命令时，等待worker处理当前请求的超时时间。超时强制杀死进程后自动重启。默认为30s',
        'example': 'e.g: 30'
    },
    'keepalive': {
        'option': '--keep-alive',
        'value': None,
        'type': 'int',
        'default': 2,
        'desc': """\
                The number of seconds to wait for requests on a Keep-Alive connection.

                Generally set in the 1-5 seconds range.
                """,
        'desc_cn': u'对请求keep alive的接口返回响应的等待时间，一般用于long polling。通常设置在1-5s之间。默认为2s',
        'example': 'e.g: 2'
    },
    'limit_request_line': {
        'option': '--limit-request-line',
        'value': None,
        'type': 'int',
        'default': 4094,
        'desc': """\
                The maximum size of HTTP request line in bytes.

                This parameter is used to limit the allowed size of a client's
                HTTP request-line. Since the request-line consists of the HTTP
                method, URI, and protocol version, this directive places a
                restriction on the length of a request-URI allowed for a request
                on the server. A server needs this value to be large enough to
                hold any of its resource names, including any information that
                might be passed in the query part of a GET request. Value is a number
                from 0 (unlimited) to 8190.

                This parameter can be used to prevent any DDOS attack.
                """,
        'desc_cn': u'请求的数据包raw最大字节，可以设置在0-8190字节之间（若设置为0，则不限制）。该参数一般用来防止DDOS攻击。默认值为4094',
        'example': 'e.g: 4094'
    },
    'limit_request_fields': {
        'option': '--limit-request-fields',
        'value': None,
        'type': 'int',
        'default': 100,
        'desc': """\
                Limit the number of HTTP headers fields in a request.

                This parameter is used to limit the number of headers in a request to
                prevent DDOS attack. Used with the *limit_request_field_size* it allows
                more safety. By default this value is 100 and can't be larger than
                32768.
                """,
        'desc_cn': u'请求头字段数量的最大值，该参数一般用来防止DDOS攻击。最大可以设置为32768，默认为100。',
        'example': 'e.g: 100'
    },
    'limit_request_field_size': {
        'option': '--limit-request-field_size',
        'value': None,
        'type': 'int',
        'default': 8190,
        'desc': """\
                Limit the allowed size of an HTTP request header field.

                Value is a positive number or 0. Setting it to 0 will allow unlimited
                header field sizes.

                .. warning::
                   Setting this parameter to a very high or unlimited value can open
                   up for DDOS attacks.
                """,
        'desc_cn': u'请求头每个字段的最大字节。设置为0，则不限制，默认为8190',
        'example': 'e.g: 8190'
    },
    'reload': {
        'option': '--reload',
        'value': None,
        'type': 'bool',
        'default': False,
        'desc': '''\
                Restart workers when code changes.

                This setting is intended for development. It will cause workers to be
                restarted whenever application code changes.

                The reloader is incompatible with application preloading. When using a
                paste configuration be sure that the server block does not import any
                application code or the reload will not work as designed.

                The default behavior is to attempt inotify with a fallback to file
                system polling. Generally, inotify should be preferred if available
                because it consumes less system resources.

                .. note::
                   In order to use the inotify reloader, you must have the ``inotify``
                   package installed.
                ''',
        'desc_cn': u'修改代码后自动重启worker。用于调试模式。默认为False',
        'example': 'e.g: False'
    },
    # 'spew': {
    #     'option': '--spew',
    #     'value': None,
    #     'desc': """\
    #             Install a trace function that spews every line executed by the server.
    #
    #             This is the nuclear option.
    #             """,
    #     'desc_cn': u''
    # },
    # 'preload_app': {
    #     'option': '--preload',
    #     'value': None,
    #     'type': 'bool',
    #     'default': False,
    #     'desc': """\
    #             Load application code before the worker processes are forked.
    #
    #             By preloading an application you can save some RAM resources as well as
    #             speed up server boot times. Although, if you defer application loading
    #             to each worker process, you can reload your application code easily by
    #             restarting workers.
    #             """,
    #     'desc_cn': u'在子进程fork前，预先加载app程序，可以节省部分内存，提高启动速度。默认为False',
    # },
    # 'sendfile': {
    #     'option': '--no-sendfile',
    #     'value': None,
    #     'desc': """\
    #             Disables the use of ``sendfile()``.
    #
    #             If not set, the value of the ``SENDFILE`` environment variable is used
    #             to enable or disable its usage.
    #
    #             .. versionadded:: 19.2
    #             .. versionchanged:: 19.4
    #                Swapped ``--sendfile`` with ``--no-sendfile`` to actually allow
    #                disabling.
    #             .. versionchanged:: 19.6
    #                added support for the ``SENDFILE`` environment variable
    #             """,
    #     'desc_cn': u''
    # },

    'daemon': {
        'option': '--daemon',
        'value': None,
        'type': 'bool',
        'default': False,
        'desc': """\
                Daemonize the Gunicorn process.

                Detaches the server from the controlling terminal and enters the
                background.
                """,
        'desc_cn': u'以守护进程模式，后台运行。默认为False',
        'example': 'e.g: False',
    },
    'raw_env': {
        'option': '-e',
        'value': None,
        'type': 'string',
        'default': '',
        'desc': """\
                Set environment variable (key=value).

                Pass variables to the execution environment. Ex.::

                    $ gunicorn -b 127.0.0.1:8000 --env FOO=1 test:app

                and test for the foo variable environment in your application.
                """,
        'desc_cn': u'运行时添加的环境变量',
        'example': 'e.g: "xxx=yyy"'
    },
    # 'pidfile': {
    #     'option': '-p',
    #     'value': None,
    #     'desc': """\
    #             A filename to use for the PID file.
    #
    #             If not set, no PID file will be written.
    #             """,
    #     'desc_cn': u''
    # },
    # 'worker_tmp_dir': {
    #     'option': '--worker-tmp-dir',
    #     'value': None,
    #     'desc': """\
    #             A directory to use for the worker heartbeat temporary file.
    #
    #             If not set, the default temporary directory will be used.
    #
    #             .. note::
    #                The current heartbeat system involves calling ``os.fchmod`` on
    #                temporary file handlers and may block a worker for arbitrary time
    #                if the directory is on a disk-backed filesystem.
    #
    #                See :ref:`blocking-os-fchmod` for more detailed information
    #                and a solution for avoiding this problem.
    #             """,
    #     'desc_cn': u''
    # },
    'user': {
        'option': '-u',
        'value': None,
        'type': 'string',
        'default': os.geteuid(),
        'desc': """\
                Switch worker processes to run as this user.

                A valid user id (as an integer) or the name of a user that can be
                retrieved with a call to ``pwd.getpwnam(value)`` or ``None`` to not
                change the worker process user.
                """,
        'desc_cn': u'切换启动worker进程的用户。默认当前用户',
        'example': 'e.g: root'
    },
    'group': {
        'option': '-g',
        'value': None,
        'type': 'string',
        'default': os.getegid(),
        'desc': """\
                Switch worker process to run as this group.

                A valid group id (as an integer) or the name of a user that can be
                retrieved with a call to ``pwd.getgrnam(value)`` or ``None`` to not
                change the worker processes group.
                """,
        'desc_cn': u'切换启动worker进程的组。默认当前组',
        'example': 'e.g: root'
    },
    # 'umask': {
    #     'option': '-m',
    #     'value': None,
    #     'desc': """\
    #             A bit mask for the file mode on files written by Gunicorn.
    #
    #             Note that this affects unix socket permissions.
    #
    #             A valid value for the ``os.umask(mode)`` call or a string compatible
    #             with ``int(value, 0)`` (``0`` means Python guesses the base, so values
    #             like ``0``, ``0xFF``, ``0022`` are valid for decimal, hex, and octal
    #             representations)
    #             """,
    #     'desc_cn': u''
    # },
    'accesslog': {
        'option': '--access-logfile',
        'value': None,
        'type': 'string(file)',
        'default': '',
        'desc': """\
                The Access log file to write to.

                ``'-'`` means log to stdout.
                """,
        'desc_cn': u'access log 文件路径',
        'example': 'e.g: /home/root/.../access.log'
    },
    'access_log_format': {
        'option': '--access-logformat',
        'value': None,
        'type': 'string',
        'default': '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"',
        'desc': """\
                The access log format.

                ===========  ===========
                Identifier   Description
                ===========  ===========
                h            remote address
                l            ``'-'``
                u            user name
                t            date of the request
                r            status line (e.g. ``GET / HTTP/1.1``)
                m            request method
                U            URL path without query string
                q            query string
                H            protocol
                s            status
                B            response length
                b            response length or ``'-'`` (CLF format)
                f            referer
                a            user agent
                T            request time in seconds
                D            request time in microseconds
                L            request time in decimal seconds
                p            process ID
                {Header}i    request header
                {Header}o    response header
                {Variable}e  environment variable
                ===========  ===========
                """,
        'desc_cn': u'access log日志格式。h -- remote address，l -- "-"占位, u -- user name, t -- date of the request, r -- status line (e.g. ``GET / HTTP/1.1``), m -- request method, U -- URL path without query string, q -- query string, H -- protocol, s -- status, B -- response length, b -- response length, f -- referer, a -- user agent, T -- request time in seconds, D -- request time in microseconds, L -- request time in decimal seconds, p -- process ID, {Header}i -- request header, {Header}o -- response header, {Variable}e -- environment variable',
        'example': 'e.g: %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
    },
    'errorlog': {
        'option': '--error-logfile',
        'value': None,
        'type': 'string(file)',
        'default': '',
        'desc': """\
                The Error log file to write to.

                Using ``'-'`` for FILE makes gunicorn log to stderr.

                .. versionchanged:: 19.2
                   Log to stderr by default.

                """,
        'desc_cn': u'error log 文件路径',
        'example': 'e.g: /home/root/.../error.log'
    },
    'loglevel': {
        'option': '--log-level',
        'value': None,
        'type': 'string',
        'default': 'info',
        'desc': """\
                The granularity of Error log outputs.

                Valid level names are:

                * debug
                * info
                * warning
                * error
                * critical
                """,
        'desc_cn': u'error日志级别',
        'example': 'e.g: debug、info、warning、error、critical'
    },
    'logconfig': {
        'option': '--log-config',
        'value': None,
        'type': 'string(file)',
        'default': '',
        'desc': """\
                The log config file to use.
                Gunicorn uses the standard Python logging module's Configuration
                file format.
                """,
        'desc_cn': u'日志配置文件，规则与标准库logging一致',
        'example': 'e.g: /home/root/.../log_config.py'
    },
    # 'proc_name': {
    #     'option': '-n',
    #     'value': None,
    #     'desc': """\
    #             A base to use with setproctitle for process naming.
    #
    #             This affects things like ``ps`` and ``top``. If you're going to be
    #             running more than one instance of Gunicorn you'll probably want to set a
    #             name to tell them apart. This requires that you install the setproctitle
    #             module.
    #
    #             If not set, the *default_proc_name* setting will be used.
    #             """,
    #     'desc_cn': u''
    # },
    # 'pythonpath': {
    #     'option': '--pythonpath',
    #     'value': None,
    #     'desc': """\
    #             A comma-separated list of directories to add to the Python path.
    #
    #             e.g.
    #             ``'/home/djangoprojects/myproject,/home/python/mylibrary'``.
    #             """,
    #     'desc_cn': u''
    # },

}

args_key_list = args_mapping.keys()

def get_args_key_with_desc():
    key_space = 30
    type_space = 20
    default_space = 20
    default_len = 15
    desc_len = 40
    result = []
    for i in sorted(args_mapping.keys(), key=lambda x: (x[0], x[1])):

        result.append(u'{}{}type: {}{}default: {}{}desc: {}'.format(
            i, ' '*(key_space-len(i)), args_mapping[i].get('type'), ' '*(type_space-len(args_mapping[i].get('type'))),
            str(args_mapping[i].get('default'))[: default_len],
            ' '*(default_space-len(str(args_mapping[i].get('default'))[: default_len])),
            args_mapping[i].get('desc_cn')[: desc_len]
        ))
        tmp_loop = 1
        while(str(args_mapping[i].get('default'))[default_len*tmp_loop: ] or args_mapping[i].get('desc_cn')[desc_len*tmp_loop: ]):
            result.append(u'{}{}{}{}'.format(
                ' '*(key_space + len('type: ') + type_space + len('default: ')),
                str(args_mapping[i].get('default'))[default_len*tmp_loop: default_len*(tmp_loop+1)],
                ' '*(default_space + len('desc: ') -
                     len(str(args_mapping[i].get('default'))[default_len*tmp_loop: default_len*(tmp_loop+1)])),
                args_mapping[i].get('desc_cn')[desc_len*tmp_loop: desc_len*(tmp_loop+1)]
            ))
            tmp_loop += 1

    return result


args_key_with_desc = get_args_key_with_desc()


if __name__ == '__main__':

    for args in args_key_with_desc:
        print args
