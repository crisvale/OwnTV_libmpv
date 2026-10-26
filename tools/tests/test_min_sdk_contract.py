import sys
import types
import unittest
from pathlib import Path


dynamic = types.ModuleType("elftools.elf.dynamic")
dynamic.DynamicSection = object
elffile = types.ModuleType("elftools.elf.elffile")
elffile.ELFFile = object
sys.modules.setdefault("elftools", types.ModuleType("elftools"))
sys.modules.setdefault("elftools.elf", types.ModuleType("elftools.elf"))
sys.modules.setdefault("elftools.elf.dynamic", dynamic)
sys.modules.setdefault("elftools.elf.elffile", elffile)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inspect_aar import EXPECTED_MIN_SDK, manifest_min_sdk


class MinSdkContractTest(unittest.TestCase):
    def test_accepts_api_25_manifest(self):
        manifest = b'<manifest><uses-sdk android:minSdkVersion="25" /></manifest>'
        self.assertEqual(EXPECTED_MIN_SDK, manifest_min_sdk(manifest))

    def test_rejects_api_26_manifest(self):
        manifest = b'<manifest><uses-sdk android:minSdkVersion="26" /></manifest>'
        self.assertNotEqual(EXPECTED_MIN_SDK, manifest_min_sdk(manifest))


if __name__ == "__main__":
    unittest.main()
