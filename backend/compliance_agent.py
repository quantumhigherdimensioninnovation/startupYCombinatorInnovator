from backend.claude_agent import query_claude

def compliance_check(document_text):
    prompt = (
        "You are a world-class startup legal counsel and compliance officer. "
        "Analyze the following contract, Terms of Service, or legal text for missing clauses, "
        "compliance risks, data privacy issues, and gaps relevant to SaaS/AI startups. "
        "Highlight any problematic terms or regulatory risks. "
        "Analyze possible ethical implications and compliance with GDPR, CCPA, and other relevant regulations. " \
        "Create a legal PR plan to address these issues and ensure compliance, and mainting a good reputation."
        "Provide a detailed report with actionable recommendations for compliance improvements. "
        f"\n\n{document_text}"
    )
    return query_claude(prompt)

if __name__ == "__main__":
    sample_text = (
        "This Terms of Service governs the use of our AI-powered SaaS platform, known as Professional Workplace live GPT live talker without using facetime. "
        "Users must agree to our data collection practices, which include storing user interactions for service improvement. "
        "We reserve the right to terminate accounts for violations of our policies."
    )
    print(compliance_check(sample_text))
