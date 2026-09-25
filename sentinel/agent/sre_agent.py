import json
from sentinel.tools.k8s_inspector import K8sInspectorTool, IncidentReport

class AgenticSRE:
    """Autonomous Kubernetes SRE Agent with Safety Guardrails."""
    
    def __init__(self, mode: str = "dry-run"):
        self.mode = mode # Guardrail: 'dry-run' enforces zero destructive action
        self.inspector = K8sInspectorTool()

    def run_incident_triage(self, incident_type: str = "OOMKilled") -> IncidentReport:
        # Step 1: Collect telemetry via MCP tool
        pod_telemetry = self.inspector.inspect_pod_health(mock_event=incident_type)
        
        # Step 2: Autonomous reasoning and diagnosis
        report = self.inspector.diagnose_and_suggest_patch(pod_telemetry)
        
        # Step 3: Guardrail check
        if self.mode == "dry-run":
            print(f"[GUARDRAIL ENFORCED] Generated remediation patch for {report.pod_name} without applying.")
            
        return report

if __name__ == "__main__":
    agent = AgenticSRE(mode="dry-run")
    report = agent.run_incident_triage("OOMKilled")
    print(json.dumps(report.model_dump(), indent=2))
