# -*- coding: utf-8 -*-
# Copyright 2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import absolute_import
from __future__ import unicode_literals

from contextlib import contextmanager

import staticconf

from data_pipeline.config import configure_from_dict
from data_pipeline.config import namespace


@contextmanager
def reconfigure(**kwargs):
    """Reconfigures the given kwargs, restoring the current configuration for
    only those kwargs when the contextmanager exits.
    """
    conf_namespace = staticconf.config.get_namespace(namespace)
    starting_config = {
        k: v for k, v in conf_namespace.get_config_values().iteritems()
        if k in kwargs
    }
    configure_from_dict(kwargs)
    try:
        yield
    finally:
        final_config = {
            k: v for k, v in conf_namespace.get_config_values().iteritems()
            if k not in kwargs
        }
        final_config.update(starting_config)
        staticconf.config.get_namespace(namespace).clear()
        configure_from_dict(final_config)
