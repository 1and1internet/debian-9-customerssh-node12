#!/usr/bin/env python3

import unittest
from testpack_helper_library.unittests.dockertests import Test1and1Common


class Test1and1BaseImage(Test1and1Common):

    # <tests to run>

    def test_docker_logs(self):
        expected_log_lines = [
            "run-parts: executing /hooks/entrypoint-pre.d/00_check_euid",
            "run-parts: executing /hooks/entrypoint-pre.d/01_ssmtp_setup",
            "run-parts: executing /hooks/entrypoint-pre.d/02_user_group_setup",
            "run-parts: executing /hooks/supervisord-pre.d/20_configurability"
        ]
        container_logs = self.container.logs().decode('utf-8')
        for expected_log_line in expected_log_lines:
            self.assertTrue(
                container_logs.find(expected_log_line) > -1,
                msg="Docker log line missing: %s from (%s)" % (expected_log_line, container_logs)
            )

    def test_OS(self):
        lines = self.exec("cat /etc/debian_version")
        self.assertTrue(lines.find("9.") > -1, msg="Failed to establish correct version")

    def test_id(self):
        self.assertEqual("ssh-user", self.exec("whoami")[:-1])

    def test_vim(self):
        self.assertPackageIsInstalled("vim")

    def test_curl(self):
        self.assertPackageIsInstalled("curl")

    def test_bzip2(self):
        self.assertPackageIsInstalled("bzip2")

    def test_traceroute(self):
        self.assertPackageIsInstalled("traceroute")

    def test_telnet(self):
        self.assertPackageIsInstalled("telnet")

    def test_nano(self):
        self.assertPackageIsInstalled("nano")

    def test_mysqlclient(self):
        self.assertPackageIsInstalled("mysql-client")

    def test_git(self):
        self.assertPackageIsInstalled("git")

    def test_bzip2(self):
        self.assertPackageIsInstalled("")

    def test_apt(self):
        self.assertTrue(
            self.exec("ls -l /var/lib/apt/lists").find("total 0") > -1,
            msg="/var/lib/apt/lists should be empty"
        )

    def test_hooks_dir(self):
        self.assertTrue(
            self.exec("stat /hooks").find("0755") > -1,
            msg="/hooks should be 0755"
        )

    def test_init_dir(self):
        self.assertTrue(
            self.exec("stat /init").find("0755") > -1,
            msg="/init should be 0755"
        )

    def test_entrypoint(self):
        self.assertTrue(
            self.exec("stat /init/entrypoint").find("regular file") > -1,
            msg="/init/entrypoint should exist"
        )

    def test_var_run_dir(self):
        self.assertTrue(
            self.exec("stat /var/run").find("0777") > -1,
            msg="/var/run should be 0777"
        )

    # </tests to run>

if __name__ == '__main__':
    unittest.main(verbosity=1)
