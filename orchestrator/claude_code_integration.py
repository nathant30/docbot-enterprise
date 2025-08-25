#!/usr/bin/env python3
"""
Claude Code Integration Layer
Interfaces with Claude Code CLI for task execution
"""

import subprocess
import json
import asyncio
from pathlib import Path
from typing import Dict, Any
from prd_parser import TaskSpec
from multi_agent_system import Task

class ClaudeCodeAgent:
    def __init__(self, agent_name: str, specialization: str):
        self.agent_name = agent_name
        self.specialization = specialization
    
    async def execute_task(self, task: TaskSpec) -> Dict[str, Any]:
        """Execute task using Claude Code CLI"""
        # Create task-specific prompt
        prompt = self._create_claude_code_prompt(task)
        
        # Write prompt to temp file
        prompt_file = f"/tmp/{task.id}_prompt.md"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        # Execute Claude Code
        result = await self._run_claude_code(prompt_file, task)
        return result
    
    def _create_claude_code_prompt(self, task: TaskSpec) -> str:
        return f"""
# Task: {task.title}

## Context
You are {self.agent_name}, specialized in {self.specialization}.
Working on DocBot Enterprise Invoice Automation System.

## Task Description
{task.description}

## Requirements from PRD
- Files to create: {', '.join(task.files_to_create)}
- Acceptance criteria: {chr(10).join(f'- {criteria}' for criteria in task.acceptance_criteria)}

## Deliverables Required
Create production-ready, enterprise-grade code for all specified files.
Include comprehensive error handling, logging, and documentation.

## Implementation Guidelines
{self._get_agent_guidelines()}

Please implement all required files with complete, working code.
"""
    
    def _get_agent_guidelines(self) -> str:
        guidelines = {
            'alice_backend': """
- Use FastAPI with async/await patterns
- Implement SQLAlchemy models with proper relationships
- Use Pydantic for validation
- Add comprehensive error handling
- Include OpenAPI documentation
- Implement JWT authentication
- Use dependency injection for database sessions
""",
            'charlie_frontend': """
- Use React 18+ with TypeScript
- Implement functional components and hooks
- Use Tailwind CSS for styling
- Add proper error boundaries
- Use React Query for API state management
- Implement responsive design
- Add accessibility features (ARIA labels)
""",
            'bob_ocr_ai': """
- Support multiple OCR providers (Azure, Google, Tesseract)
- Implement confidence scoring
- Add image preprocessing (deskewing, noise reduction)
- Include fallback mechanisms
- Optimize for processing speed
- Handle various file formats
""",
            'diana_integration': """
- Create robust API integration patterns
- Implement proper error handling and retries
- Use webhook patterns for real-time updates
- Add comprehensive logging
- Support multiple ERP systems
- Implement rate limiting and throttling
""",
            'eve_infrastructure': """
- Use Docker best practices
- Implement proper health checks
- Add monitoring and logging
- Use infrastructure as code
- Implement proper security practices
- Add backup and disaster recovery
""",
            'felix_qa_engineer': """
- Create comprehensive test suites
- Implement unit, integration, and E2E tests
- Add test coverage reporting
- Use proper mocking strategies
- Implement CI/CD pipeline
- Add performance testing
""",
            # Add guidelines for other agents...
        }
        return guidelines.get(self.agent_name, "Follow best practices for your domain.")
    
    async def _run_claude_code(self, prompt_file: str, task: TaskSpec) -> Dict[str, Any]:
        """Execute Claude Code CLI with the prompt"""
        try:
            # Note: This is a simulation - actual Claude Code CLI may have different parameters
            cmd = [
                "python", "-c", f"""
# Simulated Claude Code execution
print("Executing task: {task.title}")
print("Agent: {self.agent_name}")
print("Files to create: {', '.join(task.files_to_create)}")
print("Task completed successfully")
"""
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": result.stdout,
                    "files_created": task.files_to_create,
                    "execution_time": "unknown"
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "output": result.stdout
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

class EnhancedOrchestrator:
    """Enhanced orchestrator with Claude Code integration"""
    
    def __init__(self, project_root: Path, anthropic_api_key: str):
        from multi_agent_system import ProjectOrchestrator
        self.base_orchestrator = ProjectOrchestrator(str(project_root), anthropic_api_key)
        self.claude_code_agents = {}
        self._initialize_claude_code_agents()
    
    def _initialize_claude_code_agents(self):
        """Initialize Claude Code integrated agents"""
        agent_configs = [
            ("orchestrator_prime", "Project Orchestration and Coordination"),
            ("alice_backend", "FastAPI, PostgreSQL, API Development"),
            ("bob_ocr_ai", "OCR Processing, Computer Vision, AI"),
            ("charlie_frontend", "React, TypeScript, UI/UX"),
            ("diana_integration", "ERP Integration, APIs, Webhooks"),
            ("eve_infrastructure", "Docker, AWS, DevOps"),
            ("felix_qa_engineer", "Testing, Quality Assurance, Code Review")
        ]
        
        for agent_name, specialization in agent_configs:
            self.claude_code_agents[agent_name] = ClaudeCodeAgent(agent_name, specialization)
    
    def load_tasks_from_prds(self, prd_file: str):
        """Load tasks from PRD document"""
        from prd_parser import PRDParser
        from multi_agent_system import Task, TaskStatus
        
        parser = PRDParser(prd_file)
        task_specs = parser.extract_tasks()
        
        for task_spec in task_specs:
            task = Task(
                id=task_spec.id,
                title=task_spec.title,
                description=task_spec.description,
                agent_type=task_spec.agent_type,
                priority=task_spec.priority,
                estimated_hours=task_spec.estimated_hours,
                dependencies=task_spec.dependencies,
                files_to_create=task_spec.files_to_create,
                acceptance_criteria=task_spec.acceptance_criteria
            )
            self.base_orchestrator.add_task(task)
    
    async def run_development_cycle(self):
        """Run development cycle with Claude Code integration"""
        return await self.base_orchestrator.run_development_cycle()
    
    def __getattr__(self, name):
        """Delegate other methods to base orchestrator"""
        return getattr(self.base_orchestrator, name)

if __name__ == "__main__":
    import os
    
    # Test the enhanced orchestrator
    orchestrator = EnhancedOrchestrator(
        Path("./docbot-enterprise"), 
        os.getenv("ANTHROPIC_API_KEY")
    )
    
    # Example: load tasks from PRD (when it exists)
    if Path('MASTER_PRD.md').exists():
        orchestrator.load_tasks_from_prds("MASTER_PRD.md")
        print(f"Loaded {len(orchestrator.tasks)} tasks from PRD")
    else:
        print("MASTER_PRD.md not found - using default tasks")