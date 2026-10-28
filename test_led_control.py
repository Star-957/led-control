"""Offline call-trace tests. The OpenRGB SDK is replaced before any entrypoint runs."""
import contextlib
import io
from pathlib import Path
import runpy
import sys
import types
import unittest
from unittest.mock import patch


class LedEntryTests(unittest.TestCase):
    def run_entry(self, filename, motherboard=True, connection_failure=False):
        calls = []
        zone = types.SimpleNamespace(name='header', type='LINEAR', leds=[0])
        def resize(count):
            calls.append(('resize', count))
            zone.leds = [0] * count
        zone.resize = resize
        zone.set_color = lambda rgb: calls.append(('zone-color', rgb))
        board = types.SimpleNamespace(name='board', type='MOTHERBOARD' if motherboard else 'OTHER',
                                      zones=[zone], modes=[types.SimpleNamespace(name='Direct')])
        board.set_mode = lambda mode: calls.append(('mode', mode))
        board.set_color = lambda rgb: calls.append(('device-color', rgb))
        other = types.SimpleNamespace(name='untargeted', type='OTHER', zones=[], modes=[])
        other.set_color = lambda rgb: calls.append(('other-color', rgb))
        def connect(name):
            calls.append(('connect', name))
            if connection_failure:
                raise ConnectionError('fixture offline')
            return types.SimpleNamespace(devices=[board, other])
        sdk = types.ModuleType('openrgb')
        sdk.OpenRGBClient = connect
        utils = types.ModuleType('openrgb.utils')
        utils.RGBColor = lambda r, g, b: (r, g, b)
        utils.ZoneType = types.SimpleNamespace(LINEAR='LINEAR', MATRIX='MATRIX')
        utils.DeviceType = types.SimpleNamespace(MOTHERBOARD='MOTHERBOARD')
        code = 0
        with patch.dict(sys.modules, {'openrgb':sdk, 'openrgb.utils':utils}), patch('time.sleep'), contextlib.redirect_stdout(io.StringIO()):
            try:
                runpy.run_path(str(Path(__file__).with_name(filename)), run_name='__main__')
            except SystemExit as exc:
                code = exc.code
        return calls, code

    def test_black_and_white_preserve_device_sequence(self):
        for script, color, client in [('fans_off.py',(0,0,0),'led-control-fans-off'),
                                      ('leds_white.py',(255,255,255),'led-control-leds-white')]:
            with self.subTest(script=script):
                calls, code = self.run_entry(script)
                self.assertEqual(code, 0)
                self.assertEqual(calls, [('connect',client),('mode','Direct'),('resize',120),
                                         ('zone-color',color),('device-color',color)])

    def test_without_motherboard_all_devices_are_selected(self):
        calls, code = self.run_entry('fans_off.py', motherboard=False)
        self.assertEqual(code, 0)
        self.assertIn(('other-color',(0,0,0)), calls)

    def test_connection_failure_remains_bounded_and_nonzero(self):
        calls, code = self.run_entry('fans_off.py', connection_failure=True)
        self.assertEqual(code, 2)
        self.assertEqual(len(calls), 12)

    def test_missing_sdk_reports_import_failure_without_hardware(self):
        with patch.dict(sys.modules, {'openrgb': None, 'openrgb.utils': None}), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as stopped:
                runpy.run_path(str(Path(__file__).with_name('fans_off.py')), run_name='__main__')
        self.assertEqual(stopped.exception.code, 3)


if __name__ == '__main__':
    unittest.main()
