# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

import os
import Options
from os import unlink, link
from os.path import exists

srcdir = '.'
blddir = 'build'
VERSION = '0.1'

def set_options(opt):
  opt.tool_options('compiler_cxx')

def configure(conf):
  conf.check_tool('compiler_cxx')
  conf.check_tool('node_addon')
  conf.check_cfg(package='protobuf', args='--cflags --libs', uselib_store='PROTOBUF')
  conf.env.append_value('CCFLAGS', ['-O3'])
  conf.env.append_value('CXXFLAGS', ['-O3'])
  if Options.platform == 'darwin': conf.env.append_value('LINKFLAGS', ['-undefined', 'dynamic_lookup'])

def build(bld):
  obj = bld.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.target = 'protobuf'
  obj.source = ['addon.cc', 'protobuf_for_node.cc']
  obj.uselib = ['NODE', 'PROTOBUF']

def shutdown():
  # HACK to get protobuf.node out of build directory.
  # better way to do this?
  if exists('./protobuf.node'):
    unlink('./protobuf.node')
  if Options.commands['build']:
    if exists('./build/default/protobuf.node'):
      link('./build/default/protobuf.node', './protobuf.node')
    elif exists('./build/Release/protobuf.node'):
      link('./build/Release/protobuf.node', './protobuf.node')
    else:
      raise Exception("Cannot locate build protobuf.node")

