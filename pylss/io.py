#!/usr/bin/env python
#
# Copyright (C) 2026 Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import yaml
import csv
import io
import logging

logger = logging.getLogger(__name__)

class LSSExperiment:
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data # List of dicts or rows

    @property
    def t0(self):
        return self.metadata.get('t0') or self.metadata.get('time_zero')

    @property
    def dwell_volume(self):
        return self.metadata.get('dwell_volume') or self.metadata.get('vd')

    @property
    def flow_rate(self):
        return self.metadata.get('flow_rate') or self.metadata.get('flow')

    @property
    def column_length(self):
        return self.metadata.get('column_length') or self.metadata.get('length', 15.0)

    @property
    def column_diameter(self):
        return self.metadata.get('column_diameter') or self.metadata.get('diameter', 2.1)

    @property
    def column_particle(self):
        return self.metadata.get('column_particle') or self.metadata.get('particle', 1.7)

    @property
    def gradients(self):
        return self.metadata.get('gradients', [])

def parse_lss_input(file_path):
    """
    Parses a PyLSS input file with YAML frontmatter and CSV data.
    Format:
    ---
    t0: 0.969
    dwell_volume: 0.375
    flow_rate: 0.30
    gradients:
      - [14, 5, 95] # tg, startB, endB
      - [60, 5, 96]
    ---
    Molecule; Tr1; Tr2
    Steroid_A; 8.53; 22.11
    """
    with open(file_path, 'r') as f:
        content = f.read()

    parts = content.split('---')
    
    # Handle files with or without frontmatter
    if len(parts) >= 3:
        # standard frontmatter format
        header = yaml.safe_load(parts[1])
        if not isinstance(header, dict):
            header = {}
        data_str = parts[2].strip()
    else:
        # Fallback for old format or simple files
        # This is a very basic fallback, can be improved
        logger.warning("No standard YAML frontmatter found. Attempting legacy parsing.")
        return parse_legacy_input(file_path)

    # Parse CSV data
    data = []
    if data_str:
        # Try to detect delimiter
        dialect = csv.Sniffer().sniff(data_str[:1024]) if ';' in data_str or ',' in data_str else None
        if dialect:
            reader = csv.reader(io.StringIO(data_str), dialect)
        else:
            # Default to semicolon if sniffer fails but it looks like CSV
            reader = csv.reader(io.StringIO(data_str), delimiter=';')
        
        for row in reader:
            if row:
                data.append([item.strip() for item in row])

    return LSSExperiment(header, data)

def parse_legacy_input(file_path):
    """Fallback parser for the original PyLSS format."""
    from typing import Dict, Any
    metadata: Dict[str, Any] = {}
    data = []
    gradients = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            if ':' in line:
                key, val = [part.strip() for part in line.split(':', 1)]
                key_lower = key.lower()
                if 'time zero' in key_lower: metadata['t0'] = float(val)
                elif 'dwell volume' in key_lower: metadata['dwell_volume'] = float(val)
                elif 'flow rate' in key_lower: metadata['flow_rate'] = float(val)
                elif 'gradient' in key_lower:
                    v = val.split()
                    gradients.append([float(v[0]), float(v[1]), float(v[2])])
                elif 'column length' in key_lower: metadata['column_length'] = float(val)
                elif 'column diameter' in key_lower: metadata['column_diameter'] = float(val)
                elif 'column particle' in key_lower: metadata['column_particle'] = float(val)
            else:
                # Assume it's data
                row = [item.strip() for item in line.split(';') if item.strip()]
                if row:
                    data.append(row)
                    
    metadata['gradients'] = gradients
    return LSSExperiment(metadata, data)
