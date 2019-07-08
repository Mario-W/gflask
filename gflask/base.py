# coding=utf8

import os
import util
import argparse
import flask
from gunicorn import __version__
from gettext import gettext as _
from gunicorn.util import getcwd
from gunicorn.app.wsgiapp import WSGIApplication
from gunicorn.config import get_default_config_file, Config, ConfigError


FLASK_APP = None
MOCK_ARGS = []

class MyApplication(WSGIApplication):

    def init(self, parser, opts, args):
        if opts.paste and opts.paste is not None:
            app_name = 'main'
            path = opts.paste
            if '#' in path:
                path, app_name = path.split('#')
            path = os.path.abspath(os.path.normpath(
                os.path.join(getcwd(), path)))

            if not os.path.exists(path):
                raise ConfigError("%r not found" % path)

            # paste application, load the config
            self.cfgurl = 'config:%s#%s' % (path, app_name)
            self.relpath = os.path.dirname(path)

        self.cfg.set("default_proc_name", FLASK_APP.__dict__.get('name', ''))
        self.app_uri = FLASK_APP

    def load_config(self):
        # parse console args

        # here use mock Config class
        self.cfg = MyConfig(self.usage, prog=self.prog)

        parser = self.cfg.parser()
        args = parser.parse_args(args=MOCK_ARGS)

        # optional settings from apps
        cfg = self.init(parser, args, args.args)

        # Load up the any app specific configuration
        if cfg and cfg is not None:
            for k, v in cfg.items():
                self.cfg.set(k.lower(), v)

        if args.config:
            self.load_config_from_file(args.config)
        else:
            default_config = get_default_config_file()
            if default_config is not None:
                self.load_config_from_file(default_config)

        # Lastly, update the configuration with any command line
        # settings.
        for k, v in vars(args).items():
            if v is None:
                continue
            if k == "args":
                continue
            self.cfg.set(k.lower(), v)

    def load_wsgiapp(self):
        self.chdir()

        # load the app
        return util.import_app(self.app_uri)


class MyArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        # here use mock args
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        return args


class MyConfig(Config):
    def parser(self):
        kwargs = {
            "usage": self.usage,
            "prog": self.prog
        }
        # here use mock ArgumentParser class
        parser = MyArgumentParser(**kwargs)
        parser.add_argument("-v", "--version",
                            action="version", default=argparse.SUPPRESS,
                            version="%(prog)s (version " + __version__ + ")\n",
                            help="show program's version number and exit")
        parser.add_argument("args", nargs="*", help=argparse.SUPPRESS)

        keys = sorted(self.settings, key=self.settings.__getitem__)
        for k in keys:
            self.settings[k].add_option(parser)

        return parser


class AppServer(object):

    def __init__(self):

        pass

    def collect_config_args(self, app, args_dict):

        global FLASK_APP
        global MOCK_ARGS

        if not app.__class__ == flask.Flask:
            raise Exception('%s is not a flask.Flask instance!' % app)

        # 获取flask app config
        app_config = util.get_flask_app_config(app.config)
        # 按照参数选择优先级（args、app config、配置文件、默认参数）加载参数
        args_dict = util.combine_config_args(args_dict, app_config)
        # 将python参数转换为gunicorn命令参数
        args_list, error_msg = util.convert_args(args_dict)

        if error_msg:
            print error_msg
            raise Exception(error_msg)

        FLASK_APP = app
        MOCK_ARGS = args_list

    def gunicorn_run(self):

        # here use mock Application class to run
        MyApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()


def ready_to_run(app=None, bind=None, workers=None, worker_class=None,
                 max_requests=None, timeout=None, config=None, **kwargs):

    # 取出app， 摊平所有参数
    all_args = locals()
    all_args.pop('kwargs')
    app = all_args.pop('app')
    kwargs.update(all_args)

    app_server = AppServer()
    app_server.collect_config_args(app, kwargs)
    app_server.gunicorn_run()
