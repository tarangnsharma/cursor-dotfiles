---
name: Phase 3 Code Cleanup
overview: "Clean up all Phase 3 (Requests) code: move hardcoded magic strings/numbers to their canonical constant files, fix two Clean Architecture violations (direct ImagePicker instantiation and direct Repository usage in Presentation), and remove a typed-as-dynamic parameter."
todos:
  - id: c1
    content: "app_strings.dart: add 3 BLoC error fallback strings"
    status: completed
  - id: c2
    content: "api_constants.dart: add defaultPageSize, pagination keys, query params, 8 multipart field names"
    status: completed
  - id: c3
    content: "app_theme.dart: add Spacing.fabClearance / scrollTriggerOffset / radiusFull and AppTheme.kEmptyStateIconSize / kButtonMinHeight"
    status: completed
  - id: c4
    content: "requests_bloc.dart: replace 4 inline strings with AppStrings, replace _pageSize with ApiConstants.defaultPageSize"
    status: completed
  - id: c5
    content: "request_remote_data_source.dart: replace all 13 inline field/key/param strings with ApiConstants"
    status: completed
  - id: c6
    content: "requests_screen.dart: remove dynamic l10n param from _EmptyState, replace magic numbers with Spacing/AppTheme constants"
    status: completed
  - id: c7
    content: "request_form_screen.dart: fix DIP (use ImagePickerService), fix CA violation (use use-cases not repository), replace magic numbers"
    status: completed
  - id: c8
    content: "router.dart: provide ImagePickerService + CreateRequestUseCase + UpdateRequestUseCase to form routes; remove RequestRepository from home route"
    status: in_progress
isProject: false
---

# Phase 3 Code Cleanup

## Issues Found

### 1. Hardcoded strings in BLoC (AppStrings)

[`requests_bloc.dart`](lib/src/features/requests/presentation/bloc/requests_bloc.dart) has 4 inline fallback strings that the presentation layer will surface to users — these belong in `AppStrings`:

```dart
errorMessage: f.message ?? 'Failed to load requests.'   // → AppStrings.failedToLoadRequests
errorMessage: 'An unexpected error occurred.'             // → AppStrings.somethingWentWrong
errorMessage: f.message ?? 'Failed to load more.'        // → AppStrings.failedToLoadMore
deleteErrorMessage: f.message ?? 'Failed to delete request.' // → AppStrings.requestDeleteFailed
```

Also `static const _pageSize = 20` — belongs in `ApiConstants.defaultPageSize`.

### 2. Hardcoded API field/query names in data source

[`request_remote_data_source.dart`](lib/src/features/requests/data/datasources/request_remote_data_source.dart) has:

- Pagination keys: `'results'`, `'count'`, `'next'` used inline
- Query params: `'page'`, `'page_size'` used inline
- Multipart field names: `'request_type'`, `'customer_phone'`, `'date'`, `'time'`, `'location'`, `'city'`, `'note'`, `'reference_image'` — all inline in `_buildFormData`

All move to `ApiConstants`.

### 3. Magic numbers in screens

[`requests_screen.dart`](lib/src/features/requests/presentation/screens/requests_screen.dart):

- `200` (scroll-load trigger offset) → `Spacing.scrollTriggerOffset`
- `80` (FAB clearance bottom padding) → `Spacing.fabClearance`
- Inline `4` spacing → `Spacing.xs`
- Inline `6` (InfoRow gap) → `Spacing.xs`
- `8` (thumbnail border radius) → `Spacing.radiusSmall`
- `20` (badge pill radius) → `Spacing.radiusFull`
- `72` (empty state icon) → `AppTheme.kEmptyStateIconSize`

[`request_form_screen.dart`](lib/src/features/requests/presentation/screens/request_form_screen.dart):

- `12` (image clip radius) → `Spacing.radiusMedium`
- `20` (chip radius) → `Spacing.radiusFull`
- `8` (Positioned top/right) → `Spacing.sm`
- `6` (chip gap) → `Spacing.xs`
- `52` (button min height) → `AppTheme.kButtonMinHeight`
- Image quality/size constants already exist in `ImagePickerServiceImpl` — reuse them

### 4. `_EmptyState.l10n` typed as `dynamic`

[`requests_screen.dart`](lib/src/features/requests/presentation/screens/requests_screen.dart) declares `final dynamic l10n;` in `_EmptyState`, but the body ignores it and calls `context.l10n` directly. The constructor parameter serves no purpose and must be removed.

### 5. DIP violation — direct `ImagePicker` instantiation (Presentation depends on concrete package)

[`request_form_screen.dart`](lib/src/features/requests/presentation/screens/request_form_screen.dart) `_pickImage` does:

```dart
final picker = ImagePicker();   // ← depends on concrete class
```

The project already has `ImagePickerService` / `ImagePickerServiceImpl` exactly for this. The form screen must use `context.read<ImagePickerService>()` instead. `ImagePickerService` must be provided to the form routes in `router.dart`.

### 6. Clean Architecture violation — Presentation calls Repository directly

[`request_form_screen.dart`](lib/src/features/requests/presentation/screens/request_form_screen.dart) `_submit` does:

```dart
final repo = context.read<RequestRepository>();
await repo.createRequest(payload);   // ← Presentation → Repository (skips Use Case layer)
```

The Presentation layer must depend on **Use Cases**, not Repositories. Fix: inject `CreateRequestUseCase` and `UpdateRequestUseCase` through `RepositoryProvider` in the router, and remove `RequestRepository` from the form's provider tree.

---

## Files to Change

### `lib/src/core/constants/app_strings.dart`

Add 3 error-fallback constants (BLoC-level, no l10n context):

```dart
static const String failedToLoadRequests = 'Failed to load requests.';
static const String failedToLoadMore = 'Failed to load more.';
static const String requestDeleteFailed = 'Failed to delete request.';
```

### `lib/src/core/constants/api_constants.dart`

Add:

```dart
static const int defaultPageSize = 20;
// Pagination response keys
static const String paginationResults = 'results';
static const String paginationCount = 'count';
static const String paginationNext = 'next';
// Query params
static const String queryPage = 'page';
static const String queryPageSize = 'page_size';
// Request multipart field names
static const String fieldRequestType = 'request_type';
static const String fieldCustomerPhone = 'customer_phone';
static const String fieldDate = 'date';
static const String fieldTime = 'time';
static const String fieldLocation = 'location';
static const String fieldCity = 'city';
static const String fieldNote = 'note';
static const String fieldReferenceImage = 'reference_image';
```

### `lib/src/core/theme/app_theme.dart` (Spacing class)

Add:

```dart
static const double fabClearance = 80.0;
static const double scrollTriggerOffset = 200.0;
static const double radiusFull = 50.0;
```

Add to `AppTheme`:

```dart
static const double kEmptyStateIconSize = 72.0;
static const double kButtonMinHeight = 52.0;
```

### `lib/src/features/requests/presentation/bloc/requests_bloc.dart`

- Replace all 4 inline error strings with `AppStrings` constants
- Replace `_pageSize = 20` → `ApiConstants.defaultPageSize`

### `lib/src/features/requests/data/datasources/request_remote_data_source.dart`

- Replace `'results'`, `'count'`, `'next'` → `ApiConstants.paginationResults`, etc.
- Replace `'page'`, `'page_size'` → `ApiConstants.queryPage`, `ApiConstants.queryPageSize`
- Replace all 8 multipart field name strings → `ApiConstants.fieldXxx`

### `lib/src/features/requests/presentation/screens/requests_screen.dart`

- Remove `l10n` parameter from `_EmptyState` (typed `dynamic`); use `context.l10n` directly
- Replace magic number spacing with `Spacing` / `AppTheme` constants

### `lib/src/features/requests/presentation/screens/request_form_screen.dart`

- Replace `ImagePicker()` with `context.read<ImagePickerService>().pickFromGallery()` (or equivalent)
- Remove `context.read<RequestRepository>()` — replace with `context.read<CreateRequestUseCase>()` / `context.read<UpdateRequestUseCase>()`
- Replace magic number spacing/sizing with `Spacing` / `AppTheme` constants

### `lib/src/app/router.dart`

- Add `RepositoryProvider<ImagePickerService>` and `RepositoryProvider<CreateRequestUseCase>` / `RepositoryProvider<UpdateRequestUseCase>` to the form sub-routes
- Remove `RepositoryProvider<RequestRepository>` from the home route (no longer needed by Presentation)
