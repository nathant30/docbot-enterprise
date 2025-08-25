#!/usr/bin/env python3
"""
PRD Parser - Converts Product Requirements Documents into executable tasks
"""

import re
import yaml
from typing import List, Dict
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TaskSpec:
    id: str
    title: str
    description: str
    agent_type: str
    priority: int
    dependencies: List[str]
    files_to_create: List[str]
    acceptance_criteria: List[str]
    estimated_hours: float

class PRDParser:
    def __init__(self, prd_file_path: str):
        with open(prd_file_path, 'r', encoding='utf-8') as f:
            self.prd_content = f.read()
    
    def extract_tasks(self) -> List[TaskSpec]:
        """Parse PRD document and extract executable tasks"""
        tasks = []
        
        # Extract each PRD section
        prd_sections = re.findall(r'## (PRD-\d+.*?)\n(.*?)(?=## PRD-|\Z)', 
                                 self.prd_content, re.DOTALL)
        
        for section_header, section_content in prd_sections:
            task = self._parse_prd_section(section_header, section_content)
            if task:
                tasks.append(task)
                
        return tasks
    
    def _parse_prd_section(self, header: str, content: str) -> TaskSpec:
        """Parse individual PRD section into TaskSpec"""
        
        # Extract agent type from header or content
        agent_match = re.search(r'\*\*Agent\*\*:\s*([A-Z-]+)', content)
        if not agent_match:
            # Try to infer from header
            if 'backend' in header.lower() or 'api' in header.lower():
                agent_type = 'alice_backend'
            elif 'frontend' in header.lower() or 'react' in header.lower():
                agent_type = 'charlie_frontend'
            elif 'ocr' in header.lower() or 'ai' in header.lower():
                agent_type = 'bob_ocr_ai'
            elif 'integration' in header.lower() or 'erp' in header.lower():
                agent_type = 'diana_integration'
            elif 'infrastructure' in header.lower() or 'docker' in header.lower():
                agent_type = 'eve_infrastructure'
            elif 'qa' in header.lower() or 'test' in header.lower():
                agent_type = 'felix_qa_engineer'
            else:
                agent_type = 'orchestrator_prime'
        else:
            agent_type = agent_match.group(1).lower().replace('-', '_')
        
        # Extract priority
        priority_match = re.search(r'\*\*Priority\*\*:\s*(\d+)', content)
        priority = int(priority_match.group(1)) if priority_match else 5
        
        # Extract dependencies
        dependencies = []
        deps_match = re.search(r'\*\*Dependencies\*\*:\s*([^\n]+)', content)
        if deps_match:
            deps_text = deps_match.group(1)
            # Extract PRD references
            dependencies = re.findall(r'PRD-(\d+)', deps_text)
        
        # Extract files to create
        files_to_create = []
        deliverables_match = re.search(r'### Deliverables\n(.*?)(?=###|\n##|\Z)', content, re.DOTALL)
        if deliverables_match:
            deliverables_content = deliverables_match.group(1)
            # Extract file paths from backticks
            files_to_create = re.findall(r'`([^`]+\.(py|tsx?|js|yml|yaml|json|md|sql))`', deliverables_content)
            files_to_create = [f[0] for f in files_to_create]
        
        # Extract acceptance criteria
        acceptance_criteria = []
        criteria_match = re.search(r'### Acceptance Criteria\n(.*?)(?=###|\n##|\Z)', content, re.DOTALL)
        if criteria_match:
            criteria_content = criteria_match.group(1)
            acceptance_criteria = re.findall(r'- \[ \] ([^\n]+)', criteria_content)
        
        # Extract estimated hours
        hours_match = re.search(r'\*\*Estimated Hours\*\*:\s*(\d+(?:\.\d+)?)', content)
        estimated_hours = float(hours_match.group(1)) if hours_match else 12.0
        
        # Generate task ID
        task_id = f"{agent_type}_{priority:03d}_{len(files_to_create):02d}"
        
        return TaskSpec(
            id=task_id,
            title=header.split(':')[1].strip() if ':' in header else header.strip(),
            description=f"Implement {header.split(':')[1].strip() if ':' in header else header.strip()}",
            agent_type=agent_type,
            priority=priority,
            dependencies=dependencies,
            files_to_create=files_to_create,
            acceptance_criteria=acceptance_criteria,
            estimated_hours=estimated_hours
        )

def convert_prd_to_tasks(prd_file: str = 'MASTER_PRD.md') -> List[Dict]:
    """Convert PRD file to task list compatible with multi-agent system"""
    from multi_agent_system import Task, TaskStatus
    
    parser = PRDParser(prd_file)
    task_specs = parser.extract_tasks()
    
    tasks = []
    for task_spec in task_specs:
        task = Task(
            id=task_spec.id,
            title=task_spec.title,
            description=task_spec.description,
            agent_type=task_spec.agent_type,
            priority=task_spec.priority,
            estimated_hours=task_spec.estimated_hours,
            dependencies=task_spec.dependencies,
            status=TaskStatus.PENDING,
            files_to_create=task_spec.files_to_create,
            acceptance_criteria=task_spec.acceptance_criteria
        )
        tasks.append(task)
    
    return tasks

if __name__ == "__main__":
    # Test the parser
    if Path('MASTER_PRD.md').exists():
        parser = PRDParser('MASTER_PRD.md')
        tasks = parser.extract_tasks()
        
        print(f"Extracted {len(tasks)} tasks from PRD:")
        for task in tasks:
            print(f"- {task.title} ({task.agent_type}) - Priority: {task.priority}")
    else:
        print("MASTER_PRD.md not found. Please create it first.")