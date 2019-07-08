## It's a common and simple way to run your flask app in gunicorn server.


### Quick start:

    1. run with some arguments
        import gflask

        gflask.runserver(app=app, bind='0.0.0.0:22222')
        (app is flask app object)

    2. run with flask app config

        GFLASK_BIND = '0.0.0.0:22222'
        GFLASK_WORKERS = 4
        (these arguments in flask app config file. all argument names must be start with 'GFLASK')

        then run.

        gflask.runserver(app=app)

    3. run with config file(same as gunicorn config file format)

       bind = '0.0.0.0:22222'
       workers = 4
       (these in config file, name is 'config.conf')

       then run.

       gflask.runserver(app=app, config='/home/your path/config.conf')






### There are all available arguments(you can print these args use: gflask.print_available_args()):

> accesslog                     type: string(file)        default:                     desc: access log 文件路径
> access_log_format             type: string              default: %(h)s %(l)s %(u     desc: access log日志格式。h -- remote address，l --
                                                                 )s %(t)s "%(r)s           "-"占位, u -- user name, t -- date of the
                                                                 " %(s)s %(b)s "           request, r -- status line (e.g. ``GET /
                                                                 %(f)s" "%(a)s"            HTTP/1.1``), m -- request method, U -- U
                                                                                           RL path without query string, q -- query
                                                                                            string, H -- protocol, s -- status, B -
                                                                                           - response length, b -- response length,
                                                                                            f -- referer, a -- user agent, T -- req
                                                                                           uest time in seconds, D -- request time
                                                                                           in microseconds, L -- request time in de
                                                                                           cimal seconds, p -- process ID, {Header}
                                                                                           i -- request header, {Header}o -- respon
                                                                                           se header, {Variable}e -- environment va
                                                                                           riable
> backlog                       type: int                 default: 2048                desc: 可以接受的最大连接数，该数量指所有工作进程接受客户端连接的总数。超过这个数量的请
                                                                                           求会返回错误。通常设置为64-2048。默认为2048
> bind                          type: string(socket)      default: 0.0.0.0:34567       desc: 绑定的地址，支持ip：port、ip模式，只设置ip默认监听8000端口
> config                        type: string(file)        default:                     desc: 指定加载的配置文件，配置文件路径与运行app脚本路径一致
> daemon                        type: bool                default: False               desc: 以守护进程模式，后台运行。默认为False
> errorlog                      type: string(file)        default:                     desc: error log 文件路径
> group                         type: string              default: 20                  desc: 切换启动worker进程的组。默认当前组
> graceful_timeout              type: int                 default: 30                  desc: 当接收到重新启动worker的命令时，等待worker处理当前请求的超时时间。超
                                                                                           时强制杀死进程后自动重启。默认为30s
> keepalive                     type: int                 default: 2                   desc: 对请求keep alive的接口返回响应的等待时间，一般用于long polli
                                                                                           ng。通常设置在1-5s之间。默认为2s
> limit_request_fields          type: int                 default: 100                 desc: 请求头字段数量的最大值，该参数一般用来防止DDOS攻击。最大可以设置为32768
                                                                                           ，默认为100。
> limit_request_line            type: int                 default: 4094                desc: 请求的数据包raw最大字节，可以设置在0-8190字节之间（若设置为0，则不限制
                                                                                           ）。该参数一般用来防止DDOS攻击。默认值为4094
> limit_request_field_size      type: int                 default: 8190                desc: 请求头每个字段的最大字节。设置为0，则不限制，默认为8190
> logconfig                     type: string(file)        default:                     desc: 日志配置文件，规则与标准库logging一致
> loglevel                      type: string              default: info                desc: error日志级别
> max_requests_jitter           type: int                 default: 0                   desc: worker接受最大请求随机数的上限，worker会从1到该值随机一个数量，当处
                                                                                           理的请求达到这个数量后，worker自动重启。设置为0不会生效，默认为0
> max_requests                  type: int                 default: 10000               desc: 每一个工作进程（worker）处理请求的最大数量，处理完该数量的请求后，work
                                                                                           er自动重启，一般这种模式用于防止内存泄漏，设置为 0 时，永远不会自动重启
> raw_env                       type: string              default:                     desc: 运行时添加的环境变量
> reload                        type: bool                default: False               desc: 修改代码后自动重启worker。用于调试模式。默认为False
> threads                       type: int                 default: 1                   desc: 一个worker启动的线程数量。这个参数只有在gthread模式下生效。默认为1
> timeout                       type: int                 default: 30                  desc: 超时时间，当超过这个时间后worker会被强制杀死并重新启动。默认为30s。如果
                                                                                           需要长时间同步处理，适当调大该值
> user                          type: string              default: 501                 desc: 切换启动worker进程的用户。默认当前用户
> worker_connections            type: int                 default: 1000                desc: 单个worker同时接受的最大请求数，这个参数只在eventlet和gevent
                                                                                           两种模式下生效。默认为1000
> worker_class                  type: string              default: gevent              desc: 工作进程模式，支持：同步、eventlet、gevent、tornado、gth
                                                                                           read、gaiohttp几种模式。默认以gevent模式工作
> workers                       type: int                 default: 4                   desc: 启动的工作进程数量，通常设置为cpu核数的2-4倍，默认值为4



