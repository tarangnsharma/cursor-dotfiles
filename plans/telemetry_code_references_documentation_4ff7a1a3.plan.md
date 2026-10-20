---
name: Telemetry Code References Documentation
overview: Create a comprehensive markdown file documenting all telemetry-related code references, including OpenTelemetry implementation, isolate handling, context propagation, and error handling strategies.
todos:
  - id: "1"
    content: Create TELEMETRY_CODE_REFERENCES.md file with all sections and code references
    status: completed
  - id: "2"
    content: Add TelemetryApiClient implementation details with line numbers
    status: completed
  - id: "3"
    content: Add OpenTelemetry SDK setup and configuration details
    status: completed
  - id: "4"
    content: Add isolate entry-point code documentation
    status: completed
  - id: "5"
    content: Add ApiClient construction comparison (main vs isolate)
    status: completed
  - id: "6"
    content: Add token refresh implementation details
    status: completed
  - id: "7"
    content: Add logger and error handling documentation
    status: completed
  - id: "8"
    content: Add Zone and context propagation details
    status: completed
---

# Plan: Telemetry Code References Documentation

Create a markdown file `TELEMETRY_CODE_REFERENCES.md` in the project root with comprehensive code references organized by topic.

## File Structure

The markdown file will contain the following sections:

### 1. TelemetryApiClient Implementation

- **File**: `packages/aina_telemetry/lib/telemetry_api_client.dart`
- Document span creation flow (lines 24-33)
- Document traceparent header propagation (lines 51-52)
- Document span status management (lines 73-110)
- Document exception handling and span recording (lines 113-131)
- Document span lifecycle (finally block, lines 134-145)
- Document sendLog integration for debugging

### 2. OpenTelemetry SDK Setup

- **File**: `packages/aina_telemetry/lib/telemetry_service.dart`
- Document initialization (lines 21-52)
- Document resource configuration (lines 23-27)
- Document JsonSpanExporter setup (lines 30-36)
- Document BatchSpanProcessor configuration (lines 39-42)
- Document tracer provider creation (lines 45-48)
- Document endpoint URLs: `https://goapi.core.dev.ainaweb.app/telemetry/traces` and `/logs`
- **File**: `packages/aina_telemetry/pubspec.yaml`
- Document OpenTelemetry dependency: `opentelemetry: ^0.18.10`

### 3. Span Export and Transport

- **File**: `packages/aina_telemetry/lib/json_span_exporter.dart`
- Document OTLP/HTTP JSON format implementation (lines 15-62)
- Document span-to-JSON conversion (lines 64-117)
- Document attribute conversion (lines 134-151)
- Document error handling in export (lines 58-61)
- Document batch export mechanism

### 4. Isolate Entry-Point Code

- **File**: `lib/core/services/telemetry_service.dart`
- Document `spawnTelemetryIsolate` top-level function (lines 11-18)
- Document isolate parameter structure (TelemetryIsolateParams, lines 83-100)
- Document error handling in isolate (catch block, line 15-16)
- Document MonitoringApi.sendTelemetry call (line 13)
- Document isolate communication via SendPort (lines 14, 46-54)

### 5. ApiClient Construction: Main vs Isolate

- **Main Isolate**: `lib/core/services/auth_manager.dart`
  - Document `getApiClient()` returning TelemetryApiClient (lines 175-207)
  - Document context retrieval from TelemetryService (lines 176-177)
  - Document authentication handling
- **Spawned Isolate**: `lib/core/services/telemetry_service.dart`
  - Document `_createPlainApiClient()` method (lines 59-80)
  - Document why plain ApiClient is used (avoid span creation in isolates)
  - Document token refresh in isolate context (lines 67-74)
  - Document fallback to unauthenticated client (lines 61-64, 79)

### 6. Token Refresh Implementation

- **File**: `lib/core/services/auth_manager.dart`
- Document `refreshTheAccessToken()` method (lines 99-141)
- Document AuthenticationService integration (lines 108-113)
- Document error handling for 401 (lines 120-124)
- Document connection error detection (lines 127-136)
- Document token storage (line 116)
- Document `_loadRefreshTokenIntoService()` helper (lines 144-154)

### 7. Logger and Error Handling in Isolates

- **Isolate Error Handling**: `lib/core/services/telemetry_service.dart`
  - Document error propagation via SendPort (line 16)
  - Document error logging in main isolate (lines 47-54)
- **Main Isolate Logging**: `lib/core/utils/logging_util.dart`
  - Document AppLogger interface
  - Document AppLoggerImpl implementation
- **Global Error Handling**: `lib/main.dart`
  - Document `runZonedGuarded` usage (line 16)
  - Document global error handler (lines 46-53)
  - Document FlutterError.onError handler (lines 66-79)

### 8. Zone and Context Propagation

- **File**: `lib/main.dart`
- Document `runZonedGuarded` setup (line 16)
- Document zone error handling (lines 46-53)
- **File**: `packages/aina_telemetry/lib/telemetry_service.dart`
- Document `currentContext` getter (lines 217-221)
- Document `Context.current` usage (line 218)
- Document context passing to TelemetryApiClient (via auth_manager.dart line 177)

### 9. Integration Points

- **File**: `lib/main.dart`
  - Document TelemetryService initialization (line 23)
- **File**: `lib/core/services/auth_manager.dart`
  - Document TelemetryApiClient usage in getApiClient (lines 180, 186, 195)
- **File**: `lib/core/helper/telemetry_helper.dart`
  - Document old telemetry system integration
  - Document TelemetryService.send() calls (line 51)

## Additional Notes to Include

- Explain the dual telemetry system (old isolate-based vs new OpenTelemetry)
- Document why plain ApiClient is needed for isolates
- Explain context propagation limitations in isolates
- Document traceparent header format and W3C Trace Context standard
- Include endpoint URLs and configuration
- Document batch size (50 spans) and export mechanism

## File Location

Create the file at: `c:\Tarang\programming\flutter\aina\official\TELEMETRY_CODE_REFERENCES.md`
