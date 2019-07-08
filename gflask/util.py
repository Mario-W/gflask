# coding=utf8

import flask
import config
from gunicorn.errors import AppImportError


def import_app(app_obj):

    if app_obj is None:
        raise AppImportError("Failed to find application object: %r" % app_obj)

    if not app_obj.__class__ == flask.Flask:
        raise Exception("%s is not a flask.Flask instance!" % app_obj)

    if not callable(app_obj):
        raise AppImportError("Application object must be callable.")
    return app_obj


def get_flask_app_config(app_config):

    result_args = {}
    for c in app_config:
        if c.startswith('GFLASK_'):
            result_args[c.split('GFLASK_', 1)[-1].lower()] = app_config[c]
    return result_args


def combine_config_args(init_args, app_config):

    # 传入参数覆盖app config参数
    all_args = cover_args(app_config, init_args)
    result_args = {}

    for arg in all_args:
        if all_args.get(arg):
            # 传入的参数有值
            result_args[arg] = all_args[arg]
        elif config.default_mode.get(arg) and not all_args.get('config'):
            # 没有指定配置文件并且默认配置有的参数
            result_args[arg] = config.default_mode[arg]
        elif arg == 'config' or config.default_mode.get(arg):
            # 参数是配置文件忽略，或者指定了配置文件，默认参数均忽略
            pass
        else:
            # 其他参数（默认参数中配置的主要参数之外）
            result_args[arg] = all_args[arg]
    return result_args


def convert_args(args_dict):

    try:
        args_list = []
        exist_args_list = config.args_key_with_desc
        args_keys_string = u'\n'.join(exist_args_list)
        for a in args_dict:
            if not args_dict.get(a) and not config.default_mode.get(a):
                raise Exception(u'This argument has no value: %s' % a)
            args_detail = config.args_mapping.get(a)
            if not args_detail:
                raise Exception(u'Can not find this argument: %s!\n\nAvailable arguments are:\n\n%s' %
                                (a, unicode(args_keys_string)))
            if type(args_dict[a]) == type(True):
                if args_dict[a]:
                    args_list.extend([args_detail.get('option')])
                continue
            args_list.extend([args_detail.get('option'), str(args_dict[a])])

            #TODO print attention for some special args
        return args_list, None
    except Exception as e:
        return [], e.message


def print_available_args():
    for args in config.args_key_with_desc:
        print args


def cover_args(base_args_dict, cover_args_dict):

    base_args_dict = dict(base_args_dict)

    for arg in cover_args_dict:
        if not base_args_dict.get(arg) or cover_args_dict.get(arg):
            base_args_dict[arg] = cover_args_dict[arg]

    return base_args_dict
