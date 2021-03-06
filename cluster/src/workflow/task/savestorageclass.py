# -*- coding: utf-8 -*-
# Copyright (c) 20016-2016 The Cloudsoar.
# See LICENSE for details.
"""
保存StorageClass信息
"""

from common.util import Result
from frame.exception import InternalException
from frame.logger import PrintStack, Log
from frame.subtask import SubTask, SAVE_STORAGE_CLASS_TASK_SUFFIX, SAVE_STORAGE_CLASS_TASK, \
    SAVE_STORAGE_CLASS_INDEX


class SaveStorageClassInfoTask(SubTask):
    
    def __init__(self, task_info, workbench):
        super(SaveStorageClassInfoTask, self).__init__(task_info, SAVE_STORAGE_CLASS_TASK_SUFFIX)
        self.task_type = SAVE_STORAGE_CLASS_TASK
        self.index = SAVE_STORAGE_CLASS_INDEX
        self.weight = 0.8
        self.workbench = workbench
    
    def launch_task(self):
        Log(4,"SaveStorageClassInfoTask.launch_task")
        try:
            rlt = self.workbench.save_storage_class_info()
            if rlt.success:
                self.log("save_storage_class_info success.")
            else:
                self.log("save_storage_class_info fail. as[%s]"%(rlt.message))
                return rlt
                    
        except InternalException,ex:
            self.log("SaveStorageClassInfoTask save_storage_class_info fail,as[%s]"%(ex.value),ex.errid)
            return Result('InternalException', ex.errid, "SaveStorageClassInfoTask launch_task fail,as[%s]"%(ex.value))
                
        except Exception,e:
            PrintStack()
            self.log("launch_task except[%s]"%(str(e)))
            Log(1,"SaveStorageClassInfoTask launch_task fail,as[%s]"%(str(e)))
            return Result(self._id, 1, "SaveStorageClassInfoTask launch_task fail,as[%s]"%(str(e)))
        
        return Result(self._id)

    def snapshot(self):
        snap = super(SaveStorageClassInfoTask, self).snapshot()
        return snap
        
    
    def rollback(self):
        """
        # rollback 由外部触发，任务本身失败了，不会触发rollback
        """
        Log(4,"SaveStorageClassInfoTask.rollback")
        rlt = self.workbench.delete_storage_class_info()
        if rlt.success:
            self.log("delete_storage_class_info success.")
        else:
            self.log("delete_storage_class_info fail. as[%s]"%(rlt.message))
        return rlt

        