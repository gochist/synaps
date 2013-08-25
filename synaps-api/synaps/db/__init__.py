# -*- coding:utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2012 Samsung SDS Co., LTD
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time
import uuid
import pycassa
from datetime import datetime, timedelta
from pycassa import (types, create_index_clause, create_index_expression, EQ,
                     GT, GTE, LT, LTE)
import struct
import json
import pickle

from collections import OrderedDict
from synaps import flags
from synaps import log as logging
from synaps import utils
from synaps import exception

LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS    


def pack_dimensions(dimensions):
    return json.dumps(OrderedDict(sorted(dimensions.items())))

class Cassandra(object):
    STATISTICS = ["Sum", "SampleCount", "Average", "Minimum", "Maximum"]
    
    def __init__(self, keyspace=None):
        self.STATISTICS_TTL = FLAGS.get('statistics_ttl')
        self.ARCHIVE = map(lambda x: int(x) * 60, 
                           FLAGS.get('statistics_archives'))
        if not keyspace:
            keyspace = FLAGS.get("cassandra_keyspace", "synaps_test")
        serverlist = FLAGS.get("cassandra_server_list")
        
        # max_retries -1 means unlimited retries
        self.pool = pycassa.ConnectionPool(keyspace, server_list=serverlist,
                                           max_retries= -1)
        
        self.cf_metric = pycassa.ColumnFamily(self.pool, 'Metric')
        self.scf_stat_archive = pycassa.ColumnFamily(self.pool, 'StatArchive')
        self.cf_metric_alarm = pycassa.ColumnFamily(self.pool, 'MetricAlarm')
        self.cf_alarm_history = pycassa.ColumnFamily(self.pool, 'AlarmHistory')
        
    def delete_metric_alarm(self, alarm_key):
        try:
            self.cf_metric_alarm.remove(alarm_key)
        except pycassa.NotFoundException:
            LOG.info(_("alarm key %s is not deleted" % alarm_key))
    
    def _describe_alarms_by_names(self, project_id, alarm_names):
        for alarm_name in alarm_names:
            expr_list = [
                pycassa.create_index_expression("project_id", project_id),
                pycassa.create_index_expression("alarm_name", alarm_name)
            ]
            
            index_clause = pycassa.create_index_clause(expr_list)
            items = self.cf_metric_alarm.get_indexed_slices(index_clause)
            
            for k, v in items:
                yield k, v            

    def describe_alarms(self, project_id, action_prefix=None,
                        alarm_name_prefix=None, alarm_names=None,
                        max_records=100, next_token=None, state_value=None):
        """
        
        params:
            project_id: string
            action_prefix: TODO: not implemented yet.
            alarm_name_prefix: string
            alarm_names: string list
            max_records: integer
            next_token: string (uuid type)
            state_value: string (OK | ALARM | INSUFFICIENT_DATA)
        """
        if alarm_names:
            return self._describe_alarms_by_names(project_id, alarm_names)
        
        next_token = uuid.UUID(next_token) if next_token else ''
        
        expr_list = []
        prj_expr = create_index_expression("project_id", project_id)
        expr_list.append(prj_expr)
            
        if alarm_name_prefix:
            expr_s = create_index_expression("alarm_name", alarm_name_prefix,
                                             GTE)
            expr_e = create_index_expression("alarm_name",
                                           utils.prefix_end(alarm_name_prefix),
                                           LT)
            expr_list.append(expr_s)
            expr_list.append(expr_e)
        
        if state_value:
            expr = create_index_expression("state_value", state_value)
            expr_list.append(expr)
        LOG.info("expr %s" % expr_list)

        index_clause = create_index_clause(expr_list=expr_list,
                                           start_key=next_token,
                                           count=max_records)
        
        items = self.cf_metric_alarm.get_indexed_slices(index_clause)
        return items

    def describe_alarms_for_metric(self, project_id, namespace, metric_name,
                                   dimensions=None, period=None,
                                   statistic=None, unit=None):
        metric_key = self.get_metric_key(project_id, namespace, metric_name,
                                         dimensions)

        if not metric_key:
            raise exception.InvalidParameterValue("no metric")

        expr_list = [create_index_expression("metric_key", metric_key)]
        
        if period:
            expr = create_index_expression("period", int(period))
            expr_list.append(expr)
        
        if statistic:
            expr = create_index_expression("statistic", statistic)
            expr_list.append(expr)
            
        if unit:
            expr = create_index_expression("unit", unit)
            expr_list.append(expr)
        LOG.info("expr %s" % expr_list)
        index_clause = pycassa.create_index_clause(expr_list)
        items = self.cf_metric_alarm.get_indexed_slices(index_clause)
        return items

    def describe_alarm_history(self, project_id, alarm_name=None,
                               end_date=None, history_item_type=None,
                               max_records=100, next_token=None,
                               start_date=None):
        """
        
        params:
            project_id: string
            alarm_name: string
            end_date: datetime
            history_item_type: string (ConfigurationUpdate | StateUpdate |
                                       Action)
            max_records: integer
            next_token: string (uuid type)
            start_date: datetime
        """
        next_token = uuid.UUID(next_token) if next_token else ''
        
        expr_list = [
            pycassa.create_index_expression("project_id", project_id),
        ]
        
        if alarm_name:
            expr = create_index_expression("alarm_name", alarm_name)
            expr_list.append(expr)
        
        if end_date:
            expr = create_index_expression("timestamp", end_date, LTE)
            expr_list.append(expr)
        
        if start_date:
            expr = create_index_expression("timestamp", start_date, GTE)
            expr_list.append(expr)
        
        if history_item_type:
            expr = create_index_expression("history_item_type",
                                           history_item_type)
            expr_list.append(expr)
        
        index_clause = pycassa.create_index_clause(expr_list=expr_list,
                                                   start_key=next_token,
                                                   count=max_records)
        items = self.cf_alarm_history.get_indexed_slices(index_clause)
        return items        

    def get_metric_alarm_key(self, project_id, alarm_name):
        expr_list = [
            pycassa.create_index_expression("project_id", project_id),
            pycassa.create_index_expression("alarm_name", alarm_name)
        ]
        
        index_clause = pycassa.create_index_clause(expr_list)
        items = self.cf_metric_alarm.get_indexed_slices(index_clause)
        
        for k, v in items:
            return k
        return None
    
    def get_metric_alarm(self, alarm_key):
        ret = None
        try:
            ret = self.cf_metric_alarm.get(alarm_key)
        except pycassa.NotFoundException:
            pass
        return ret
            
    def get_metric_key(self, project_id, namespace, metric_name, dimensions):
        dimensions = pack_dimensions(dimensions)
        expr_list = [
            pycassa.create_index_expression("project_id", project_id),
            pycassa.create_index_expression("name", metric_name),
            pycassa.create_index_expression("namespace", namespace),
            pycassa.create_index_expression("dimensions", dimensions)
        ]

        index_clause = pycassa.create_index_clause(expr_list)
        
        items = self.cf_metric.get_indexed_slices(index_clause)

        for k, v in items:
            return k
        return None
    
    def get_metric_key_or_create(self, project_id, namespace, metric_name,
                                 dimensions, unit='None'):
        # get metric key
        key = self.get_metric_key(project_id, namespace, metric_name,
                                  dimensions)
        
        # or create metric 
        if not key:
            key = uuid.uuid4()
            json_dim = pack_dimensions(dimensions)
            columns = {'project_id': project_id, 'namespace': namespace,
                       'name': metric_name, 'dimensions': json_dim,
                       'unit': unit}
            
            self.cf_metric.insert(key=key, columns=columns)
        
        return key

    def get_metric_statistics(self, project_id, namespace, metric_name,
                              start_time, end_time, period, statistics,
                              dimensions=None):
        def get_stat(key, super_column, column_start, column_end):
            stat = {}
            count = (column_end - column_start).total_seconds() / 60
            try:
                stat = self.scf_stat_archive.get(key,
                                                 super_column=super_column,
                                                 column_start=column_start,
                                                 column_finish=column_end,
                                                 column_count=count)
            except pycassa.NotFoundException:
                LOG.debug("not found %s %s %s %s" % (key, super_column,
                                                     column_start,
                                                     column_end))
            
            return stat
        
        # get metric key
        key = self.get_metric_key(project_id, namespace, metric_name,
                                  dimensions)

        # or return {}
        if not key:
            return {}

        statistics = map(utils.to_ascii, statistics)
        stats = map(lambda x: get_stat(key, x, start_time, end_time),
                    statistics)
        
        return stats
    
    def get_metric_statistics_for_key(self, key, time_idx):
        
        def get_stat(key, super_column, column_start, column_end):
            stat = {}
            try:
                stat = self.scf_stat_archive.get(key,
                                                 super_column=super_column,
                                                 column_start=column_start,
                                                 column_finish=column_end,
                                                 column_count=1440)
            except pycassa.NotFoundException:
                LOG.debug("not found %s %s %s %s" % (key, super_column,
                                                     column_start,
                                                     column_end))
            
            return stat
        
        if not key:
            return {}

        stats = map(lambda x: get_stat(key, x, time_idx, time_idx),
                    self.STATISTICS)
        
        return stats
            
    def get_metric_unit(self, metric_key):
        try:
            metric = self.cf_metric.get(key=metric_key)
        except pycassa.NotFoundException:
            return "None"
        return metric.get('unit', "None")

    def insert_stat(self, metric_key, stat, ttl=None):
        ttl = ttl if ttl else self.STATISTICS_TTL
        self.scf_stat_archive.insert(metric_key, stat, ttl=ttl)
    
    def insert_alarm_history(self, key, column):
        self.cf_alarm_history.insert(key, column, ttl=self.STATISTICS_TTL)
        
    def update_alarm_state(self, alarmkey, state, reason, reason_data,
                           timestamp):
        state_info = {'state_value': state, 'state_reason': reason,
                      'state_reason_data': reason_data,
                      'state_updated_timestamp':timestamp}
        self.cf_metric_alarm.insert(alarmkey, state_info)

    def list_metrics(self, project_id, namespace=None, metric_name=None,
                     dimensions=None, next_token=""):
        def to_dict(v):
            return {'project_id': v['project_id'],
                    'dimensions': json.loads(v['dimensions']),
                    'name': v['name'],
                    'namespace': v['namespace']}
        
        def check_dimension(item):
            if isinstance(dimensions, dict): 
                def to_set(d):
                    return set(d.items())
                    
                l_set = to_set(dimensions)
                r_set = to_set(json.loads(item['dimensions']))
                return l_set.issubset(r_set)
            return True

        next_token = uuid.UUID(next_token) if next_token else ''
        expr_list = [pycassa.create_index_expression("project_id",
                                                     project_id), ]
        if namespace:
            expr = pycassa.create_index_expression("namespace", namespace)
            expr_list.append(expr)
            
        if metric_name:
            expr = pycassa.create_index_expression("name", metric_name)
            expr_list.append(expr)
            
        if dimensions:
            packed_dimensions = pack_dimensions(dimensions)
            expr = pycassa.create_index_expression("dimensions",
                                                   packed_dimensions)
            expr_list.append(expr)
            
        index_clause = pycassa.create_index_clause(expr_list,
                                                   start_key=next_token,
                                                   count=501)
        items = self.cf_metric.get_indexed_slices(index_clause)
        metrics = ((k, to_dict(v)) for k, v in items)
        return metrics
    
    def load_metric_data(self, metric_key):
        try:
            data = self.cf_metric_archive.get(metric_key, column_count=1440)
        except pycassa.NotFoundException:
            data = {}
        return data
    
    def load_statistics(self, metric_key, start, finish):
        def get_stat(statistic):
            datapoints = self.scf_stat_archive.get(metric_key,
                                                   super_column=statistic,
                                                   column_start=start,
                                                   column_finish=finish)
            return statistic, datapoints
        
        try:
            stat = dict([get_stat(statistic) 
                         for statistic in self.STATISTICS])
            
        except pycassa.NotFoundException:
            stat = {}

        return stat

    def load_alarms(self, metric_key):
        expr_list = [
            pycassa.create_index_expression("metric_key", metric_key),
        ]
        index_clause = pycassa.create_index_clause(expr_list)

        try:
            items = self.cf_metric_alarm.get_indexed_slices(index_clause)
        except pycassa.NotFoundException:
            items = {}
        return items
    
    def put_metric_alarm(self, alarm_key, metricalarm):
        """
        MetricAlarm 을 DB에 생성 또는 업데이트 함.
        """
        self.cf_metric_alarm.insert(key=alarm_key, columns=metricalarm)
        return alarm_key
        
    def restructed_stats(self, stat):
        def get_stat(timestamp):
            ret = {}
            for key in stat.keys():
                ret[key] = stat[key][timestamp]
            return ret
        
        ret = []
        timestamps = reduce(lambda x, y: x if x == y else None,
                            map(lambda x: x.keys(), stat.values()))
        
        for timestamp in timestamps:
            ret.append((timestamp, get_stat(timestamp)))

        return ret

    @staticmethod
    def syncdb(keyspace=None):
        """
        카산드라 database schema 를 체크, 
        필요한 KEYSPACE, CF, SCF 가 없으면 새로 생성.
        """
        if not keyspace:
            keyspace = FLAGS.get("cassandra_keyspace", "synaps_test")
        serverlist = FLAGS.get("cassandra_server_list")
        replication_factor = FLAGS.get("cassandra_replication_factor")
        manager = pycassa.SystemManager(server=serverlist[0])
        strategy_options = {'replication_factor':replication_factor}
        

        # keyspace 체크, keyspace 가 없으면 새로 생성
        LOG.info(_("cassandra syncdb is started for keyspace(%s)" % keyspace))
        if keyspace not in manager.list_keyspaces():
            LOG.info(_("cassandra keyspace %s does not exist.") % keyspace)
            manager.create_keyspace(keyspace, strategy_options=strategy_options)
            LOG.info(_("cassandra keyspace %s is created.") % keyspace)
        else:
            property = manager.get_keyspace_properties(keyspace)
            
            # strategy_option 체크, option 이 다르면 수정
            if not (strategy_options == property.get('strategy_options')):
                manager.alter_keyspace(keyspace,
                                       strategy_options=strategy_options)
                LOG.info(_("cassandra keyspace strategy options is updated - %s" 
                           % str(strategy_options)))
        
        # CF 체크
        column_families = manager.get_keyspace_column_families(keyspace)        
        
        if 'Metric' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='Metric',
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                column_validation_classes={
                    'project_id': pycassa.UTF8_TYPE,
                    'name': pycassa.UTF8_TYPE,
                    'namespace': pycassa.UTF8_TYPE,
                    'unit': pycassa.UTF8_TYPE,
                    'dimensions': pycassa.UTF8_TYPE
                }
            )
            manager.create_index(keyspace=keyspace, column_family='Metric',
                                column='project_id',
                                value_type=types.UTF8Type())
            manager.create_index(keyspace=keyspace, column_family='Metric',
                                 column='name',
                                 value_type=types.UTF8Type())
            manager.create_index(keyspace=keyspace, column_family='Metric',
                                 column='namespace',
                                 value_type=types.UTF8Type())
            manager.create_index(keyspace=keyspace, column_family='Metric',
                                 column='dimensions',
                                 value_type=types.UTF8Type())


        if 'StatArchive' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='StatArchive', super=True,
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                comparator_type=pycassa.ASCII_TYPE,
                subcomparator_type=pycassa.DATE_TYPE,
                default_validation_class=pycassa.DOUBLE_TYPE
            )

        if 'MetricAlarm' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='MetricAlarm',
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                column_validation_classes={
                    'metric_key': pycassa.LEXICAL_UUID_TYPE,
                    'project_id': pycassa.UTF8_TYPE,
                    'actions_enabled': pycassa.BOOLEAN_TYPE,
                    'alarm_actions': pycassa.UTF8_TYPE,
                    'alarm_arn': pycassa.UTF8_TYPE,
                    'alarm_configuration_updated_timestamp': pycassa.DATE_TYPE,
                    'alarm_description': pycassa.UTF8_TYPE,
                    'alarm_name': pycassa.UTF8_TYPE,
                    'comparison_operator': pycassa.UTF8_TYPE,
                    'dimensions':pycassa.UTF8_TYPE,
                    'evaluation_periods':pycassa.INT_TYPE,
                    'insufficient_data_actions': pycassa.UTF8_TYPE,
                    'metric_name':pycassa.UTF8_TYPE,
                    'namespace':pycassa.UTF8_TYPE,
                    'ok_actions':pycassa.UTF8_TYPE,
                    'period':pycassa.INT_TYPE,
                    'state_reason':pycassa.UTF8_TYPE,
                    'state_reason_data':pycassa.UTF8_TYPE,
                    'state_updated_timestamp':pycassa.DATE_TYPE,
                    'state_value':pycassa.UTF8_TYPE,
                    'statistic':pycassa.UTF8_TYPE,
                    'threshold':pycassa.DOUBLE_TYPE,
                    'unit':pycassa.UTF8_TYPE
                }
            )

            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='project_id',
                                 value_type=types.UTF8Type())            
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='metric_key',
                                 value_type=types.LexicalUUIDType())
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='alarm_name',
                                 value_type=types.UTF8Type())
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='state_updated_timestamp',
                                 value_type=types.DateType())
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='alarm_configuration_updated_timestamp',
                                 value_type=types.DateType())
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='state_value',
                                 value_type=types.UTF8Type())
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='period',
                                 value_type=types.IntegerType())
            manager.create_index(keyspace=keyspace,
                                 column_family='MetricAlarm',
                                 column='statistic',
                                 value_type=types.UTF8Type())
            
        if 'AlarmHistory' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='AlarmHistory',
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                column_validation_classes={
                    'project_id': pycassa.UTF8_TYPE,
                    'alarm_key': pycassa.LEXICAL_UUID_TYPE,
                    'alarm_name': pycassa.UTF8_TYPE,
                    'history_data': pycassa.UTF8_TYPE,
                    'history_item_type': pycassa.UTF8_TYPE,
                    'history_summary': pycassa.UTF8_TYPE,
                    'timestamp': pycassa.DATE_TYPE,
                }
            )

            manager.create_index(keyspace=keyspace,
                                 column_family='AlarmHistory',
                                 column='project_id',
                                 value_type=types.UTF8Type())   
            
            manager.create_index(keyspace=keyspace,
                                 column_family='AlarmHistory',
                                 column='alarm_key',
                                 value_type=types.LexicalUUIDType())    
              
            manager.create_index(keyspace=keyspace,
                                 column_family='AlarmHistory',
                                 column='alarm_name',
                                 value_type=types.UTF8Type())            
            
            manager.create_index(keyspace=keyspace,
                                 column_family='AlarmHistory',
                                 column='history_item_type',
                                 value_type=types.UTF8Type())            
            
            manager.create_index(keyspace=keyspace,
                                 column_family='AlarmHistory',
                                 column='timestamp',
                                 value_type=types.DateType())            
                        
        LOG.info(_("cassandra syncdb has finished"))

