from agent.orchestrator import StatefulAgent


def run_saas_dashboard_launch(agent: StatefulAgent):
    print("\nUSE CASE: SaaS Dashboard Launch\n")

    task_description = """
    Launch a new analytics dashboard feature for our SaaS product.
    This involves creating a feature specification document, generating preliminary
    success metrics based on user data, drafting a go-to-market plan, and preparing
    internal communication for the engineering and product teams.
    """

    context = {
        "task_type": "saas_launch",
        "product": "Analytics Dashboard",
        "target_audience": "B2B SaaS customers",
        "user_data": {
            "current_active_users": 12500,
            "avg_session_duration_minutes": 24,
            "weekly_active_users": 8900,
            "monthly_active_users": 11200,
            "churn_rate_percent": 3.2,
            "avg_revenue_per_user": 49.99
        },
        "timeline": "6 week launch cycle",
        "team_size": 8,
        "budget": "allocated for development and marketing"
    }

    result = agent.run_task(task_description, context)

    print("\n\nTASK SUMMARY")
    print(f"Goal: {result['goal']}")
    print(f"Steps Completed: {result['successful_steps']}/{result['total_steps']}")
    print(f"Success Rate: {result['success_rate']*100:.1f}%")

    print("\n\nDECISION TRACE")
    print(agent.get_decision_trace())

    return result


def run_custom_saas_launch(agent: StatefulAgent, custom_context: dict):
    task_description = """
    Launch a new feature for the SaaS product based on provided specifications.
    Create comprehensive launch materials including feature documentation,
    success metrics, and team communication plans.
    """

    result = agent.run_task(task_description, custom_context)

    print("\n\nTask completed. Results summary:")
    print(f"Success rate: {result['success_rate']*100:.1f}%")

    return result
