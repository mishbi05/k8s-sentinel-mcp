from typing import Dict, List, Any
from pydantic import BaseModel, Field

class IncidentReport(BaseModel):
    pod_name: str
    namespace: str
    reason: str
    exit_code: int
    root_cause_analysis: str
    suggested_patch: str

class K8sInspectorTool:
    """Read-Only SRE Diagnostic tool exposed via MCP."""
    
    @staticmethod
    def inspect_pod_health(mock_event: str = "CrashLoopBackOff") -> Dict[str, Any]:
        """Simulates/queries Kubernetes API for pod failures."""
        if mock_event == "OOMKilled":
            return {
                "pod_name": "payment-api-7b89f-2z1a",
                "namespace": "production",
                "status": "Failed",
                "reason": "OOMKilled",
                "exit_code": 137,
                "current_memory_limit": "128Mi",
                "observed_usage": "129Mi",
                "last_log_line": "Fatal error: JavaScript heap out of memory"
            }
        else:
            return {
                "pod_name": "auth-service-9c44d-5k8p",
                "namespace": "staging",
                "status": "Waiting",
                "reason": "CrashLoopBackOff",
                "exit_code": 1,
                "last_log_line": "KeyError: 'DATABASE_URL' environment variable is missing"
            }

    @staticmethod
    def diagnose_and_suggest_patch(pod_data: Dict[str, Any]) -> IncidentReport:
        """SRE reasoning engine to generate non-destructive remediation."""
        reason = pod_data.get("reason", "Unknown")
        pod_name = pod_data.get("pod_name", "unknown")
        namespace = pod_data.get("namespace", "default")
        exit_code = pod_data.get("exit_code", 0)

        if reason == "OOMKilled" or exit_code == 137:
            root_cause = "Container exceeded allocated memory quota (Exit Code 137)."
            patch = (
                "spec:\n"
                "  template:\n"
                "    spec:\n"
                "      containers:\n"
                "      - name: app\n"
                "        resources:\n"
                "          limits:\n"
                "            memory: 512Mi\n"
                "          requests:\n"
                "            memory: 256Mi"
            )
        elif "DATABASE_URL" in pod_data.get("last_log_line", ""):
            root_cause = "Missing mandatory runtime secret/config 'DATABASE_URL'."
            patch = (
                "spec:\n"
                "  template:\n"
                "    spec:\n"
                "      containers:\n"
                "      - name: app\n"
                "        env:\n"
                "        - name: DATABASE_URL\n"
                "          valueFrom:\n"
                "            secretKeyRef:\n"
                "              name: db-credentials\n"
                "              key: url"
            )
        else:
            root_cause = f"Unhandled container crash ({reason})."
            patch = "# Manual inspection required"

        return IncidentReport(
            pod_name=pod_name,
            namespace=namespace,
            reason=reason,
            exit_code=exit_code,
            root_cause_analysis=root_cause,
            suggested_patch=patch
        )
