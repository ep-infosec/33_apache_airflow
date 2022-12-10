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

import importlib
import logging

# HACK:
# Sphinx-autoapi doesn't like imports to excluded packages in the main module.
conf = importlib.import_module("airflow.configuration").conf  # type: ignore[attr-defined]

PROVIDERS_GOOGLE_VERBOSE_LOGGING: bool = conf.getboolean(
    "providers_google", "VERBOSE_LOGGING", fallback=False
)
if PROVIDERS_GOOGLE_VERBOSE_LOGGING:
    for logger_name in ["google_auth_httplib2", "httplib2", "googleapiclient"]:
        logger = logging.getLogger(logger_name)
        logger.handlers += [
            handler for handler in logging.getLogger().handlers if handler.name in ["task", "console"]
        ]
        logger.level = logging.DEBUG
        logger.propagate = False

    import httplib2

    httplib2.debuglevel = 4
