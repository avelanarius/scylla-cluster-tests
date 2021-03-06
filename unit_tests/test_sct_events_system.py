# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2020 ScyllaDB

import pickle
import unittest
from textwrap import dedent

from sdcm.sct_events.system import \
    StartupTestEvent, TestFrameworkEvent, SpotTerminationEvent, InfoEvent, \
    ThreadFailedEvent, CoreDumpEvent, TestResultEvent


class TestSystemEvents(unittest.TestCase):
    def test_startup_test_event(self):
        event = StartupTestEvent()
        self.assertEqual(str(event), "(StartupTestEvent Severity.NORMAL)")
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_test_framework_event(self):
        event = TestFrameworkEvent(source="s1",
                                   source_method="m1",
                                   args=("a1", "a2", ),
                                   kwargs={"k1": "v1", "k2": "v2", },
                                   message="msg1",
                                   exception="e1")
        self.assertEqual(
            str(event),
            "(TestFrameworkEvent Severity.ERROR), source=s1.m1(args=('a1', 'a2'), kwargs={'k1': 'v1', 'k2': 'v2'})"
            " message=msg1\nexception=e1",
        )
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_spot_termination_event(self):
        event = SpotTerminationEvent(node="node1", message="m1")
        self.assertEqual(str(event), "(SpotTerminationEvent Severity.CRITICAL): node=node1 message=m1")
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_info_event(self):
        event = InfoEvent(message="m1")
        self.assertEqual(str(event), "(InfoEvent Severity.NORMAL): message=m1")
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_thread_failed_event(self):
        event = ThreadFailedEvent(message="m1", traceback="t1")
        self.assertEqual(str(event), "(ThreadFailedEvent Severity.ERROR): message=m1\nt1")
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_coredump_event(self):
        event = CoreDumpEvent(node="node1", corefile_url="url1", backtrace="b1", download_instructions="d1")
        self.assertEqual(
            str(event),
            "(CoreDumpEvent Severity.ERROR) node=node1\ncorefile_url=url1\nbacktrace=b1\ndownload_instructions=d1\n",
        )
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_test_result_event_fail(self):
        event = TestResultEvent(test_status="FAILED", events={"g1": ["e1", "e2", ], "g2": ["e3", ], })
        self.assertEqual(
            str(event),
            dedent("""\
                ================================= TEST RESULTS =================================

                ----- LAST g1 EVENT ----------------------------------------------------------
                e1
                e2
                ----- LAST g2 EVENT ----------------------------------------------------------
                e3
                ================================================================================
                FAILED :(
            """)
        )
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))

    def test_test_result_event_ok(self):
        event = TestResultEvent(test_status="SUCCESS", events={"g1": ["e1", "e2", ], "g2": ["e3", ], })
        self.assertEqual(
            str(event),
            dedent("""\
                ================================= TEST RESULTS =================================
                ================================================================================
                SUCCESS :)
            """),
        )
        self.assertEqual(event, pickle.loads(pickle.dumps(event)))
