# Client runtime workflows

These workflows execute the real Facebook client primitives against a configured Camofox session. They are not smoke tests and do not mock browser behavior.

Runtime credentials are supplied through GitHub Actions secrets and loaded by the test process with `python-dotenv` support for local execution.

The runtime suite must fail when an actual primitive fails. Logs should identify the domain, primitive, surface, input target, result, and exception without printing credentials, TOTP secrets, cookies, or session state.
