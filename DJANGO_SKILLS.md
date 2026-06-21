# Django Skills for Bhagwati Hardware

These skills are tailored specifically for this project to help AI assistants (like Claude, Cursor, Gemini, or Antigravity) apply best practices when working on tasks. They are imported and adapted from the SaaS Pegasus Django Skills.

## 1. Fix Types (`/fix-types`)

**Description**: Interactively fix any type checking issues in Python code.

### Instructions for AI Agent:
1. Run the type checker (e.g., `mypy .` or your preferred linter).
2. Group the errors you find into logical buckets.
3. For each bucket of errors, go through them one at a time, explain the fix you want to apply, and ask if the user has any questions or suggestions before proceeding.
4. Only once the user approves, apply the fix and move onto the next error.
5. Once you've completed a bucket, ask the user if they'd like to move on to the next bucket.

#### Prefer `cast()` over `type: ignore`
When mypy can't infer the correct type, prefer using `cast()` over `# type: ignore`:
```python
# Preferred - documents the expected type
choices = cast(list[tuple[str, str]], field.choices)

# Avoid when cast is possible - just silences the error
choices = list(field.choices)  # type: ignore[arg-type]
```
**Why:** `cast()` explicitly documents what type you expect, making the code more readable and maintainable. It also doesn't silence other potential errors on the same line.

#### Prefer proper errors over assertions for null checks
```python
# Preferred - proper error handling
if obj.related_field is None:
    raise ValueError("Object must have a related field")
result = obj.related_field.some_method()

# Avoid - assertions can be disabled with -O flag
assert obj.related_field is not None
result = obj.related_field.some_method()
```
**Why:** Assertions can be disabled in production with `python -O`, making them unreliable for runtime validation. Proper exceptions ensure the check always runs and provides better error handling.

#### When using `type: ignore`, add a comment
If `type: ignore` is necessary, always add a short explanation:
```python
# Good - explains why the ignore is needed
self.tier = tier  # type: ignore[misc]  # mypy can't handle Enum tuple values with custom __init__
```

#### Type Hints for Django Lazy Translation Strings
When using type hints with Django's lazy translation strings (`gettext_lazy`), use the following pattern:
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise

def my_function(name: StrOrPromise) -> StrOrPromise:
    ...
```

---

## 2. Upgrade Python Dependencies (`/upgrade-python-deps`)

**Description**: Upgrade Python dependencies and ensure nothing is broken.

### Instructions for AI Agent:
1. Review the `requirements.txt` file for available upgrades.
2. Upgrade the packages to their latest compatible versions using `pip install -U -r requirements.txt`. 
3. Run post-upgrade checks:
   - **Type checking**: Run `mypy .` (if configured) and report any new type errors.
   - **Tests**: Run `pytest` to verify the test suite still passes.
4. Summarize what was done:
   - Which packages were upgraded (notable version changes).
   - Whether any type errors were introduced.
   - Whether all tests passed.
   - Any issues that need manual attention.
5. If there were failures, present the issues and ask how to proceed.
6. If everything passed, ask if the changes should be committed.

---

## 3. Upgrade JavaScript Dependencies (`/upgrade-js-deps`)

*(Note: Use this primarily if frontend tools like npm/Node.js are present in the project).*

**Description**: Upgrade JavaScript dependencies and run post-upgrade checks.

### Instructions for AI Agent:
1. Run `npx npm-check-updates -u` to update `package.json` with the new versions.
2. Run `npm install` (or equivalent like `make npm-install`) to install updated dependencies.
3. Run post-upgrade checks:
   - **Type checking**: Run `npm run type-check` (or `make npm-type-check`).
   - **Build**: Run `npm run build` (or `make npm-build`).
   - **Tests**: Run `npm test` (or `make test`).
4. Summarize what was done and present the results to the user.
5. Ask for permission to commit the changes if everything passed.
