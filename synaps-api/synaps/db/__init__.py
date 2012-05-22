# -*- coding:utf-8 -*-
# Copyright 2012 Samsung SDS
# All Rights Reserved

import time
import uuid
import pycassa
import datetime
from pycassa import types
import struct
import json

from collections import OrderedDict
from synaps import flags
from synaps import log as logging
from synaps import utils

LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS    

STAT_TYPE = types.CompositeType(types.IntegerType(), # statistics resolution
                                types.AsciiType()) # Average | SampleCount ...

RESOURCE_NUMBER_TYPE = types.CompositeType(
    types.UTF8Type(), # project_id
    types.UTF8Type(), # resource type (ex. 'alarm', 'alarm action')
    types.UTF8Type(), # resource name (ex. 'CPUUtilization-Cold-i128932')
) 

def certificate_create(admin, cert):
    # TBD: implement here
    pass

def certificate_get_all_by_user_and_project(admin, user_id, project_id):
    # TBD: implement here
    pass

def certificate_get_all_by_project(admin, project_id):
    # TBD: implement here
    pass

def certificate_get_all_by_user(admin, user_id):
    # TBD: implement here
    pass


class Cassandra(object):
    METRIC_TTL = FLAGS.get('metric_ttl')
    STATISTICS_TTL = FLAGS.get('statistics_ttl')
    ARCHIVE = map(lambda x: int(x) * 60, FLAGS.get('statistics_archives'))
    STATISTICS = ["Sum", "SampleCount", "Average", "Minimum", "Maximum"]
    
    def __init__(self):
        keyspace = FLAGS.get("cassandra_keyspace", "synaps_test")
        serverlist = FLAGS.get("cassandra_server_list")
        
        self.pool = pycassa.ConnectionPool(keyspace, server_list=serverlist)
        
        self.cf_metric = pycassa.ColumnFamily(self.pool, 'Metric')
        self.cf_metric_archive = pycassa.ColumnFamily(self.pool,
                                                      'MetricArchive')
        self.scf_stat_archive = pycassa.ColumnFamily(self.pool, 'StatArchive')
        self.cf_metricalarm = pycassa.ColumnFamily(self.pool, 'MetricAlarm')

    @staticmethod
    def syncdb():
        """
        카산드라 database schema 를 체크, 
        필요한 KEYSPACE, CF, SCF 가 없으면 새로 생성.
        """
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
                key_validation_class=pycassa.LEXICAL_UUID_TYPE
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
        
        if 'MetricArchive' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='MetricArchive',
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                comparator_type=pycassa.DATE_TYPE,
                default_validation_class=pycassa.DOUBLE_TYPE
            )

        if 'StatArchive' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='StatArchive', super=True,
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                comparator_type=STAT_TYPE,
                subcomparator_type=pycassa.DATE_TYPE,
                default_validation_class=pycassa.DOUBLE_TYPE
            )

        if 'MetricAlarm' not in column_families.keys():
            manager.create_column_family(
                keyspace=keyspace,
                name='MetricAlarm',
                key_validation_class=pycassa.LEXICAL_UUID_TYPE,
                column_validation_classes={
                    'project_id': pycassa.UTF8_TYPE,
                    'metric_id': pycassa.LEXICAL_UUID_TYPE,
                    'action_enabled': pycassa.BOOLEAN_TYPE,
                    'alarm_actions': pycassa.UTF8_TYPE,
                    'alarm_arn': pycassa.UTF8_TYPE,
                    'alarm_configuration_updated_timestamp': pycassa.DATE_TYPE,
                    'alarm_description': pycassa.UTF8_TYPE,
                    'alarm_name': pycassa.UTF8_TYPE,
                    'comparison_operator': pycassa.UTF8_TYPE,
                    'dimensions':pycassa.UTF8_TYPE,
                    'evaluation_period':pycassa.INT_TYPE,
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
                                 column='metric_id',
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
        
        LOG.info(_("cassandra syncdb has finished"))
    
    def _get_metric_data(self, project_id, namespace, metric_name, dimensions,
                        start, end):

        key = self.get_metric_key(project_id, namespace, metric_name,
                                  dimensions)
        return self.cf_metric_archive.get(key, column_start=start,
                                          column_finish=end)
    
        
    def get_metric_key(self, project_id, namespace, metric_name, dimensions):
        expr_list = [
            pycassa.create_index_expression("project_id", project_id),
            pycassa.create_index_expression("name", metric_name),
            pycassa.create_index_expression("namespace", namespace)             
        ]

        index_clause = pycassa.create_index_clause(expr_list)
        
        items = self.cf_metric.get_indexed_slices(index_clause)

        for k, v in items:
            if json.loads(v['dimensions']) == dimensions: 
                return k
        return None
    
    def get_metric_key_or_create(self, project_id, namespace, metric_name,
                                 dimensions):
        # get metric key
        key = self.get_metric_key(project_id, namespace, metric_name,
                                  dimensions)
        
        # or create metric 
        if not key:
            key = uuid.uuid4()
            json_dim = json.dumps(dimensions)
            columns = {'project_id': project_id, 'namespace': namespace,
                       'name': metric_name, 'dimensions': json_dim}
        
            self.cf_metric.insert(key=key, columns=columns)
        
        return key
    
    def get_metric_alarm_key(self, project_id, metric_key, metricalarm):
        """
        
        """
        expr_list = [
            pycassa.create_index_expression("project_id", project_id),
            pycassa.create_index_expression("metric_key", metric_key),
            pycassa.create_index_expression("alarm_name",
                                            metricalarm.alarm_name)
        ]
        
        index_clause = pycassa.create_index_clause(expr_list)
        items = self.cf_metricalarm.get_indexed_slices(index_clause)
        
        for k, v in items:
            return k
        
        return None
        

    def put_metric_alarm(self, project_id, metric_key, metricalarm):
        """
        MetricAlarm 을 DB에 생성 또는 업데이트 함.
        """
        # 해당 알람이 DB에 있는지 확인
        alarm_key = self.get_metric_alarm_key(project_id, metric_key,
                                              metricalarm)
        columns = metricalarm.to_columns()
        columns['alarm_arn'] = "rn:spcs:suwon:%s:alarm:%s" % (
            project_id, metricalarm.alarm_name
        )
        columns['alarm_configuration_updated_timestamp'] = utils.utcnow()
        
        if alarm_key:
            # TODO: 알람 업데이트 관련 알람 히스토리 생성
            pass
        else:
            # TODO: 알람 신규 관련 알람 히스토리 생성 
            alarm_key = uuid.uuid4()
            columns['state_updated_timestamp'] = utils.utcnow()
            columns['state_reason'] = "alarm initial setup"
            columns['state_reason_data'] = "{}"
            columns['state_value'] = "INSUFFICIENT_DATA"
            
        self.cf_metricalarm.insert(key=alarm_key, columns=columns)
        
        return alarm_key

    def put_metric_data(self, project_id, namespace, metric_name, dimensions,
                        value, unit=None, timestamp=None, metric_key=None):
        def get_stat(metric_id, super_column, aligned_timestamp):
            """
            super_column: (60, 'Average')
            """
            resolution, statistic = super_column
            try:
                ret = self.scf_stat_archive.get(metric_id,
                                                super_column=super_column,
                                                columns=[aligned_timestamp])
            except pycassa.NotFoundException:
                if statistic in ("Minimum", "Maximum"):
                    ret = {aligned_timestamp: None}
                else:
                    ret = {aligned_timestamp: 0.0}
            return ret.get(aligned_timestamp)

        def put_stats(metric_id, resolution, timestamp, value):
            stattime = utils.align_metrictime(timestamp, resolution)

            super_column_names = [(resolution, s) for s in self.STATISTICS]
            (p_sum, p_n_samples, p_avg, p_min, p_max) = [
                get_stat(metric_id, sc_name, stattime)
                for sc_name in super_column_names
            ]

            cur_sum = p_sum + value
            cur_n_samples = p_n_samples + 1
            cur_avg = cur_sum / cur_n_samples
            cur_min = value if p_min is None or p_min > value else p_min
            cur_max = value if p_max is None or p_max < value else p_max
            
            values = {
                (resolution, "Sum"): {stattime: cur_sum},
                (resolution, "SampleCount"): {stattime: cur_n_samples},
                (resolution, "Average"): {stattime: cur_avg},
                (resolution, "Minimum"): {stattime: cur_min},
                (resolution, "Maximum"): {stattime: cur_max},
            }
            
            self.scf_stat_archive.insert(metric_id, values,
                                         ttl=self.STATISTICS_TTL)
        
        
        key = metric_key if metric_key else self.get_metric_key_or_create(
            project_id, namespace, metric_name, dimensions
        )

        # if it doesn't hav a value to put, then return
        if value is None: 
            return key
        
        metric_col = {timestamp: value}
        self.cf_metric_archive.insert(key=key, columns=metric_col,
                                      ttl=self.METRIC_TTL)
        
        # and build statistics data
        stats = map(lambda r: put_stats(key, r, timestamp, value),
                    self.ARCHIVE)
        
        return key 

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
        
        expr_list = [pycassa.create_index_expression("project_id",
                                                     project_id), ]
        if namespace:
            expr = pycassa.create_index_expression("namespace", namespace)
            expr_list.append(expr)
            
        if metric_name:
            expr = pycassa.create_index_expression("name", metric_name)
            expr_list.append(expr)
            
        index_clause = pycassa.create_index_clause(expr_list)
        items = self.cf_metric.get_indexed_slices(index_clause)
        
        metrics = [(k, to_dict(v)) for k, v in items if check_dimension(v)]
        
        return metrics
    
    def get_metric_statistics(self, project_id, namespace, metric_name,
                              start_time, end_time, period, statistics,
                              unit=None, dimensions=None):
        # get metric key
        key = self.get_metric_key(project_id, namespace, metric_name,
                                   dimensions)

        # or return {}
        if not key:
            return {}
        
        stat_dict = {}
        for statistic in statistics:
            statistic = utils.to_ascii(statistic)
            super_column = (period, statistic)
            try:
                stat = self.scf_stat_archive.get(key,
                                                 super_column=super_column,
                                                 column_start=start_time,
                                                 column_finish=end_time)
            except pycassa.NotFoundException:
                LOG.debug("not found %s %s ~ %s" % (super_column, start_time,
                                                   end_time))
                stat = {}
                
            stat_dict[statistic] = stat

        # build stat info
        return self.restructed_stats(stat_dict)
    
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
