"""
Report Generator Module
Generate reproducible, professional reports from red-teaming activities
"""

import json
from datetime import datetime
from typing import Dict, List
import os


class ReportGenerator:
    """Generate comprehensive red-teaming reports"""
    
    def __init__(self):
        self.reports = []
        
    def create_executive_summary(
        self,
        test_results: List[Dict],
        project_name: str = "AI Red-Team Assessment"
    ) -> str:
        """
        Generate an executive summary
        
        Args:
            test_results: List of test results
            project_name: Name of the project/assessment
            
        Returns:
            Executive summary as markdown
        """
        # Calculate statistics
        total_tests = len(test_results)
        high_severity = sum(1 for r in test_results if r.get('severity') == 'HIGH')
        medium_severity = sum(1 for r in test_results if r.get('severity') == 'MEDIUM')
        low_severity = sum(1 for r in test_results if r.get('severity') == 'LOW')
        
        successful_attacks = sum(1 for r in test_results 
                                if r.get('jailbreak_successful', False) or 
                                   r.get('is_suspicious', False))
        
        summary = f"""
# Executive Summary: {project_name}

**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Assessment Type:** AI Red-Team Security Testing  
**Total Tests Conducted:** {total_tests}

## Overview

This report summarizes the findings from comprehensive adversarial testing of AI systems, including jailbreak attempts, prompt injection testing, and vulnerability analysis.

## Key Findings

### Test Results Summary
- **Total Tests Executed:** {total_tests}
- **Successful Exploitation Attempts:** {successful_attacks}
- **Success Rate:** {(successful_attacks/total_tests*100) if total_tests > 0 else 0:.1f}%

### Severity Distribution
- 🔴 **Critical/High Severity:** {high_severity} findings
- 🟡 **Medium Severity:** {medium_severity} findings
- 🟢 **Low/Informational:** {low_severity} findings

## Risk Assessment

"""
        
        if high_severity > 0:
            summary += f"""
### ⚠️ HIGH RISK IDENTIFIED

{high_severity} high-severity vulnerabilities were discovered that could lead to:
- Unauthorized access or data exposure
- Bypass of safety mechanisms
- Potential for exploitation in production environments

**Immediate Action Required**
"""
        elif medium_severity > 0:
            summary += """
### MODERATE RISK IDENTIFIED

Multiple medium-severity issues discovered. While not immediately critical, these should be addressed to strengthen security posture.

**Recommended Timeline: 30-60 days**
"""
        else:
            summary += """
### LOW RISK PROFILE

No critical vulnerabilities identified. System demonstrates good resilience against tested attack vectors.

**Continue Monitoring**
"""
        
        summary += f"""

## Recommendations Priority

1. **Immediate (0-7 days):** Address all HIGH severity findings
2. **Short-term (7-30 days):** Implement mitigations for MEDIUM severity issues
3. **Long-term (30+ days):** Enhance monitoring and strengthen defensive posture
4. **Ongoing:** Continuous adversarial testing and monitoring

## Next Steps

1. Review detailed findings in the Technical Assessment section
2. Prioritize remediation based on severity and impact
3. Implement recommended security controls
4. Schedule follow-up testing to validate fixes
5. Establish ongoing red-team testing program

---

*This executive summary provides a high-level overview. Detailed technical findings, evidence, and recommendations are provided in subsequent sections.*
"""
        
        return summary
    
    def create_technical_report(
        self,
        test_result: Dict,
        include_evidence: bool = True
    ) -> str:
        """
        Generate detailed technical report for a single test
        
        Args:
            test_result: Individual test result
            include_evidence: Whether to include detailed evidence
            
        Returns:
            Technical report as markdown
        """
        report = f"""
## Test Case: {test_result.get('test_id', 'N/A')}

**Timestamp:** {test_result.get('timestamp', datetime.now().isoformat())}  
**Test Type:** {test_result.get('jailbreak_type') or test_result.get('injection_type', 'Unknown')}  
**Severity:** {test_result.get('severity', 'N/A')}  
**Status:** {test_result.get('status', 'N/A')}

### Description
{test_result.get('description', 'No description provided')}

### Test Objective
{test_result.get('test_objective') or test_result.get('malicious_task', 'N/A')}

### Attack Vector
"""
        
        if 'prompt' in test_result:
            report += f"""
```
{test_result['prompt'][:500]}{"..." if len(test_result.get('prompt', '')) > 500 else ""}
```
"""
        elif 'test_payloads' in test_result:
            report += "\n**Test Payloads:**\n"
            for i, payload in enumerate(test_result['test_payloads'][:3], 1):
                report += f"{i}. `{payload[:200]}{'...' if len(payload) > 200 else ''}`\n"
        
        if include_evidence and 'evidence' in test_result:
            report += "\n### Evidence\n"
            for i, evidence in enumerate(test_result['evidence'], 1):
                report += f"{i}. {evidence}\n"
        
        if 'indicators' in test_result:
            report += f"\n### Indicators of Compromise\n"
            for indicator in test_result['indicators']:
                report += f"- {indicator}\n"
        
        if 'impact' in test_result:
            report += f"\n### Potential Impact\n{test_result['impact']}\n"
        
        if 'owasp_categories' in test_result:
            report += "\n### OWASP LLM Top 10 Mapping\n"
            for cat in test_result['owasp_categories']:
                report += f"- **{cat['id']}:** {cat['name']}\n"
        
        if 'mitre_tactics' in test_result:
            report += "\n### MITRE ATLAS Framework\n"
            for tactic in test_result['mitre_tactics']:
                report += f"- **{tactic['tactic'].title()}:** {tactic['technique']}\n"
        
        if 'recommendations' in test_result and test_result['recommendations']:
            report += "\n### Remediation Recommendations\n"
            for i, rec in enumerate(test_result['recommendations'][:5], 1):
                report += f"{i}. {rec}\n"
        
        report += "\n---\n"
        
        return report
    
    def create_full_report(
        self,
        test_results: List[Dict],
        project_name: str = "AI Red-Team Assessment",
        output_path: str = None,
        include_raw_data: bool = True
    ) -> str:
        """
        Generate a complete assessment report
        
        Args:
            test_results: All test results
            project_name: Project name
            output_path: Where to save the report (optional)
            include_raw_data: Whether to include raw JSON data
            
        Returns:
            Complete report as markdown
        """
        report = f"""
# AI Red-Team Assessment Report
## {project_name}

**Report Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
**Assessment Period:** {datetime.now().strftime('%B %Y')}  
**Framework:** OWASP LLM Top 10, MITRE ATLAS  
**Methodology:** Adversarial Testing, Prompt Injection, Jailbreak Analysis

---

"""
        
        # Add executive summary
        report += self.create_executive_summary(test_results, project_name)
        
        # Add methodology section
        report += """

---

# Methodology

## Testing Approach

This assessment employed a comprehensive adversarial testing methodology:

### 1. **Jailbreak Testing**
- Systematic testing of role-play exploits (DAN, AIM, etc.)
- Multi-turn conversation attacks
- System prompt leaking attempts
- Constraint breaking scenarios

### 2. **Prompt Injection Analysis**
- Direct instruction injection
- Indirect injection via data sources
- Context switching and delimiter confusion
- Encoded payload testing

### 3. **Vulnerability Classification**
- OWASP LLM Top 10 framework mapping
- MITRE ATLAS tactic identification
- CVSS-style severity scoring
- Risk categorization and prioritization

### 4. **Adversarial Probing**
- Bias and fairness testing
- Harmful content generation attempts
- Privacy leakage detection
- Model behavior boundary testing

## Testing Tools
- Custom red-teaming toolkit
- Industry-standard attack patterns
- Reproducible test cases
- Automated and manual testing

---

# Technical Findings

"""
        
        # Group results by severity
        high_severity = [r for r in test_results if r.get('severity') == 'HIGH']
        medium_severity = [r for r in test_results if r.get('severity') == 'MEDIUM']
        low_severity = [r for r in test_results if r.get('severity') == 'LOW']
        
        # High severity findings
        if high_severity:
            report += "## 🔴 HIGH SEVERITY FINDINGS\n\n"
            for result in high_severity:
                report += self.create_technical_report(result)
        
        # Medium severity findings
        if medium_severity:
            report += "## 🟡 MEDIUM SEVERITY FINDINGS\n\n"
            for result in medium_severity[:5]:  # Limit to first 5
                report += self.create_technical_report(result)
            
            if len(medium_severity) > 5:
                report += f"\n*{len(medium_severity) - 5} additional medium severity findings documented in appendix.*\n\n"
        
        # Low severity findings summary
        if low_severity:
            report += f"## 🟢 LOW SEVERITY FINDINGS\n\n"
            report += f"**Total:** {len(low_severity)} informational findings\n\n"
            report += "These findings represent minimal risk but are documented for completeness. See appendix for details.\n\n"
        
        # Recommendations section
        report += """
---

# Consolidated Recommendations

## Immediate Actions (Priority 1)

1. **Input Validation & Sanitization**
   - Implement robust input validation for all user-supplied data
   - Sanitize special characters and delimiters
   - Use structured input formats (JSON with validation)

2. **Output Filtering**
   - Treat all LLM outputs as untrusted
   - Implement content filtering before downstream processing
   - Validate outputs against expected formats

3. **Access Controls**
   - Implement principle of least privilege
   - Add human-in-the-loop for critical operations
   - Establish clear authorization boundaries

## Short-term Improvements (Priority 2)

4. **Prompt Engineering**
   - Strengthen system prompts against injection
   - Use clear context separation
   - Implement instruction hierarchy

5. **Monitoring & Logging**
   - Log all suspicious inputs
   - Implement anomaly detection
   - Establish alerting for attack patterns

6. **Rate Limiting & Resource Controls**
   - Implement query rate limiting
   - Set resource consumption limits
   - Add timeout mechanisms

## Long-term Strategy (Priority 3)

7. **Continuous Testing**
   - Establish regular red-team exercises
   - Maintain updated attack pattern database
   - Track emerging vulnerabilities

8. **Security Training**
   - Train development team on AI security
   - Establish secure development practices
   - Create incident response procedures

9. **Defense in Depth**
   - Implement multiple layers of security controls
   - Add redundant safety mechanisms
   - Regular security audits

---

# Conclusion

"""
        
        success_rate = sum(1 for r in test_results if r.get('jailbreak_successful', False)) / len(test_results) * 100 if test_results else 0
        
        report += f"""
This assessment identified {len(test_results)} test cases with a {success_rate:.1f}% exploitation success rate. 

**Overall Security Posture:** {"NEEDS IMPROVEMENT" if high_severity else "GOOD" if medium_severity else "STRONG"}

The findings demonstrate {'areas requiring immediate attention' if high_severity else 'opportunities for security enhancement' if medium_severity else 'a solid security foundation'}.

## Key Takeaways

1. AI systems require specialized security testing beyond traditional approaches
2. Adversarial testing uncovers vulnerabilities automated tests miss
3. Continuous red-teaming is essential for maintaining security
4. Defense-in-depth strategies provide the best protection

## Next Steps

1. ✅ Review and prioritize findings with stakeholders
2. ✅ Implement high-priority recommendations
3. ✅ Schedule follow-up testing after remediation
4. ✅ Establish ongoing security monitoring
5. ✅ Develop incident response procedures

---

# Appendix

## A. Testing Frameworks

- **OWASP LLM Top 10:** Industry-standard LLM vulnerability taxonomy
- **MITRE ATLAS:** Adversarial tactics for machine learning systems
- **Custom Red-Team Methodology:** Tailored testing approach

## B. References

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

"""
        
        if include_raw_data:
            report += f"""
## C. Raw Test Data

Complete test results are available in JSON format for further analysis and integration into security tools.

```json
{json.dumps({"test_results": test_results[:2]}, indent=2)}
```

*[Additional results truncated for readability]*

"""
        
        report += f"""
---

**Report End**  
*Generated by AI Red-Teaming Toolkit*  
*{datetime.now().isoformat()}*
"""
        
        # Save if output path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {output_path}")
        
        return report
    
    def create_dataset_export(
        self,
        test_results: List[Dict],
        format_type: str = "json",
        output_path: str = "red_team_dataset.json"
    ) -> str:
        """
        Export test results as a dataset for training or analysis
        
        Args:
            test_results: Test results to export
            format_type: Export format (json, csv, jsonl)
            output_path: Output file path
            
        Returns:
            Path to exported dataset
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        if format_type == "json":
            with open(output_path, 'w') as f:
                json.dump({
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "total_samples": len(test_results),
                        "dataset_type": "red_team_adversarial"
                    },
                    "samples": test_results
                }, f, indent=2)
        
        elif format_type == "jsonl":
            with open(output_path, 'w') as f:
                for result in test_results:
                    f.write(json.dumps(result) + '\n')
        
        elif format_type == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if test_results:
                    writer = csv.DictWriter(f, fieldnames=test_results[0].keys())
                    writer.writeheader()
                    writer.writerows(test_results)
        
        return output_path
    
    def create_attack_chain_visualization(self, test_results: List[Dict]) -> str:
        """Generate a Mermaid diagram of attack chains"""
        
        diagram = """
```mermaid
graph TD
    A[Initial Reconnaissance] --> B{Identify Target}
    B -->|Jailbreak| C[Craft Exploit]
    B -->|Injection| D[Prepare Payload]
    C --> E[Execute Attack]
    D --> E
    E --> F{Success?}
    F -->|Yes| G[Exploit Vulnerability]
    F -->|No| H[Refine Approach]
    H --> C
    H --> D
    G --> I[Document Finding]
    I --> J[Generate Report]
```

**Attack Chain Breakdown:**

1. **Reconnaissance:** Identify model capabilities and constraints
2. **Exploitation:** Execute jailbreak or injection attack
3. **Validation:** Confirm successful bypass of safety mechanisms
4. **Documentation:** Record reproducible attack case
5. **Reporting:** Generate actionable findings
"""
        
        return diagram


# Example usage
if __name__ == "__main__":
    generator = ReportGenerator()
    
    # Sample test results
    sample_results = [
        {
            "test_id": "JB_001",
            "timestamp": datetime.now().isoformat(),
            "jailbreak_type": "DAN",
            "severity": "HIGH",
            "test_objective": "Bypass safety guidelines",
            "jailbreak_successful": True,
            "description": "DAN jailbreak successfully bypassed safety controls"
        },
        {
            "test_id": "INJ_001",
            "timestamp": datetime.now().isoformat(),
            "injection_type": "DIRECT",
            "severity": "MEDIUM",
            "is_suspicious": True,
            "description": "Direct prompt injection detected"
        }
    ]
    
    # Generate full report
    report = generator.create_full_report(
        sample_results,
        project_name="Sample AI System Assessment",
        output_path="test_report.md"
    )
    
    print("Report generated successfully!")
    print(f"Length: {len(report)} characters")
