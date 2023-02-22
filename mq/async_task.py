#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/12/26 17:28
# FileName: 异步任务

import traceback

from utils import util, context, thread_func, log_sls


def delay(func, *args, **kwargs):
    task_id = util.gen_unique_str()
    log_sls.info('async_task', '发布异步任务', task_id=task_id)       # 根据此条日志，关联request_id与task_id

    def action(task_id_, fc, values, options):
        context.set_args('task_id', task_id_)
        try:
            fc(*values, **options)
        except Exception as e:
            log_sls.error('async_task', '异步任务出现异常', func=func.__name__, args=values, kwargs=options,
                          e=str(e), trace=str(traceback.format_exc()))

    thread_func.submit(action, task_id, func, args, kwargs)
    return task_id
