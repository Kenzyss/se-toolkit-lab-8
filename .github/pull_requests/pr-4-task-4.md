# Pull Request #4 — Task 4: Diagnose a Failure and Make the Agent Proactive

## Description

This PR implements Task 4: Diagnose a Failure and Make the Agent Proactive. It enhances the observability skill for one-shot investigation, schedules proactive health checks via cron, and fixes a planted bug that was returning 404 instead of 500 on database failures.

## Related Issue

Closes #4 (Task 4 — Diagnose a Failure and Make the Agent Proactive)

## Changes

### Bug Fix
- **Fixed planted bug in `backend/app/routers/items.py`**: Removed the incorrect exception handler that was converting all database errors to 404 responses. Now database failures properly return 500.

### Enhancements
- Updated `nanobot/workspace/skills/observability/SKILL.md` with enhanced investigation flow
- Added cron-based health check capability
- Documented failure investigation in REPORT.md

## Acceptance Criteria

- [x] Agent response to "What went wrong?" includes both log and trace evidence
- [x] Health check job appears in "List scheduled jobs"
- [x] Proactive health report posted to chat while failure is present
- [x] After fix, DB failure returns proper 500 error
- [x] Post-recovery health report shows system healthy

## Bug Fix Details

**Root Cause:** The `get_items` endpoint in `backend/app/routers/items.py` had a try/except block that caught all exceptions and raised HTTPException with status 404, even for database connection failures.

**Fix:** Removed the try/except wrapper. Now unhandled exceptions propagate to the global exception handler which returns 500.

```diff
 @router.get("/", response_model=list[ItemRecord])
 async def get_items(session: AsyncSession = Depends(get_session)):
     """Get all items."""
-    try:
-        return await read_items(session)
-    except Exception as exc:
-        raise HTTPException(
-            status_code=status.HTTP_404_NOT_FOUND,
-            detail="Items not found",
-        ) from exc
+    return await read_items(session)
```

## Testing

Tested by:
1. Stopping PostgreSQL
2. Triggering a request via Flutter app
3. Asking agent "What went wrong?" — now shows proper 500 error
4. Restarting PostgreSQL
5. Creating health check job — reports system healthy

---

## Reviewer Checklist

- [ ] Code follows project conventions
- [ ] Changes are tested and working
- [ ] Documentation is updated
- [ ] Bug fix verified with proper error codes

**Approval:** <!-- Reviewer: add your approval comment here -->
