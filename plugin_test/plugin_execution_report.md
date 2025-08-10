# Plugin Execution Report

**Plugin**: code_analyzer
**Execution Time**: 2025-08-10T00:52:41.627845

## Plugin Information

- **Name**: code_analyzer
- **Description**: Analyzes code complexity, quality metrics, and provides recommendations
- **Author**: AutoDevCore Team
- **Version**: 1.0.0
- **Status**: ✅ Valid

## Execution Results

```json
{
  "status": "success",
  "message": "Code analysis completed successfully",
  "results": {
    "files_analyzed": 66,
    "total_lines": 6377,
    "functions": [
      {
        "name": "main",
        "file": "cli.py",
        "line": 22,
        "length": 15,
        "complexity": 16
      },
      {
        "name": "show_splash",
        "file": "splash.py",
        "line": 7,
        "length": 6,
        "complexity": 1
      },
      {
        "name": "show_help",
        "file": "splash.py",
        "line": 31,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "__init__",
        "file": "modes/journal.py",
        "line": 16,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "execute",
        "file": "modes/journal.py",
        "line": 20,
        "length": 36,
        "complexity": 2
      },
      {
        "name": "_analyze_codebase_metrics",
        "file": "modes/journal.py",
        "line": 84,
        "length": 12,
        "complexity": 23
      },
      {
        "name": "_calculate_nesting_depth",
        "file": "modes/journal.py",
        "line": 175,
        "length": 4,
        "complexity": 3
      },
      {
        "name": "_analyze_technical_debt",
        "file": "modes/journal.py",
        "line": 185,
        "length": 6,
        "complexity": 15
      },
      {
        "name": "_analyze_performance_patterns",
        "file": "modes/journal.py",
        "line": 253,
        "length": 6,
        "complexity": 10
      },
      {
        "name": "_detect_security_vulnerabilities",
        "file": "modes/journal.py",
        "line": 295,
        "length": 5,
        "complexity": 9
      },
      {
        "name": "_calculate_quality_metrics",
        "file": "modes/journal.py",
        "line": 340,
        "length": 9,
        "complexity": 7
      },
      {
        "name": "_generate_ai_insights",
        "file": "modes/journal.py",
        "line": 389,
        "length": 3,
        "complexity": 8
      },
      {
        "name": "_fallback_ai_insights",
        "file": "modes/journal.py",
        "line": 445,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_journal_report",
        "file": "modes/journal.py",
        "line": 455,
        "length": 4,
        "complexity": 17
      },
      {
        "name": "_generate_actionable_recommendations",
        "file": "modes/journal.py",
        "line": 545,
        "length": 13,
        "complexity": 7
      },
      {
        "name": "__init__",
        "file": "modes/compose.py",
        "line": 18,
        "length": 6,
        "complexity": 1
      },
      {
        "name": "execute",
        "file": "modes/compose.py",
        "line": 26,
        "length": 29,
        "complexity": 1
      },
      {
        "name": "_save_files",
        "file": "modes/compose.py",
        "line": 71,
        "length": 10,
        "complexity": 6
      },
      {
        "name": "_generate_dependency_files",
        "file": "modes/compose.py",
        "line": 98,
        "length": 4,
        "complexity": 5
      },
      {
        "name": "__init__",
        "file": "modes/blueprint.py",
        "line": 16,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "execute",
        "file": "modes/blueprint.py",
        "line": 20,
        "length": 35,
        "complexity": 2
      },
      {
        "name": "_analyze_structure",
        "file": "modes/blueprint.py",
        "line": 80,
        "length": 4,
        "complexity": 13
      },
      {
        "name": "_analyze_code_with_gpt_oss",
        "file": "modes/blueprint.py",
        "line": 130,
        "length": 3,
        "complexity": 2
      },
      {
        "name": "_get_key_files",
        "file": "modes/blueprint.py",
        "line": 152,
        "length": 5,
        "complexity": 2
      },
      {
        "name": "_analyze_architecture_patterns",
        "file": "modes/blueprint.py",
        "line": 170,
        "length": 2,
        "complexity": 8
      },
      {
        "name": "_analyze_code_quality",
        "file": "modes/blueprint.py",
        "line": 220,
        "length": 2,
        "complexity": 8
      },
      {
        "name": "_analyze_design_patterns",
        "file": "modes/blueprint.py",
        "line": 269,
        "length": 4,
        "complexity": 9
      },
      {
        "name": "_analyze_complexity",
        "file": "modes/blueprint.py",
        "line": 299,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_analyze_security_patterns",
        "file": "modes/blueprint.py",
        "line": 310,
        "length": 4,
        "complexity": 9
      },
      {
        "name": "_fallback_code_analysis",
        "file": "modes/blueprint.py",
        "line": 339,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_analyze_dependencies",
        "file": "modes/blueprint.py",
        "line": 349,
        "length": 5,
        "complexity": 9
      },
      {
        "name": "_extract_api_documentation",
        "file": "modes/blueprint.py",
        "line": 381,
        "length": 4,
        "complexity": 7
      },
      {
        "name": "_detect_code_patterns",
        "file": "modes/blueprint.py",
        "line": 407,
        "length": 4,
        "complexity": 10
      },
      {
        "name": "_generate_architecture_diagram",
        "file": "modes/blueprint.py",
        "line": 443,
        "length": 4,
        "complexity": 8
      },
      {
        "name": "_generate_analysis_report",
        "file": "modes/blueprint.py",
        "line": 493,
        "length": 4,
        "complexity": 17
      },
      {
        "name": "_generate_refactoring_recommendations",
        "file": "modes/blueprint.py",
        "line": 569,
        "length": 7,
        "complexity": 11
      },
      {
        "name": "__init__",
        "file": "modes/plugin.py",
        "line": 19,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "execute",
        "file": "modes/plugin.py",
        "line": 27,
        "length": 22,
        "complexity": 7
      },
      {
        "name": "_list_available_plugins",
        "file": "modes/plugin.py",
        "line": 89,
        "length": 6,
        "complexity": 3
      },
      {
        "name": "_discover_all_plugins",
        "file": "modes/plugin.py",
        "line": 109,
        "length": 5,
        "complexity": 4
      },
      {
        "name": "_analyze_plugin_file",
        "file": "modes/plugin.py",
        "line": 126,
        "length": 4,
        "complexity": 13
      },
      {
        "name": "_discover_plugin_info",
        "file": "modes/plugin.py",
        "line": 185,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "_load_plugin_safely",
        "file": "modes/plugin.py",
        "line": 194,
        "length": 4,
        "complexity": 5
      },
      {
        "name": "_execute_plugin_safely",
        "file": "modes/plugin.py",
        "line": 228,
        "length": 2,
        "complexity": 2
      },
      {
        "name": "_generate_plugin_documentation",
        "file": "modes/plugin.py",
        "line": 246,
        "length": 7,
        "complexity": 7
      },
      {
        "name": "_generate_execution_report",
        "file": "modes/plugin.py",
        "line": 315,
        "length": 4,
        "complexity": 4
      },
      {
        "name": "__init__",
        "file": "modes/base.py",
        "line": 17,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "log_thought",
        "file": "modes/base.py",
        "line": 26,
        "length": 4,
        "complexity": 3
      },
      {
        "name": "save_thought_trail",
        "file": "modes/base.py",
        "line": 43,
        "length": 6,
        "complexity": 2
      },
      {
        "name": "generate_mermaid_diagram",
        "file": "modes/base.py",
        "line": 55,
        "length": 8,
        "complexity": 6
      },
      {
        "name": "generate_interactive_html_report",
        "file": "modes/base.py",
        "line": 108,
        "length": 6,
        "complexity": 3
      },
      {
        "name": "_generate_html_template",
        "file": "modes/base.py",
        "line": 121,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "export_thought_trail",
        "file": "modes/base.py",
        "line": 536,
        "length": 2,
        "complexity": 4
      },
      {
        "name": "execute",
        "file": "modes/base.py",
        "line": 561,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "__init__",
        "file": "modes/score.py",
        "line": 16,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "execute",
        "file": "modes/score.py",
        "line": 21,
        "length": 26,
        "complexity": 3
      },
      {
        "name": "_load_template",
        "file": "modes/score.py",
        "line": 70,
        "length": 5,
        "complexity": 5
      },
      {
        "name": "_analyze_codebase",
        "file": "modes/score.py",
        "line": 88,
        "length": 3,
        "complexity": 2
      },
      {
        "name": "_get_key_files",
        "file": "modes/score.py",
        "line": 110,
        "length": 6,
        "complexity": 4
      },
      {
        "name": "_analyze_file_structure",
        "file": "modes/score.py",
        "line": 132,
        "length": 4,
        "complexity": 8
      },
      {
        "name": "_analyze_code_quality",
        "file": "modes/score.py",
        "line": 159,
        "length": 2,
        "complexity": 8
      },
      {
        "name": "_analyze_security",
        "file": "modes/score.py",
        "line": 211,
        "length": 2,
        "complexity": 8
      },
      {
        "name": "_analyze_performance",
        "file": "modes/score.py",
        "line": 256,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_analyze_architecture",
        "file": "modes/score.py",
        "line": 265,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_fallback_analysis",
        "file": "modes/score.py",
        "line": 274,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_evaluate_app_intelligent",
        "file": "modes/score.py",
        "line": 284,
        "length": 9,
        "complexity": 3
      },
      {
        "name": "_evaluate_criterion_intelligent",
        "file": "modes/score.py",
        "line": 321,
        "length": 4,
        "complexity": 7
      },
      {
        "name": "_generate_recommendations",
        "file": "modes/score.py",
        "line": 357,
        "length": 9,
        "complexity": 6
      },
      {
        "name": "_generate_radar_chart",
        "file": "modes/score.py",
        "line": 381,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "_generate_report",
        "file": "modes/score.py",
        "line": 402,
        "length": 4,
        "complexity": 9
      },
      {
        "name": "__init__",
        "file": "agents/composer.py",
        "line": 14,
        "length": 1,
        "complexity": 1
      },
      {
        "name": "create_app_plan",
        "file": "agents/composer.py",
        "line": 17,
        "length": 3,
        "complexity": 3
      },
      {
        "name": "_create_fallback_plan",
        "file": "agents/composer.py",
        "line": 48,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_app_name",
        "file": "agents/composer.py",
        "line": 102,
        "length": 4,
        "complexity": 4
      },
      {
        "name": "__init__",
        "file": "agents/security_generator.py",
        "line": 12,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "generate_security_features",
        "file": "agents/security_generator.py",
        "line": 16,
        "length": 3,
        "complexity": 2
      },
      {
        "name": "_generate_auth_system",
        "file": "agents/security_generator.py",
        "line": 31,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_auth_models",
        "file": "agents/security_generator.py",
        "line": 108,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_security_middleware",
        "file": "agents/security_generator.py",
        "line": 166,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_security_config",
        "file": "agents/security_generator.py",
        "line": 224,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_validation_utils",
        "file": "agents/security_generator.py",
        "line": 265,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_security_requirements",
        "file": "agents/security_generator.py",
        "line": 314,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_auth_dependencies",
        "file": "agents/security_generator.py",
        "line": 326,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "__init__",
        "file": "agents/prd_writer.py",
        "line": 11,
        "length": 1,
        "complexity": 1
      },
      {
        "name": "generate_prd",
        "file": "agents/prd_writer.py",
        "line": 14,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "_get_current_date",
        "file": "agents/prd_writer.py",
        "line": 207,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_identify_primary_persona",
        "file": "agents/prd_writer.py",
        "line": 212,
        "length": 3,
        "complexity": 3
      },
      {
        "name": "_get_persona_role",
        "file": "agents/prd_writer.py",
        "line": 223,
        "length": 3,
        "complexity": 3
      },
      {
        "name": "_get_persona_goals",
        "file": "agents/prd_writer.py",
        "line": 234,
        "length": 3,
        "complexity": 3
      },
      {
        "name": "_get_persona_pain_points",
        "file": "agents/prd_writer.py",
        "line": 245,
        "length": 3,
        "complexity": 3
      },
      {
        "name": "_generate_use_cases",
        "file": "agents/prd_writer.py",
        "line": 256,
        "length": 5,
        "complexity": 6
      },
      {
        "name": "_format_features",
        "file": "agents/prd_writer.py",
        "line": 277,
        "length": 5,
        "complexity": 3
      },
      {
        "name": "_format_architecture",
        "file": "agents/prd_writer.py",
        "line": 288,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "_format_database_schema",
        "file": "agents/prd_writer.py",
        "line": 302,
        "length": 6,
        "complexity": 4
      },
      {
        "name": "_format_api_endpoints",
        "file": "agents/prd_writer.py",
        "line": 323,
        "length": 5,
        "complexity": 4
      },
      {
        "name": "_format_ui_components",
        "file": "agents/prd_writer.py",
        "line": 341,
        "length": 5,
        "complexity": 3
      },
      {
        "name": "_format_deployment",
        "file": "agents/prd_writer.py",
        "line": 352,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "__init__",
        "file": "agents/readme_writer.py",
        "line": 11,
        "length": 1,
        "complexity": 1
      },
      {
        "name": "generate_readme",
        "file": "agents/readme_writer.py",
        "line": 14,
        "length": 6,
        "complexity": 2
      },
      {
        "name": "_format_features",
        "file": "agents/readme_writer.py",
        "line": 318,
        "length": 5,
        "complexity": 3
      },
      {
        "name": "_format_api_endpoints",
        "file": "agents/readme_writer.py",
        "line": 329,
        "length": 5,
        "complexity": 4
      },
      {
        "name": "_format_tech_stack",
        "file": "agents/readme_writer.py",
        "line": 347,
        "length": 6,
        "complexity": 3
      },
      {
        "name": "_format_architecture",
        "file": "agents/readme_writer.py",
        "line": 360,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "_format_database_schema",
        "file": "agents/readme_writer.py",
        "line": 376,
        "length": 6,
        "complexity": 7
      },
      {
        "name": "__init__",
        "file": "agents/code_generator.py",
        "line": 13,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "generate_codebase",
        "file": "agents/code_generator.py",
        "line": 17,
        "length": 6,
        "complexity": 4
      },
      {
        "name": "_generate_python_codebase",
        "file": "agents/code_generator.py",
        "line": 42,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "_generate_node_codebase",
        "file": "agents/code_generator.py",
        "line": 71,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_main_py",
        "file": "agents/code_generator.py",
        "line": 86,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_generate_models_py",
        "file": "agents/code_generator.py",
        "line": 144,
        "length": 5,
        "complexity": 2
      },
      {
        "name": "_generate_database_py",
        "file": "agents/code_generator.py",
        "line": 190,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_routes_py",
        "file": "agents/code_generator.py",
        "line": 221,
        "length": 5,
        "complexity": 2
      },
      {
        "name": "_generate_helpers_py",
        "file": "agents/code_generator.py",
        "line": 307,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_tests_py",
        "file": "agents/code_generator.py",
        "line": 331,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_generate_config_py",
        "file": "agents/code_generator.py",
        "line": 365,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_requirements_txt",
        "file": "agents/code_generator.py",
        "line": 388,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_env_example",
        "file": "agents/code_generator.py",
        "line": 414,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_dockerfile",
        "file": "agents/code_generator.py",
        "line": 435,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_gitignore",
        "file": "agents/code_generator.py",
        "line": 460,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_index_js",
        "file": "agents/code_generator.py",
        "line": 511,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_generate_package_json",
        "file": "agents/code_generator.py",
        "line": 564,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_generate_user_model_js",
        "file": "agents/code_generator.py",
        "line": 594,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_api_routes_js",
        "file": "agents/code_generator.py",
        "line": 624,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_helpers_js",
        "file": "agents/code_generator.py",
        "line": 662,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "_generate_tests_js",
        "file": "agents/code_generator.py",
        "line": 690,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "__init__",
        "file": "integrations/gpt_oss.py",
        "line": 20,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "_make_request",
        "file": "integrations/gpt_oss.py",
        "line": 25,
        "length": 2,
        "complexity": 3
      },
      {
        "name": "generate",
        "file": "integrations/gpt_oss.py",
        "line": 52,
        "length": 7,
        "complexity": 3
      },
      {
        "name": "generate_with_tools",
        "file": "integrations/gpt_oss.py",
        "line": 94,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "analyze_code",
        "file": "integrations/gpt_oss.py",
        "line": 109,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "generate_app_plan",
        "file": "integrations/gpt_oss.py",
        "line": 128,
        "length": 6,
        "complexity": 4
      },
      {
        "name": "generate_code",
        "file": "integrations/gpt_oss.py",
        "line": 174,
        "length": 5,
        "complexity": 1
      },
      {
        "name": "score_application",
        "file": "integrations/gpt_oss.py",
        "line": 193,
        "length": 6,
        "complexity": 1
      },
      {
        "name": "create_tool_call",
        "file": "integrations/gpt_oss.py",
        "line": 224,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "create_tool_result",
        "file": "integrations/gpt_oss.py",
        "line": 233,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "format_conversation",
        "file": "integrations/gpt_oss.py",
        "line": 242,
        "length": 4,
        "complexity": 5
      },
      {
        "name": "get_db",
        "file": "demo_output/task-management/app/database.py",
        "line": 20,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "test_read_main",
        "file": "demo_output/task-management/app/tests/test_main.py",
        "line": 11,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_health_check",
        "file": "demo_output/task-management/app/tests/test_main.py",
        "line": 17,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_get_users",
        "file": "demo_output/task-management/app/tests/test_main.py",
        "line": 23,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "hash_password",
        "file": "demo_output/task-management/app/utils/helpers.py",
        "line": 9,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "generate_token",
        "file": "demo_output/task-management/app/utils/helpers.py",
        "line": 13,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "format_datetime",
        "file": "demo_output/task-management/app/utils/helpers.py",
        "line": 17,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "get_users",
        "file": "demo_output/task-management/app/api/routes.py",
        "line": 14,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "get_user",
        "file": "demo_output/task-management/app/api/routes.py",
        "line": 29,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "get_db",
        "file": "gpt_oss_test/SimpleTodoApp/database.py",
        "line": 20,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "test_read_main",
        "file": "gpt_oss_test/SimpleTodoApp/tests/test_main.py",
        "line": 11,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_health_check",
        "file": "gpt_oss_test/SimpleTodoApp/tests/test_main.py",
        "line": 17,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_get_users",
        "file": "gpt_oss_test/SimpleTodoApp/tests/test_main.py",
        "line": 23,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "hash_password",
        "file": "gpt_oss_test/SimpleTodoApp/utils/helpers.py",
        "line": 9,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "generate_token",
        "file": "gpt_oss_test/SimpleTodoApp/utils/helpers.py",
        "line": 13,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "format_datetime",
        "file": "gpt_oss_test/SimpleTodoApp/utils/helpers.py",
        "line": 17,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "get_users",
        "file": "gpt_oss_test/SimpleTodoApp/api/routes.py",
        "line": 14,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "get_user",
        "file": "gpt_oss_test/SimpleTodoApp/api/routes.py",
        "line": 29,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "get_db",
        "file": "output/restaurant-inventory/app/database.py",
        "line": 20,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "test_read_main",
        "file": "output/restaurant-inventory/app/tests/test_main.py",
        "line": 11,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_health_check",
        "file": "output/restaurant-inventory/app/tests/test_main.py",
        "line": 17,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_get_users",
        "file": "output/restaurant-inventory/app/tests/test_main.py",
        "line": 23,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "hash_password",
        "file": "output/restaurant-inventory/app/utils/helpers.py",
        "line": 9,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "generate_token",
        "file": "output/restaurant-inventory/app/utils/helpers.py",
        "line": 13,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "format_datetime",
        "file": "output/restaurant-inventory/app/utils/helpers.py",
        "line": 17,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "get_users",
        "file": "output/restaurant-inventory/app/api/routes.py",
        "line": 14,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "get_user",
        "file": "output/restaurant-inventory/app/api/routes.py",
        "line": 29,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "get_products",
        "file": "output/restaurant-inventory/app/api/routes.py",
        "line": 44,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "get_product",
        "file": "output/restaurant-inventory/app/api/routes.py",
        "line": 61,
        "length": 5,
        "complexity": 2
      },
      {
        "name": "get_db",
        "file": "secure_app_test/SecureTaskApp/database.py",
        "line": 20,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "setup_security_middleware",
        "file": "secure_app_test/SecureTaskApp/middleware/security.py",
        "line": 30,
        "length": 7,
        "complexity": 1
      },
      {
        "name": "verify_password",
        "file": "secure_app_test/SecureTaskApp/auth/auth.py",
        "line": 23,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "get_password_hash",
        "file": "secure_app_test/SecureTaskApp/auth/auth.py",
        "line": 27,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "create_access_token",
        "file": "secure_app_test/SecureTaskApp/auth/auth.py",
        "line": 31,
        "length": 6,
        "complexity": 2
      },
      {
        "name": "verify_token",
        "file": "secure_app_test/SecureTaskApp/auth/auth.py",
        "line": 42,
        "length": 2,
        "complexity": 3
      },
      {
        "name": "get_current_user",
        "file": "secure_app_test/SecureTaskApp/auth/auth.py",
        "line": 53,
        "length": 8,
        "complexity": 3
      },
      {
        "name": "get_current_active_user",
        "file": "secure_app_test/SecureTaskApp/auth/auth.py",
        "line": 69,
        "length": 3,
        "complexity": 2
      },
      {
        "name": "validate_username",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 16,
        "length": 3,
        "complexity": 3
      },
      {
        "name": "validate_password",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 24,
        "length": 5,
        "complexity": 5
      },
      {
        "name": "require_admin",
        "file": "secure_app_test/SecureTaskApp/auth/dependencies.py",
        "line": 13,
        "length": 3,
        "complexity": 2
      },
      {
        "name": "require_user_permission",
        "file": "secure_app_test/SecureTaskApp/auth/dependencies.py",
        "line": 22,
        "length": 3,
        "complexity": 2
      },
      {
        "name": "test_read_main",
        "file": "secure_app_test/SecureTaskApp/tests/test_main.py",
        "line": 11,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_health_check",
        "file": "secure_app_test/SecureTaskApp/tests/test_main.py",
        "line": 17,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "test_get_users",
        "file": "secure_app_test/SecureTaskApp/tests/test_main.py",
        "line": 23,
        "length": 4,
        "complexity": 1
      },
      {
        "name": "hash_password",
        "file": "secure_app_test/SecureTaskApp/utils/helpers.py",
        "line": 9,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "generate_token",
        "file": "secure_app_test/SecureTaskApp/utils/helpers.py",
        "line": 13,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "format_datetime",
        "file": "secure_app_test/SecureTaskApp/utils/helpers.py",
        "line": 17,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "validate_email",
        "file": "secure_app_test/SecureTaskApp/utils/validation.py",
        "line": 9,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "validate_password_strength",
        "file": "secure_app_test/SecureTaskApp/utils/validation.py",
        "line": 14,
        "length": 7,
        "complexity": 5
      },
      {
        "name": "sanitize_input",
        "file": "secure_app_test/SecureTaskApp/utils/validation.py",
        "line": 35,
        "length": 4,
        "complexity": 2
      },
      {
        "name": "validate_request_size",
        "file": "secure_app_test/SecureTaskApp/utils/validation.py",
        "line": 43,
        "length": 2,
        "complexity": 1
      },
      {
        "name": "get_users",
        "file": "secure_app_test/SecureTaskApp/api/routes.py",
        "line": 14,
        "length": 3,
        "complexity": 1
      },
      {
        "name": "get_user",
        "file": "secure_app_test/SecureTaskApp/api/routes.py",
        "line": 29,
        "length": 4,
        "complexity": 2
      }
    ],
    "classes": [
      {
        "name": "JournalMode",
        "file": "modes/journal.py",
        "line": 13,
        "methods": 12
      },
      {
        "name": "ComposeMode",
        "file": "modes/compose.py",
        "line": 15,
        "methods": 4
      },
      {
        "name": "BlueprintMode",
        "file": "modes/blueprint.py",
        "line": 13,
        "methods": 17
      },
      {
        "name": "PluginMode",
        "file": "modes/plugin.py",
        "line": 16,
        "methods": 10
      },
      {
        "name": "BaseMode",
        "file": "modes/base.py",
        "line": 14,
        "methods": 8
      },
      {
        "name": "ScoreMode",
        "file": "modes/score.py",
        "line": 13,
        "methods": 16
      },
      {
        "name": "ComposerAgent",
        "file": "agents/composer.py",
        "line": 11,
        "methods": 4
      },
      {
        "name": "SecurityGeneratorAgent",
        "file": "agents/security_generator.py",
        "line": 9,
        "methods": 9
      },
      {
        "name": "PRDWriterAgent",
        "file": "agents/prd_writer.py",
        "line": 8,
        "methods": 14
      },
      {
        "name": "READMEWriterAgent",
        "file": "agents/readme_writer.py",
        "line": 8,
        "methods": 7
      },
      {
        "name": "CodeGeneratorAgent",
        "file": "agents/code_generator.py",
        "line": 10,
        "methods": 21
      },
      {
        "name": "GPTOSSClient",
        "file": "integrations/gpt_oss.py",
        "line": 17,
        "methods": 8
      },
      {
        "name": "HarmonyFormat",
        "file": "integrations/gpt_oss.py",
        "line": 220,
        "methods": 3
      },
      {
        "name": "Settings",
        "file": "demo_output/task-management/app/config.py",
        "line": 8,
        "methods": 0
      },
      {
        "name": "Config",
        "file": "demo_output/task-management/app/config.py",
        "line": 15,
        "methods": 0
      },
      {
        "name": "User",
        "file": "demo_output/task-management/app/models.py",
        "line": 11,
        "methods": 0
      },
      {
        "name": "Settings",
        "file": "gpt_oss_test/SimpleTodoApp/config.py",
        "line": 8,
        "methods": 0
      },
      {
        "name": "Config",
        "file": "gpt_oss_test/SimpleTodoApp/config.py",
        "line": 15,
        "methods": 0
      },
      {
        "name": "User",
        "file": "gpt_oss_test/SimpleTodoApp/models.py",
        "line": 11,
        "methods": 0
      },
      {
        "name": "Settings",
        "file": "output/restaurant-inventory/app/config.py",
        "line": 8,
        "methods": 0
      },
      {
        "name": "Config",
        "file": "output/restaurant-inventory/app/config.py",
        "line": 15,
        "methods": 0
      },
      {
        "name": "User",
        "file": "output/restaurant-inventory/app/models.py",
        "line": 11,
        "methods": 0
      },
      {
        "name": "Product",
        "file": "output/restaurant-inventory/app/models.py",
        "line": 24,
        "methods": 0
      },
      {
        "name": "Settings",
        "file": "secure_app_test/SecureTaskApp/config.py",
        "line": 8,
        "methods": 0
      },
      {
        "name": "Config",
        "file": "secure_app_test/SecureTaskApp/config.py",
        "line": 15,
        "methods": 0
      },
      {
        "name": "User",
        "file": "secure_app_test/SecureTaskApp/models.py",
        "line": 11,
        "methods": 0
      },
      {
        "name": "SecurityMiddleware",
        "file": "secure_app_test/SecureTaskApp/middleware/security.py",
        "line": 17,
        "methods": 0
      },
      {
        "name": "SecuritySettings",
        "file": "secure_app_test/SecureTaskApp/config/security.py",
        "line": 9,
        "methods": 0
      },
      {
        "name": "Config",
        "file": "secure_app_test/SecureTaskApp/config/security.py",
        "line": 34,
        "methods": 0
      },
      {
        "name": "UserCreate",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 9,
        "methods": 2
      },
      {
        "name": "UserLogin",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 35,
        "methods": 0
      },
      {
        "name": "Token",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 40,
        "methods": 0
      },
      {
        "name": "UserResponse",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 45,
        "methods": 0
      },
      {
        "name": "Config",
        "file": "secure_app_test/SecureTaskApp/auth/models.py",
        "line": 53,
        "methods": 0
      }
    ],
    "complexity_metrics": {
      "high_complexity_functions": [
        {
          "name": "main",
          "file": "cli.py",
          "line": 22,
          "length": 15,
          "complexity": 16
        },
        {
          "name": "_analyze_codebase_metrics",
          "file": "modes/journal.py",
          "line": 84,
          "length": 12,
          "complexity": 23
        },
        {
          "name": "_analyze_technical_debt",
          "file": "modes/journal.py",
          "line": 185,
          "length": 6,
          "complexity": 15
        },
        {
          "name": "_generate_journal_report",
          "file": "modes/journal.py",
          "line": 455,
          "length": 4,
          "complexity": 17
        },
        {
          "name": "_analyze_structure",
          "file": "modes/blueprint.py",
          "line": 80,
          "length": 4,
          "complexity": 13
        },
        {
          "name": "_generate_analysis_report",
          "file": "modes/blueprint.py",
          "line": 493,
          "length": 4,
          "complexity": 17
        },
        {
          "name": "_generate_refactoring_recommendations",
          "file": "modes/blueprint.py",
          "line": 569,
          "length": 7,
          "complexity": 11
        },
        {
          "name": "_analyze_plugin_file",
          "file": "modes/plugin.py",
          "line": 126,
          "length": 4,
          "complexity": 13
        }
      ],
      "long_functions": [
        {
          "name": "execute",
          "file": "modes/journal.py",
          "line": 20,
          "length": 36,
          "complexity": 2
        },
        {
          "name": "execute",
          "file": "modes/compose.py",
          "line": 26,
          "length": 29,
          "complexity": 1
        },
        {
          "name": "execute",
          "file": "modes/blueprint.py",
          "line": 20,
          "length": 35,
          "complexity": 2
        },
        {
          "name": "execute",
          "file": "modes/plugin.py",
          "line": 27,
          "length": 22,
          "complexity": 7
        },
        {
          "name": "execute",
          "file": "modes/score.py",
          "line": 21,
          "length": 26,
          "complexity": 3
        }
      ],
      "deep_nesting": []
    },
    "quality_issues": [],
    "recommendations": [
      "Consider refactoring high complexity functions into smaller, more focused functions",
      "Break down long functions into smaller, more manageable pieces",
      "Consider splitting large files into smaller modules"
    ]
  },
  "report_file": "plugin_test/code_analysis_report.md"
}
```

## Available Functions

- `run`
- `calculate_complexity`
