#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import pytest

from airflow.models import Connection
from airflow.models.dag import DAG
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.mongo.sensors.mongo import MongoSensor
from airflow.utils import db, timezone

DEFAULT_DATE = timezone.datetime(2017, 1, 1)


@pytest.mark.integration("mongo")
class TestMongoSensor:
    def setup_method(self):
        db.merge_conn(
            Connection(conn_id="mongo_test", conn_type="mongo", host="mongo", port=27017, schema="test")
        )

        args = {"owner": "airflow", "start_date": DEFAULT_DATE}
        self.dag = DAG("test_dag_id", default_args=args)

        hook = MongoHook("mongo_test")
        hook.insert_one("foo", {"bar": "baz"})

        self.sensor = MongoSensor(
            task_id="test_task",
            mongo_conn_id="mongo_test",
            dag=self.dag,
            collection="foo",
            query={"bar": "baz"},
        )

    def test_poke(self):
        assert self.sensor.poke(None)

    def test_sensor_with_db(self):
        hook = MongoHook("mongo_test")
        hook.insert_one("nontest", {"1": "2"}, mongo_db="nontest")

        sensor = MongoSensor(
            task_id="test_task2",
            mongo_conn_id="mongo_test",
            dag=self.dag,
            collection="nontest",
            query={"1": "2"},
            mongo_db="nontest",
        )
        assert sensor.poke(None)
