# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2010 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.


from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.api import IGrapher
from timeside.grapher.core import *


class WaveformAwdio(Processor):
    implements(IGrapher)
    
    FFT_SIZE = 0x400

    @interfacedoc
    def __init__(self, width=572, height=74, bg_color=None, color_scheme='awdio'):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.color_scheme = color_scheme

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_awdio"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform Awdio"

    @interfacedoc
    def set_colors(self, background, scheme):
        self.bg_color = background
        self.color_scheme = scheme

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(WaveformAwdio, self).setup(channels, samplerate, nframes)
        self.graph = WaveformImageSimple(self.width, self.height, self.nframes(), self.samplerate(), self.FFT_SIZE, 
                                    bg_color=self.bg_color, color_scheme=self.color_scheme)
    
    @interfacedoc
    def process(self, frames, eod=False):
        self.graph.process(frames, eod)
        return frames, eod

    @interfacedoc
    def render(self, output):
        if output:
            self.graph.save(output)
        return self.graph.image
        
    def watermark(self, text, font=None, color=(255, 255, 255), opacity=.6, margin=(5,5)):
        self.graph.watermark(text, color=color, opacity=opacity, margin=margin)
