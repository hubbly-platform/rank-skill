#!/usr/bin/env bash
# Thin, fail-closed client for the governed Rank agent gateway.
set -euo pipefail

rank_cmd="${1:-}"
rank_api_url="${RANK_API_URL:-}"
rank_api_key="${RANK_API_KEY:-}"

if [[ ! "$rank_api_key" =~ ^hbr_[0-9a-f]{32}_[0-9a-f]{32}_[A-Za-z0-9_-]{43}$ ]]; then
  printf 'A valid RANK_API_KEY is required.\n' >&2
  exit 2
fi
if [[ ! "$rank_api_url" =~ ^https://[A-Za-z0-9.-]+(:[0-9]+)?$ ]] &&
   [[ ! "$rank_api_url" =~ ^http://(127\.0\.0\.1|localhost)(:[0-9]+)?$ ]]; then
  printf 'RANK_API_URL must be HTTPS (or local loopback for testing).\n' >&2
  exit 2
fi
if ! command -v curl >/dev/null || ! command -v jq >/dev/null; then
  printf 'curl and jq are required.\n' >&2
  exit 2
fi

rank_method=""
rank_template=""
rank_path=""
rank_payload=""
rank_inline_json=""
rank_id="${2:-}"

case "$rank_cmd" in
  rank) rank_method=GET; rank_template=/v1/agent/status; rank_path="$rank_template" ;;
  rank-setup) rank_method=GET; rank_template=/v1/agent/connections; rank_path="$rank_template" ;;
  rank-scan)
    rank_method=POST; rank_template=/v1/agent/scan; rank_path="$rank_template"
    if [[ ! "$rank_id" =~ ^https://[A-Za-z0-9.-]+(:[0-9]+)?(/[A-Za-z0-9._~/%?=+&-]*)?$ ]]; then
      printf 'A public HTTPS URL is required.\n' >&2
      exit 2
    fi
    rank_inline_json="$(jq -cn --arg url "$rank_id" '{url:$url}')"
    ;;
  rank-health|rank-opportunities|rank-visibility|rank-questions|rank-plan|rank-write|rank-reviews|rank-report)
    if [[ ! "$rank_id" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
      printf 'A site UUID is required.\n' >&2
      exit 2
    fi
    case "$rank_cmd" in
      rank-health) rank_method=GET; rank_template='/v1/agent/sites/{id}/health'; rank_path="/v1/agent/sites/$rank_id/health" ;;
      rank-opportunities) rank_method=GET; rank_template='/v1/agent/sites/{id}/opportunities'; rank_path="/v1/agent/sites/$rank_id/opportunities" ;;
      rank-visibility) rank_method=GET; rank_template='/v1/agent/sites/{id}/ai-visibility'; rank_path="/v1/agent/sites/$rank_id/ai-visibility" ;;
      rank-questions) rank_method=PUT; rank_template='/v1/agent/sites/{id}/questions'; rank_path="/v1/agent/sites/$rank_id/questions"; rank_payload="${3:-}" ;;
      rank-plan) rank_method=GET; rank_template='/v1/agent/sites/{id}/plan'; rank_path="/v1/agent/sites/$rank_id/plan" ;;
      rank-write) rank_method=POST; rank_template='/v1/agent/sites/{id}/drafts'; rank_path="/v1/agent/sites/$rank_id/drafts"; rank_payload="${3:-}" ;;
      rank-reviews) rank_method=GET; rank_template='/v1/agent/sites/{id}/reviews'; rank_path="/v1/agent/sites/$rank_id/reviews" ;;
      rank-report) rank_method=GET; rank_template='/v1/agent/sites/{id}/report'; rank_path="/v1/agent/sites/$rank_id/report" ;;
    esac
    ;;
  rank-publish)
    if [[ ! "$rank_id" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
      printf 'A draft UUID is required.\n' >&2
      exit 2
    fi
    rank_method=POST; rank_template='/v1/agent/drafts/{id}/publish'
    rank_path="/v1/agent/drafts/$rank_id/publish"; rank_payload="${3:-}"
    ;;
  *) printf 'Unknown Rank command.\n' >&2; exit 2 ;;
esac

case "$rank_cmd" in
  rank-questions|rank-write|rank-publish)
    printf '%s is disabled until the client supports gateway preview and confirmation. No action was sent.\n' "$rank_cmd" >&2
    exit 3
    ;;
esac

if [[ "$rank_method" != GET && -z "$rank_inline_json" ]]; then
  if [[ -z "$rank_payload" || ! -f "$rank_payload" ]] || ! jq -e . "$rank_payload" >/dev/null; then
    printf 'A readable JSON payload file is required.\n' >&2
    exit 2
  fi
fi

rank_request() {
  local request_method="$1" request_path="$2" payload_file="${3:-}" inline_json="${4:-}"
  if [[ -n "$inline_json" ]]; then
    printf 'header = "Authorization: Bearer %s"\n' "$rank_api_key" |
      curl --config - --silent --show-error --fail-with-body --max-time 30 \
        --request "$request_method" --header 'Content-Type: application/json' \
        --data-binary "$inline_json" --url "$rank_api_url$request_path"
  elif [[ -n "$payload_file" ]]; then
    printf 'header = "Authorization: Bearer %s"\n' "$rank_api_key" |
      curl --config - --silent --show-error --fail-with-body --max-time 30 \
        --request "$request_method" --header 'Content-Type: application/json' \
        --data-binary "@$payload_file" --url "$rank_api_url$request_path"
  else
    printf 'header = "Authorization: Bearer %s"\n' "$rank_api_key" |
      curl --config - --silent --show-error --fail-with-body --max-time 30 \
        --request "$request_method" --url "$rank_api_url$request_path"
  fi
}

rank_capabilities="$(rank_request GET /v1/agent/capabilities)"
if ! jq -e --arg cmd "$rank_cmd" --arg method "$rank_method" --arg path "$rank_template" \
  '.available | any(.command == $cmd and .method == $method and .path == $path)' \
  >/dev/null <<< "$rank_capabilities"; then
  printf '%s is unavailable from the governed Rank gateway. No action was sent.\n' "$rank_cmd" >&2
  exit 3
fi

rank_request "$rank_method" "$rank_path" "$rank_payload" "$rank_inline_json"
