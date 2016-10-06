#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Dirk Toewe
#
# This file is part of Makerspace Cura Launcher.
#
# Makerspace Cura Launcher is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# Makerspace Cura Launcher is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Makerspace Cura Launcher. If not, see
# <http://www.gnu.org/licenses/>.
'''
Created on Sep 28, 2016

@author: Dirk Toewe
'''
import logging

from Cura.gui.sceneView import SceneView
from Cura.util import gcodeInterpreter, sliceEngine
from Cura.util.gcodeInterpreter import gcode
from Cura.util.sliceEngine import EngineResult
from pkg_resources import resource_filename
import os


def main():

  def getCost( profile, length, weight ):

    cost_kg    = profile.getPreferenceFloat('filament_cost_kg')
    cost_meter = profile.getPreferenceFloat('filament_cost_meter') / 1000.0

    if cost_kg > 0.0 and cost_meter > 0.0:
      return "%.2f EUR (weight*EUR/kg)\n%.2f EUR (length*EUR/m)" % (weight * cost_kg, length * cost_meter)
    elif cost_kg > 0.0:
      return "%.2f EUR" % (weight * cost_kg)
    elif cost_meter > 0.0:
      return "%.2f EUR" % (length * cost_meter)
    return None  

  gcode.calculateCost          = lambda self    : getCost( gcodeInterpreter.profile, self.extrusionAmount, self.calculateWeight() )
  EngineResult.getFilamentCost = lambda self,e=0: getCost(      sliceEngine.profile, self._filamentMM[e],  self.getFilamentWeight(e) )

  _drawMachine = SceneView._drawMachine

  machine_names = {}

  def drawMachine(self):

    try:
      from Cura.gui.sceneView import profile, meshLoader, openglHelpers, numpy
  
      machine_type = profile.getMachineSetting('machine_type')
      machine_name = profile.getMachineSetting('machine_name')
      if machine_type not in self._platformMesh or machine_name != machine_names[machine_type]:
        self._platformMesh[machine_type] = None
        machine_names[machine_type] = machine_name
  
        filename = None
        texture_name = None
        offset = [0,0,0]
        texture_offset = [0,0,0]
        texture_scale = 1.0

        print machine_type
        print machine_name

        if machine_name == 'Prusa Mendel i3':
          filename = os.path.expanduser('~')+'/Documents/Cura Printer Models/prusa_i3.stl'
          print filename
          offset = [+180,-50,60]
  
        if filename is not None:
          meshes = meshLoader.loadMeshes(filename)
          if len(meshes) > 0:
            self._platformMesh[machine_type] = meshes[0]
            self._platformMesh[machine_type]._drawOffset = numpy.array(offset, numpy.float32)
            self._platformMesh[machine_type].texture = None
            if texture_name is not None:
              self._platformMesh[machine_type].texture = openglHelpers.loadGLTexture(texture_name)
              self._platformMesh[machine_type].texture_offset = texture_offset
              self._platformMesh[machine_type].texture_scale = texture_scale
  
      return _drawMachine(self)
    except Exception as e:
      logging.exception('test')

  SceneView._drawMachine = drawMachine

  import Cura.cura as cura

  cura.main()

if '__main__' == __name__:
  main()