"""Exercise the real curl wrapper against an in-process gateway fixture."""

from __future__ import annotations

import json
import os
import subprocess
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "rank" / "scripts" / "rank-command.sh"
TOKEN = "hbr_" + "0" * 32 + "_" + "1" * 32 + "_" + "a" * 43
SITE_ID = "00000000-0000-4000-8000-000000000001"
GET_CASES = [
    ("rank", "/v1/agent/status"),
    ("rank-setup", "/v1/agent/connections"),
    ("rank-health", f"/v1/agent/sites/{SITE_ID}/health"),
    ("rank-opportunities", f"/v1/agent/sites/{SITE_ID}/opportunities"),
    ("rank-visibility", f"/v1/agent/sites/{SITE_ID}/ai-visibility"),
    ("rank-plan", f"/v1/agent/sites/{SITE_ID}/plan"),
    ("rank-reviews", f"/v1/agent/sites/{SITE_ID}/reviews"),
    ("rank-report", f"/v1/agent/sites/{SITE_ID}/report"),
]
GET_PATHS = {path for _, path in GET_CASES}


class Gateway(BaseHTTPRequestHandler):
    available = []
    calls = []

    def do_GET(self):
        self.calls.append(("GET", self.path, self.headers.get("Authorization")))
        if self.path == "/v1/agent/capabilities":
            body = {"available": self.available, "unavailable": []}
        elif self.path == "/v1/agent/status":
            body = {"status": "ready"}
        elif self.path in GET_PATHS:
            body = {"path": self.path}
        else:
            self.send_error(404)
            return
        content = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.calls.append(("POST", self.path, self.headers.get("Authorization"), body))
        if self.path != "/v1/agent/scan":
            self.send_error(404)
            return
        content = json.dumps({"accepted": True}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *_args):
        pass


class RankCommandTests(unittest.TestCase):
    def setUp(self):
        Gateway.available = []
        Gateway.calls = []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Gateway)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def run_command(self, *args):
        env = dict(os.environ)
        env.update(
            RANK_API_KEY=TOKEN,
            RANK_API_URL=f"http://127.0.0.1:{self.server.server_port}",
        )
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            env=env, capture_output=True, text=True, check=False,
        )

    def test_unavailable_command_never_calls_action_route(self):
        result = self.run_command("rank")
        self.assertEqual(result.returncode, 3)
        self.assertIn("unavailable", result.stderr.lower())
        self.assertEqual([path for _, path, _ in Gateway.calls], ["/v1/agent/capabilities"])
        self.assertNotIn(TOKEN, result.stdout + result.stderr)

    def test_advertised_command_calls_only_its_route(self):
        Gateway.available = [
            {"command": "rank", "method": "GET", "path": "/v1/agent/status"}
        ]
        result = self.run_command("rank")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"status": "ready"})
        self.assertEqual(
            [path for _, path, _ in Gateway.calls],
            ["/v1/agent/capabilities", "/v1/agent/status"],
        )
        self.assertTrue(all(auth == f"Bearer {TOKEN}" for _, _, auth in Gateway.calls))
        self.assertNotIn(TOKEN, result.stdout + result.stderr)

    def test_every_read_get_uses_its_exact_catalog_route(self):
        Gateway.available = [
            {"command": command, "method": "GET", "path": path.replace(SITE_ID, "{id}")}
            for command, path in GET_CASES
        ]
        for command, expected_path in GET_CASES:
            with self.subTest(command=command):
                Gateway.calls = []
                args = [] if command in {"rank", "rank-setup"} else [SITE_ID]
                result = self.run_command(command, *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    [path for _, path, _ in Gateway.calls],
                    ["/v1/agent/capabilities", expected_path],
                )

    def test_scan_accepts_url_and_sends_json_only_when_advertised(self):
        Gateway.available = [
            {"command": "rank-scan", "method": "POST", "path": "/v1/agent/scan"}
        ]
        result = self.run_command("rank-scan", "https://example.com")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"accepted": True})
        self.assertEqual(Gateway.calls[-1][:3], ("POST", "/v1/agent/scan", f"Bearer {TOKEN}"))
        self.assertEqual(json.loads(Gateway.calls[-1][3]), {"url": "https://example.com"})

    def test_scan_rejects_credentials_and_plain_http_before_any_request(self):
        for url in ("https://user:pass@example.com", "http://example.com", "https:///no-host"):
            with self.subTest(url=url):
                Gateway.calls = []
                result = self.run_command("rank-scan", url)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(Gateway.calls, [])

    def test_all_writes_stay_disabled_even_if_advertised(self):
        cases = [
            ("rank-questions", "PUT", "/v1/agent/sites/{id}/questions"),
            ("rank-write", "POST", "/v1/agent/sites/{id}/drafts"),
            ("rank-publish", "POST", "/v1/agent/drafts/{id}/publish"),
        ]
        for command, method, path in cases:
            with self.subTest(command=command):
                Gateway.available = [{"command": command, "method": method, "path": path}]
                Gateway.calls = []
                result = self.run_command(command, SITE_ID, "/nonexistent/payload.json")
                self.assertEqual(result.returncode, 3)
                self.assertIn("preview and confirmation", result.stderr)
                self.assertEqual(Gateway.calls, [])


if __name__ == "__main__":
    unittest.main()
