# Pull Request #2 — Task 2: Deploy and Connect a Web Client

## Description

This PR implements Task 2: Deploy and Connect a Web Client. It Dockerizes nanobot, adds a WebSocket channel for real-time chat, and builds a Flutter web UI.

## Related Issue

Closes #2 (Task 2 — Deploy and Connect a Web Client)

## Changes

- Added `nanobot-websocket-channel` service to docker-compose.yml
- Created Flutter web client in `client-web-flutter/`
- Configured WebSocket channel for nanobot
- Added `NANOBOT_ACCESS_KEY` environment variable for access control
- Updated Caddy configuration to serve Flutter app at `/flutter`

## Acceptance Criteria

- [x] Can access Flutter chat UI in browser
- [x] Can send messages and receive agent responses
- [x] Agent can list its capabilities in the chat

## Testing

Tested by:
- Opening `http://localhost:42002/flutter` in browser
- Sending messages and verifying agent responses
- Confirming access key protection works

---

## Reviewer Checklist

- [ ] Code follows project conventions
- [ ] Changes are tested and working
- [ ] Documentation is updated

**Approval:** <!-- Reviewer: add your approval comment here -->
