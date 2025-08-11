"""
PRD Writer Agent - Generates Product Requirements Documents
"""

from typing import Dict, Any


class PRDWriterAgent:
    """Agent responsible for generating Product Requirements Documents."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def generate_prd(self, idea: str, app_plan: Dict[str, Any]) -> str:
        """
        Generate a comprehensive Product Requirements Document.

        Args:
            idea: The original app idea
            app_plan: The app plan from the composer agent

        Returns:
            Markdown-formatted PRD content
        """
        if self.verbose:
            print(f"[PRDWriterAgent] Generating PRD for: {idea}")

        prd_content = f"""# Product Requirements Document (PRD)

## 1. Product Overview

**Product Name**: {app_plan.get('name', 'AutoDevApp')}  
**Date**: {self._get_current_date()}  
**Status**: Draft  
**Target Release**: v1.0 - Q1 2024

## 2. Business Objectives & Goals

- **Primary Goal**: {idea}
- **Success Metrics**: 
  - User adoption rate > 80%
  - System uptime > 99.9%
  - Response time < 200ms
- **Business Value**: Streamline operations and improve efficiency

## 3. Background & Strategic Fit

This application addresses the need for {idea.lower()}. It provides a comprehensive solution that integrates seamlessly with existing workflows while maintaining high performance and security standards.

## 4. Assumptions & Constraints

### Assumptions
- Users have basic technical proficiency
- Internet connectivity is available
- Data privacy compliance is required

### Constraints
- Must work offline-first
- Maximum response time: 200ms
- Must be accessible on mobile devices

## 5. User Personas & Use Cases

### Primary Persona: {self._identify_primary_persona(idea)}
- **Role**: {self._get_persona_role(idea)}
- **Goals**: {self._get_persona_goals(idea)}
- **Pain Points**: {self._get_persona_pain_points(idea)}

### Use Cases
{self._generate_use_cases(app_plan)}

## 6. Functional Requirements

### Core Features
{self._format_features(app_plan.get('features', []))}

### Technical Requirements
- **Backend**: {app_plan.get('tech_stack', {}).get('backend', 'Python/FastAPI')}
- **Database**: {app_plan.get('tech_stack', {}).get('database', 'SQLite')}
- **Frontend**: {app_plan.get('tech_stack', {}).get('frontend', 'Web UI')}
- **Deployment**: {app_plan.get('tech_stack', {}).get('deployment', 'Local')}

## 7. Non-Functional Requirements

### Performance
- Page load time: < 2 seconds
- API response time: < 200ms
- Concurrent users: 100+

### Security
- Authentication required for all user actions
- Data encryption at rest and in transit
- Regular security audits

### Scalability
- Horizontal scaling capability
- Database optimization for large datasets
- Caching strategy implementation

## 8. Technical Architecture

### System Design
{self._format_architecture(app_plan.get('architecture', {}))}

### Database Schema
{self._format_database_schema(app_plan.get('database_schema', {}))}

### API Endpoints
{self._format_api_endpoints(app_plan.get('api_endpoints', []))}

## 9. User Interface Requirements

### Design Principles
- Clean, intuitive interface
- Mobile-responsive design
- Accessibility compliance (WCAG 2.1)

### Key Components
{self._format_ui_components(app_plan.get('ui_components', []))}

## 10. Testing Strategy

### Test Types
- Unit tests (coverage > 80%)
- Integration tests
- End-to-end tests
- Performance tests

### Test Environment
- Development environment
- Staging environment
- Production environment

## 11. Deployment & DevOps

### Deployment Strategy
{self._format_deployment(app_plan.get('deployment', {}))}

### Monitoring & Logging
- Application performance monitoring
- Error tracking and alerting
- User analytics

## 12. Success Criteria

### Technical Success
- [ ] All functional requirements implemented
- [ ] Performance benchmarks met
- [ ] Security requirements satisfied
- [ ] Test coverage > 80%

### Business Success
- [ ] User adoption targets met
- [ ] Performance metrics achieved
- [ ] Positive user feedback
- [ ] Reduced operational costs

## 13. Risk Assessment

### Technical Risks
- **Risk**: Integration complexity
  - **Mitigation**: Phased rollout with thorough testing

- **Risk**: Performance bottlenecks
  - **Mitigation**: Load testing and optimization

### Business Risks
- **Risk**: User adoption challenges
  - **Mitigation**: User training and support

## 14. Timeline & Milestones

### Phase 1: Foundation (Weeks 1-2)
- [ ] Core architecture setup
- [ ] Basic CRUD operations
- [ ] Authentication system

### Phase 2: Features (Weeks 3-4)
- [ ] Core business logic
- [ ] User interface development
- [ ] API integration

### Phase 3: Polish (Weeks 5-6)
- [ ] Testing and bug fixes
- [ ] Performance optimization
- [ ] Documentation

## 15. Future Enhancements

### Version 2.0
- Advanced analytics dashboard
- Mobile application
- Third-party integrations

### Version 3.0
- AI-powered insights
- Advanced automation
- Enterprise features

---

*This PRD was generated by AutoDevCore - The core of intelligent development.*
"""

        return prd_content

    def _get_current_date(self) -> str:
        """Get the current date in a formatted string."""
        from datetime import datetime

        return datetime.now().strftime("%B %d, %Y")

    def _identify_primary_persona(self, idea: str) -> str:
        """Identify the primary user persona based on the idea."""
        idea_lower = idea.lower()

        if any(word in idea_lower for word in ["inventory", "stock", "management"]):
            return "Inventory Manager"
        elif any(word in idea_lower for word in ["user", "account", "profile"]):
            return "System Administrator"
        else:
            return "End User"

    def _get_persona_role(self, idea: str) -> str:
        """Get the role description for the primary persona."""
        idea_lower = idea.lower()

        if any(word in idea_lower for word in ["inventory", "stock"]):
            return "Manages product inventory and stock levels"
        elif any(word in idea_lower for word in ["user", "account"]):
            return "Manages user accounts and system access"
        else:
            return "Uses the application for daily tasks"

    def _get_persona_goals(self, idea: str) -> str:
        """Get the goals for the primary persona."""
        idea_lower = idea.lower()

        if any(word in idea_lower for word in ["inventory", "stock"]):
            return "Maintain accurate inventory levels, prevent stockouts, optimize ordering"
        elif any(word in idea_lower for word in ["user", "account"]):
            return "Efficiently manage user accounts, ensure security, maintain access control"
        else:
            return "Complete tasks efficiently, access information quickly, maintain data accuracy"

    def _get_persona_pain_points(self, idea: str) -> str:
        """Get the pain points for the primary persona."""
        idea_lower = idea.lower()

        if any(word in idea_lower for word in ["inventory", "stock"]):
            return "Manual inventory tracking, stockouts, inaccurate data, time-consuming processes"
        elif any(word in idea_lower for word in ["user", "account"]):
            return "Complex user management, security concerns, access control issues"
        else:
            return "Slow systems, difficult navigation, data entry errors, lack of automation"

    def _generate_use_cases(self, app_plan: Dict[str, Any]) -> str:
        """Generate use cases based on the app plan."""
        use_cases = []

        # Generate use cases based on features
        features = app_plan.get("features", [])

        for feature in features:
            if "authentication" in feature.lower():
                use_cases.append("- **UC001**: User logs into the system")
                use_cases.append("- **UC002**: User resets password")
            elif "inventory" in feature.lower():
                use_cases.append("- **UC003**: Manager adds new product to inventory")
                use_cases.append("- **UC004**: System alerts low stock levels")
            elif "dashboard" in feature.lower():
                use_cases.append("- **UC005**: User views system dashboard")
            elif "search" in feature.lower():
                use_cases.append("- **UC006**: User searches for specific data")

        return (
            "\n".join(use_cases)
            if use_cases
            else "- **UC001**: User performs basic operations"
        )

    def _format_features(self, features: list) -> str:
        """Format features as a markdown list."""
        if not features:
            return "- Basic CRUD operations\n- User authentication\n- Data management"

        formatted_features = []
        for feature in features:
            formatted_features.append(f"- {feature}")

        return "\n".join(formatted_features)

    def _format_architecture(self, architecture: Dict[str, Any]) -> str:
        """Format architecture information."""
        pattern = architecture.get("pattern", "MVC")
        layers = architecture.get("layers", [])

        layers_text = "\n".join([f"- {layer}" for layer in layers])

        return f"""
**Architecture Pattern**: {pattern}

**System Layers**:
{layers_text}
"""

    def _format_database_schema(self, schema: Dict[str, Any]) -> str:
        """Format database schema information."""
        tables = schema.get("tables", [])

        if not tables:
            return "Standard user and data tables"

        schema_text = []
        for table in tables:
            table_name = table.get("name", "unknown")
            columns = table.get("columns", [])

            schema_text.append(f"**{table_name}**:")
            for column in columns:
                col_name = column.get("name", "unknown")
                col_type = column.get("type", "TEXT")
                schema_text.append(f"  - {col_name}: {col_type}")
            schema_text.append("")

        return "\n".join(schema_text)

    def _format_api_endpoints(self, endpoints: list) -> str:
        """Format API endpoints information."""
        if not endpoints:
            return "Standard REST API endpoints"

        endpoint_text = []
        for endpoint in endpoints:
            if isinstance(endpoint, dict):
                method = endpoint.get("method", "GET")
                path = endpoint.get("path", "/")
                description = endpoint.get("description", "API endpoint")
                endpoint_text.append(f"- **{method} {path}**: {description}")
            else:
                # Handle string format
                endpoint_text.append(f"- **{endpoint}**")

        return "\n".join(endpoint_text)

    def _format_ui_components(self, components: list) -> str:
        """Format UI components information."""
        if not components:
            return "- Navigation\n- Forms\n- Data displays\n- Modals"

        component_text = []
        for component in components:
            component_text.append(f"- {component}")

        return "\n".join(component_text)

    def _format_deployment(self, deployment: Dict[str, Any]) -> str:
        """Format deployment information."""
        platform = deployment.get("platform", "Docker")
        environment = deployment.get("environment", "Local Development")
        database = deployment.get("database", "SQLite")

        return f"""
**Platform**: {platform}
**Environment**: {environment}
**Database**: {database}
**Monitoring**: Basic logging and health checks
"""
