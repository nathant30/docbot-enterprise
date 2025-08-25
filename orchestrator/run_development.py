#!/usr/bin/env python3
"""
DocBot Enterprise Development Runner
Entry point for the multi-agent development system
"""

import asyncio
import os
import sys
from pathlib import Path

# Add orchestrator to path
sys.path.append(str(Path(__file__).parent))

from claude_code_integration import EnhancedOrchestrator

async def main():
    """Main development execution function"""
    print("🚀 DocBot Enterprise Multi-Agent Development System")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not found in environment")
        print("   Set your API key: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Initialize orchestrator
    project_root = Path(__file__).parent.parent
    orchestrator = EnhancedOrchestrator(project_root, api_key)
    
    print(f"📁 Project root: {project_root}")
    print(f"🤖 Initialized {len(orchestrator.agents)} agents")
    
    # Load tasks from PRD if it exists
    prd_file = project_root / "MASTER_PRD.md"
    if prd_file.exists():
        orchestrator.load_tasks_from_prds(str(prd_file))
        print(f"📋 Loaded {len(orchestrator.tasks)} tasks from MASTER_PRD.md")
    else:
        print("📋 MASTER_PRD.md not found - using default tasks")
        print("   Create MASTER_PRD.md for custom task definitions")
    
    print("\n🎯 Starting development cycle...")
    print("   Press Ctrl+C to stop\n")
    
    # Start development cycle
    try:
        await orchestrator.run_development_cycle()
    except KeyboardInterrupt:
        print("\n🛑 Development cycle stopped by user")
    except Exception as e:
        print(f"\n❌ Error during development cycle: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())