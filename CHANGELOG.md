# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-17

### Added
- Initial release of the `chordian` Python SDK.
- `CompanySearch`, `PeopleSearch`, `Research`, `EnterpriseSearch` and `Memory`
  resource classes covering the documented Chordian API surface.
- Module-level configuration (`chordian.api_key`, `service_id`, base-URL overrides).
- Server-Sent Events streaming for Deep Research and Enterprise chat.
- Typed exception hierarchy and `examples/` for every API group.
